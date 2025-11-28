from pydantic import BaseModel
import base64
from PIL import Image
import io

from agent import agent

class AnalyzeRequest(BaseModel):
    image_data: str = None
    # Далее поля, которые фигуруют в последующих запросах
    questions: str = None
    question_answers: str = None
    rash_description: str = None

async def analyze(
    analyze_request: AnalyzeRequest,
):
    if analyze_request.questions and analyze_request.question_answers and analyze_request.rash_description:
        return {
            'recommendations' : agent.generate_recommendation(analyze_request.questions,
            analyze_request.question_answers, 
            analyze_request.rash_description)
        }
    elif analyze_request.image_data:
        image = Image.open(io.BytesIO(base64.b64decode(analyze_request.image_data)))

        questions, rash_description = agent.generate_questions(image)
        return {
            'questions' : questions,
            'rash_description': rash_description
        }
    return {
        'error': 'Недостаточно данных. Предоставьте либо изображение, либо все данные для диагностики'
    }