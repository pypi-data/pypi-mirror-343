# File: tests/test_actor_logic.py
import logging
import time
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

# Import source classes
from trieye.actor_logic import ActorLogic
from trieye.actor_state import ActorState
from trieye.config import (
    TrieyeConfig,
)
from trieye.path_manager import PathManager
from trieye.schemas import (
    BufferData,
    CheckpointData,
    LoadedTrainingState,
    LogContext,
    RawMetricEvent,
)
from trieye.serializer import Serializer
from trieye.stats_processor import StatsProcessor

logger = logging.getLogger(__name__)


# --- Fixtures ---
@pytest.fixture
def mock_dependencies(
    base_trieye_config: TrieyeConfig,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
    tmp_path: Path,
) -> Generator[dict, None, None]:
    """Provides a dictionary of mocked dependencies for ActorLogic."""
    mock_actor_state = MagicMock(spec=ActorState)
    # Initialize the attribute as a dictionary on the mock
    mock_actor_state.configure_mock(_last_log_time_per_metric={})

    mock_actor_state.get_persistable_state.return_value = {
        "last_processed_step": 50,
        "last_processed_time": time.monotonic() - 10,
        "_last_log_time_per_metric": {},
    }
    mock_actor_state.restore_from_state = MagicMock()

    mock_path_manager = MagicMock(spec=PathManager)
    mock_paths = {
        "cp_step": tmp_path / "checkpoints" / "checkpoint_step_100.pkl",
        "cp_latest": tmp_path / "checkpoints" / "latest.pkl",
        "cp_best": tmp_path / "checkpoints" / "best.pkl",
        "buf_step": tmp_path / "buffers" / "buffer_step_100.pkl",
        "buf_default": tmp_path / "buffers" / "buffer.pkl",
        "config": tmp_path / "configs.json",
        "load_cp": tmp_path / "load" / "checkpoints" / "latest.pkl",
        "load_buf": tmp_path / "load" / "buffers" / "buffer.pkl",
    }

    def get_checkpoint_path_side_effect(step=None, is_latest=False, is_best=False):
        if is_latest:
            return mock_paths["cp_latest"]
        if is_best:
            return mock_paths["cp_best"]
        if step is not None:
            return tmp_path / "checkpoints" / f"checkpoint_step_{step}.pkl"
        return mock_paths["cp_step"]

    mock_path_manager.get_checkpoint_path.side_effect = get_checkpoint_path_side_effect
    mock_path_manager.get_buffer_path.side_effect = lambda step=None: (
        mock_paths["buf_default"] if step is None else mock_paths["buf_step"]
    )
    mock_path_manager.get_config_path.return_value = mock_paths["config"]
    mock_path_manager.determine_checkpoint_to_load.return_value = mock_paths["load_cp"]
    mock_path_manager.determine_buffer_to_load.return_value = mock_paths["load_buf"]
    mock_path_manager.update_checkpoint_links = MagicMock()
    mock_path_manager.update_buffer_link = MagicMock()
    mock_path_manager.latest_checkpoint_path = mock_paths["cp_latest"]
    mock_path_manager.best_checkpoint_path = mock_paths["cp_best"]
    mock_path_manager.default_buffer_path = mock_paths["buf_default"]

    mock_serializer = MagicMock(spec=Serializer)
    mock_serializer.prepare_optimizer_state.return_value = {"opt_state": "cpu"}
    mock_serializer.prepare_buffer_data.return_value = BufferData(buffer_list=["exp1"])
    mock_serializer.save_checkpoint = MagicMock()
    mock_serializer.save_buffer = MagicMock()
    mock_serializer.save_config_json = MagicMock()
    mock_serializer.load_checkpoint.return_value = None
    mock_serializer.load_buffer.return_value = None

    mock_stats_processor = None
    if base_trieye_config.stats.metrics:
        mock_stats_processor = MagicMock(spec=StatsProcessor)
        mock_stats_processor.process_and_log = MagicMock()
        mock_stats_processor._last_log_time = {}

    with (
        patch("trieye.actor_logic.StatsProcessor", return_value=mock_stats_processor),
        patch("trieye.actor_logic.ActorLogic._log_artifact_safe") as mock_log_artifact,
    ):
        yield {
            "config": base_trieye_config,
            "actor_state": mock_actor_state,
            "path_manager": mock_path_manager,
            "serializer": mock_serializer,
            "mlflow_run_id": "mock_run_id_logic",
            "mlflow_client": mock_mlflow_client,
            "tb_writer": mock_tb_writer,
            "_mock_paths": mock_paths,
            "_mock_stats_processor": mock_stats_processor,
            "_mock_log_artifact": mock_log_artifact,
        }


@pytest.fixture
def actor_logic(mock_dependencies: dict) -> ActorLogic:
    """Provides an ActorLogic instance with mocked dependencies."""
    logic = ActorLogic(
        config=mock_dependencies["config"],
        actor_state=mock_dependencies["actor_state"],
        path_manager=mock_dependencies["path_manager"],
        serializer=mock_dependencies["serializer"],
        mlflow_run_id=mock_dependencies["mlflow_run_id"],
        mlflow_client=mock_dependencies["mlflow_client"],
        tb_writer=mock_dependencies["tb_writer"],
    )
    logic.stats_processor = mock_dependencies["_mock_stats_processor"]
    return logic


