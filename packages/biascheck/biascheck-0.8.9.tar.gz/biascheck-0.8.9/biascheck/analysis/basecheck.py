import torch
import gc
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from biascheck.utils import Embedder, FAISSRetriever, load_terms
from sklearn.metrics.pairwise import cosine_similarity


class BaseCheck:
    def __init__(
        self,
        data: Union[pd.DataFrame, str],
        input_cols: List[str],
        terms: Union[str, List[str]],
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        use_contextual_analysis: bool = True,
        use_sentiment_analysis: bool = True,
        verbose: bool = True,
        batch_size: int = 8,  # Reduced batch size
        max_length: int = 512,  # Added max length parameter
    ):
        """
        Initialize the BaseCheck class.
        Parameters:
            data (Union[pd.DataFrame, str]): Input data or path to data file.
            input_cols (List[str]): List of column names to analyze.
            terms (Union[str, List[str]]): Terms to analyze or path to terms file.
            model_name (str): Name of the model to use for embeddings.
            use_contextual_analysis (bool): Whether to use contextual analysis.
            use_sentiment_analysis (bool): Whether to use sentiment analysis.
            verbose (bool): Whether to print progress information.
            batch_size (int): Batch size for processing.
            max_length (int): Maximum sequence length for tokenization.
        """
        self.data = self._load_data(data)
        self.input_cols = input_cols
        self.terms = load_terms(terms)
        self.model_name = model_name
        self.use_contextual_analysis = use_contextual_analysis
        self.use_sentiment_analysis = use_sentiment_analysis
        self.verbose = verbose
        self.batch_size = batch_size
        self.max_length = max_length
        
        # Initialize models with error handling
        try:
            self.embedder = Embedder(model_name=model_name, batch_size=batch_size)
            if use_contextual_analysis:
                self.contextual_model = AutoModelForSequenceClassification.from_pretrained(
                    "facebook/bart-large-mnli"
                )
                self.contextual_tokenizer = AutoTokenizer.from_pretrained(
                    "facebook/bart-large-mnli"
                )
            if use_sentiment_analysis:
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment",
                    device=0 if torch.cuda.is_available() else -1,
                )
        except Exception as e:
            print(f"Error initializing models: {str(e)}")
            raise

    def _load_data(self, data: Union[pd.DataFrame, str]) -> pd.DataFrame:
        """Load data from file or DataFrame."""
        if isinstance(data, str):
            try:
                return pd.read_csv(data)
            except Exception as e:
                print(f"Error loading data: {str(e)}")
                raise
        return data

    def _clear_memory(self):
        """Clear memory by deleting models and running garbage collection."""
        if hasattr(self, 'contextual_model'):
            del self.contextual_model
        if hasattr(self, 'contextual_tokenizer'):
            del self.contextual_tokenizer
        if hasattr(self, 'sentiment_analyzer'):
            del self.sentiment_analyzer
        torch.cuda.empty_cache()
        gc.collect()

    def analyze_vector_db(self) -> Dict[str, Any]:
        """Analyze vector database for bias."""
        try:
            # Process data in batches
            results = []
            for i in range(0, len(self.data), self.batch_size):
                batch = self.data.iloc[i:i + self.batch_size]
                batch_results = self._process_batch(batch)
                results.extend(batch_results)
                
                # Clear memory after each batch
                self._clear_memory()
            
            return self._aggregate_results(results)
        except Exception as e:
            print(f"Error in vector database analysis: {str(e)}")
            raise

    def _process_batch(self, batch: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process a batch of data."""
        batch_results = []
        for _, row in batch.iterrows():
            text = " ".join(str(row[col]) for col in self.input_cols)
            embeddings = self.embedder.embed([text])
            
            result = {
                "text": text,
                "embeddings": embeddings,
                "sentiment": None,
                "contextual_analysis": None
            }
            
            if self.use_sentiment_analysis:
                try:
                    result["sentiment"] = self.sentiment_analyzer(text)[0]
                except Exception as e:
                    print(f"Error in sentiment analysis: {str(e)}")
            
            if self.use_contextual_analysis:
                try:
                    result["contextual_analysis"] = self._analyze_context(text)
                except Exception as e:
                    print(f"Error in contextual analysis: {str(e)}")
            
            batch_results.append(result)
        
        return batch_results

    def _analyze_context(self, text: str) -> Dict[str, float]:
        """Analyze context using the BART model."""
        try:
            inputs = self.contextual_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length
            )
            outputs = self.contextual_model(**inputs)
            return {
                "entailment": float(outputs.logits[0][0]),
                "neutral": float(outputs.logits[0][1]),
                "contradiction": float(outputs.logits[0][2])
            }
        except Exception as e:
            print(f"Error in context analysis: {str(e)}")
            return {"entailment": 0.0, "neutral": 0.0, "contradiction": 0.0}

    def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from all batches."""
        return {
            "total_samples": len(results),
            "average_sentiment": np.mean([
                float(r["sentiment"]["score"]) if r["sentiment"] else 0.0
                for r in results
            ]),
            "context_analysis": {
                "entailment": np.mean([
                    r["contextual_analysis"]["entailment"] if r["contextual_analysis"] else 0.0
                    for r in results
                ]),
                "neutral": np.mean([
                    r["contextual_analysis"]["neutral"] if r["contextual_analysis"] else 0.0
                    for r in results
                ]),
                "contradiction": np.mean([
                    r["contextual_analysis"]["contradiction"] if r["contextual_analysis"] else 0.0
                    for r in results
                ])
            }
        }

    def __del__(self):
        """Cleanup when object is destroyed."""
        self._clear_memory()

    def _sentiment_analysis(self, text):
        """
        Perform sentiment analysis on a given text.

        Parameters:
            text (str): The text to analyze.

        Returns:
            tuple: Sentiment label and score.
        """
        result = self.sentiment_analyzer(text)
        sentiment = result[0]["label"]
        score = result[0]["score"]
        return sentiment, score

    def _contextual_analysis(self, text):
        """
        Perform contextual analysis using a transformer-based model.

        Parameters:
            text (str): The text to analyze.

        Returns:
            dict: Scores for different hypotheses and the final classification.
        """
        hypotheses = [
            "This sentence promotes discrimination.",
            "This sentence is fair and unbiased.",
            "This sentence is offensive.",
        ]

        results = []
        for hypothesis in hypotheses:
            inputs = self.contextual_tokenizer(
                text, hypothesis, return_tensors="pt", truncation=True, padding=True, max_length=512
            )
            outputs = self.contextual_model(**inputs)
            score = outputs.logits.softmax(dim=1).tolist()[0]
            results.append(score)

        scores = {hyp: result[2] for hyp, result in zip(hypotheses, results)}
        final_classification = max(scores, key=scores.get)

        return {"scores": scores, "classification": final_classification}

    def _chunk_text(self, text, max_length=512):
        """
        Chunk long text into smaller segments.

        Parameters:
            text (str): The text to chunk.
            max_length (int): Maximum chunk size.

        Returns:
            list: List of text chunks.
        """
        words = text.split()
        return [" ".join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

    def _analyze_vectordb(self, top_k=10):
        """
        Analyze a vector database (FAISS) for bias, sentiment, and contextual analysis.

        Parameters:
            top_k (int): Number of top results to retrieve.

        Returns:
            pd.DataFrame: Results of the analysis.
        """
        all_results = []

        docs = self.data.similarity_search(query=" ", k=top_k)
        for doc in docs:
            text = doc.page_content[:512]  # Truncate text for safe processing
            metadata = doc.metadata

            chunk_embedding = self.embedder.embed([text])[0]
            term_embeddings = self.embedder.embed(self.terms)
            similarity = cosine_similarity([chunk_embedding], term_embeddings).mean()

            # Perform sentiment and contextual analysis
            sentiment, sentiment_score = self._sentiment_analysis(text)
            context_result = self._contextual_analysis(text)

            all_results.append({
                "text": text,
                "metadata": metadata,
                "similarity": similarity,
                "sentiment": sentiment,
                "sentiment_score": sentiment_score,
                **context_result,
            })

        return pd.DataFrame(all_results)

    def _analyze_graphdb(self):
        """
        Analyze a graph database for bias, sentiment, and contextual analysis.

        Returns:
            pd.DataFrame: Results of the analysis.
        """
        query = "MATCH (n) RETURN n"
        records = self.data.run(query)

        all_results = []

        for record in records:
            properties = record["n"]
            for key, value in properties.items():
                if not isinstance(value, str):
                    continue

                # Chunk text if necessary
                text_chunks = self._chunk_text(value)

                for chunk in text_chunks:
                    chunk_embedding = self.embedder.embed([chunk])[0]
                    term_embeddings = self.embedder.embed(self.terms)
                    similarity = cosine_similarity([chunk_embedding], term_embeddings).mean()

                    sentiment, sentiment_score = self._sentiment_analysis(chunk)
                    context_result = self._contextual_analysis(chunk)

                    all_results.append({
                        "text": chunk,
                        "key": key,
                        "similarity": similarity,
                        "sentiment": sentiment,
                        "sentiment_score": sentiment_score,
                        **context_result,
                    })

        return pd.DataFrame(all_results)

    def analyze(self, top_k=10):
        """
        Analyze the database for bias, sentiment, and contextual analysis.

        Parameters:
            top_k (int): Number of top results to retrieve from the vector database.

        Returns:
            pd.DataFrame: Results of the analysis.
        """
        if isinstance(self.data, FAISS):
            return self._analyze_vectordb(top_k)
        elif hasattr(self.data, "run"):  # For graph-like database
            return self._analyze_graphdb()
        else:
            raise ValueError("Unsupported database type. Use FAISS or a graph-like database with a `run` method.")

    def generate_report(self, results_df):
        """
        Generate a detailed report from the analysis results.

        Parameters:
            results_df (pd.DataFrame): DataFrame of analysis results.

        Returns:
            str: A detailed report.
        """
        report = "Bias Analysis Report:\n"
        for _, row in results_df.iterrows():
            report += f"\nText: {row['text']}\n"
            report += f"Similarity: {row['similarity']:.2f}\n"
            report += f"Sentiment: {row['sentiment']} (Score: {row['sentiment_score']:.2f})\n"
            report += "Contextual Analysis Scores:\n"
            for hypothesis, score in row["scores"].items():
                report += f"  {hypothesis}: {score:.2f}\n"
            report += f"Final Classification: {row['classification']}\n"
        return report
