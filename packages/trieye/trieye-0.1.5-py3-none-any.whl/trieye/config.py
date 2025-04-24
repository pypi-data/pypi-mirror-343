# File: trieye/config.py
import logging
import time
from pathlib import Path
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)

logger = logging.getLogger(__name__)

# --- Persistence Config ---


class PersistenceConfig(BaseModel):
    """Configuration for saving/loading artifacts (Pydantic model)."""

    # --- Core Paths & Identifiers (Set by TrieyeConfig or defaults) ---
    ROOT_DATA_DIR: str = Field(
        default=".trieye_data",
        description="Root directory for all application data managed by Trieye.",
    )
    APP_NAME: str = Field(
        default="default_app",
        description="Application name (used as subdirectory under ROOT_DATA_DIR).",
    )
    RUN_NAME: str = Field(
        default_factory=lambda: f"run_{time.strftime('%Y%m%d_%H%M%S')}",
        description="Specific identifier for the current run (used as subdirectory under runs/).",
    )

    # --- Subdirectory Names (Usually defaults) ---
    RUNS_DIR_NAME: str = Field(
        default="runs", description="Name for the runs parent directory."
    )
    MLFLOW_DIR_NAME: str = Field(
        default="mlruns", description="Name for the MLflow data directory."
    )
    CHECKPOINT_SAVE_DIR_NAME: str = Field(
        default="checkpoints", description="Subdirectory name for checkpoints."
    )
    BUFFER_SAVE_DIR_NAME: str = Field(
        default="buffers", description="Subdirectory name for saved buffers."
    )
    LOG_DIR_NAME: str = Field(
        default="logs", description="Subdirectory name for text logs."
    )
    TENSORBOARD_DIR_NAME: str = Field(
        default="tensorboard", description="Subdirectory name for TensorBoard logs."
    )
    PROFILE_DIR_NAME: str = Field(
        default="profile_data", description="Subdirectory name for profiling data."
    )

    # --- Filenames (Usually defaults) ---
    LATEST_CHECKPOINT_FILENAME: str = Field(
        default="latest.pkl", description="Filename for the latest checkpoint link."
    )
    BEST_CHECKPOINT_FILENAME: str = Field(
        default="best.pkl", description="Filename for the best checkpoint link."
    )
    BUFFER_FILENAME: str = Field(
        default="buffer.pkl", description="Default filename for the saved buffer."
    )
    CONFIG_FILENAME: str = Field(
        default="configs.json", description="Filename for saving the run configuration."
    )

    # --- Persistence Behavior ---
    SAVE_BUFFER: bool = Field(
        default=True, description="Whether to save the replay buffer."
    )
    BUFFER_SAVE_FREQ_STEPS: int = Field(
        default=1000,
        ge=0,
        description="Save buffer every N global steps (0 to disable step-based saving).",
    )
    CHECKPOINT_SAVE_FREQ_STEPS: int = Field(
        default=1000,
        ge=0,
        description="Save checkpoint every N global steps (0 to disable step-based saving).",
    )
    AUTO_RESUME_LATEST: bool = Field(
        default=True,
        description="Automatically load latest checkpoint/buffer from previous run if available.",
    )
    LOAD_CHECKPOINT_PATH: str | None = Field(
        default=None,
        description="Explicit path to a checkpoint file to load, overriding auto-resume.",
    )
    LOAD_BUFFER_PATH: str | None = Field(
        default=None,
        description="Explicit path to a buffer file to load, overriding auto-resume.",
    )

    # --- Computed Paths (Internal Use by PathManager) ---
    def _get_absolute_root(self) -> Path:
        """Resolves ROOT_DATA_DIR to an absolute path."""
        # Ensure ROOT_DATA_DIR is treated as relative to CWD if not absolute
        root_path = Path(self.ROOT_DATA_DIR)
        if not root_path.is_absolute():
            root_path = Path.cwd() / root_path
        return root_path.resolve()

    def get_app_root_dir(self) -> Path:
        """Gets the absolute path to the directory for the specific application."""
        return self._get_absolute_root() / self.APP_NAME

    def get_runs_root_dir(self) -> Path:
        """Gets the absolute path to the directory containing all runs for the app."""
        return self.get_app_root_dir() / self.RUNS_DIR_NAME

    def get_run_base_dir(self) -> Path:
        """Gets the absolute base directory path for the specific run."""
        return self.get_runs_root_dir() / self.RUN_NAME

    def get_mlflow_abs_path(self) -> Path:
        """Gets the absolute OS path to the MLflow directory for the app."""
        return self.get_app_root_dir() / self.MLFLOW_DIR_NAME

    @computed_field  # type: ignore[misc]
    @property
    def MLFLOW_TRACKING_URI(self) -> str:
        """Constructs the absolute file URI for MLflow tracking."""
        abs_path = self.get_mlflow_abs_path()
        # Directory creation is handled by PathManager/Actor init
        return abs_path.as_uri()


