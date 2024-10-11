import pytest
import requests
import uuid
import logging
import os
from utils.keywordrepository import get_test_data, update_test_data
from utils.basetest import delete_all_existing_models
from utils.model_utils import create_model, delete_model

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


def test_add_model_with_valid_data():
    """
    Test to add a model with valid data.
    Steps:
    1. Fetch the expected status code and model details from the JSON file.
    2. Add a new model.
    3. Validate the response data.
    4. Update the test data with the new model ID.
    """
    # Step 1: Fetch test data from the JSON file
    test_case_name = "test_add_model_with_valid_data"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Create a new model
    logger.info(f"Creating a new model with name: {test_data['name']} and owner: {test_data['owner']}.")
    response_model = create_model(test_case_name, file_name)
    response_model_data = response_model.json()
    model_id = response_model_data["id"]

    # Log the response details
    if model_id:
        logger.info(f"Model created successfully with ID: {model_id}.")
    else:
        logger.error("Model creation failed. Model ID not found in the response.")
        raise AssertionError("Model ID not found in the response.")

    # Step 3: Validate the response data
    logger.info("Validating the model creation response.")
    assert response_model.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_model.status_code}."
    )
    assert response_model_data["name"] == test_data["name"], (
        f"Expected name '{test_data['name']}', but got '{response_model_data['name']}'."
    )
    assert response_model_data.get("owner") == test_data["owner"], (
        f"Expected owner '{test_data['owner']}', but got '{response_model_data['owner']}'."
    )

    # Step 4: Update the test data with the new model ID
    logger.info(f"Updating the test data with the new model ID: {model_id}.")
    update_test_data(test_case_name, "id", model_id, file_name)
    update_test_data("test_delete_model_with_valid_id", "model_id", model_id, file_name)
    logger.info("Test data updated successfully with the new model ID.")


def test_add_model_with_no_data():
    """
    Test to add a model with empty data (empty name and owner).
    Steps:
    1. Fetch the expected status code and model details from the JSON file.
    2. Add a new model with an empty name and owner.
    3. Validate the response data.
    4. Update the test data with the new model ID.
    """
    # Step 1: Fetch test data from the JSON file
    test_case_name = "test_add_model_with_no_data"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Create a new model with an empty name and owner
    logger.info(f"Creating a new model with name: '{test_data['name']}' and owner: '{test_data['owner']}'.")
    response_model = create_model(test_case_name, file_name)
    response_model_data = response_model.json()
    model_id = response_model_data.get("id")

    # Log the response details
    if model_id:
        logger.info(f"Model created successfully with ID: {model_id}.")
    else:
        logger.error("Model creation failed. Model ID not found in the response.")
        raise AssertionError("Model ID not found in the response.")

    # Step 3: Validate the response data
    logger.info("Validating the model creation response.")
    assert response_model.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_model.status_code}."
    )
    assert response_model_data.get("name") == test_data["name"], (
        f"Expected name '{test_data['name']}', but got '{response_model_data.get('name')}'."
    )
    assert response_model_data.get("owner") == test_data["owner"], (
        f"Expected owner '{test_data['owner']}', but got '{response_model_data.get('owner')}'."
    )

    # Step 4: Update the test data with the new model ID
    logger.info(f"Updating the test data with the new model ID: {model_id}.")
    update_test_data(test_case_name, "id", model_id, file_name)
    logger.info("Test data updated successfully with the new model ID.")


def test_create_model_with_missing_owner_this_test_will_fail():
    """
    Test creating a model without specifying the owner.
    The test should fail with status 422 due to the missing required field 'owner'.
    This test is expected to fail because the actual status code (422) differs from the expected (404).
    """
    # Step 1: Fetch test data from the JSON file
    test_case_name = "test_create_model_with_missing_owner_this_test_will_fail"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Attempt to create a new model with the missing owner
    logger.info(f"Attempting to create a model with name: '{test_data['name']}' and missing owner.")
    response_model = create_model(test_case_name, file_name)
    response_status = response_model.status_code
    response_model_data = response_model.json()

    # Step 3: Validate the response status code
    logger.info("Validating the response status code.")
    assert response_status == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_status}."
    )

    # Step 4: Validate the error message in the response
    logger.info("Checking for 'Field required' error message in the response details.")
    detail = response_model_data.get("detail", [])
    assert any("Field required" in error.get("msg", "") for error in detail), (
        "Expected 'Field required' error message not found in the response."
    )

    # Log that the test has correctly identified the failure scenario
    logger.info("Test passed. The model creation failed as expected due to the missing owner.")


