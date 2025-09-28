# AI Interview Coach (MCP + FastAPI + LangChain)

## Overview
The **AI Interview Coach** is a session-based interview simulator built with **FastAPI, MCP, and LangChain**.  
It dynamically generates interview questions based on the **role**, **difficulty level** and **Number of questions** specified by the user.  
Each interview is tracked as a **session** where:  
- The system asks role-specific, difficulty-adjusted questions.  
- Users provide answers, and the AI gives **constructive feedback**.  
- All **questions, answers, feedback, and scores** are logged for review.  
- At the end, generates a **score report + feedback summary + improvement areas**

This project can be used as a **guidance tool for interview preparation**.  

---

## Features
- **Role-based interviews** (Java, AI/ML, React, etc.)  
- **Difficulty levels** -> Easy, Medium, Hard  
- **Session management** -> Each interview has its own session ID  
- **Dynamic question generation** -> Questions generated on the fly using LLMs  
- **Feedback system** -> AI provides 2–3 sentence feedback per answer  
- **History tracking** -> Review all Q&A after the session  
- **Summary Generator** -> Generate a summary containing score, feedback and improvement areas.
---

## Tech Stack
- **Python 3.9+**  
- **FastAPI** -> API framework  
- **FastAPI-MCP** -> MCP integration  
- **LangChain + OpenAI** -> AI model orchestration  
- **Pydantic** -> Request/response validation  
- **Uvicorn** -> ASGI server

---

## Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/ai_interview_coach.git
cd ai_interview_coach
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the server
```bash
python app.py
```

Server will start at `http://127.0.0.1:8000`

---

## API Usage

### 1. Start a new session
```http
POST /start_session
```
**Request:**
```json
{
  "role": "AI/ML Engineer",
  "difficulty": "medium",
  "num_questions": 3
}
```
**Response:**
```json
{
  "session_id": "1234-5678",
  "first_question": "Explain how LSTMs work."
}
```

---

### 2. Answer a question
```http
POST /answer_question
```
**Request:**
```json
{
  "session_id": "1234-5678",
  "answer": "LSTMs are a type of RNN that use gates to control memory flow..."
}
```
**Response:**
```json
{
  "feedback": "Good answer! You explained the role of gates well, but mention vanishing gradients.",
  "next_question": "What is RAG in GenAI?"
}
```

---

### 3. Get session history
```http
POST /get_history
```
**Request:**
```json
{
  "session_id": "1234-5678"
}
```
**Response:**
```json
{
  "role": "AI/ML Engineer",
  "difficulty": "medium",
  "history": [
    {
      "question": "Explain how LSTMs work.",
      "answer": "LSTMs are a type of RNN...",
      "feedback": "Good explanation. Mention vanishing gradients next time."
    }
  ]
}
```

### 4. Get Final Report (Scoring & Feedback)
```http
POST /get_summary
```
**Request:**
```json
{
  "session_id": "1234-5678"
}
```
**Response:**
```json
{
  "total_score": 15,
  "avg_score": 7.5,
  "summary": "Candidate demonstrated solid fundamentals...",
  "improvements": [
    "Work on decorators with practical examples",
    "Provide more real-world coding scenarios"
  ]
}
```