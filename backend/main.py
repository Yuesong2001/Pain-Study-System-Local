from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class Answer(BaseModel):
    question_id: int
    response: List = Field(..., min_items=1)



questions = [
    {
        "id": 1,
        "question": "1. How have you been feeling lately? (allow multiple choices here)",
        "type": "multiple_choice",
        "options": ["pain", "discomfort", "stress", "none of the above"]
    },
    {
        "id": 2,
        "question": "Can you tell me a little more about your pain?",
        "type": "VAS"
    },
    {
        "id": 10,
        "question": "Can you describe your diet? ",
        "type": "text"
    },
    {
        "id": 25,
        "question": "BMI. Please tell us your height and weight:",
        "type": "text"
    },
    {   "id": 100,
        "question": "Thank you",
        "type": "text"
    }
    ]


@app.post("/submit-answer/")
async def submit_answer(answer: Answer):
    # print(answer)
    if answer.question_id == 1:
        if "none of the above" in answer.response:
            next_question_id = 10
            message = "It’s great that you're feeling well. Would you like tips for maintaining your health and preventing future issues?"
        else:
            next_question_id = 2
            message = "Got it! I’ll help you with strategies to manage them. Let’s start with your pain."

    elif answer.question_id == 2:
        if 5- int(answer.response[0]) >= 2 or (5- int(answer.response[0]) )/5 >= 1/3:
            next_question_id = 100
            message = "Although you're still experiencing some pain, it seems like you're making improvements! That’s a great sign. Let’s take a moment to reflect on what’s changed since our last check-in."
        elif int(answer.response[0])  - 5 >= 2 or (int(answer.response[0])  - 5)/5 >= 1/3:
            next_question_id = 100
            message = "It looks like your pain has increased since our last check-in. I’m sorry to hear that. Let’s see what we can do to help manage it."
        else:
            next_question_id = 100
            message = "It looks like your pain has not changed since our last check-in."

    elif answer.question_id == 10:
        message  = "It sounds like your approach has been helpful for you. "
        next_question_id = 25
    elif answer.question_id == 25:
        height = answer.response[0]
        weight = answer.response[2]
        next_question_id = 100
        message = "Thank you"
    return {"message": message, "next_question_id": next_question_id}


class Username(BaseModel):
    username: str

users = {"test": {"visited": True}}

@app.get("/get-question/{question_id}")
async def get_question(question_id: int):
    question = next((q for q in questions if q["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "id": question["id"],
        "text": question["question"],  
        "type": question["type"],
        "options": question.get("options", [])
    }

@app.post("/welcome/")
async def welcome_user(username: Username):
    if username.username in users:
        return {"message": f"""Welcome back, {username.username}! I hope you’ve had a chance to reflect on the progress you’ve made so far. 
                Today is another opportunity to take positive steps toward managing your pain and improving your well-being. 
                Remember, this journey is about steady progress, not perfection, and every small effort counts. 
                Let’s get started for today!"""}
    else:
        users[username.username] = {"visited": True}
        return {"message": f"""Welcome. Nice to e-meet you, {username.username}. I understand that you are suffering from pain. I’m here to help you. 
                Today, let’s stay open to learning, be patient with ourselves, and focus on what we can control. Together, you will build the skills and strategies to manage pain and enhance your quality of life. Let’s get started!
                """}
