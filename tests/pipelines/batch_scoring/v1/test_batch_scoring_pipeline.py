import os
import pytest

from mlflow.exceptions import MlflowException
from mlflow.pipelines.batch_scoring.v1.pipeline import BatchScoringPipeline

# pylint: disable=unused-import
from tests.pipelines.helper_functions import (
    enter_batch_scoring_pipeline_example_directory,
)  # pylint: enable=unused-import


@pytest.fixture
def create_pipeline(enter_batch_scoring_pipeline_example_directory):
    pipeline_root_path = enter_batch_scoring_pipeline_example_directory
    profile = "local"
    return BatchScoringPipeline(pipeline_root_path=pipeline_root_path, profile=profile)


def test_create_pipeline_works(enter_batch_scoring_pipeline_example_directory):
    pipeline_root_path = enter_batch_scoring_pipeline_example_directory
    pipeline_name = os.path.basename(pipeline_root_path)
    profile = "local"
    p = BatchScoringPipeline(pipeline_root_path=pipeline_root_path, profile=profile)
    assert p.name == pipeline_name
    assert p.profile == profile


@pytest.mark.parametrize(
    "pipeline_name,profile",
    [("name_a", "local"), ("", "local"), ("sklearn_batch_scoring", "profile_a")],
)
def test_create_pipeline_fails_with_invalid_input(
    pipeline_name, profile, enter_batch_scoring_pipeline_example_directory
):
    pipeline_root_path = os.path.join(
        os.path.dirname(enter_batch_scoring_pipeline_example_directory), pipeline_name
    )
    with pytest.raises(
        MlflowException,
        match=r"(Failed to find|Did not find the YAML configuration)",
    ):
        BatchScoringPipeline(pipeline_root_path=pipeline_root_path, profile=profile)


def test_pipeline_run_and_clean_the_whole_pipeline_works(create_pipeline):
    p = create_pipeline
    p.run()
    p.clean()


@pytest.mark.parametrize("step", ["ingest", "preprocessing"])  # exclude predict for now
def test_pipeline_run_and_clean_individual_step_works(step, create_pipeline):
    p = create_pipeline
    p.run(step)
    p.clean(step)
