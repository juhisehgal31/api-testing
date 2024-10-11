import requests
import logging
from utils.keywordrepository import get_test_data

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def delete_all_existing_models(file_name):
    """
    Utility function to delete all existing models, if any, to ensure a clean state.
    """
    # Fetch test data for the cleanup
    data = get_test_data("test_delete_all_existing_models", file_name)
    expected_status_code = data["expected_status_code"]

    # Step 1: Get all existing models
    logger.info("Fetching all existing models for cleanup...")
    get_response = requests.get(f"{BASE_URL}/models")
    assert get_response.status_code == expected_status_code, (
        f"Failed to fetch models. Expected status code {expected_status_code}, got {get_response.status_code}"
    )
    models = get_response.json()

    # Step 2: Delete each model found
    logger.info(f"Found {len(models)} models. Attempting to delete each model...")
    for model in models:
        model_id = model.get("id")
        if model_id:
            logger.info(f"Deleting model with ID: {model_id}")
            delete_response = requests.delete(f"{BASE_URL}/models/{model_id}")
            assert delete_response.status_code == expected_status_code, (
                f"Failed to delete model with ID {model_id}. Expected status code {expected_status_code}, "
                f"got {delete_response.status_code}"
            )
    logger.info("All models deleted successfully.")

    # Step 3: Verify that no models are left
    logger.info("Verifying that no models are left after cleanup...")
    get_response_after_deletion = requests.get(f"{BASE_URL}/models")
    assert get_response_after_deletion.status_code == expected_status_code, (
        f"Failed to fetch models after deletion. Expected status code {expected_status_code}, "
        f"got {get_response_after_deletion.status_code}"
    )
    models_after_deletion = get_response_after_deletion.json()
    assert len(models_after_deletion) == 0, "Models are still present after deletion."
    logger.info("No models are present after deletion. Cleanup passed.")
