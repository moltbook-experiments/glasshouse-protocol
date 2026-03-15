import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any
from config import config

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

def setup_logging(config_obj: 'SimulationConfig' = config) -> None:
    """Setup structured logging for the simulation."""
    log_level = getattr(logging, config_obj.get('logging.level', 'INFO').upper())
    log_format = config_obj.get('logging.format', 'json')
    log_file = config_obj.get('logging.file', 'uat_simulation.log')

    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    if log_format.lower() == 'json':
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Configure root logger
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Set specific loggers
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

def log_simulation_event(event_type: str, **kwargs: Any) -> None:
    """Log a simulation event with structured data."""
    logger = get_logger('simulation')
    extra = {'extra_data': {'event_type': event_type, **kwargs}}
    logger.info(f"Simulation event: {event_type}", extra=extra)

def log_agent_action(agent_id: str, action: str, **kwargs: Any) -> None:
    """Log an agent action with structured data."""
    logger = get_logger('agent')
    extra = {'extra_data': {'agent_id': agent_id, 'action': action, **kwargs}}
    logger.info(f"Agent {agent_id}: {action}", extra=extra)

def log_job_event(job_id: str, event: str, **kwargs: Any) -> None:
    """Log a job-related event with structured data."""
    logger = get_logger('job')
    extra = {'extra_data': {'job_id': job_id, 'event': event, **kwargs}}
    logger.info(f"Job {job_id}: {event}", extra=extra)