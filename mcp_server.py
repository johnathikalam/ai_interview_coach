import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from interview_agent import InterviewAgent
from pydantic import BaseModel

class Response(BaseModel):
    answer: str
    session_id: str

class StartRequest(BaseModel):
    role: str
    difficulty: str
    num_questions: int = 5

class History(BaseModel):
    session_id: str
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp = FastApiMCP(app, "AI Interview Coach")
mcp.mount()

sessions = {}

agent = InterviewAgent()


@app.post("/start_session")
async def start_session(request: StartRequest):
    
    session_id = str(uuid.uuid4())
    questions = agent.generate_questions(request.role, request.difficulty, request.num_questions)

    sessions[session_id] = {
        "role": request.role,
        "difficulty": request.difficulty,
        "questions": questions,
        "index": 0,
        "history": []
    }

    first_question = questions[0] if questions else "No questions available."
    return {"session_id": session_id, "first_question": first_question}

@app.post("/answer_question")
async def answer_question(response: Response):
    """Submit an answer and get feedback + next question"""
    if response.session_id not in sessions:
        return {"error": "Invalid session ID."}

    session = sessions[response.session_id]
    idx = session["index"]

    if idx >= len(session["questions"]):
        return {"message": "Interview already complete."}

    question = session["questions"][idx]

    feedback = agent.evaluate_answer(question, response.answer)

    session["history"].append({
        "question": question,
        "answer": response.answer,
        "feedback": feedback
    })

    session["index"] += 1
    next_q = (
        session["questions"][session["index"]]
        if session["index"] < len(session["questions"])
        else "Interview complete. Great job!"
    )

    return {"feedback": feedback, "next_question": next_q}

@app.post("/get_history")
async def get_history(history: History):
    """Retrieve history of a session"""
    if history.session_id not in sessions:
        return {"error": "Invalid session ID."}
    return sessions[history.session_id]