# --- Stats Config ---

AggregationMethod = Literal[
    "latest", "mean", "sum", "rate", "min", "max", "std", "count"
]
LogTarget = Literal["mlflow", "tensorboard", "console"]
DataSource = Literal["trainer", "worker", "loop", "buffer", "system", "custom"]
XAxis = Literal["global_step", "wall_time", "episode"]


class MetricConfig(BaseModel):
    """Configuration for a single metric to be tracked and logged."""

    name: str = Field(
        ..., description="Unique name for the metric (e.g., 'Loss/Total')"
    )
    source: DataSource = Field(
        default="custom",  # Default source if not specified
        description="Origin of the raw metric data (e.g., 'trainer', 'worker', 'custom')",
    )
    raw_event_name: str | None = Field(
        default=None,
        description="Specific raw event name if different from metric name (e.g., 'episode_end'). If None, uses 'name'.",
    )
    aggregation: AggregationMethod = Field(
        default="latest",
        description="How to aggregate raw values over the logging interval ('rate' calculates per second)",
    )
    log_frequency_steps: int = Field(
        default=1,
        description="Log metric every N global steps. Set to 0 to disable step-based logging.",
        ge=0,
    )
    log_frequency_seconds: float = Field(
        default=0.0,
        description="Log metric every N seconds. Set to 0 to disable time-based logging.",
        ge=0.0,
    )
    log_to: list[LogTarget] = Field(
        default=["mlflow", "tensorboard"],
        description="Where to log the processed metric.",
    )
    x_axis: XAxis = Field(
        default="global_step", description="The primary x-axis for logging."
    )
    rate_numerator_event: str | None = Field(
        default=None,
        description="Raw event name for the numerator in rate calculation (e.g., 'step_completed')",
    )
    context_key: str | None = Field(
        default=None,
        description="Key within the RawMetricEvent context dictionary to extract the value from.",
    )

    @field_validator("rate_numerator_event")
    @classmethod
    def check_rate_config(
        cls,
        v: str | None,
        info: ValidationInfo,
    ):
        """Ensure numerator is specified if aggregation is 'rate'."""
        if info.data.get("aggregation") == "rate" and v is None:
            metric_name = info.data.get("name", "Unknown Metric")
            raise ValueError(
                f"Metric '{metric_name}' has aggregation 'rate' but 'rate_numerator_event' is not set."
            )
        return v

    @model_validator(mode="after")
    def validate_rate_numerator_event(self) -> "MetricConfig":
        """Catch any remaining cases where rate_numerator_event is missing."""
        if self.aggregation == "rate" and self.rate_numerator_event is None:
            raise ValueError(
                f"Metric '{self.name}' has aggregation 'rate' but 'rate_numerator_event' is not set."
            )
        return self

    @property
    def event_key(self) -> str:
        """The key used to store/retrieve raw events for this metric."""
        return self.raw_event_name or self.name


