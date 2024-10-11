import requests
import logging
import time
from utils.keywordrepository import get_test_data

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8000"


def create_model(test_case_name, json_file_name):
    """
    Utility function to create a model using data from a JSON file.

    Args:
        test_case_name (str): The name of the test case to fetch data for.
        json_file_name (str): The name of the JSON file containing the test data.

    Returns:
        Response: The response object from the POST request.

    Raises:
        Exception: If the model creation fails.
    """
    # Fetch test data for the specified test case
    model_data = get_test_data(test_case_name, json_file_name)

    # Send POST request to create the model
    logger.info(f"Creating a model with the name: {model_data['name']} and owner: {model_data['owner']}")
    response = requests.post(f"{BASE_URL}/models", json=model_data)

    # Log the model creation response
    logger.info(f"response is: {response.json()}")
    return response


def create_model_version(test_case_name, json_file_name):
    """
    Utility function to create a model version using data from a JSON file.

    Args:
        test_case_name (str): The name of the test case to fetch data for.
        json_file_name (str): The name of the JSON file containing the test data.

    Returns:
        Response: The response object from the POST request.

    Raises:
        Exception: If the model version creation fails.
    """
    # Fetch test data for the specified test case
    version_data = get_test_data(test_case_name, json_file_name)
    model_id = version_data['id']
    # Send POST request to create the model version
    logger.info(
        f"Creating a model version for model ID: {model_id} with the name: {version_data['name']} and Hugging Face model: {version_data['hugging_face_model']}")
    response = requests.post(f"{BASE_URL}/models/{model_id}/versions", json=version_data)

    # Log the model version creation response
    logger.info(f"Model version created successfully with response: {response.json()}")
    return response


def perform_inference(test_case_name, json_file_name, timeout=60):
    """
    Utility function to perform inference using data from a JSON file.

    Args:
        test_case_name (str): The name of the test case to fetch data for.
        json_file_name (str): The name of the JSON file containing the test data.
        timeout (int): The maximum time to wait for the inference request, in seconds. Default is 60.

    Returns:
        Response: The response object from the POST request.

    Raises:
        requests.exceptions.Timeout: If the request takes longer than the specified timeout.
        requests.exceptions.RequestException: For any other request-related issues.
    """
    # Fetch test data for the specified test case
    inference_data = get_test_data(test_case_name, json_file_name)
    model_id = inference_data['model_id']
    version_id = inference_data['version_id']
    text = inference_data['text']

    # Perform the POST request to the inference endpoint with a timeout
    logger.info(f"Performing inference with model ID: {model_id}, version ID: {version_id}, and text: {text}")
    response = requests.post(
        f"{BASE_URL}/models/{model_id}/versions/{version_id}/infer",
        json={"text": text},
        timeout=timeout
    )

    # Log the response and return it
    logger.info(f"Inference response received with status code: {response.status_code}")
    return response


def delete_model(test_case_name, json_file_name):
    """
    Utility function to delete a model using the model_id from a JSON file.

    Args:
        test_case_name (str): The name of the test case to fetch data for.
        json_file_name (str): The name of the JSON file containing the test data.

    Returns:
        Response: The response object from the DELETE request.

    Raises:
        Exception: If the model deletion fails.
    """
    # Fetch test data for the specified test case
    model_data = get_test_data(test_case_name, json_file_name)

    # Get the model_id from the test data
    model_id = model_data.get("model_id")
    if not model_id:
        raise ValueError(f"Model ID not found in the test data for test case '{test_case_name}'")

    # Send DELETE request to delete the model
    logger.info(f"Deleting model with ID: {model_id}")
    response = requests.delete(f"{BASE_URL}/models/{model_id}")

    # Log the model deletion response
    logger.info(f"Model deleted with response: {response.json()}")
    return response


def delete_model_version(test_case_name, json_file_name):
    """
    Utility function to delete a model version using data from a JSON file.

    Args:
        test_case_name (str): The name of the test case to fetch data for.
        json_file_name (str): The name of the JSON file containing the test data.

    Returns:
        Response: The response object from the DELETE request.

    Raises:
        Exception: If the model version deletion fails.
    """
    # Fetch test data for the specified test case
    test_data = get_test_data(test_case_name, json_file_name)
    model_id = test_data.get("model_id")
    version_id = test_data.get("version_id")

    if not model_id or not version_id:
        raise ValueError("Model ID or Version ID not found in the test data.")

    # Send DELETE request to delete the model version
    logger.info(f"Deleting version with ID: {version_id} for model with ID: {model_id}")
    response = requests.delete(f"{BASE_URL}/models/{model_id}/versions/{version_id}")

    # Log the deletion response
    logger.info(f"Model version deleted successfully with response: {response.json()}")
    return response