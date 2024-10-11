import json
import os

def get_test_data(test_case_name, file_name):
    """
    Fetch test data for a given test case from a specified JSON file.

    Args:
        test_case_name (str): Name of the test case to fetch data for.
        file_name (str): Name of the JSON file containing the test data.

    Returns:
        dict: Test data for the specified test case.

    Raises:
        ValueError: If the test case is not found in the JSON file.
    """
    # Get the current working directory
    project_root = os.getcwd()
    file_path = os.path.join(project_root, "utils", file_name)

    # Load the JSON data from the specified file
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found in the 'utils' directory.")

    # Fetch the data for the specified test case
    if test_case_name in data:
        return data[test_case_name]
    else:
        raise ValueError(f"Test case '{test_case_name}' not found in the JSON file '{file_name}'.")


def update_test_data(test_case_name, key, value, file_name):
    """
    Update test data for a given test case in the specified JSON file.

    Args:
        test_case_name (str): The name of the test case to update.
        key (str): The key to update (e.g., "id").
        value (str): The new value to set for the specified key.
        file_name (str): The name of the JSON file containing the test data.

    Raises:
        ValueError: If the test case is not found in the JSON file.
    """
    # Get the current working directory
    project_root = os.getcwd()
    file_path = os.path.join(project_root, "utils", file_name)

    # Load the JSON data from the specified file
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found in the 'utils' directory.")

    # Update the specified key with the new value for the given test case
    if test_case_name in data:
        data[test_case_name][key] = value
    else:
        raise ValueError(f"Test case '{test_case_name}' not found in the JSON file '{file_name}'.")

    # Save the updated JSON data back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
