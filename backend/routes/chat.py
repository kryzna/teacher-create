from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.models import User
from backend.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest, current_user: User = Depends(get_current_user)):
    response = generate_response(body.message)
    return ChatResponse(response=response)


def generate_response(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "lesson" in prompt_lower or "plan" in prompt_lower:
        return "I'd be happy to help you create a lesson plan! What subject area and age group are you working with? I can suggest activities aligned with Montessori curriculum standards."
    elif "observation" in prompt_lower or "observe" in prompt_lower:
        return "For effective observations, focus on: 1) What the child is choosing to do 2) How long they maintain focus 3) Any repeated behaviors 4) Social interactions. Would you like me to create an observation template?"
    elif "material" in prompt_lower or "materials" in prompt_lower:
        return "Montessori materials should be: accessible, self-correcting, and presented in a logical sequence. What specific material area are you looking to incorporate?"
    elif "progress" in prompt_lower or "report" in prompt_lower:
        return "I can help you generate progress reports! I can create personalized newsletters highlighting each student's achievements and next steps. Would you like me to generate one for a specific student or the whole class?"
    else:
        return f"That's a great question about '{prompt}'! As your Montessori assistant, I can help with lesson planning, observations, student progress tracking, and generating parent communications. What specific aspect would you like to explore?"