def test_create_model_with_duplicate_data():
    """
    Test to add a model with duplicate data.
    Steps:
    1. Fetch the expected status code and model details from the JSON file.
    2. Add a new model (expected to be a duplicate).
    3. Validate the response data.
    """
    # Step 1: Fetch test data from the JSON file
    test_case_name = "test_create_model_with_duplicate_data"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Attempt to create a new model that is expected to be a duplicate
    logger.info(f"Creating a new model with name: '{test_data['name']}' and owner: '{test_data['owner']}'.")
    response_model = create_model(test_case_name, file_name)
    response_status = response_model.status_code
    response_model_data = response_model.json()

    # Step 3: Validate the response status code
    logger.info("Validating the response status code for duplicate model creation.")
    assert response_status == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_status}."
    )

    # Step 4: Validate the duplicate error message in the response
    logger.info("Checking for 'Duplicate name' error message in the response details.")
    duplicate_error_message = "Duplicate name"
    assert duplicate_error_message in response_model_data.get("detail", ""), (
        f"Expected '{duplicate_error_message}' error message not found in the response."
    )

    # Log the successful identification of the duplicate model
    logger.info("Test passed. Correctly identified duplicate model creation attempt.")


def test_delete_model_with_valid_id():
    """
    Test deleting a model with a valid ID.
    Steps:
    1. Fetch the expected status code and model details from the JSON file.
    2. Delete the previously created model.
    3. Validate the response status code.
    """
    test_case_name = "test_delete_model_with_valid_id"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Ensure the model exists before deletion
    create_model("test_add_model_with_valid_data", file_name)

    # Attempt to delete the model
    logger.info(f"Attempting to delete the model with ID: '{test_data['model_id']}'.")
    response = delete_model(test_case_name, file_name)
    response_status = response.status_code

    # Validate the response status code
    logger.info("Validating the response status code for model deletion.")
    assert response_status == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_status}."
    )
    logger.info("Test passed. Model deleted successfully.")



def test_delete_model_with_invalid_id():
    """
    Test deleting a model with an invalid ID.
    Steps:
    1. Fetch the expected status code from the JSON file.
    2. Generate a random UUID to use as an invalid model ID.
    3. Attempt to delete the model with the invalid ID.
    4. Validate the response to ensure it returns a 404 status code and appropriate error message.
    """
    # Step 1: Fetch test data from the JSON file
    test_case_name = "test_delete_model_with_invalid_id"
    logger.info(f"Fetching test data for '{test_case_name}' from file '{file_name}'.")

    # Get the expected status code from the test data
    test_data = get_test_data(test_case_name, file_name)
    expected_status_code = test_data["expected_status_code"]

    # Step 2: Generate a random UUID to use as an invalid model ID
    model_id = str(uuid.uuid4())
    logger.info(f"Generated a random UUID as an invalid model ID: {model_id}.")

    # Update the test data with the generated invalid model ID
    update_test_data(test_case_name, "model_id", model_id, file_name)
    logger.info(f"Test data updated with invalid model ID: {model_id} for test case '{test_case_name}'.")

    # Step 3: Attempt to delete the model with the invalid ID
    logger.info(f"Attempting to delete a model with the invalid ID: '{model_id}'.")
    response = delete_model(test_case_name, file_name)
    response_status = response.status_code
    response_data = response.json()

    # Step 4: Validate the response data
    logger.info("Validating the response for deletion with an invalid model ID.")
    assert response_status == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response_status}."
    )

    # Validate that the error message indicates "Model not found"
    error_message = response_data.get("detail", "")
    assert "Model not found" in error_message, (
        f"Expected 'Model not found' error message not found. Got: '{error_message}'"
    )
    logger.info("Test passed. Correctly returned a 404 status and 'Model not found' message for invalid model ID.")
