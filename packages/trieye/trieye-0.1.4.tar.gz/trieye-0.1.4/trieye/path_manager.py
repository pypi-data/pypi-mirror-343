# File: trieye/path_manager.py
import contextlib
import datetime
import logging
import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import PersistenceConfig  # Use relative import

logger = logging.getLogger(__name__)


class PathManager:
    """
    Manages file paths and directory creation based solely on PersistenceConfig.
    Derives all paths relative to the configured ROOT_DATA_DIR, APP_NAME, and RUN_NAME.
    """

    def __init__(self, persist_config: "PersistenceConfig"):
        self.persist_config = persist_config
        self._update_paths()  # Initialize paths on creation

    def _update_paths(self):
        """Updates all path properties based on the current persist_config."""
        # --- Base Directories ---
        self.root_data_dir = self.persist_config._get_absolute_root()
        self.app_root_dir = self.persist_config.get_app_root_dir()
        self.runs_root_dir = self.persist_config.get_runs_root_dir()
        self.run_base_dir = self.persist_config.get_run_base_dir()
        self.mlflow_dir = self.persist_config.get_mlflow_abs_path()

        # --- Run-Specific Subdirectories ---
        self.checkpoint_dir = (
            self.run_base_dir / self.persist_config.CHECKPOINT_SAVE_DIR_NAME
        )
        self.buffer_dir = self.run_base_dir / self.persist_config.BUFFER_SAVE_DIR_NAME
        self.log_dir = self.run_base_dir / self.persist_config.LOG_DIR_NAME
        self.tb_log_dir = self.run_base_dir / self.persist_config.TENSORBOARD_DIR_NAME
        self.profile_dir = self.run_base_dir / self.persist_config.PROFILE_DIR_NAME
        self.config_path = self.run_base_dir / self.persist_config.CONFIG_FILENAME

        # --- Specific File Paths ---
        self.latest_checkpoint_path = (
            self.checkpoint_dir / self.persist_config.LATEST_CHECKPOINT_FILENAME
        )
        self.best_checkpoint_path = (
            self.checkpoint_dir / self.persist_config.BEST_CHECKPOINT_FILENAME
        )
        self.default_buffer_path = self.buffer_dir / self.persist_config.BUFFER_FILENAME

    def create_run_directories(self):
        """Creates necessary directories for the current run."""
        self.app_root_dir.mkdir(parents=True, exist_ok=True)
        self.runs_root_dir.mkdir(parents=True, exist_ok=True)
        self.run_base_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.tb_log_dir.mkdir(parents=True, exist_ok=True)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        if self.persist_config.SAVE_BUFFER:
            self.buffer_dir.mkdir(parents=True, exist_ok=True)
        # Ensure MLflow dir exists for file URI
        self.mlflow_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured run directories exist under: {self.run_base_dir}")

    def get_checkpoint_path(
        self, step: int | None = None, is_latest: bool = False, is_best: bool = False
    ) -> Path:
        """Constructs the absolute path for a checkpoint file for the CURRENT run."""
        if is_latest:
            return self.latest_checkpoint_path
        if is_best:
            return self.best_checkpoint_path
        if step is not None:
            filename = f"checkpoint_step_{step}.pkl"
            return self.checkpoint_dir / filename
        # Default to latest if no specific identifier given
        return self.latest_checkpoint_path

    def get_buffer_path(self, step: int | None = None) -> Path:
        """Constructs the absolute path for a buffer file for the CURRENT run."""
        if step is not None:
            filename = f"buffer_step_{step}.pkl"
            return self.buffer_dir / filename
        return self.default_buffer_path

    def get_config_path(self) -> Path:
        """Constructs the absolute path for the config JSON file for the CURRENT run."""
        return self.config_path

    def get_profile_path(self, worker_id: int, episode_seed: int) -> Path:
        """Constructs the absolute path for a profile data file for the CURRENT run."""
        filename = f"worker_{worker_id}_ep_{episode_seed}.prof"
        return self.profile_dir / filename

    def get_log_file_path(self) -> Path:
        """Constructs the path for the Trieye-specific log file."""
        return self.log_dir / f"{self.persist_config.RUN_NAME}_trieye.log"

    def _get_sorted_previous_runs(self, current_run_name: str) -> list[str]:
        """Gets a list of previous run names, sorted by timestamp descending."""
        potential_runs: list[tuple[datetime.datetime, str]] = []
        run_name_pattern = re.compile(r"(\d{8}_\d{6})")
        if not self.runs_root_dir.exists():
            return []
        try:
            for d in self.runs_root_dir.iterdir():
                if d.is_dir() and d.name != current_run_name:
                    match = run_name_pattern.search(d.name)
                    if match:
                        try:
                            run_time = datetime.datetime.strptime(
                                match.group(1), "%Y%m%d_%H%M%S"
                            )
                            potential_runs.append((run_time, d.name))
                        except ValueError:
                            pass
            potential_runs.sort(key=lambda item: item[0], reverse=True)
            return [run_name for _, run_name in potential_runs]
        except Exception as e:
            logger.error(f"Error finding previous run directories: {e}", exc_info=True)
            return []

    def find_latest_run_dir(self, current_run_name: str) -> str | None:
        """Finds the most recent *previous* run directory based on timestamp."""
        sorted_runs = self._get_sorted_previous_runs(current_run_name)
        if sorted_runs:
            latest_run_name = sorted_runs[0]
            logger.info(f"Selected latest previous run: {latest_run_name}")
            return latest_run_name
        return None

    def determine_checkpoint_to_load(
        self, load_path_config: str | None, auto_resume: bool
    ) -> Path | None:
        """Determines the absolute path of the checkpoint file to load."""
        current_run_name = self.persist_config.RUN_NAME
        checkpoint_to_load: Path | None = None
        load_run_name: str | None = None

        if load_path_config:
            load_path = Path(load_path_config).resolve()
            if load_path.exists() and load_path.is_file():
                checkpoint_to_load = load_path
                with contextlib.suppress(Exception):
                    load_run_name = load_path.parent.parent.name
                logger.info(f"Using explicit checkpoint path: {checkpoint_to_load}")
            else:
                logger.warning(
                    f"Specified checkpoint path not found or not a file: {load_path_config}"
                )
        if not checkpoint_to_load and auto_resume:
            logger.info(
                "Auto-resume enabled, searching for latest previous checkpoint..."
            )
            sorted_prev_runs = self._get_sorted_previous_runs(current_run_name)
            for prev_run_name in sorted_prev_runs:
                potential_latest_path = (
                    self.runs_root_dir
                    / prev_run_name
                    / self.persist_config.CHECKPOINT_SAVE_DIR_NAME
                    / self.persist_config.LATEST_CHECKPOINT_FILENAME
                )
                if potential_latest_path.exists():
                    checkpoint_to_load = potential_latest_path.resolve()
                    load_run_name = prev_run_name
                    logger.info(
                        f"Auto-resuming from latest checkpoint in '{load_run_name}': {checkpoint_to_load}"
                    )
                    break  # Found the latest valid one
            if not checkpoint_to_load:
                logger.info(
                    "No valid checkpoint found in previous runs for auto-resume."
                )

        if not checkpoint_to_load:
            logger.info("No checkpoint found to load.")
        return checkpoint_to_load

    def determine_buffer_to_load(
        self,
        load_path_config: str | None,
        auto_resume: bool,
        checkpoint_run_name: str | None,
    ) -> Path | None:
        """Determines the buffer file path to load."""
        buffer_to_load: Path | None = None
        load_run_name: str | None = None

        if load_path_config:
            load_path = Path(load_path_config).resolve()
            if load_path.exists() and load_path.is_file():
                buffer_to_load = load_path
                with contextlib.suppress(Exception):
                    load_run_name = load_path.parent.parent.name
                logger.info(f"Using explicit buffer path: {buffer_to_load}")
            else:
                logger.warning(
                    f"Specified buffer path not found or not a file: {load_path_config}"
                )
        if not buffer_to_load and checkpoint_run_name:
            # Load buffer from the same run as the loaded checkpoint
            potential_buffer_path = (
                self.runs_root_dir
                / checkpoint_run_name
                / self.persist_config.BUFFER_SAVE_DIR_NAME
                / self.persist_config.BUFFER_FILENAME
            )
            if potential_buffer_path.exists():
                buffer_to_load = potential_buffer_path.resolve()
                load_run_name = checkpoint_run_name
                logger.info(
                    f"Loading buffer from checkpoint run '{checkpoint_run_name}': {buffer_to_load}"
                )
        if not buffer_to_load and auto_resume and not checkpoint_run_name:
            # Auto-resume buffer from latest *previous* run if no checkpoint was loaded
            logger.info(
                "Auto-resume enabled for buffer, searching latest previous run..."
            )
            sorted_prev_runs = self._get_sorted_previous_runs(
                self.persist_config.RUN_NAME
            )
            for prev_run_name in sorted_prev_runs:
                potential_buffer_path = (
                    self.runs_root_dir
                    / prev_run_name
                    / self.persist_config.BUFFER_SAVE_DIR_NAME
                    / self.persist_config.BUFFER_FILENAME
                )
                if potential_buffer_path.exists():
                    buffer_to_load = potential_buffer_path.resolve()
                    load_run_name = prev_run_name
                    logger.info(
                        f"Auto-resuming buffer from latest previous run '{load_run_name}': {buffer_to_load}"
                    )
                    break  # Found the latest valid one
            if not buffer_to_load:
                logger.info("No valid buffer found in previous runs for auto-resume.")

        if not buffer_to_load:
            logger.info("No suitable buffer file found to load.")
        return buffer_to_load

    def update_checkpoint_links(self, step_checkpoint_path: Path, is_best: bool):
        """Updates the 'latest' and optionally 'best' checkpoint links."""
        if not step_checkpoint_path.exists():
            logger.warning(
                f"Cannot update links, source checkpoint does not exist: {step_checkpoint_path}"
            )
            return
        try:
            shutil.copy2(step_checkpoint_path, self.latest_checkpoint_path)
            logger.debug(f"Updated latest checkpoint link to {step_checkpoint_path}")
        except Exception as e:
            logger.error(f"Failed to update latest checkpoint link: {e}")
        if is_best:
            try:
                shutil.copy2(step_checkpoint_path, self.best_checkpoint_path)
                logger.debug(f"Updated best checkpoint link to {step_checkpoint_path}")
            except Exception as e:
                logger.error(f"Failed to update best checkpoint link: {e}")

    def update_buffer_link(self, step_buffer_path: Path):
        """Updates the default buffer link ('buffer.pkl')."""
        if not step_buffer_path.exists():
            logger.warning(
                f"Cannot update buffer link, source buffer does not exist: {step_buffer_path}"
            )
            return
        try:
            shutil.copy2(step_buffer_path, self.default_buffer_path)
            logger.debug(f"Updated default buffer link to {step_buffer_path}")
        except Exception as e:
            logger.error(f"Error updating default buffer file link: {e}")
