__version__ = "0.8.10"

# Initialize logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import utilities
from .utils.env_config import env_config
from .utils.lazy_imports import torch, transformers, spacy, faiss

# Log environment configuration
env_config.log_config()

# Import main components
from .analysis.docucheck import DocuCheck
from .analysis.moducheck import ModuCheck
from .analysis.setcheck import SetCheck
from .analysis.basecheck import BaseCheck
from .analysis.ragcheck import RAGCheck

__all__ = ["DocuCheck", "ModuCheck", "SetCheck", "BaseCheck", "RAGCheck"]