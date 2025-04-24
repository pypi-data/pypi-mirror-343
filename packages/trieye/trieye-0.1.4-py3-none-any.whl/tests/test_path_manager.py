# File: tests/test_path_manager.py
import time
from pathlib import Path

import pytest

from trieye.config import PersistenceConfig
from trieye.path_manager import PathManager


@pytest.fixture
def base_persist_config_pm(temp_data_dir: Path) -> PersistenceConfig:
    """Basic PersistenceConfig using the temporary directory for PathManager tests."""
    run_name = f"pm_test_run_{time.time_ns()}"
    return PersistenceConfig(
        ROOT_DATA_DIR=str(temp_data_dir),
        APP_NAME="pm_test_app",
        RUN_NAME=run_name,
    )


@pytest.fixture
def path_manager(base_persist_config_pm: PersistenceConfig) -> PathManager:
    """Provides a PathManager instance using the base temporary config."""
    pm = PathManager(base_persist_config_pm)
    pm.create_run_directories()
    return pm


def test_directory_creation(
    path_manager: PathManager, base_persist_config_pm: PersistenceConfig
):
    """Test if standard directories are created correctly."""
    pm = path_manager
    cfg = base_persist_config_pm

    assert pm.root_data_dir.exists()
    assert pm.app_root_dir.exists()
    assert pm.runs_root_dir.exists()
    assert pm.run_base_dir.exists()
    assert pm.checkpoint_dir.exists()
    assert pm.buffer_dir.exists()
    assert pm.log_dir.exists()
    assert pm.tb_log_dir.exists()
    assert pm.profile_dir.exists()
    assert pm.mlflow_dir.exists()

    assert pm.app_root_dir.name == cfg.APP_NAME
    assert pm.run_base_dir.name == cfg.RUN_NAME
    assert pm.runs_root_dir == pm.app_root_dir / cfg.RUNS_DIR_NAME
    assert pm.mlflow_dir == pm.app_root_dir / cfg.MLFLOW_DIR_NAME


def test_get_paths(
    path_manager: PathManager, base_persist_config_pm: PersistenceConfig
):
    """Test path generation methods for the CURRENT run."""
    pm = path_manager
    cfg = base_persist_config_pm
    step = 123

    cp_path = pm.get_checkpoint_path(step=step)
    assert cp_path.name == f"checkpoint_step_{step}.pkl"
    assert cp_path.parent == pm.checkpoint_dir

    latest_cp_path = pm.get_checkpoint_path(is_latest=True)
    assert latest_cp_path.name == cfg.LATEST_CHECKPOINT_FILENAME
    assert latest_cp_path.parent == pm.checkpoint_dir
    assert latest_cp_path == pm.latest_checkpoint_path

    best_cp_path = pm.get_checkpoint_path(is_best=True)
    assert best_cp_path.name == cfg.BEST_CHECKPOINT_FILENAME
    assert best_cp_path.parent == pm.checkpoint_dir
    assert best_cp_path == pm.best_checkpoint_path

    buf_path = pm.get_buffer_path(step=step)
    assert buf_path.name == f"buffer_step_{step}.pkl"
    assert buf_path.parent == pm.buffer_dir

    default_buf_path = pm.get_buffer_path()
    assert default_buf_path.name == cfg.BUFFER_FILENAME
    assert default_buf_path.parent == pm.buffer_dir
    assert default_buf_path == pm.default_buffer_path

    config_path = pm.get_config_path()
    assert config_path.name == cfg.CONFIG_FILENAME
    assert config_path.parent == pm.run_base_dir
    assert config_path == pm.config_path

    profile_path = pm.get_profile_path(worker_id=0, episode_seed=456)
    assert profile_path.name == "worker_0_ep_456.prof"
    assert profile_path.parent == pm.profile_dir

    log_file_path = pm.get_log_file_path()
    assert log_file_path.name == f"{cfg.RUN_NAME}_trieye.log"
    assert log_file_path.parent == pm.log_dir


def test_find_latest_run_dir(
    path_manager: PathManager, base_persist_config_pm: PersistenceConfig
):
    """Test finding the latest previous run directory."""
    pm = path_manager
    app_runs_dir = pm.runs_root_dir

    time.strftime("%Y%m%d_%H%M%S")
    time.sleep(1.1)
    ts_latest = time.strftime("%Y%m%d_%H%M%S")
    time.sleep(1.1)
    ts_older = time.strftime("%Y%m%d_%H%M%S")

    current_run = base_persist_config_pm.RUN_NAME
    latest_prev_run = f"run_{ts_latest}_latest"
    older_run = f"run_{ts_older}_older"
    no_ts_run = "run_no_timestamp"

    (app_runs_dir / latest_prev_run).mkdir()
    (app_runs_dir / older_run).mkdir()
    (app_runs_dir / no_ts_run).mkdir()
    (app_runs_dir / "not_a_run_dir.txt").touch()

    found_latest = pm.find_latest_run_dir(current_run_name=current_run)

    assert found_latest == older_run


def test_find_latest_run_dir_no_previous(path_manager: PathManager):
    """Test finding latest run when no other valid runs exist."""
    assert path_manager.run_base_dir.exists()
    found_latest = path_manager.find_latest_run_dir(
        current_run_name=path_manager.persist_config.RUN_NAME
    )
    assert found_latest is None


def test_determine_checkpoint_to_load(
    path_manager: PathManager,
    tmp_path: Path,  # Removed unused base_persist_config_pm
):
    """Test logic for determining which checkpoint to load."""
    pm = path_manager

    # Case 1: Explicit path provided and exists
    explicit_path = tmp_path / "explicit_checkpoint.pkl"
    explicit_path.touch()
    assert pm.determine_checkpoint_to_load(str(explicit_path), True) == explicit_path

    # Case 2: Explicit path provided but doesn't exist
    non_existent_path = tmp_path / "non_existent.pkl"
    assert pm.determine_checkpoint_to_load(str(non_existent_path), True) is None

    # Case 3: Auto-resume, latest previous run exists with checkpoint
    latest_prev_run_with_cp = f"run_{time.strftime('%Y%m%d_%H%M%S')}_prev_cp"
    prev_run_dir_cp = pm.runs_root_dir / latest_prev_run_with_cp
    prev_cp_dir = prev_run_dir_cp / pm.persist_config.CHECKPOINT_SAVE_DIR_NAME
    prev_cp_dir.mkdir(parents=True)
    expected_prev_latest_path = (
        prev_cp_dir / pm.persist_config.LATEST_CHECKPOINT_FILENAME
    )
    expected_prev_latest_path.touch()
    time.sleep(1.1)  # Ensure this is older than the next one

    # Case 4: Auto-resume, a *newer* previous run exists but *without* checkpoint
    latest_prev_run_no_cp = f"run_{time.strftime('%Y%m%d_%H%M%S')}_prev_no_cp"
    (pm.runs_root_dir / latest_prev_run_no_cp).mkdir()
    time.sleep(1.1)  # Ensure this is older than the next one

    # Case 5: An even older run exists, also without checkpoint
    older_prev_run_no_cp = f"run_{time.strftime('%Y%m%d_%H%M%S')}_older_no_cp"
    (pm.runs_root_dir / older_prev_run_no_cp).mkdir()

    # Verification: Auto-resume should find the checkpoint from latest_prev_run_with_cp
    found_path = pm.determine_checkpoint_to_load(None, True)
    assert found_path == expected_prev_latest_path, (
        f"Expected {expected_prev_latest_path}, got {found_path}"
    )

    # Case 6: No auto-resume, no explicit path
    assert pm.determine_checkpoint_to_load(None, False) is None
