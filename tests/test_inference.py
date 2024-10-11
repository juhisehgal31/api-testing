import pytest
import logging
import requests
import os
from utils.keywordrepository import get_test_data, update_test_data
from utils.basetest import delete_all_existing_models
from utils.model_utils import create_model, create_model_version, perform_inference

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
file_name = os.path.splitext(os.path.basename(__file__))[0] + "_data.json"


def test_cleanup_before_class():
    """"
    Clears existing data by deleting all previously created models.
    """
    logger.info("Starting data cleanup: Deleting all existing models before test execution.")
    delete_all_existing_models(file_name)
    logger.info("Data cleanup completed successfully.")


def test_inference_with_valid_data():
    """
    Test to perform inference using valid data.
    Steps:
    1. Create a model.
    2. Create a model version.
    3. Perform inference.
    4. Validate the response.
    """
    # Step 1: Fetch the expected status code from the JSON file
    test_case_name = "test_inference_with_valid_data"
    logger.info(f"Fetching test data for {test_case_name} from file {file_name}.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Create a new model
    logger.info("Creating a new model for inference testing.")
    response_model = create_model(test_case_name, file_name)
    response_model_data = response_model.json()
    model_id = response_model_data["id"]
    logger.info(f"Model created successfully with ID: {model_id}.")

    # Update model ID in the test data
    update_test_data(test_case_name, "id", model_id, file_name)

    # Step 3: Create a model version
    logger.info("Creating a version for the newly created model.")
    response_model_version = create_model_version(test_case_name, file_name)
    response_model_version_data = response_model_version.json()
    version_id = response_model_version_data["id"]
    parent_model_id = response_model_version_data["parent_model_id"]
    logger.info(f"Model version created successfully with ID: {version_id} for model ID: {parent_model_id}.")

    # Update model and version IDs in the test data
    update_test_data(test_case_name, "model_id", parent_model_id, file_name)
    update_test_data(test_case_name, "version_id", version_id, file_name)

    # Step 4: Perform inference
    logger.info(f"Performing inference on model ID: {parent_model_id}, version ID: {version_id}.")
    try:
        response_inference = perform_inference(test_case_name, file_name)
        response_inference_data = response_inference.json()
        logger.info("Inference response received successfully.")

        # Step 5: Validate the inference response
        assert response_inference.status_code == expected_status_code, (
            f"Expected status code {expected_status_code}, but got {response_inference.status_code}."
        )
        logger.info("Test passed: Inference performed successfully with the expected response.")
    except requests.exceptions.Timeout:
        logger.error("Inference request timed out.")
        assert False, "Test failed: Inference request timed out."
    except requests.exceptions.RequestException as e:
        logger.error(f"Inference request failed: {e}")
        assert False, f"Test failed: Inference request failed with error {e}"