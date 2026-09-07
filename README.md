# Client API Integration System

## Overview

This project demonstrates a Python-based API integration system between a client system and a loan management platform.

The Integration Service receives loan application data from a client API, validates client-specific configuration, transforms the data into the required format, sends it to another REST API, and stores the received data in MySQL.

## Integration Flow

Client API  
↓  
Integration Service  
↓  
Validation & Configuration  
↓  
Data Transformation  
↓  
Loan Management API  
↓  
MySQL Database



## Project Structure


client-api-integration-system/
│
├── bank_api/
│   └── main.py
│
├── target_api/
│   ├── main.py
│   └── database.py
│
└── integration/
    ├── service.py
    └── config.py

 Key Features
REST API integration using Python
JSON data exchange
Data validation and transformation
Client-specific configuration
MySQL database integration
SQL queries
API error handling
Exception handling
Integration logging
Troubleshooting support



Technologies Used
Python
FastAPI
REST APIs
JSON
Requests
SQL
MySQL
SQLAlchemy
Pydantic
Python Logging


Data Mapping and Transformation

The Client API and Target API use different field names.

The Integration Service transforms the incoming data before sending it to the Target API.

Field Mapping
Client Field	Target Field
applicationId	applicationId
customerId	customerId
name	customerName
loanAmount	loanAmount
tenure	tenure
Example

Client API:

{
    "applicationId": "A001",
    "customerId": "C001",
    "name": "Rahul",
    "loanAmount": 200000,
    "tenure": 24
}

After transformation:

{
    "applicationId": "A001",
    "customerId": "C001",
    "customerName": "Rahul",
    "loanAmount": 200000,
    "tenure": 24
}

This transformation allows the two systems to communicate even though their field names are different.

Client Configuration

Client-specific configuration is maintained separately from the main integration logic.

Example:

CLIENT_CONFIG = {
    "BankA": {
        "max_loan_amount": 500000
    }
}

The Integration Service reads this configuration before sending the application to the Target API.

If the loan amount exceeds the configured limit, the application is blocked before being sent.

Keeping configuration separate from the main integration logic makes it easier to support different client-specific requirements.





 Database Structure

The project uses MySQL to store processed loan applications.

Database
onefin
Table
loans
Table Structure
Column	Description
application_id	Unique loan application ID
customer_id	Customer ID
customer_name	Customer name
loan_amount	Requested loan amount
tenure	Loan tenure
status	Current processing status
Example SQL
SELECT * FROM loans;

This query is used to verify that the applications received by the Target API have been successfully stored.
