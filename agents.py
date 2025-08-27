


import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent
from tools import read_pdf, analyze_investment, create_risk_assessment, search_tool

# TODO: Replace with actual LLM from your setup (example: OpenAI GPT or local model)
from crewai.llms import OpenAI
llm = OpenAI(model="gpt-4")   # <--- FIXED (was llm=llm before, invalid)

# ---- Financial Analyst Agent ----
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and provide structured investment insights.",
    verbose=True,
    memory=True,
    backstory=(
        "An experienced financial analyst who evaluates market trends, "
        "ratios, and company performance to provide investment insights."
    ),
    tools=[read_pdf, analyze_investment],
    llm=llm,
    max_iter=2,
    max_rpm=1,
    allow_delegation=True
)

# ---- Document Verifier Agent ----
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify if the uploaded file is a financial document.",
    verbose=True,
    memory=True,
    backstory="You are responsible for ensuring that uploaded documents are valid financial reports.",
    tools=[read_pdf],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# ---- Investment Advisor Agent ----
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide investment recommendations based on financial document insights.",
    verbose=True,
    backstory="A knowledgeable advisor who recommends investments based on analysis and trends.",
    tools=[analyze_investment, search_tool],
    llm=llm,
    max_iter=2,
    max_rpm=1,
    allow_delegation=False
)

# ---- Risk Assessor Agent ----
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Evaluate risks associated with investments and provide a risk score.",
    verbose=True,
    backstory="Expert in identifying financial and market risks from documents.",
    tools=[create_risk_assessment],
    llm=llm,
    max_iter=2,
    max_rpm=1,
    allow_delegation=False
)
