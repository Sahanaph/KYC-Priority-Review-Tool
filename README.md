# KYC Priority Review Tool

An AI powered automation tool that identifies high-risk KYC customers 
and generates compliance review recommendations using LLM.

## What it does
- Reads customer data from CSV
- Automatically flags customers with Pending KYC and High risk rating
- Generates AML compliance review for each priority customer using AI
- Built for banking and fintech compliance teams

## Tech Stack
- Python
- pandas — data filtering and analysis
- Groq API + LLaMA — AI powered review generation
- requests — API integration

## How to run
1. Add your customer data to `customers.csv`
2. Add your Groq API key to `config.py`
3. Run `python Automate_kycanalysis.py`

## Background
Built as part of my AI engineering journey, combining 3 years of 
AML/KYC domain expertise with Python and LLM API development.
