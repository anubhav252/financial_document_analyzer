


from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_pdf, analyze_investment, create_risk_assessment, search_tool

# ---- Verification Task ----
verification = Task(
    description="Verify whether the uploaded document is a valid financial report.",
    expected_output="A validation result confirming if the document is a financial report.",
    agent=verifier,
    tools=[read_pdf],
    async_execution=False,
)

# ---- Financial Document Analysis Task ----
analyze_financial_document = Task(
    description=(
        "Analyze the financial document (path: {file_path}) and summarize key financial data. "
        "User query: {query}"
    ),
    expected_output="Detailed summary with extracted key financial metrics and market insights.",
    agent=financial_analyst,
    tools=[read_pdf, analyze_investment],
    async_execution=False,
)

# ---- Investment Analysis Task ----
investment_analysis = Task(
    description=(
        "Based on the financial analysis: {analyze_financial_document}, "
        "provide investment recommendations."
    ),
    expected_output="Actionable investment recommendations (buy/sell/hold, diversification, opportunities).",
    agent=investment_advisor,
    tools=[analyze_investment, search_tool],
    async_execution=False,
)

# ---- Risk Assessment Task ----
risk_assessment = Task(
    description=(
        "Based on the financial analysis: {analyze_financial_document} "
        "and the investment recommendations: {investment_analysis}, "
        "generate a structured risk assessment."
    ),
    expected_output="Risk score, risk category (Low/Medium/High), risk factors, and mitigation advice.",
    agent=risk_assessor,
    tools=[create_risk_assessment],
    async_execution=False,
)
