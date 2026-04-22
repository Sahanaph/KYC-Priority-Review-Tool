"""
KYC Priority Review Tool
Automatically identifies high-risk KYC customers and generates
AI powered compliance review recommendations.
"""

import json
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
 
    Rules you must follow:
    - Never make assumptions beyond the data provided
    - Always recommend a specific action
    - Never use casual language
    - If data is insufficient, say so explicitly

    Customer Name: {customer["customer_name"]}
    KYC Status: {customer["kyc_status"]}
    Risk Rating: {customer["risk_rating"]}
    Account Balance: {customer["account_balance"]}

    Respond ONLY in this exact JSON format, no other text:
   {{
    "risk_summary": "one sentence stating the risk",
    "why_it_matters": "one sentence explaining the impact",
    "action_required": "one sentence with specific action",
    "urgency": "High or Medium or Low"
   }}

    """
    messages = [
        {"role": "system", "content": "You are an AML and KYC banking compliance expert. with 10 years of experiance. You have a deep understanding of AML regulations, KYC processes, and risk management in the banking industry. Your expertise allows you to analyze customer data and provide insightful recommendations to ensure compliance and mitigate risks effectively."},
        {"role": "user", "content": prompt}
    ]
    body = {"model": "llama-3.3-70b-versatile", "messages": messages}

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        raw = data["choices"][0]["message"]["content"]
        parsed = json.loads(raw)
        return parsed
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
        if isinstance(review, dict): 
          print(f"Risk: {review['risk_summary']}")
          print(f"Impact: {review['why_it_matters']}")
          print(f"Action Required: {review['action_required']}")
          print(f"Urgency: {review['urgency']}")

        else:
          print(review)
          print("-----")


if __name__ == "__main__":
    main()