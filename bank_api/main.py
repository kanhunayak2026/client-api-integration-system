from fastapi import FastAPI

app = FastAPI()


loan_applications = [
    {
        "applicationId": "A001",
        "customerId": "C001",
        "name": "Rahul",
        "email": "rahul@gmail.com",
        "loanAmount": 200000,
        "tenure": 24
    },
    {
        "applicationId": "A002",
        "customerId": "C002",
        "name": "Amit",
        "email": "amit@gmail.com",
        "loanAmount": 300000,
        "tenure": 36
    },
    {
        "applicationId": "A003",
        "customerId": "C003",
        "name": "Priya",
        "email": "priya@gmail.com",
        "loanAmount": 150000,
        "tenure": 12
    }
]


@app.get("/bank/loan-applications")
def get_loan_applications():
    return loan_applications
