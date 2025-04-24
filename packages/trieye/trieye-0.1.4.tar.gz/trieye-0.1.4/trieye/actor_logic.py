# File: trieye/actor_logic.py
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .actor_state import ActorState
from .exceptions import ConfigurationError, ProcessingError, SerializationError
from .path_manager import PathManager
from .schemas import CheckpointData, LoadedTrainingState, LogContext, RawMetricEvent
from .serializer import Serializer
from .stats_processor import StatsProcessor

if TYPE_CHECKING:
    from mlflow.tracking import MlflowClient
    from torch.utils.tensorboard import SummaryWriter

    from .config import TrieyeConfig

logger = logging.getLogger(__name__)


class ActorLogic:
    """
    Encapsulates the core, non-Ray-specific logic for statistics processing
    and data persistence. Orchestrates interactions between state, paths,
    serialization, and processing.
    """

    def __init__(
        self,
        config: "TrieyeConfig",
        actor_state: ActorState,
        path_manager: PathManager,
        serializer: Serializer,
        mlflow_run_id: str | None,
        mlflow_client: "MlflowClient | None",
        tb_writer: "SummaryWriter | None",
    ):
        self.config = config
        self.actor_state = actor_state
        self.path_manager = path_manager
        self.serializer = serializer
        self.mlflow_run_id = mlflow_run_id
        self.mlflow_client = mlflow_client
        self.tb_writer = tb_writer

        self.stats_processor: StatsProcessor | None = None
        if self.config.stats.metrics:
            self.stats_processor = StatsProcessor(
                config=self.config.stats,
                run_name=self.config.run_name,
                tb_writer=self.tb_writer,
                mlflow_run_id=self.mlflow_run_id,
                _mlflow_client=self.mlflow_client,
            )
            # Initialize processor's log times from actor state's initial value
            # Assumes ActorState.__init__ correctly initializes the attribute
            self.stats_processor._last_log_time = (
                self.actor_state._last_log_time_per_metric.copy()
            )
        else:
            logger.warning(
                "No metrics defined in StatsConfig. StatsProcessor not initialized."
            )

        logger.info("ActorLogic initialized.")

    def process_and_log_metrics(
        self, raw_data: dict[int, dict[str, list[RawMetricEvent]]], context: LogContext
    ):
        """Processes raw data and logs aggregated metrics using StatsProcessor."""
        if not self.stats_processor:
            logger.debug("StatsProcessor not available, skipping metric processing.")
            return
        try:
            # Update processor's state from actor state before processing
            self.stats_processor._last_log_time = (
                self.actor_state._last_log_time_per_metric.copy()
            )

            self.stats_processor.process_and_log(raw_data, context)

            # Update actor state from processor state after processing
            self.actor_state._last_log_time_per_metric = (
                self.stats_processor._last_log_time.copy()
            )
        except ProcessingError as e:
            logger.error(f"Error during metric processing: {e}", exc_info=True)
        except Exception as e:
            logger.error(
                f"Unexpected error during metric processing: {e}", exc_info=True
            )

    def load_initial_state(self) -> LoadedTrainingState:
        """
        Loads the initial training state (checkpoint and buffer) based on config.
        Handles auto-resume logic and explicit path overrides from PersistenceConfig.
        """
        checkpoint_data: CheckpointData | None = None
        buffer_data = None
        checkpoint_run_name: str | None = None

        auto_resume = self.config.persistence.AUTO_RESUME_LATEST
        load_checkpoint_path_override = self.config.persistence.LOAD_CHECKPOINT_PATH
        load_buffer_path_override = self.config.persistence.LOAD_BUFFER_PATH

        checkpoint_path = self.path_manager.determine_checkpoint_to_load(
            load_checkpoint_path_override, auto_resume
        )

        if checkpoint_path:
            try:
                checkpoint_data = self.serializer.load_checkpoint(checkpoint_path)
                if checkpoint_data:
                    self.actor_state.restore_from_state(checkpoint_data.actor_state)
                    checkpoint_run_name = checkpoint_data.run_name
                    logger.info(
                        f"Checkpoint loaded successfully from {checkpoint_path} (Run: {checkpoint_run_name}, Step: {checkpoint_data.global_step})"
                    )
                else:
                    logger.warning(
                        f"Serializer returned None for checkpoint: {checkpoint_path}"
                    )
            except SerializationError as e:
                logger.error(f"Failed to load checkpoint: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading checkpoint: {e}", exc_info=True)

        buffer_path = self.path_manager.determine_buffer_to_load(
            load_buffer_path_override, auto_resume, checkpoint_run_name
        )

        if buffer_path and self.config.persistence.SAVE_BUFFER:
            try:
                buffer_data = self.serializer.load_buffer(buffer_path)
                if buffer_data:
                    logger.info(f"Buffer loaded successfully from {buffer_path}")
                else:
                    logger.warning(
                        f"Serializer returned None for buffer: {buffer_path}"
                    )
            except SerializationError as e:
                logger.error(f"Failed to load buffer: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading buffer: {e}", exc_info=True)
        elif self.config.persistence.SAVE_BUFFER:
            logger.info("Buffer loading skipped (no suitable path found).")
        else:
            logger.info("Buffer loading skipped (SAVE_BUFFER is False).")

        return LoadedTrainingState(
            checkpoint_data=checkpoint_data, buffer_data=buffer_data
        )

    def _log_artifact_safe(self, local_path: Path, artifact_path: str):
        """Safely logs an artifact to MLflow if the client exists and path is valid."""
        if self.mlflow_client and self.mlflow_run_id and local_path.exists():
            try:
                self.mlflow_client.log_artifact(
                    self.mlflow_run_id, str(local_path), artifact_path=artifact_path
                )
            except Exception as e:
                logger.error(f"Failed to log artifact {local_path} to MLflow: {e}")
        elif not local_path.exists():
            logger.warning(f"Cannot log artifact, path does not exist: {local_path}")

    def save_training_state(
        self,
        nn_state_dict: dict[str, Any],
        optimizer_state_dict: dict[str, Any],
        buffer_content: list[Any],
        global_step: int,
        episodes_played: int,
        total_simulations_run: int,
        actor_state_data: dict[str, Any],
        is_best: bool = False,
        save_buffer: bool = False,
        model_config_dict: dict | None = None,
        env_config_dict: dict | None = None,
        user_data: dict | None = None,
    ):
        """Saves checkpoint and optionally buffer, updating links and logging artifacts."""
        if not self.serializer or not self.path_manager:
            raise ConfigurationError("Serializer or PathManager not initialized.")

        # --- Save Checkpoint ---
        step_checkpoint_path: Path | None = None
        try:
            opt_state_cpu = self.serializer.prepare_optimizer_state(
                optimizer_state_dict
            )
            checkpoint_data = CheckpointData(
                run_name=self.config.run_name,
                global_step=global_step,
                episodes_played=episodes_played,
                total_simulations_run=total_simulations_run,
                model_state_dict=nn_state_dict,
                optimizer_state_dict=opt_state_cpu,
                actor_state=actor_state_data,
                user_data=user_data or {},
                model_config_dict=model_config_dict or {},
                env_config_dict=env_config_dict or {},
            )
            step_checkpoint_path = self.path_manager.get_checkpoint_path(
                step=global_step
            )
            self.serializer.save_checkpoint(checkpoint_data, step_checkpoint_path)
            self.path_manager.update_checkpoint_links(step_checkpoint_path, is_best)

            self._log_artifact_safe(step_checkpoint_path, "checkpoints")
            self._log_artifact_safe(
                self.path_manager.latest_checkpoint_path, "checkpoints"
            )
            if is_best:
                self._log_artifact_safe(
                    self.path_manager.best_checkpoint_path, "checkpoints"
                )

        except (SerializationError, OSError) as e:
            logger.error(f"Failed to save checkpoint at step {global_step}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving checkpoint: {e}", exc_info=True)

        # --- Save Buffer (if requested and configured) ---
        step_buffer_path: Path | None = None
        if save_buffer and self.config.persistence.SAVE_BUFFER:
            try:
                buffer_data = self.serializer.prepare_buffer_data(buffer_content)
                if buffer_data:
                    step_buffer_path = self.path_manager.get_buffer_path(
                        step=global_step
                    )
                    self.serializer.save_buffer(buffer_data, step_buffer_path)
                    self.path_manager.update_buffer_link(step_buffer_path)

                    self._log_artifact_safe(step_buffer_path, "buffers")
                    self._log_artifact_safe(
                        self.path_manager.default_buffer_path, "buffers"
                    )
                else:
                    logger.error(
                        f"Failed to prepare buffer data at step {global_step}, cannot save."
                    )
            except (SerializationError, OSError) as e:
                logger.error(f"Failed to save buffer at step {global_step}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error saving buffer: {e}", exc_info=True)

    def save_initial_config(self):
        """Saves the initial TrieyeConfig to JSON."""
        try:
            config_path = self.path_manager.get_config_path()
            self.serializer.save_config_json(self.config.model_dump(), config_path)
            self._log_artifact_safe(config_path, "config")
        except (SerializationError, OSError) as e:
            logger.error(f"Failed to save initial config: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving initial config: {e}", exc_info=True)

    def save_run_config(self, configs: dict[str, Any]):
        """Saves a combined configuration dictionary as JSON and logs to MLflow."""
        try:
            config_path = self.path_manager.get_config_path()
            self.serializer.save_config_json(configs, config_path)
            self._log_artifact_safe(config_path, "config")
        except (SerializationError, OSError) as e:
            logger.error(f"Failed to save run config: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving run config: {e}", exc_info=True)
