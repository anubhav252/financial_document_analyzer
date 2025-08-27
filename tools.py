


import os
import re
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tool
from pypdf import PdfReader
from crewai_tools.tools.serper_dev_tool import SerperDevTool

# ---- Search Tool ----
search_tool = SerperDevTool()


# ---- PDF Reader Tool ----
@tool("Read and extract plain text from a PDF file")
def read_pdf(path: str = "data/sample.pdf") -> str:
    """
    Read a PDF from the given path and return all text as a single string.
    """
    if not path or not os.path.exists(path):
        return f"ERROR: File not found at {path}"

    try:
        reader = PdfReader(path)
        pages_text = []
        for page in reader.pages:
            text = page.extract_text() or ""
            while "\n\n" in text:
                text = text.replace("\n\n", "\n")
            pages_text.append(text.strip())
        return "\n\n".join(pages_text).strip()
    except Exception as e:
        return f"ERROR: Failed to read PDF: {e}"


# ---- Investment Analysis Tool ----
@tool("Perform investment analysis on extracted financial document data")
def analyze_investment(financial_document_data: str) -> str:
    """
    Analyze financial document data to extract investment insights.
    Returns Buy / Hold / Sell recommendations with reasoning.
    """
    if not financial_document_data:
        return "ERROR: No financial document data provided."

    text = financial_document_data.lower()

    # Simple keyword-based financial indicators
    bullish_signals = []
    bearish_signals = []

    if "revenue growth" in text or "increased revenue" in text:
        bullish_signals.append("Revenue growth indicates business expansion.")
    if "profit" in text or "net income" in text:
        bullish_signals.append("Profitable company — strong fundamentals.")
    if "loss" in text or "negative income" in text:
        bearish_signals.append("Reported losses — financial weakness.")
    if "debt" in text or "liabilities" in text:
        bearish_signals.append("High debt levels may constrain growth.")
    if "cash flow" in text and "positive" in text:
        bullish_signals.append("Positive cash flow — good liquidity.")
    if "decline" in text or "drop" in text:
        bearish_signals.append("Declining performance metrics found.")

    # Simple recommendation logic
    if len(bullish_signals) > len(bearish_signals):
        recommendation = "BUY — bullish indicators outweigh risks."
    elif len(bullish_signals) < len(bearish_signals):
        recommendation = "SELL — risks outweigh positive signals."
    else:
        recommendation = "HOLD — mixed signals detected."

    return (
        f"📊 Investment Analysis\n"
        f"Recommendation: {recommendation}\n\n"
        f"✅ Bullish Signals:\n- " + "\n- ".join(bullish_signals or ["None"]) +
        f"\n\n⚠️ Bearish Signals:\n- " + "\n- ".join(bearish_signals or ["None"])
    )


# ---- Risk Assessment Tool ----
@tool("Perform risk assessment based on financial document data")
def create_risk_assessment(financial_document_data: str) -> str:
    """
    Assess risks based on financial document data.
    Returns a risk score (0–10) and risk category.
    """
    if not financial_document_data:
        return "ERROR: No financial document data provided."

    text = financial_document_data.lower()

    risk_keywords = {
        "debt": 2,
        "lawsuit": 3,
        "inflation": 2,
        "volatility": 2,
        "uncertain": 2,
        "liabilities": 2,
        "regulatory": 3,
        "decline": 1,
        "loss": 2,
        "crisis": 3,
    }

    score = 0
    risks_found = []

    for word, weight in risk_keywords.items():
        if word in text:
            score += weight
            risks_found.append(f"{word.title()} (weight {weight})")

    # Cap risk score at 10
    score = min(score, 10)

    if score <= 3:
        category = "Low Risk"
    elif score <= 6:
        category = "Medium Risk"
    else:
        category = "High Risk"

    return (
        f"⚠️ Risk Assessment\n"
        f"Risk Score: {score}/10\n"
        f"Category: {category}\n\n"
        f"Identified Risks:\n- " + "\n- ".join(risks_found or ["No major risks detected."])
    )
