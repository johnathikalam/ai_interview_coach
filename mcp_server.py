from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from interview_agent import InterviewAgent
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    answer: str

class RoleRequest(BaseModel):
    role: str

# Create FastAPI app
app = FastAPI()

# Attach MCP to FastAPI
mcp = FastApiMCP(app, "AI Interview Coach")
mcp.mount()
agent = InterviewAgent()

@app.post("/start_session")
async def start_session(role: str = "Java Backend Developer"):
    """Start a new interview session"""
    return {"message": f"Starting interview for {role}", "question": agent.get_question()}

@app.post("/answer_question")
async def answer_question(request: AnswerRequest):
    """Submit answer and get feedback + next question"""
    feedback, next_q = agent.evaluate_answer(request.answer)
    return {"feedback": feedback, "next_question": next_q}
