import pytest
import requests
import logging
import os
from utils.keywordrepository import get_test_data, update_test_data
from utils.basetest import delete_all_existing_models
from utils.model_utils import create_model, create_model_version, delete_model_version

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
file_name = os.path.splitext(os.path.basename(__file__))[0] + "_data.json"



def test_cleanup_before_class():
    """
    Pytest fixture to run the cleanup before each test class.
    """
    delete_all_existing_models(file_name)


def test_add_model_version_with_valid_data():
    """
    Test to create a model version with valid data.
    Steps:
    1. Fetch the expected status code and model details from the JSON file.
    2. Create a new model.
    3. Create a model version for the newly created model.
    4. Validate the response.
    5. Update the test data with the new model and version IDs.
    """
    # Step 1: Fetch the test data from the JSON file
    test_case_name = "test_add_model_version_with_valid_data"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Create a new model
    logger.info("Creating a new model with the test data.")
    response_model = create_model(test_case_name, file_name)
    response_model_data = response_model.json()

    # Validate model creation response
    model_id = response_model_data.get("id")
    if not model_id:
        logger.error("Model creation failed. Model ID not found in the response.")
        raise AssertionError("Model ID not found in the response.")
    logger.info(f"Model created successfully with ID: {model_id}.")

    # Update model ID in the test data
    logger.info(f"Updating the test data with the new model ID: {model_id}.")
    update_test_data(test_case_name, "id", model_id, file_name)

    # Step 3: Create a model version
    logger.info(f"Creating a version for the newly created model with ID: {model_id}.")
    response_model_version = create_model_version(test_case_name, file_name)
    response_model_version_data = response_model_version.json()

    # Validate model version creation response
    version_id = response_model_version_data.get("id")
    parent_model_id = response_model_version_data.get("parent_model_id")

    # Step 4: Update model and version IDs in the test data
    logger.info(f"Updating the test data with the new model and version IDs: {model_id}, {version_id}.")
    update_test_data(test_case_name, "model_id", parent_model_id, file_name)
    update_test_data(test_case_name, "version_id", version_id, file_name)

    # Step 5: Validate the response status code and data
    logger.info("Validating the response for model version creation.")
    assert response_model_version.status_code == expected_status_code, (
        f"Failed to add model version. Expected status code {expected_status_code}, "
        f"got {response_model_version.status_code}."
    )

    # Validate the response data
    logger.info("Validating the model version creation response data.")
    assert "id" in response_model_version_data, "Model version ID not found in the response."
    assert response_model_version_data["name"] == test_data["name"], (
        f"Expected model version name '{test_data['name']}', got '{response_model_version_data['name']}'."
    )
    assert response_model_version_data["hugging_face_model"] == test_data["hugging_face_model"], (
        f"Expected Hugging Face model '{test_data['hugging_face_model']}', got '{response_model_version_data['hugging_face_model']}'."
    )










def test_delete_model_version_with_valid_id():
    """
    Test deleting a model version with a valid ID.
    """
    # Specify the test case name and JSON file name
    test_case_name = "test_add_model_version_with_valid_data"

    # Fetch test data
    data = get_test_data(test_case_name, file_name)
    expected_status_code = data["expected_status_code"]

    # Step 1: Delete the model version using the utility function
    logger.info("Attempting to delete the model version...")
    delete_response = delete_model_version(test_case_name, file_name)

    # Get the response data
    response_data = delete_response.json()

    # Perform assertions to verify the response
    assert delete_response.status_code == expected_status_code, (
        f"Failed to delete model version. Expected status code {expected_status_code}, "
        f"got {delete_response.status_code}"
    )

    # Log the successful deletion
    logger.info("Test passed: Model version deleted successfully.")