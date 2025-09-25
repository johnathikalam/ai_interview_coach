from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import settings

class InterviewAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=settings.openai_api_key)

    def generate_questions(self, role, difficulty, num_questions=5):
        """Generate interview questions dynamically"""
        prompt = ChatPromptTemplate.from_template(
            "You are an expert interviewer.\n"
            "Generate {num} {difficulty}-level interview questions for the role of {role}.\n"
            "Return the questions as a numbered list, without answers."
        )
        response = self.llm(prompt.format_messages(
            role=role, difficulty=difficulty, num=num_questions
        ))
        
        questions = [q.strip(" .") for q in response.content.split("\n") if q.strip()]
        return questions
    
    def evaluate_answer(self, question, answer):
        """Generate feedback for a given answer"""
        prompt = ChatPromptTemplate.from_template(
            "You are an interview coach. Evaluate the candidate's answer.\n"
            "Question: {question}\nAnswer: {answer}\n"
            "Provide short, constructive feedback (2-3 sentences)."
        )
        response = self.llm(prompt.format_messages(question=question, answer=answer))
        return response.content