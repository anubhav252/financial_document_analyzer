# Financial Document Analyzer

## Overview
A CrewAI-powered system to analyze financial documents, provide AI-driven investment recommendations, and assess risk.  
The system leverages multiple AI agents for financial analysis, verification, investment advisory, and risk assessment.

---

## Features
- Upload and analyze PDF financial documents
- AI-generated investment recommendations
- Risk assessment with dramatic, imaginative analysis
- Market insights and financial advice
- Modular tools for PDF reading, investment analysis, and risk assessment

---

## Bugs Found & Fixes
1. **Agent Import Error**: `Agent` class from CrewAI was incompatible; updated imports and agent initialization.
2. **PDF Reading Issues**: Fixed `PdfReader` usage and cleaned up formatting in `tools.py`.
3. **Async Issues**: Corrected `async` usage in custom tools for reading, analyzing, and risk assessment.
4. **Missing Dependencies**: Added `starlette`, `json_repair`, `pypdf` and other missing packages in `requirements.txt`.
5. **Uvicorn Server Errors**: Corrected module paths and ASGI app configuration.
6. **Incomplete Investment & Risk Logic**: Implemented basic processing and sample analysis logic for tools.
7. **Prompt Optimization**: Improved agent backstories and prompts for more realistic output.

---

## Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/<username>/<repo>.git
cd financial-document-analyzer

2.**Create and activate a virtual environment:**
python -m venv .venv
# Windows
.\.venv\Scripts\activate

3.**Install dependencies:**
pip install -r requirements.txt

4.**Set up environment variables:**
Create a .env file in the project root with your API keys:
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here

5.**Run the FastAPI server:**
uvicorn main:app --reload

----------------------------------------------------------------------------------------
API Documentation:-

Health Check:
GET /
Response:
{
  "message": "Financial Document Analyzer API is running"
}

Analyze Financial Document:
POST /analyze
Form-data:
- file: PDF document
- query: Optional query string

Response:
{
  "status": "success",
  "query": "Analyze this financial document for investment insights",
  "analysis": "AI-generated financial insights...",
  "file_processed": "uploaded_filename.pdf"
}

-------------------------------------------------------------------------------------
Tools Overview:-

FinancialDocumentTool:
.Reads PDF documents
.Cleans and formats financial content

InvestmentTool:
.Analyzes financial document data
.Generates investment recommendations

RiskTool:
.Performs risk assessment
.Produces extreme risk scenarios and insights

Search Tool:
.Uses SerperDev API to search the internet for financial references

-----------------------------------------------------------------------------------------
Notes:-

.The AI agents are designed for educational and demonstration purposes. Do not rely on them for real financial advice.
.Ensure your OpenAI API key is valid and has sufficient quota.