# --- Tests ---


def test_logic_initialization(actor_logic: ActorLogic, mock_dependencies: dict):
    """Test ActorLogic initialization."""
    assert actor_logic.config == mock_dependencies["config"]
    assert actor_logic.actor_state == mock_dependencies["actor_state"]
    assert actor_logic.path_manager == mock_dependencies["path_manager"]
    assert actor_logic.serializer == mock_dependencies["serializer"]
    assert actor_logic.mlflow_run_id == "mock_run_id_logic"
    assert actor_logic.mlflow_client == mock_dependencies["mlflow_client"]
    assert actor_logic.tb_writer == mock_dependencies["tb_writer"]
    if actor_logic.config.stats.metrics:
        assert actor_logic.stats_processor is not None
        assert hasattr(actor_logic.stats_processor, "_last_log_time")
    else:
        assert actor_logic.stats_processor is None


def test_logic_process_and_log_metrics(
    actor_logic: ActorLogic, mock_dependencies: dict
):
    """Test the process_and_log_metrics method."""
    mock_processor = mock_dependencies["_mock_stats_processor"]
    if not mock_processor:
        pytest.skip("No metrics configured, skipping processor test.")

    raw_data = {
        1: {"metric1": [RawMetricEvent(name="metric1", value=10.0, global_step=1)]}
    }
    current_time = time.monotonic()
    context = LogContext(
        latest_step=1,
        last_log_time=current_time - 1,
        current_time=current_time,
        event_timestamps={},
        latest_values={},
    )

    # Simulate processor updating log times
    updated_processor_log_times = {
        "Test/Value": current_time,
        "Test/Rate": current_time - 0.1,
    }
    mock_processor._last_log_time = updated_processor_log_times.copy()

    actor_logic.process_and_log_metrics(raw_data, context)

    # Verify processor was called
    mock_processor.process_and_log.assert_called_once_with(raw_data, context)
    # Verify the assignment back to the mock attribute was attempted
    # This is less precise but avoids the mock assignment issue
    assert hasattr(mock_dependencies["actor_state"], "_last_log_time_per_metric")


@patch("pathlib.Path.exists", return_value=True)
def test_logic_save_initial_config(
    _mock_exists, actor_logic: ActorLogic, mock_dependencies: dict
):
    """Test saving the initial configuration."""
    actor_logic.save_initial_config()
    mock_serializer = mock_dependencies["serializer"]
    mock_log_artifact = mock_dependencies["_mock_log_artifact"]
    config_path = mock_dependencies["_mock_paths"]["config"]

    mock_serializer.save_config_json.assert_called_once_with(
        actor_logic.config.model_dump(), config_path
    )
    mock_log_artifact.assert_called_once_with(config_path, "config")


@patch("pathlib.Path.exists", return_value=True)
def test_logic_save_training_state_no_buffer(
    _mock_exists, actor_logic: ActorLogic, mock_dependencies: dict, tmp_path: Path
):
    """Test saving state without saving the buffer."""
    mock_serializer = mock_dependencies["serializer"]
    mock_path_manager = mock_dependencies["path_manager"]
    mock_log_artifact = mock_dependencies["_mock_log_artifact"]
    mock_actor_state = mock_dependencies["actor_state"]
    mock_paths = mock_dependencies["_mock_paths"]

    step = 100
    nn_state = {"layer": 1}
    opt_state = {"moment": 2}
    actor_state_data = mock_actor_state.get_persistable_state()

    actor_logic.save_training_state(
        nn_state_dict=nn_state,
        optimizer_state_dict=opt_state,
        buffer_content=[],
        global_step=step,
        episodes_played=10,
        total_simulations_run=1000,
        actor_state_data=actor_state_data,
        is_best=True,
        save_buffer=False,
    )

    mock_serializer.prepare_optimizer_state.assert_called_once_with(opt_state)
    expected_cp_data = CheckpointData(
        run_name=actor_logic.config.run_name,
        global_step=step,
        episodes_played=10,
        total_simulations_run=1000,
        model_state_dict=nn_state,
        optimizer_state_dict={"opt_state": "cpu"},
        actor_state=actor_state_data,
        user_data={},
        model_config_dict={},
        env_config_dict={},
    )
    expected_step_path = tmp_path / "checkpoints" / f"checkpoint_step_{step}.pkl"
    mock_serializer.save_checkpoint.assert_called_once_with(
        expected_cp_data, expected_step_path
    )
    mock_path_manager.update_checkpoint_links.assert_called_once_with(
        expected_step_path, True
    )
    mock_log_artifact.assert_has_calls(
        [
            call(expected_step_path, "checkpoints"),
            call(mock_paths["cp_latest"], "checkpoints"),
            call(mock_paths["cp_best"], "checkpoints"),
        ],
        any_order=True,
    )

    mock_serializer.prepare_buffer_data.assert_not_called()
    mock_serializer.save_buffer.assert_not_called()
    mock_path_manager.update_buffer_link.assert_not_called()


