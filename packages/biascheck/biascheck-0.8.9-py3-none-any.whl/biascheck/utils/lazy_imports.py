import importlib
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class LazyImport:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module: Optional[Any] = None

    def __getattr__(self, name: str) -> Any:
        if self._module is None:
            try:
                self._module = importlib.import_module(self.module_name)
                logger.info(f"Lazily imported {self.module_name}")
            except ImportError as e:
                logger.error(f"Failed to import {self.module_name}: {str(e)}")
                raise
        return getattr(self._module, name)

# Lazy imports for heavy dependencies
torch = LazyImport("torch")
transformers = LazyImport("transformers")
spacy = LazyImport("spacy")
faiss = LazyImport("faiss") 