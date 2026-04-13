"""
KYC Priority Review Tool
Automatically identifies high-risk KYC customers and generates
AI powered compliance review recommendations.
"""

import os
import pandas as pd
import requests
from config import API_KEY


def get_ai_review(customer):
    """Generate an AI powered AML compliance review for a customer."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    Customer Name: {customer["customer_name"]}
    KYC Status: {customer["kyc_status"]}
    Risk Rating: {customer["risk_rating"]}
    Account Balance: {customer["account_balance"]}

    As an AML expert, explain in 3 lines why this customer needs 
    priority review and what action should be taken.
    """
    messages = [
        {"role": "system", "content": "You are an AML and KYC banking compliance expert."},
        {"role": "user", "content": prompt}
    ]
    body = {"model": "llama-3.3-70b-versatile", "messages": messages}

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Could not generate review: {e}"


def main():
    """Main script — load data, identify priority customers, generate reviews."""
    # Load customer data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "customers.csv")
    df = pd.read_csv(csv_path)

    # Flag priority customers — Pending KYC with High risk rating
    df["priority_review"] = (df["kyc_status"] == "Pending") & (df["risk_rating"] == "High")
    priority_customers = df[df["priority_review"] == True]

    print(f"Found {len(priority_customers)} customer(s) requiring priority review.\n")

    # Generate AI review for each priority customer
    for index, customer in priority_customers.iterrows():
        print(f"Customer: {customer['customer_name']}")
        review = get_ai_review(customer)
        print(f"Review: {review}")
        print("---")


if __name__ == "__main__":
    main()