class StatsConfig(BaseModel):
    """Overall configuration for statistics collection and logging."""

    processing_interval_seconds: float = Field(
        default=1.0,
        description="How often the TrieyeActor aggregates and logs metrics.",
        gt=0,
    )
    metrics: list[MetricConfig] = Field(
        default_factory=list, description="List of metrics to track and log."
    )

    @field_validator("metrics")
    @classmethod
    def check_metric_names_unique(cls, metrics: list[MetricConfig]):
        """Ensure all configured metric names are unique."""
        names = [m.name for m in metrics]
        if len(names) != len(set(names)):
            from collections import Counter

            duplicates = [name for name, count in Counter(names).items() if count > 1]
            raise ValueError(f"Duplicate metric names found in config: {duplicates}")
        return metrics


# --- Trieye Config ---


class TrieyeConfig(BaseModel):
    """Top-level configuration for the Trieye library/actor."""

    app_name: str = Field(
        default="default_app",
        description="Namespace for data storage (.trieye_data/<app_name>).",
    )
    run_name: str = Field(
        default_factory=lambda: f"run_{time.strftime('%Y%m%d_%H%M%S')}",
        description="Specific identifier for the current run.",
    )
    persistence: PersistenceConfig = Field(
        default_factory=PersistenceConfig,
        description="Configuration for data persistence.",
    )
    stats: StatsConfig = Field(
        default_factory=StatsConfig,
        description="Configuration for statistics collection and logging.",
    )

    @model_validator(mode="after")
    def sync_names_to_persistence(self) -> "TrieyeConfig":
        """Ensures APP_NAME and RUN_NAME are synced to the PersistenceConfig sub-model."""
        if hasattr(self, "persistence"):
            self.persistence.APP_NAME = self.app_name
            self.persistence.RUN_NAME = self.run_name
        return self


# Rebuild models
PersistenceConfig.model_rebuild(force=True)
MetricConfig.model_rebuild(force=True)
StatsConfig.model_rebuild(force=True)
TrieyeConfig.model_rebuild(force=True)


# Default metrics list (can be imported and used by applications)
DEFAULT_METRICS = [
    MetricConfig(
        name="Loss/Total", source="trainer", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Policy", source="trainer", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Value", source="trainer", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Entropy",
        source="trainer",
        aggregation="mean",
        log_frequency_steps=10,
    ),
    MetricConfig(
        name="Loss/Mean_Abs_TD_Error",
        source="trainer",
        aggregation="mean",
        log_frequency_steps=10,
    ),
    MetricConfig(
        name="LearningRate",
        source="trainer",
        aggregation="latest",
        log_frequency_steps=10,
    ),
    MetricConfig(
        name="Episode/Score",  # Changed name for clarity
        source="worker",
        raw_event_name="episode_end",
        context_key="score",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Episode/Length",
        source="worker",
        raw_event_name="episode_end",
        context_key="length",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Episode/Triangles_Cleared",  # Changed name for clarity
        source="worker",
        raw_event_name="episode_end",
        context_key="triangles_cleared",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="MCTS/Avg_Simulations_Per_Step",
        source="worker",
        raw_event_name="mcts_step",  # Assuming worker sends this event name
        aggregation="mean",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="MCTS/Avg_Tree_Depth",  # Added metric for MCTS depth
        source="worker",
        raw_event_name="episode_end",  # Assuming depth is logged at episode end
        context_key="avg_mcts_depth",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="RL/Step_Reward_Mean",
        source="worker",
        raw_event_name="step_reward",
        aggregation="mean",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Buffer/Size",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Total_Simulations",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Episodes_Played",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Weight_Updates_Total",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="System/Num_Active_Workers",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="System/Num_Pending_Tasks",
        source="loop",  # Logged by the training loop
        aggregation="latest",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Rate/Steps_Per_Sec",
        source="loop",  # Based on step_completed event from loop
        aggregation="rate",
        rate_numerator_event="step_completed",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="Rate/Episodes_Per_Sec",
        source="worker",  # Based on episode_end event from worker
        aggregation="rate",
        rate_numerator_event="episode_end",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="Rate/Simulations_Per_Sec",
        source="worker",  # Based on mcts_step event from worker
        aggregation="rate",
        rate_numerator_event="mcts_step",  # Assuming mcts_step value is #sims
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="PER/Beta", source="trainer", aggregation="latest", log_frequency_steps=10
    ),
]
