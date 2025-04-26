import os
import platform
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EnvironmentConfig:
    def __init__(self):
        self.system = platform.system()
        self.python_version = platform.python_version()
        self.is_gpu_available = self._check_gpu_availability()
        self.config = self._get_config()

    def _check_gpu_availability(self) -> bool:
        """Check if GPU is available and properly configured."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def _get_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration."""
        config = {
            "system": self.system,
            "python_version": self.python_version,
            "gpu_available": self.is_gpu_available,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "Not set"),
            "default_device": "cuda" if self.is_gpu_available else "cpu"
        }

        # Platform-specific configurations
        if self.system == "Darwin":  # macOS
            config.update({
                "faiss_backend": "cpu",
                "torch_backend": "cpu" if not self.is_gpu_available else "mps"
            })
        elif self.system == "Linux":
            config.update({
                "faiss_backend": "gpu" if self.is_gpu_available else "cpu",
                "torch_backend": "cuda" if self.is_gpu_available else "cpu"
            })
        else:  # Windows
            config.update({
                "faiss_backend": "cpu",  # Windows typically uses CPU version
                "torch_backend": "cuda" if self.is_gpu_available else "cpu"
            })

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def log_config(self):
        """Log the current configuration."""
        logger.info("Environment Configuration:")
        for key, value in self.config.items():
            logger.info(f"{key}: {value}")

# Global environment configuration
env_config = EnvironmentConfig() 