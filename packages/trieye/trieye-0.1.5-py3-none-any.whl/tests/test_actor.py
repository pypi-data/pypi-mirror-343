# File: tests/test_actor.py
import contextlib
import logging
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import ray
from ray.util.state import list_actors

# Import from source
from trieye.actor import TrieyeActor
from trieye.actor_state import ActorState
from trieye.config import PersistenceConfig, StatsConfig, TrieyeConfig
from trieye.path_manager import PathManager
from trieye.schemas import (
    BufferData,
    CheckpointData,
    LoadedTrainingState,
)
from trieye.serializer import Serializer

logger = logging.getLogger(__name__)


# --- Fixture for Actor with Injected Mocks (for Local Mode Tests) ---
@pytest.fixture
def trieye_actor_local(
    ray_local_mode_init,  # noqa: ARG001 - Manages Ray lifecycle
    base_trieye_config: TrieyeConfig,
    mock_mlflow_client: MagicMock,
    temp_data_dir: Path,
):
    """
    Provides an instance of the TrieyeActor running in Ray local mode.
    Mocks are created *inside* the actor process via a setup method
    to avoid serialization issues.
    Uses real PathManager, Serializer, ActorState.
    """
    actor_name = f"test_trieye_actor_local_{time.time_ns()}"
    actor_handle = None

    # Use real components where possible
    real_path_manager = PathManager(base_trieye_config.persistence)
    real_serializer = Serializer()
    real_actor_state = ActorState()

    # Patch module-level functions used in __init__
    with (
        patch("trieye.actor.mlflow.set_tracking_uri"),
        patch("trieye.actor.mlflow.set_experiment"),
        patch("trieye.actor.mlflow.start_run"),
        patch("trieye.actor.mlflow.active_run"),
        patch("trieye.actor.mlflow.end_run"),
        patch("trieye.actor.logging.FileHandler"),
    ):
        try:
            actor_handle = TrieyeActor.options(  # type: ignore[attr-defined]
                name=actor_name, get_if_exists=False
            ).remote(
                config=base_trieye_config,
                _path_manager=real_path_manager,
                _serializer=real_serializer,
                _actor_state=real_actor_state,
                _mlflow_client=None,
                _tb_writer=None,
            )

            mock_run_id = mock_mlflow_client._mock_run_id
            mock_tb_log_dir_str = str(temp_data_dir / "mock_tb_dir")
            setup_run_id = ray.get(
                actor_handle._setup_mock_dependencies.remote(
                    mock_mlflow_run_id=mock_run_id, mock_tb_log_dir=mock_tb_log_dir_str
                )
            )

            assert setup_run_id == mock_run_id
            assert ray.get(actor_handle.get_mlflow_run_id.remote()) == mock_run_id

        except Exception as e:
            if actor_handle:
                with contextlib.suppress(Exception):
                    ray.kill(actor_handle)
            pytest.fail(
                f"Error during trieye_actor_local fixture setup: {e}", pytrace=True
            )

    yield actor_handle

    logger.debug(f"Tearing down fixture for local actor handle: {actor_name}")
    if actor_handle:
        try:
            ray.get(actor_handle.shutdown.remote())
        except Exception as e:
            logger.warning(f"Error during actor shutdown in local fixture: {e}")
        finally:
            with contextlib.suppress(Exception):
                ray.kill(actor_handle)


