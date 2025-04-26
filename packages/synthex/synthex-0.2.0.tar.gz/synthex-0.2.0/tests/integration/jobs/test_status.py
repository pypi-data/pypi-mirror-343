import pytest
from typing import Any

from synthex import Synthex
from synthex.models import JobStatusResponseModel
from synthex.exceptions import ValidationError


@pytest.mark.integration
def test_status(synthex: Synthex, generate_data_params: dict[Any, Any]):
    
    # Start a job
    job_id = synthex.jobs._create_job( # type: ignore
        schema_definition=generate_data_params["schema_definition"],
        examples=generate_data_params["examples"],
        requirements=generate_data_params["requirements"],
        number_of_samples=generate_data_params["number_of_samples"]
    )
    
    # Check its status
    job_status = synthex.jobs.status()
        
    assert isinstance(job_status, JobStatusResponseModel)
    assert job_status.status == "On Hold"
    assert job_status.progress == 0.0
    
    
@pytest.mark.integration
def test_status_no_job_running(synthex: Synthex, generate_data_params: dict[Any, Any]):
    # Ensure no job is running by setting the current job ID to None
    synthex.jobs._current_job_id = None # type: ignore
    
    try:
        # Check status without starting a job
        with pytest.raises(ValidationError):
            synthex.jobs.status()
    except AssertionError:
        pytest.fail("Expected ValidationError to be raised when no job is running, but it wasn't.")