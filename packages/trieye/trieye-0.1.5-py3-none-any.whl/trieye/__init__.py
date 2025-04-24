# File: trieye/__init__.py
"""
Trieye Library: Asynchronous Stats & Persistence for ML Experiments using Ray.
"""

from .actor import TrieyeActor
from .actor_logic import ActorLogic
from .actor_state import ActorState

# Import DEFAULT_METRICS from config directly
from .config import (
    DEFAULT_METRICS,  # <-- IMPORTED HERE
    AggregationMethod,
    DataSource,
    LogTarget,
    MetricConfig,
    PersistenceConfig,
    StatsConfig,
    TrieyeConfig,
    XAxis,
)
from .exceptions import (
    ConfigurationError,
    ProcessingError,
    SerializationError,
    TrieyeError,
)
from .path_manager import PathManager
from .schemas import (
    BufferData,
    CheckpointData,
    LoadedTrainingState,
    LogContext,
    RawMetricEvent,
)
from .serializer import Serializer
from .stats_processor import StatsProcessor

__version__ = "0.1.3"  # Ensure version is updated if needed

__all__ = [
    "DEFAULT_METRICS",  # <-- ADDED TO __all__
    # Internal Components (exposed for potential extension/testing)
    "ActorLogic",
    "ActorState",
    "AggregationMethod",
    "BufferData",
    "CheckpointData",
    "ConfigurationError",
    "DataSource",
    "LoadedTrainingState",
    "LogContext",
    "LogTarget",
    "MetricConfig",
    "PathManager",
    "PersistenceConfig",
    "ProcessingError",
    # Schemas & Types
    "RawMetricEvent",
    "SerializationError",
    "Serializer",
    "StatsConfig",
    "StatsProcessor",
    # Core Actor
    "TrieyeActor",
    # Configuration
    "TrieyeConfig",
    # Exceptions
    "TrieyeError",
    "XAxis",
]
