from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import settings

class InterviewAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=settings.openai_api_key)  # or your preferred model
        self.questions = [
            "Explain OOP concepts in Java with examples.",
            "What is RAG (Retrieval Augmented Generation) in GenAI?",
            "How do you optimize Python code for ML pipelines?",
            "Explain REST vs GraphQL in a real-world project."
        ]
        self.index = 0

    def get_question(self):
        if self.index < len(self.questions):
            return self.questions[self.index]
        return "Interview complete. Great job!"

    def evaluate_answer(self, answer):
        prompt = ChatPromptTemplate.from_template(
            "You are an interview coach. Evaluate the following answer and give short feedback.\n"
            "Question: {question}\nAnswer: {answer}\n\nGive feedback in 2-3 sentences."
        )
        feedback = self.llm(prompt.format_messages(
            question=self.questions[self.index], answer=answer
        )).content

        self.index += 1
        return feedback, self.get_question()
