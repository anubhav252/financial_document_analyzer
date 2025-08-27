



from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from tasks import analyze_financial_document, investment_analysis, risk_assessment, verification

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the full Crew pipeline sequentially with structured outputs"""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
    )
    
    # Kickoff with inputs
    results = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    # Build structured JSON
    structured_output = {
        "verification": str(results[verification.id]) if verification.id in results else "N/A",
        "analysis": str(results[analyze_financial_document.id]) if analyze_financial_document.id in results else "N/A",
        "recommendations": str(results[investment_analysis.id]) if investment_analysis.id in results else "N/A",
        "risk_assessment": str(results[risk_assessment.id]) if risk_assessment.id in results else "N/A",
    }
    return structured_output

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_api(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if not query.strip():
            query = "Analyze this financial document for investment insights"
        
        response = run_crew(query=query.strip(), file_path=file_path)
        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "results": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
