from config import API_KEY
import pandas as pd
import requests
import os

API_KEY = API_KEY


def get_ai_response(Customer):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"""
    Customer_name: {Customer["customer_name"]},
    KYC_status: {Customer["kyc_status"]},
    Risk_Ratng: {Customer["risk_rating"]},
    Account_balance: {Customer["account_balance"]}

    As an AML expert, explain in 3 lines why this customer needs priority review and what action should be taken.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an AML and KYC banking compliance expert.",
        },
        {"role": "user", "content": prompt},
    ]

    body = {"model": "llama-3.3-70b-versatile", "messages": messages}

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f" could not generate review :{e}"


# Your turn — write the main script below:
# 1. Read customers.csv into a DataFrame
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "customers.csv")
df = pd.read_csv(csv_path)
# 2. Add priority_review column
df["priority_review"] = (df["kyc_status"] == "Pending") & (df["risk_rating"] == "High")
# 3. Filter only priority_review == True customers
priority_customer = df[df["priority_review"] == True]
# 4. Loop through each one
for index, customer in priority_customer.iterrows():
    # 5. Call get_ai_review() for each customer
    # 6. Print customer name + AI review
    review = get_ai_response(customer)  # ← inside loop
    print(customer["customer_name"])  # ← inside loop
    print(review)  # ← inside loop
    print("---")  # ← separator
