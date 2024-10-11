****Project Description****
This project provides an automated testing framework for an API that manages Models, Model Versions, and inference functionality. It covers endpoints for creating, deleting, and performing various operations on Models and their Versions.

****Prerequisites****
1. Install Python:
2. Requires Python 3.11. Ensure Python is installed
3. Set Up a Virtual Environment: python3.11 -m venv venv
4. Install Dependencies:- pip install -r requirements.txt

****Project Utilities****
The project includes utility scripts and test data management for smooth execution:

1. **Utilities**:

   basetest.py: Ensures a clean test environment by clearing previously created Models and Model Versions before test execution.
   keywordrepository.py: Provides functions for accessing and updating test data stored in JSON files.
   model_utils.py: Offers functions for creating and deleting Models and their Versions.

2. **Test Data:**

   Test data is maintained in JSON files and utilized within the test scripts:
   test_inference_data.json: Data for inference-related tests.
   test_model_data.json: Data for model-related tests.
   test_model_version_data.json: Data for model version-related tests.

****Test Scripts****
All test scripts are located in the tests/ directory and cover various API operations:

   test_inference.py: Contains test cases for inference operations.
   test_model.py: Test cases for managing Models, such as adding or deleting a Model.
   test_model_version.py: Test cases for managing Model Versions, such as adding or deleting Versions.

****Test Execution****
Setup Before Running Tests
Each test script contains a cleanup function to remove any previously created Models and Versions before the tests start, ensuring a clean environment for every run.

   **Steps to Run Tests:**
   1. Clone the Repository: git clone https://github.com/openinnovationai/recruiting-qa-challenge
   2. Navigate to the Project Directory: cd recruiting-qa-challenge
   3. Create a Virtual Environment: python3 -m venv venv
   4. Activate the Virtual Environment: source venv/bin/activate
   5. Install Dependencies: pip install -r requirements.txt
   6. Run the Server: fastapi dev application.py
   7. Execute Tests: pytest --alluredir=allure-results
      
****Reporting****

   1. Allure Reports:- allure serve allure-results
   2. HTML Report:- pytest --html=report.html --self-contained-html

****Troubleshooting****
Inference Takes Too Long:
If the inference operation is slow, verify that the server is functioning correctly, and adjust the timeout settings in the test scripts if needed.

****API Documentation****
The following endpoints are covered in the tests:

   **Model Endpoints:**
   1. GET /models: Fetch all Models.
   2. POST /models: Create a new Model.
   3. DELETE /models/{model_id}: Delete a Model by its ID.
      
   **Model Version Endpoints:**
   1. GET /models/{model_id}/versions: Fetch all Versions of a Model.
   2. POST /models/{model_id}/versions: Add a new Version to a Model.
   3. DELETE /models/{model_id}/versions/{version_id}: Delete a specific Model Version.

   **Inference Endpoint:**
   1. POST /models/{model_id}/versions/{version_id}/infer: Perform inference using a specified Model Version.

****Project Structure****

api-testing/
├── .venv/                              # Virtual environment setup
├── allure-results/                     # Directory for Allure report results
├── tests/                              # Directory containing all test scripts
│   ├── report.html                     # Generated test report in HTML format
│   ├── test_inference.py               # Test cases for inference-related functionalities
│   ├── test_model.py                   # Test cases for operations related to Models
│   └── test_model_version.py           # Test cases for operations related to Model Versions
├── utils/                              # Directory for utility scripts and test data files
│   ├── basetest.py                     # Base setup for tests, including cleanup of existing Models
│   ├── keywordrepository.py            # Utility script for accessing and updating test data in JSON files
│   ├── model_utils.py                  # Utility functions for managing Models and their Versions
│   ├── test_inference_data.json        # Test data for inference-related tests
│   ├── test_model_data.json            # Test data for Model-related tests
│   └── test_model_version_data.json    # Test data for Model Version-related tests
├── venv/                               # Directory for the virtual environment setup (or .venv)
├── pytest.ini                          # Configuration file for pytest settings
├── README.md                           # Documentation for project setup and usage
├── report.html                         # Test execution report in HTML format
└── requirements.txt                    # File containing project dependencies


****Advantages****

1. Modular Structure:
The project is organized with a clear separation between test scripts, utilities, and data, making it easy to manage and extend.

2. Automated Cleanup:
A clean testing environment is maintained by automatically clearing previously created Models and Versions before running new tests.

3. Data-Driven Testing:
JSON files are used for test data, allowing easy management of test cases and scenarios without modifying the code.

4. Comprehensive Reporting:
Allure reports offer detailed insights into the test execution, showing logs, results, and historical data for easy analysis.

5. Reusable Utilities:
Utility functions for managing Models and performing inference are used across multiple tests, reducing redundancy and promoting best practices.

****Disadvantages****
1. Slow Inference Tests:
Inference operations can be time-consuming, leading to longer test execution times.

2. No Parallel Execution of Tests:
Tests run sequentially, which could become a bottleneck if the number of tests increases significantly.

****Screenshots of Test Report****

<img width="1721" alt="Screenshot 2024-10-11 at 7 49 59 PM" src="https://github.com/user-attachments/assets/4ebcacfb-6b54-41c2-99b6-3761a6d13172">
<img width="1724" alt="Screenshot 2024-10-11 at 7 51 18 PM" src="https://github.com/user-attachments/assets/69247830-055a-46d7-9995-f1d0161434a1">
<img width="1728" alt="Screenshot 2024-10-11 at 7 52 28 PM" src="https://github.com/user-attachments/assets/c2c6d10a-7bba-46b4-931a-2f3fb59a6873">
<img width="1728" alt="Screenshot 2024-10-11 at 7 53 06 PM" src="https://github.com/user-attachments/assets/798edde1-68f5-4502-8d1f-824a92df4473">