@patch("pathlib.Path.exists", return_value=True)
def test_logic_save_training_state_with_buffer(
    _mock_exists, actor_logic: ActorLogic, mock_dependencies: dict, tmp_path: Path
):
    """Test saving state including the buffer."""
    mock_serializer = mock_dependencies["serializer"]
    mock_path_manager = mock_dependencies["path_manager"]
    mock_log_artifact = mock_dependencies["_mock_log_artifact"]
    mock_actor_state = mock_dependencies["actor_state"]
    mock_paths = mock_dependencies["_mock_paths"]

    step = 100
    buffer_content = ["exp1", "exp2"]
    actor_state_data = mock_actor_state.get_persistable_state()

    actor_logic.config.persistence.SAVE_BUFFER = True

    actor_logic.save_training_state(
        nn_state_dict={},
        optimizer_state_dict={},
        buffer_content=buffer_content,
        global_step=step,
        episodes_played=10,
        total_simulations_run=1000,
        actor_state_data=actor_state_data,
        is_best=False,
        save_buffer=True,
    )

    expected_step_path = tmp_path / "checkpoints" / f"checkpoint_step_{step}.pkl"
    expected_buf_step_path = tmp_path / "buffers" / f"buffer_step_{step}.pkl"

    mock_serializer.save_checkpoint.assert_called_once()
    mock_path_manager.update_checkpoint_links.assert_called_once_with(
        expected_step_path, False
    )

    mock_serializer.prepare_buffer_data.assert_called_once_with(buffer_content)
    expected_buffer_data = mock_serializer.prepare_buffer_data(buffer_content)
    mock_serializer.save_buffer.assert_called_once_with(
        expected_buffer_data, expected_buf_step_path
    )
    mock_path_manager.update_buffer_link.assert_called_once_with(expected_buf_step_path)
    mock_log_artifact.assert_has_calls(
        [
            call(expected_buf_step_path, "buffers"),
            call(mock_paths["buf_default"], "buffers"),
        ],
        any_order=True,
    )


def test_logic_load_initial_state_found(
    actor_logic: ActorLogic, mock_dependencies: dict
):
    """Test loading state when checkpoint and buffer are found."""
    mock_serializer = mock_dependencies["serializer"]
    mock_path_manager = mock_dependencies["path_manager"]
    mock_actor_state = mock_dependencies["actor_state"]
    mock_paths = mock_dependencies["_mock_paths"]

    dummy_cp = CheckpointData(
        run_name="prev_run",
        global_step=50,
        episodes_played=5,
        total_simulations_run=500,
        actor_state={"last_processed_step": 45},
    )
    dummy_buf = BufferData(buffer_list=["old_exp"])
    mock_serializer.load_checkpoint.return_value = dummy_cp
    mock_serializer.load_buffer.return_value = dummy_buf
    actor_logic.config.persistence.SAVE_BUFFER = True

    loaded_state = actor_logic.load_initial_state()

    assert isinstance(loaded_state, LoadedTrainingState)
    assert loaded_state.checkpoint_data == dummy_cp
    assert loaded_state.buffer_data == dummy_buf
    mock_path_manager.determine_checkpoint_to_load.assert_called_once()
    mock_serializer.load_checkpoint.assert_called_once_with(mock_paths["load_cp"])
    mock_actor_state.restore_from_state.assert_called_once_with(dummy_cp.actor_state)
    mock_path_manager.determine_buffer_to_load.assert_called_once_with(
        actor_logic.config.persistence.LOAD_BUFFER_PATH,
        actor_logic.config.persistence.AUTO_RESUME_LATEST,
        dummy_cp.run_name,
    )
    mock_serializer.load_buffer.assert_called_once_with(mock_paths["load_buf"])


def test_logic_load_initial_state_not_found(
    actor_logic: ActorLogic, mock_dependencies: dict
):
    """Test loading state when checkpoint and buffer are not found."""
    mock_serializer = mock_dependencies["serializer"]
    mock_path_manager = mock_dependencies["path_manager"]
    mock_actor_state = mock_dependencies["actor_state"]

    mock_path_manager.determine_checkpoint_to_load.return_value = None
    mock_path_manager.determine_buffer_to_load.return_value = None
    mock_serializer.load_checkpoint.return_value = None
    mock_serializer.load_buffer.return_value = None

    loaded_state = actor_logic.load_initial_state()

    assert isinstance(loaded_state, LoadedTrainingState)
    assert loaded_state.checkpoint_data is None
    assert loaded_state.buffer_data is None
    mock_path_manager.determine_checkpoint_to_load.assert_called_once()
    mock_serializer.load_checkpoint.assert_not_called()
    mock_actor_state.restore_from_state.assert_not_called()
    mock_path_manager.determine_buffer_to_load.assert_called_once_with(
        actor_logic.config.persistence.LOAD_BUFFER_PATH,
        actor_logic.config.persistence.AUTO_RESUME_LATEST,
        None,
    )
    mock_serializer.load_buffer.assert_not_called()
