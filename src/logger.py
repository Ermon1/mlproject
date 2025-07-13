import logging
from pathlib import Path
from datetime import datetime
import json
from logging.handlers import RotatingFileHandler
import sys
from typing import Dict, Any, Optional

class MLFormatter(logging.Formatter):
    """Enhanced formatter for ML experiments with JSON metadata support"""
    def format(self, record):
        # Ensure metadata exists
        if not hasattr(record, 'ml_metadata'):
            record.ml_metadata = {}
        
        # Base formatting
        message = super().format(record)
        
        # Append structured metadata if present
        if record.ml_metadata:
            return f"{message} | METADATA: {json.dumps(record.ml_metadata)}"
        return message

def get_log_file_path(run_id: Optional[str] = None) -> Path:
    """
    Creates organized log directory structure:
    logs/
    └── YYYY-MM-DD/
        └── RUN_ID_OR_TIMESTAMP/
            └── execution.log
    """
    project_root = Path(__file__).resolve().parent.parent
    date_str = datetime.now().strftime("%Y-%m-%d")
    run_id = run_id or datetime.now().strftime("%H%M%S")  # Default to timestamp if no ID provided
    
    log_dir = project_root / "logs" / date_str / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "execution.log"

def get_logger(
    name: Optional[str] = None,
    *,
    log_level: int = logging.INFO,
    console: bool = True,
    metadata: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """
    Thread-safe singleton logger factory with ML-specific enhancements.
    
    Args:
        name: Logger name (usually __name__)
        log_level: Default logging level
        console: Enable console output
        metadata: Initial metadata to log
    
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    # Return existing configured logger
    if logger.handlers:
        return logger
    
    # Configure new logger
    log_file = get_log_file_path()
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(MLFormatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    ))
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(
            "%(levelname)s - %(message)s"
        ))
    
    # Apply configuration
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    if console:
        logger.addHandler(console_handler)
    logger.propagate = False
    
    # Initial metadata if provided
    if metadata:
        logger.info("Logger initialized", extra={'ml_metadata': metadata})
    
    return logger

# Example ML-specific extensions
def log_metrics(
    logger: logging.Logger,
    metrics: Dict[str, float],
    prefix: str = "",
    step: Optional[int] = None
):
    """Standardized metric logging with metadata"""
    metadata = {
        'metrics': {f"{prefix}{k}": float(v) for k, v in metrics.items()},
        'step': step
    }
    for k, v in metrics.items():
        logger.info(
            f"{prefix}{k}: {v:.4f}",
            extra={'ml_metadata': metadata}
        )

def log_params(logger: logging.Logger, params: Dict[str, Any]):
    """Hyperparameter logging with structured metadata"""
    logger.info(
        "HYPERPARAMETERS",
        extra={'ml_metadata': {'params': params}}
    )

 