from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text

from onefin_api.database import engine

app = FastAPI()


# -----------------------------
# API Request Model
# -----------------------------

class Loan(BaseModel):
    applicationId: str
    customerId: str
    customerName: str
    loanAmount: float
    tenure: int


# -----------------------------
# Create Loan
# -----------------------------

@app.post("/onefin/loan")
def create_loan(loan: Loan):

    query = text("""
        INSERT INTO loans
        (application_id, customer_id, customer_name, loan_amount, tenure, status)
        VALUES
        (:application_id, :customer_id, :customer_name, :loan_amount, :tenure, :status)
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "application_id": loan.applicationId,
                "customer_id": loan.customerId,
                "customer_name": loan.customerName,
                "loan_amount": loan.loanAmount,
                "tenure": loan.tenure,
                "status": "RECEIVED"
            }
        )

    return {
        "status": "success",
        "message": "Loan received and stored in MySQL",
        "applicationId": loan.applicationId
    }


# -----------------------------
# Get All Loans
# -----------------------------

@app.get("/onefin/loans")
def get_loans():

    query = text("SELECT * FROM loans")

    with engine.connect() as connection:

        result = connection.execute(query)

        loans = [dict(row._mapping) for row in result]

    return {
        "total_loans": len(loans),
        "loans": loans
    }