# --- Fixture for Actor with Injected Mocks (for Integration Tests) ---
@pytest.fixture
def trieye_actor_integration(
    ray_init_shutdown_session,  # noqa: ARG001 - Manages Ray lifecycle
    base_trieye_config: TrieyeConfig,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
    temp_data_dir: Path,
):
    """
    Provides an instance of the TrieyeActor running remotely (integration).
    Mocks are created *inside* the actor process via a setup method
    to avoid serialization issues.
    Uses real PathManager, Serializer, ActorState.
    """
    actor_name = f"test_trieye_actor_integration_{time.time_ns()}"
    actor_handle = None

    real_path_manager = PathManager(base_trieye_config.persistence)
    real_serializer = Serializer()
    real_actor_state = ActorState()

    with (
        patch("trieye.actor.mlflow.set_tracking_uri") as mock_set_uri,
        patch("trieye.actor.mlflow.set_experiment") as mock_set_exp,
        patch("trieye.actor.mlflow.start_run") as mock_start_run,
        patch("trieye.actor.mlflow.active_run") as mock_active_run,
        patch("trieye.actor.mlflow.end_run") as mock_end_run,
        patch("trieye.actor.logging.FileHandler") as mock_file_handler_class,
    ):
        mock_file_handler_instance = MagicMock()
        mock_file_handler_class.return_value = mock_file_handler_instance

        try:
            actor_handle = TrieyeActor.options(  # type: ignore[attr-defined]
                name=actor_name, get_if_exists=False
            ).remote(
                config=base_trieye_config,
                _path_manager=real_path_manager,
                _serializer=real_serializer,
                _actor_state=real_actor_state,
                _mlflow_client=None,
                _tb_writer=None,
            )

            mock_run_id = mock_mlflow_client._mock_run_id
            mock_tb_log_dir_str = str(temp_data_dir / "mock_tb_dir_integration")
            setup_run_id = ray.get(
                actor_handle._setup_mock_dependencies.remote(
                    mock_mlflow_run_id=mock_run_id, mock_tb_log_dir=mock_tb_log_dir_str
                ),
                timeout=15,
            )

            retrieved_run_id = ray.get(
                actor_handle.get_mlflow_run_id.remote(), timeout=15
            )
            assert setup_run_id == mock_run_id
            assert retrieved_run_id == mock_run_id, (
                "Actor did not return injected mock run ID after setting dependencies"
            )

            mock_set_uri.assert_not_called()
            mock_set_exp.assert_not_called()
            mock_active_run.assert_not_called()
            mock_start_run.assert_not_called()
            mock_file_handler_class.assert_not_called()

        except Exception as e:
            if actor_handle:
                with contextlib.suppress(Exception):
                    ray.kill(actor_handle)
            pytest.fail(
                f"Error during trieye_actor_integration fixture setup: {e}",
                pytrace=True,
            )

    yield actor_handle

    logger.debug(f"Tearing down fixture for integration actor: {actor_name}")
    if actor_handle:
        try:
            actor_info = next(
                (
                    a
                    for a in list_actors(filters=[("name", "=", actor_name)])
                    if a["state"] != "DEAD"
                ),
                None,
            )
            if actor_info:
                logger.info(f"Attempting to shutdown actor '{actor_name}'...")
                try:
                    ray.get(actor_handle.shutdown.remote(), timeout=10.0)
                    logger.info(f"Shutdown call completed for actor '{actor_name}'.")
                    mock_tb_writer.close.assert_called_once()
                    mock_end_run.assert_not_called()
                    mock_file_handler_instance.close.assert_not_called()
                except ray.exceptions.RayActorError as shutdown_err:
                    logger.warning(
                        f"RayActorError during shutdown for '{actor_name}': {shutdown_err}"
                    )
                except Exception as e:
                    logger.warning(f"Error during actor shutdown '{actor_name}': {e}")
                finally:
                    logger.info(f"Attempting to kill actor '{actor_name}'...")
                    try:
                        ray.kill(actor_handle)
                        logger.info(f"Killed actor '{actor_name}'.")
                    except ValueError:
                        logger.info(
                            f"Actor '{actor_name}' not found for killing (already dead?)."
                        )
                    except Exception as kill_e:
                        logger.warning(f"Error killing actor '{actor_name}': {kill_e}")
            else:
                logger.info(
                    f"Actor '{actor_name}' already dead or doesn't exist at teardown."
                )
        except Exception as e:
            logger.error(
                f"Error during trieye_actor_integration fixture teardown for '{actor_name}': {e}"
            )


# === Local Mode Tests (using Actor Handle with Mocks) ===


def test_actor_local_initialization(
    trieye_actor_local: ray.actor.ActorHandle, mock_mlflow_client
):
    """Test actor initialization in local mode."""
    assert trieye_actor_local is not None
    config = ray.get(trieye_actor_local.get_config.remote())
    run_id = ray.get(trieye_actor_local.get_mlflow_run_id.remote())
    actor_name = ray.get(trieye_actor_local.get_actor_name.remote())
    run_base_dir = ray.get(trieye_actor_local.get_run_base_dir_str.remote())

    assert isinstance(config, TrieyeConfig)
    assert run_id == mock_mlflow_client._mock_run_id
    assert actor_name == f"trieye_actor_{config.run_name}"
    assert Path(run_base_dir).name == config.run_name


def test_actor_local_log_event(
    trieye_actor_local: ray.actor.ActorHandle,
    create_event,
    mock_mlflow_client,  # noqa: ARG001
    mock_tb_writer,  # noqa: ARG001
):
    """Test logging a single event in local mode."""
    actor = trieye_actor_local
    event = create_event("Test/Value", 10.0, 1)
    ray.get(actor.log_event.remote(event))


def test_actor_local_log_batch_events(
    trieye_actor_local: ray.actor.ActorHandle,
    create_event,
    mock_mlflow_client,  # noqa: ARG001
    mock_tb_writer,  # noqa: ARG001
):
    """Test logging a batch of events in local mode."""
    actor = trieye_actor_local
    event1 = create_event("Test/Value", 10.0, 1)
    event2 = create_event("Test/Value", 20.0, 1)
    ray.get(actor.log_batch_events.remote([event1, event2]))


