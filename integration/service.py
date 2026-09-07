import requests
import logging

from config import CLIENT_CONFIG


# --------------------------------
# Logging setup
# --------------------------------

logging.basicConfig(
    filename="integration.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------
# Client configuration
# --------------------------------

client_config = CLIENT_CONFIG["BankA"]


# --------------------------------
# 1. Get loan applications from Bank
# --------------------------------

bank_url = "http://127.0.0.1:8001/bank/loan-applications"

try:

    bank_response = requests.get(
        bank_url,
        timeout=5
    )

    print("Bank Status:", bank_response.status_code)

    if bank_response.status_code != 200:

        print("Error: Could not get data from Bank")

        logging.error(
            "Bank API returned status %s",
            bank_response.status_code
        )

        exit()

    loan_applications = bank_response.json()

    logging.info(
        "Successfully received loan applications from Bank"
    )


except requests.exceptions.Timeout:

    print("Error: Bank API request timed out")

    logging.error(
        "Bank API request timed out"
    )

    exit()


except requests.exceptions.ConnectionError:

    print("Error: Could not connect to Bank API")

    logging.error(
        "Could not connect to Bank API"
    )

    exit()


except requests.exceptions.RequestException as e:

    print("Bank Request Error:", e)

    logging.error(
        "Bank request error: %s",
        e
    )

    exit()


# --------------------------------
# 2. OneFin API
# --------------------------------

onefin_url = "http://127.0.0.1:8002/onefin/loan"


# --------------------------------
# 3. Process each loan application
# --------------------------------

for application in loan_applications:

    application_id = application["applicationId"]
    loan_amount = application["loanAmount"]


    # --------------------------------
    # Check client-specific configuration
    # --------------------------------

    if loan_amount > client_config["max_loan_amount"]:

        print(
            "\nApplication:",
            application_id,
            "- Loan amount exceeds client limit"
        )

        logging.error(
            "Application %s rejected - "
            "Loan amount %s exceeds client limit %s",
            application_id,
            loan_amount,
            client_config["max_loan_amount"]
        )

        continue


    # --------------------------------
    # Transform Bank data into OneFin format
    # --------------------------------

    onefin_data = {

        "applicationId": application["applicationId"],

        "customerId": application["customerId"],

        "customerName": application["name"],

        "loanAmount": application["loanAmount"],

        "tenure": application["tenure"]
    }


    # --------------------------------
    # Send data to OneFin
    # --------------------------------

    try:

        response = requests.post(

            onefin_url,

            json=onefin_data,

            timeout=5
        )


        print("\nApplication:", application_id)

        print(
            "OneFin Status:",
            response.status_code
        )


        # --------------------------------
        # Handle API responses
        # --------------------------------

        if response.status_code == 200:

            print(
                "Success:",
                response.json()
            )

            logging.info(
                "Application %s successfully sent to OneFin",
                application_id
            )


        elif response.status_code == 404:

            print(
                "Error: OneFin endpoint not found"
            )

            logging.error(
                "Application %s failed - "
                "OneFin endpoint not found (404)",
                application_id
            )


        elif response.status_code == 422:

            print(
                "Error: Invalid data sent to OneFin"
            )

            logging.error(
                "Application %s failed - "
                "Invalid data (422)",
                application_id
            )


        elif response.status_code >= 500:

            print(
                "Error: OneFin server problem"
            )

            logging.error(
                "Application %s failed - "
                "OneFin server error (%s)",
                application_id,
                response.status_code
            )


        else:

            print(
                "Error:",
                response.json()
            )

            logging.error(
                "Application %s failed with status %s",
                application_id,
                response.status_code
            )


    # --------------------------------
    # Exception handling
    # --------------------------------

    except requests.exceptions.Timeout:

        print(
            "Error: OneFin API request timed out"
        )

        logging.error(
            "Application %s failed - "
            "OneFin API timeout",
            application_id
        )


    except requests.exceptions.ConnectionError:

        print(
            "Error: Could not connect to OneFin API"
        )

        logging.error(
            "Application %s failed - "
            "Could not connect to OneFin API",
            application_id
        )


    except requests.exceptions.RequestException as e:

        print(
            "Request Error:",
            e
        )

        logging.error(
            "Application %s request error: %s",
            application_id,
            e
        )
