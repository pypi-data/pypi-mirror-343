from .embed_utils import Embedder
from .faiss_utils import FAISSRetriever
from .terms_loader import load_terms
import os
import torch
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_torch(device: Optional[str] = None) -> torch.device:
    """
    Safely initialize PyTorch with appropriate device settings.
    
    Args:
        device: Optional device specification ('cpu' or 'cuda')
    
    Returns:
        torch.device: The initialized device
    """
    try:
        # Set default device to CPU if not specified
        if device is None:
            device = 'cpu'
            
        # If CUDA is requested but not available, fallback to CPU
        if device == 'cuda' and not torch.cuda.is_available():
            logger.warning("CUDA requested but not available. Falling back to CPU.")
            device = 'cpu'
            
        # Initialize the device
        torch_device = torch.device(device)
        logger.info(f"PyTorch initialized with device: {device}")
        return torch_device
        
    except Exception as e:
        logger.error(f"Error initializing PyTorch: {str(e)}")
        return torch.device('cpu')

def check_dependencies():
    """
    Check and log the status of key dependencies.
    """
    try:
        # Check PyTorch
        logger.info(f"PyTorch version: {torch.__version__}")
        logger.info(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logger.info(f"CUDA version: {torch.version.cuda}")
            
        # Check environment variables
        logger.info(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES', 'Not set')}")
        
    except Exception as e:
        logger.error(f"Error checking dependencies: {str(e)}")

__all__ = ["Embedder", "FAISSRetriever", "load_terms"]