def test_actor_local_process_and_log(
    trieye_actor_local: ray.actor.ActorHandle,
    create_event,
    mock_mlflow_client: MagicMock,  # noqa: ARG001
    mock_tb_writer: MagicMock,  # noqa: ARG001
    base_stats_config: StatsConfig,
):
    """Test processing and logging in local mode."""
    actor = trieye_actor_local
    event1 = create_event("Test/Value", 20.0, 1)
    event2 = create_event("item_processed", 5, 1)
    event3 = create_event("context_event", 0, 1, context={"my_val": 55.0})

    ray.get(actor.log_event.remote(event1))
    ray.get(actor.log_event.remote(event2))
    ray.get(actor.log_event.remote(event3))

    processing_interval = base_stats_config.processing_interval_seconds
    time.sleep(processing_interval + 0.1)

    ray.get(actor.process_and_log.remote(current_global_step=1))
    pass


def test_actor_local_get_set_state(
    trieye_actor_local: ray.actor.ActorHandle,
    dummy_checkpoint_data: CheckpointData,
):
    """Test getting and setting actor state in local mode."""
    actor = trieye_actor_local
    initial_state = ray.get(actor.get_state.remote())
    assert "last_processed_step" in initial_state
    assert initial_state["last_processed_step"] == -1

    new_state = dummy_checkpoint_data.actor_state
    ray.get(actor.set_state.remote(new_state))

    restored_state = ray.get(actor.get_state.remote())
    assert restored_state["last_processed_step"] == new_state["last_processed_step"]
    assert restored_state["last_processed_time"] == new_state["last_processed_time"]


# === Integration Tests (using Remote Actor with Mocks) ===


@pytest.mark.integration
def test_actor_integration_log_and_process(
    trieye_actor_integration: ray.actor.ActorHandle,
    create_event,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
    base_stats_config: StatsConfig,
):
    """Test logging and processing via the remote actor."""
    actor = trieye_actor_integration
    event1 = create_event("Test/Value", 20.0, 1)
    event2 = create_event("item_processed", 5, 1)
    event3 = create_event("context_event", 0, 1, context={"my_val": 55.0})

    ray.get(actor.log_event.remote(event1))
    ray.get(actor.log_event.remote(event2))
    ray.get(actor.log_event.remote(event3))

    processing_interval = base_stats_config.processing_interval_seconds
    time.sleep(processing_interval + 0.1)

    ray.get(actor.process_and_log.remote(current_global_step=1))
    time.sleep(0.2)

    mock_run_id = mock_mlflow_client._mock_run_id
    mock_mlflow_client.log_metric.assert_any_call(
        run_id=mock_run_id,
        key="Test/Value",
        value=pytest.approx(20.0),
        step=1,
        timestamp=pytest.approx(time.time() * 1000, abs=5000),
    )
    mock_tb_writer.add_scalar.assert_any_call("Test/Value", pytest.approx(20.0), 1)

    mock_mlflow_client.log_metric.assert_any_call(
        run_id=mock_run_id,
        key="Test/Count",
        value=pytest.approx(1.0),
        step=1,
        timestamp=pytest.approx(time.time() * 1000, abs=5000),
    )
    mock_tb_writer.add_scalar.assert_any_call("Test/Count", pytest.approx(1.0), 1)

    mock_mlflow_client.log_metric.assert_any_call(
        run_id=mock_run_id,
        key="Test/ContextValue",
        value=pytest.approx(55.0),
        step=1,
        timestamp=pytest.approx(time.time() * 1000, abs=5000),
    )
    mock_tb_writer.add_scalar.assert_any_call(
        "Test/ContextValue", pytest.approx(55.0), 1
    )

    rate_metric_config = next(
        (m for m in base_stats_config.metrics if m.name == "Test/Rate"), None
    )
    assert rate_metric_config is not None
    rate_interval = rate_metric_config.log_frequency_seconds
    assert rate_interval > 0

    time.sleep(rate_interval + 0.1)
    ray.get(actor.force_process_and_log.remote(current_global_step=2))
    time.sleep(0.2)

    expected_rate = pytest.approx(5.0 / rate_interval, abs=5.0)

    mock_mlflow_client.log_metric.assert_any_call(
        run_id=mock_run_id,
        key="Test/Rate",
        value=expected_rate,
        step=2,
        timestamp=pytest.approx(time.time() * 1000, abs=5000),
    )
    mock_tb_writer.add_scalar.assert_any_call("Test/Rate", expected_rate, 2)


@pytest.mark.integration
def test_actor_integration_save_load_state(
    trieye_actor_integration: ray.actor.ActorHandle,
    dummy_checkpoint_data: CheckpointData,
    dummy_buffer_data: BufferData,
    # temp_data_dir: Path, # Removed unused argument
    mock_mlflow_client: MagicMock,
):
    """Test saving and loading state via the remote actor."""
    actor = trieye_actor_integration
    step = dummy_checkpoint_data.global_step
    mock_run_id = mock_mlflow_client._mock_run_id

    with patch.object(Path, "exists", return_value=True):
        ray.get(
            actor.save_training_state.remote(
                nn_state_dict=dummy_checkpoint_data.model_state_dict,
                optimizer_state_dict=dummy_checkpoint_data.optimizer_state_dict,
                buffer_content=dummy_buffer_data.buffer_list,
                global_step=step,
                episodes_played=dummy_checkpoint_data.episodes_played,
                total_simulations_run=dummy_checkpoint_data.total_simulations_run,
                save_buffer=True,
                user_data=dummy_checkpoint_data.user_data,
                model_config_dict=dummy_checkpoint_data.model_config_dict,
                env_config_dict=dummy_checkpoint_data.env_config_dict,
                is_best=True,
            )
        )

        actor_config_save: TrieyeConfig = ray.get(actor.get_config.remote())
        persist_config = actor_config_save.persistence
        pm = PathManager(persist_config)
        cp_path = pm.get_checkpoint_path(step=step)
        buf_path = pm.get_buffer_path(step=step)
        latest_cp_path = pm.get_checkpoint_path(is_latest=True)
        best_cp_path = pm.get_checkpoint_path(is_best=True)
        latest_buf_path = pm.get_buffer_path()

        mock_mlflow_client.log_artifact.assert_any_call(
            mock_run_id, str(cp_path), artifact_path="checkpoints"
        )
        mock_mlflow_client.log_artifact.assert_any_call(
            mock_run_id, str(latest_cp_path), artifact_path="checkpoints"
        )
        mock_mlflow_client.log_artifact.assert_any_call(
            mock_run_id, str(best_cp_path), artifact_path="checkpoints"
        )
        mock_mlflow_client.log_artifact.assert_any_call(
            mock_run_id, str(buf_path), artifact_path="buffers"
        )
        mock_mlflow_client.log_artifact.assert_any_call(
            mock_run_id, str(latest_buf_path), artifact_path="buffers"
        )

    with (
        patch.object(
            Serializer, "load_checkpoint", return_value=dummy_checkpoint_data
        ) as mock_load_cp,
        patch.object(
            Serializer, "load_buffer", return_value=dummy_buffer_data
        ) as mock_load_buf,
        patch.object(Path, "exists") as mock_exists_load,
    ):
        previous_run_name_for_load = "previous_run_for_load_test_integration"
        loaded_actor_config: TrieyeConfig = ray.get(actor.get_config.remote())
        persist_config_load = loaded_actor_config.persistence

        # Create a temporary PersistenceConfig for the previous run
        prev_persist_config = PersistenceConfig(
            ROOT_DATA_DIR=persist_config_load.ROOT_DATA_DIR,
            APP_NAME=persist_config_load.APP_NAME,
            RUN_NAME=previous_run_name_for_load,
        )
        prev_pm = PathManager(prev_persist_config)
        previous_cp_path = prev_pm.get_checkpoint_path(is_latest=True)
        previous_buf_path = prev_pm.get_buffer_path()

        with patch.object(
            PathManager, "find_latest_run_dir", return_value=previous_run_name_for_load
        ):

            def exists_side_effect_prev(path_instance):
                return path_instance in (previous_cp_path, previous_buf_path)

            mock_exists_load.side_effect = exists_side_effect_prev

            # Modify the actor's config temporarily for the test
            # This is hacky, ideally the actor would accept overrides for load
            original_auto_resume = loaded_actor_config.persistence.AUTO_RESUME_LATEST
            loaded_actor_config.persistence.AUTO_RESUME_LATEST = True
            # Need a way to update the actor's internal config state for the test...
            # For now, assume the logic handler uses its self.config which we can't easily modify remotely.
            # The test relies on the mocked PathManager.find_latest_run_dir and mocked Serializer.

            loaded_state_prev: LoadedTrainingState = ray.get(
                actor.load_initial_state.remote()  # Call without extra args
            )

            # Restore original config value if needed
            loaded_actor_config.persistence.AUTO_RESUME_LATEST = original_auto_resume

        mock_load_cp.assert_called_once_with(previous_cp_path)
        mock_load_buf.assert_called_once_with(previous_buf_path)

        assert loaded_state_prev is not None
        assert loaded_state_prev.checkpoint_data is not None
        assert loaded_state_prev.buffer_data is not None
        loaded_cp = loaded_state_prev.checkpoint_data
        assert loaded_cp.global_step == step
        assert (
            loaded_state_prev.buffer_data.buffer_list == dummy_buffer_data.buffer_list
        )
        internal_state = ray.get(actor.get_state.remote())
        assert (
            internal_state["last_processed_step"]
            == loaded_cp.actor_state["last_processed_step"]
        )
