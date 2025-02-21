from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import pymysql
import datetime
import pandas as pd
from typing import Optional

from collections import defaultdict

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
# please update the following database configuration
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',        
        user='root',           
        password= 'root',# put your password here''
        database='pain_study',  
        charset='utf8mb4')
    return connection


questions = [
    {
        "id": 1,
        "question": "How have you been feeling lately? Have you experienced any of the following symptoms in the last couple of weeks? (allow multiple choices here)",
        "type": "multiple_choice",
        "options": ["pain", "discomfort", "stress", "none of the above"]
    },
    {
        "id": 2,
        "question": "Can you tell me a little more about your pain? On a scale of 1 to 10, how intense was your average pain in the past 2 weeks?",
        "type": "VAS"
    },
    {
        "id": 8,
        "question": "Based on what we’ve talked about, it sounds like there are a few things we can work on. What is the one small goal you’d like to set for yourself in the next week?",
        "type": "single_choice",
        "options": [
            "Yes, I have a clear goal for the next week.",
            "Yes, I want to set a goal, but I’m not sure what it is now.",
            "Not sure. Why do I need to set a goal?"
        ]
    },
    {
        "id": 10,
        "question": "Can you describe any strategies or activities you’ve tried that might have helped?",
        "type": "text"
    },
    {
        "id": 11,
        "question": "Would you like to continue with this approach, or would you like me to suggest a couple of additional strategies that could support your improvement?",
        "type": "single_choice",
        "options": [
            "I think I’m good, and I would like to continue with my current approach.",
            "I will continue with my approach for sure, but I’d like to learn other approaches.",
            "I definitely want to try other new approaches.",
            "I’m not sure."
        ]
    },
    {
        "id": 12,
        "question": "Would you like to learn something new and add it to your routine, or would you just stick with what’s been working?",
        "type": "single_choice",
        "options": [
            "I think I’m good, and I would like to continue with my current approach.",
            "I will continue with my approach for sure, but I’d like to learn other approaches.",
            "I definitely want to try other new approaches.",
            "I’m not sure."
        ]
    },
    {
        "id": 13,
        "question": "It looks like your pain has increased since our last check-in. I’m sorry to hear that. Let’s see what we can do to help manage it. Have there been any changes in your routine or new activities that might be affecting your pain?",
        "type": "single_choice",
        "options": [
            "Yes, there are some changes that might increase my pain.",
            "No, I don’t think so.",
            "I’m not sure."
        ]
    },
    {
        "id": 14,
        "question": "Please let me know what happened.",
        "type": "text"
    },
    {
        "id": 15,
        "question": "Would you like suggestions on how to adjust your routine to reduce pain?",
        "type": "single_choice",
        "options": [
            "Yes. Let me know.",
            "No, I think I can handle it myself."
        ]
    },
    {
        "id": 16,
        "question": "New strategies: Here are some approaches that may help you further. Please select the one you would most like to learn more about.",
        "type": "single_choice",
        "options": [
            "core exercises",
            "increasing activity",
            "breathing techniques",
            "mindfulness",
            "stretching",
            "dietary adjustments"
        ]
    },
    {
        "id": 3,
        "question": "Have you noticed whether specific activities or stress seem to worsen your symptoms, like sitting too long or working too much?",
        "type": "single_choice",
        "options": ["Yes, that's true.", "No, I don’t think so."]
    },
    {
        "id": 17,
        "question": "It’s helpful to recognize what triggers your pain. Would you like tips on managing these, like taking breaks or stress relief?",
        "type": "single_choice",
        "options": [
            "Yes, that’ll be great.",
            "No, I’m good. I’m already doing regular activities. We can skip this for now."
        ]
    },
    {
        "id": 4,
        "question": "How would you describe your activity level over the past two weeks?",
        "type": "single_choice",
        "options": [
            "Low Activity <150 minutes/week",
            "Moderate Activity 150-300 minutes/week",
            "High Activity >300 minutes/week"
        ]
    },
    {
        "id": 5,
        "question": "It seems like stress has been a factor for you recently. Please tell me more about what’s been stressing you out and how you’ve been managing it?",
        "type": "text"
    },
    {
        "id": 18,
        "question": "Do you feel your stress is managed under control?",
        "type": "single_choice",
        "options": ["Yes, I think so.", "No, it often gets out of my control."]
    },
    {
        "id": 19,
        "question": "Would you like additional tools to maintain emotional balance, like guided meditation or mindfulness exercises?",
        "type": "single_choice",
        "options": ["Yes, tell me more.", "No, let’s skip that for now."]
    },
    {
        "id": 20,
        "question": "Let’s try some stress-relief strategies like breathing exercises or progressive muscle relaxation. Would you like to start a session?",
        "type": "single_choice",
        "options": [
            "Yes, tell me more.",
            "No, I don’t feel like learning them today. Maybe next time."
        ]
    },
    {
        "id": 6,
        "question": "Diet can sometimes affect pain. Do you want to describe your typical daily diet?",
        "type": "single_choice",
        "options": [
            "Yes, I’m happy to describe my diet.",
            "I don’t have a typical diet pattern, so it's hard to describe.",
            "No, I want to skip this."
        ]
    },
    {
        "id": 21,
        "question": "Please describe your diet here:",
        "type": "text"
    },
    {
        "id": 22,
        "question": "Your diet plays a significant role in managing inflammation and pain. Have you heard about anti-inflammatory diet?",
        "type": "single_choice",
        "options": [
            "No, I’ve never heard about it. I don’t want to change my diet.",
            "No, I’ve never heard about it, but I’m interested. Please tell me more.",
            "I’ve heard about it, but I don’t know what it means.",
            "Yes, I know it very well, but I don’t practice it in my life.",
            "Yes, I know it and I actually often have anti-inflammatory diet."
        ]
    },
    {
        "id": 23,
        "question": "It’s great that you already know it. There might be barriers that prevent you from actual practice of anti-inflammatory diet. Do you want to tell us?",
        "type": "single_choice",
        "options": ["Yes", "No"]
    },
    {
        "id": 24,
        "question": "Text here",
        "type": "text"
    },
    {
        "id": 25,
        "question": "BMI. Please tell us your height and weight:",
        "type": "text"
    },
    {
        "id": 7,
        "question": "Are you taking any medications to manage your pain, what are they?",
        "type": "single_choice",
        "options": ["Yes", "No"]
    },
    {
        "id": 26,
        "question": "Please tell us what you are taking",
        "type": "text"
    },
    {
        "id": 27,
        "question": "Have you experienced any side effects from your medications?",
        "type": "single_choice",
        "options": [
            "Yes, I’ve noticed some side effects.",
            "No, I haven’t noticed any side effects.",
            "I’m not sure."
        ]
    },
    {
        "id": 28,
        "question": "Please describe the side effects you’ve experienced.",
        "type": "text"
    },
    {
        "id": 29,
        "question": "Are you considering adjusting or stopping any of your medications?",
        "type": "single_choice",
        "options": [
            "Yes, I’m thinking about it.",
            "No, I plan to continue as prescribed.",
            "I’m not sure yet."
        ]
    },
    {
        "id": 30,
        "question": "Please tell us more about your thoughts on adjusting or stopping your medications.",
        "type": "text"
    },
    {
        "id": 31,
        "question": "Reflecting on your small goal, do you feel it is realistic and achievable within the next week?",
        "type": "single_choice",
        "options": [
            "Yes, I’m confident it’s achievable.",
            "No, I think it might be too ambitious.",
            "I’m not sure."
        ]
    },
    {
        "id": 32,
        "question": "What support or resources would help you achieve this goal?",
        "type": "text"
    },
    {
        "id": 33,
        "question": "Have you had any recent doctor or therapist visits for your pain management? If so, what was the outcome?",
        "type": "text"
    },
    {
        "id": 34,
        "question": "Would you like to share the advice or treatments you received during your visit?",
        "type": "single_choice",
        "options": [
            "Yes, I’d like to share.",
            "No, I prefer to keep it private."
        ]
    },
    {
        "id": 35,
        "question": "Do you have something in your mind now?",
        "type": "single_choice",
        "options": ["Yes", "No"]
    },
    {
        "id": 36,
        "question": "What is your goal?",
        "type": "text"
    },
    {   "id": 100,
        "question": "Thank you",
        "type": "text"
    }
    ]

import datetime
from typing import Optional
from collections import defaultdict

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, constr
import pymysql

class Username(BaseModel):
    username: constr(min_length=1) = Field(..., description="用户名不能为空")

users = defaultdict(lambda: {
    'new_user': True,
    'last_response': None,
    'information': None,
    'new_response': None
})

# Dependency for username
def get_current_user(username: Optional[str] = None):
    if username is not None:
        get_current_user.username = username
    return getattr(get_current_user, 'username', None)

@app.post("/welcome/")
async def welcome_user(
    user_data: Username,
    username_dependent: str = Depends(get_current_user)
):
    # 从请求体中取出 username 字符串
    username = user_data.username



    # 如果需要认证
    get_current_user(username)

    connection = get_db_connection()
    cursor = connection.cursor()

    # 先检查 user_table 中是否存在用户
    cursor.execute("SELECT * FROM user_table WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # 如果 users 字典里没有，就先初始化
        if username not in users:
            users[username] = {}

        users[username]['new_user'] = False

        # 获取最后一条 user_response
        cursor.execute("""
            SELECT * 
            FROM user_response
            WHERE username = %s
            ORDER BY submited_dt DESC
            LIMIT 1
        """, (username,))
        response = cursor.fetchone()

        if response:
            columns = [desc[0] for desc in cursor.description]
            response_dict = dict(zip(columns, response))
            users[username]['last_response'] = response_dict
        else:
            response_dict = {}
            users[username]['last_response'] = None

        # 获取 user_data 信息
        cursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
        info = cursor.fetchone()
        if info:
            columns = [desc[0] for desc in cursor.description]
            info_dict = dict(zip(columns, info))
            users[username]['information'] = info_dict

        # 创建 new_response
        if response_dict:
            users[username]['new_response'] = {key: '' for key in response_dict.keys()}
            users[username]['new_response']['response_id'] = 0
            users[username]['new_response']['user_id'] = response_dict.get('user_id', 0)
            users[username]['new_response']['username'] = response_dict.get('username', username)
        else:
            # 如果之前没提交过 response，则用表结构初始化
            cursor.execute("DESCRIBE user_response")
            columns = [column[0] for column in cursor.fetchall()]
            users[username]['new_response'] = {col: '' for col in columns}
            users[username]['new_response']['response_id'] = 0

            # 注意：只调用一次 fetchone()
            cursor.execute("SELECT user_id FROM user_table WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                user_id = row[0]
            else:
                user_id = 0

            users[username]['new_response']['user_id'] = user_id
            users[username]['new_response']['username'] = username

        users[username]['new_response']['new_user'] = False

        cursor.close()
        connection.close()

        return {
            "message": f"""Welcome back, {username}! I hope you’ve had a chance to reflect on the progress you’ve made so far. 
                Today is another opportunity to take positive steps toward managing your pain and improving your well-being. 
                Remember, this journey is about steady progress, not perfection, and every small effort counts. 
                Let’s get started for today!"""
        }

    else:
        # 新用户逻辑
        cursor.execute(
            "INSERT INTO user_table (username, created_dt) VALUES(%s, %s)",
            (username, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        connection.commit()

        # 获取新插入的 user_id
        cursor.execute("SELECT user_id FROM user_table WHERE username = %s", (username,))
        new_user_row = cursor.fetchone()
        if new_user_row:
            user_id = new_user_row[0]
        else:
            # 理论上不会出现，但做个防御
            user_id = 0

        # 初始化 new_response
        cursor.execute("DESCRIBE user_response")
        columns = [column[0] for column in cursor.fetchall()]

        if username not in users:
            users[username] = {}

        users[username]['new_response'] = {col: '' for col in columns}
        users[username]['new_response']['response_id'] = 0
        users[username]['new_response']['user_id'] = user_id
        users[username]['new_response']['username'] = username
        users[username]['new_response']['new_user'] = True

        cursor.close()
        connection.close()

        return {
            "message": f"""Welcome. Nice to e-meet you, {username}. I understand that you are suffering from pain. I’m here to help you. 
                Today, let’s stay open to learning, be patient with ourselves, and focus on what we can control. 
                Together, you will build the skills and strategies to manage pain and enhance your quality of life. 
                Let’s get started!
                """
        }

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

@app.post("/submit-answer/")
async def submit_answer(answer: Answer,current_user: str = Depends(get_current_user)):
    #print(answer)
    #print("**************")
    #print('current_user:',current_user)
    #print(type(current_user))
    if answer.question_id == 1:
        users[current_user]['new_response']['start_dt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if "none of the above" in answer.response:
            next_question_id = 8
            message = "It’s great that you're feeling well. Would you like tips for maintaining your health and preventing future issues?"
        else:
            next_question_id = 2
            message = "Got it! I’ll help you with strategies to manage them. Let’s start with your pain."

    elif answer.question_id == 2:
        diff_ratio = (5 - int(answer.response[0])) / 5
        print(f"[DEBUG] diff_ratio = {diff_ratio}")

        user_val = int(answer.response[0])
        print(f"[DEBUG] user_val = {user_val}")

        if 5 - user_val >= 2 or diff_ratio >= 1 / 3:
            print("[DEBUG] --> Entering the first if branch (pain improved)")
            next_question_id = 10
            message = "Although you're still experiencing some pain..."
        elif user_val - 5 >= 2 or (user_val - 5) / 5 >= 1 / 3:
            print("[DEBUG] --> Entering the second elif branch (pain increased)")
            next_question_id = 13
            message = "It looks like your pain has increased..."
        else:
            print("[DEBUG] --> Entering the else branch (no change)")
            next_question_id = 12
            message = "It looks like your pain has not changed.."

    elif answer.question_id == 10:
        message  = "It sounds like your approach has been helpful for you. "
        next_question_id = 11

    elif answer.question_id == 11:
        if "I think I" in answer.response[0]:
            next_question_id = 3
            message = "That’s great. Keep up with your approach. Feel free to let me know when you would like to learn about other strategies."
        elif "not sure" in answer.response[0]:
            next_question_id = 16
            message = "No worries! Sometimes progress happens gradually. Let's see whether you are interested in some other strategies."
        else:
            next_question_id = 16
            message = "Sure. Let me tell you more options."
    elif answer.question_id == 12:
        if "I think I" in answer.response[0]:
            next_question_id = 3
            message = "No problem. Sometimes progress happens gradually. Keep up with your approach. Feel free to let me know when you would like to learn about other strategies. "
        elif "not sure" in answer.response[0]:
            next_question_id = 16
            message = "No worries! Sometimes progress happens gradually. Let's see whether you are interested in some other strategies. "
        else:
            next_question_id = 16
            message = "Sure. Let me tell you more options."
    elif answer.question_id == 13:
        if "Yes" in answer.response[0]:
            next_question_id = 14
            message = "Please let me know what happened. "
        elif "No" in answer.response[0]:
            next_question_id = 3
            message = "Ok then. Let’s talk about something else."
        else:
            next_question_id = 3
            message = "That’s fine. Let’s not worry about it and move on to the next question."
    elif answer.question_id ==14:
        next_question_id = 15
        message= "Thanks for sharing that. **It seems like [identified change] could be contributing to the increase.**"
    elif answer.question_id == 15:
        if "Yes" in answer.response[0]:
            next_question_id = 3
            message = "Offer suggestions based on the identified changes."
        else:
            next_question_id = 3
            message = "Sure, I hope you feel better soon."
    elif answer.question_id ==16:   
        next_question_id = 3
        message  = "Thank you. That’s a good choice. I’m glad that you are interested in xxx. Let me tell you more about how it can help with your pain. [details following this can be the next step] "
    elif answer.question_id == 3:
        if "Yes" in answer.response[0]:
            next_question_id = 17
            message = "It’s helpful to recognize what triggers your pain."
        else:
            next_question_id = 4
            message = "????"

    elif answer.question_id == 17:
        if "Yes" in answer.response[0]:
            next_question_id = 4
            message = "Provide tips based on trigger (e.g., posture adjustment, stress management techniques). "
        else:
            next_question_id = 4
            message = "Great! Regular activity is important. Let’s move on and talk about something else. "
    elif answer.question_id == 4:
        if answer.response[0] <= 25:
                next_question_id = 5
                message = """It looks like you're not hitting the recommended 150 minutes of moderate exercise each week. Increasing your activity could help reduce pain and stress. We suggest that you start with some gentle exercises, such as walking or stretching, or get a plan tailored to your schedule. 
                                •	Beginner Exercise Plan: Start small, like a 10-minute walk or gentle yoga session. Provide video guides.
                                •	We can also set daily reminders to help you gradually increase your activity level.
                                    """
        elif answer.response[0] > 25 and answer.response[0] <= 35:
            next_question_id = 5
            message = """Great! You're staying active, which is key for managing pain. To build on this, we suggest you try adding some core strengthening exercises or flexibility training like yoga. Provide information."""
        else:
            next_question_id = 5
            message = """You're doing a fantastic job staying active! To ensure your muscles get the recovery they need, we suggest that you try some recovery activities like light stretching or gentle yoga today. Provide information"""
    elif answer.question_id == 5:
        next_question_id = 18
        message = "Thank you for sharing your experience. Realizing your own stressors can be a key first step toward successful management of you pain. "
    elif answer.question_id == 18:
        if "Yes" in answer.response[0]:
            next_question_id = 19
            message = "That’s great! "
        else:
            next_question_id = 20
            message = "Let’s try some stress-relief strategies like breathing exercises or progressive muscle relaxation. "
    elif answer.question_id == 19:
        if "Yes" in answer.response[0]:
            next_question_id = 6
            message = "Offer mindfulness tools"
        else:
            next_question_id = 6
            message = "Sure, let’s skip it and talk about something else"
    elif answer.question_id == 20:
        if "Yes" in answer.response[0]:
            next_question_id = 6
            message = "Provide relaxation techniques with video/audio guides"
        else:
            next_question_id = 6
            message = "Sure, let’s skip it and talk about something else"
    
    elif answer.question_id == 6:
        if "Yes" in answer.response[0]:
            next_question_id = 21
            message = "Describe your diet"
        else:
            next_question_id = 22
            message = "No worries. That’s totally ok."
    elif answer.question_id == 21:
        next_question_id = 22
        message = "Thank you for sharing with us."
    elif answer.question_id == 22:
        if "change my diet" in answer.response[0]:
            next_question_id = 25
            message = "I understand that it sometimes very difficult to change your diet. But we do want to let you know that a healthy diet can help reduce inflammation and pain. Anti-inflammatory diet, including foods like leafy greens, berries, and healthy fats, can be very helpful.  No pressures. Let’s move on for now. You are always welcome to come back to us to learn more about healthy diet. "
        elif "very well" in answer.response[0]:
            next_question_id = 23
            message = "It’s great that you already know it. There might be barriers that prevent you from actual practice of anti-inflammatory diet."
        else:
            next_question_id = 25
            message = """Great! That’s a good start. A healthy diet can help reduce inflammation and pain. 
                            Provide an anti-inflammatory diet guide with recipes and tips.
                            Suggest meal tracking for continued improvement.
                        """
    elif answer.question_id == 23:
        if "Yes" in answer.response[0]:
            next_question_id = 24
            message = "Tell us the barriers that prevent you from actual practice of anti-inflammatory diet."
        else:
            next_question_id = 25
            message = "That’s fine. Let’s move on. "
    elif answer.question_id == 24:
        next_question_id = 25
        message = "Thank you."
    elif answer.question_id == 25:
        height_ft = int(answer.response[0].split()[0])
        height_in = int(answer.response[1].split()[0])
        weight = int(answer.response[2].split()[0])
        
        next_question_id = 7
        message = "Thank you"
    elif answer.question_id == 7:
        if "Yes" in answer.response[0]:
            next_question_id = 26
            message = "Please tell us what you are taking"
        else:
            next_question_id = 8
            message = " I’m glad to know that you don’t need to take any medications for your pain. Many people manage pain without medication. But it can be helpful to help with acute pain flare up. →  Provide education.  → Offer non-pharmacological strategies based on their response."
    elif answer.question_id == 26:
        next_question_id = 27
        message = "Thank you. "
    elif answer.question_id == 27:
        if "help a lot" in answer.response[0]:
            next_question_id = 29
            message = "Good to hear they’re helping! Long-term taking these medication can cause health issues ____. "
        else:
            next_question_id = 28
            message = "It sounds like the medication isn’t working as expected. Let’s dig a little more. "

    elif answer.question_id ==28:
        next_question_id = 8
        message = "Identify medication taken issues and provide education. Provide options for physical activities or alternative relief strategies. "

    elif answer.question_id == 29:
        next_question_id = 8
        message = "???"
    elif answer.question_id == 8:
        if "a clear goal" in answer.response[0]:
            message = "That’s great. "
            next_question_id = 30
        elif "set a goal" in answer.response[0]:
            message = 'No problem! Your goals should reflect what’s important and realistic for you. You can adjust your goals based on how you’re feeling, ensuring they remain achievable and relevant. Be clear about how you will measure success. Use numbers or time to define your goals so you can track progress. For example: "I will stretch for 10 minutes every morning" or "I will meditate for 5 minutes every day.”'
            next_question_id = 31
        else:
            message = '''Pain is unique to each person, and you know your body best. Setting your own goals allows you to tailor them to your specific needs, challenges, and lifestyle. Reaching a goal, no matter how small, brings a sense of accomplishment. This also gives you a sense of control and responsibility, which can be incredibly motivating.
                        Your goals should reflect what’s important and realistic for you. You can adjust your goals based on how you’re feeling, ensuring they remain achievable and relevant. Be clear about how you will measure success. Use numbers or time to define your goals so you can track progress. For example: "I will stretch for 10 minutes every morning" or "I will meditate for 5 minutes every day.”
                        '''
            next_question_id = 35
    elif answer.question_id == 30:
        message =  "That’s a great goal! Let’s schedule some reminders to keep you on track."
        next_question_id = 33
    elif answer.question_id == 31:
        if "Yes" in answer.response[0]:
            next_question_id =32
            message = "That’s great. "
        else:
            next_question_id = 34
            message = "No problem. Let me suggest one based on our conversation. "
    elif answer.question_id == 32:
        message = "That’s a great goal! Let’s schedule some reminders to keep you on track. "
        next_question_id = 33
    elif answer.question_id == 33:
        message = "Offer reminders based on their goal."
        next_question_id = 100
        users[current_user]['new_response']['submited_dt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = get_db_connection()
        cursor = connection.cursor()
        columns = ', '.join(users[current_user]['new_response'].keys())  
        placeholders = ""
        for val in users[current_user]['new_response'].values():
            if type(val) == str:
                placeholders += f'"{val}",'
            else:
                placeholders += str(val)
                placeholders += ','
        placeholders= placeholders[:-1]
        insert_query = f'INSERT INTO user_response ({columns}) VALUES ({placeholders})'
        cursor.execute(insert_query)
        connection.commit()
        bmi_text = users[current_user]['new_response']['answer25']
        if bmi_text != '':
            result = []
            for i in bmi_text.split(','):
                result.append(int(i.split()[0]))
            info_query = f"INSERT INTO pain_study.user_data (username, weight_lbs, height_feet, height_inches) VALUES('{current_user}',{result[2]}, {result[0]}, {result[1]});"
            cursor.execute(info_query)
            connection.commit()
        cursor.close()
    elif answer.question_id == 34:
        message = "Provide preset goals with simple reminders."
        next_question_id  = 100
        #print('current_user:',current_user)
        users[current_user]['new_response']['submited_dt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = get_db_connection()
        cursor = connection.cursor()
        #print(users[current_user]['new_response'])
        columns = ', '.join(users[current_user]['new_response'].keys()) 
        placeholders = ""
        for val in users[current_user]['new_response'].values():
            if type(val) == str:
                placeholders += f'"{val}",'
            else:
                placeholders += str(val)
                placeholders += ','
        placeholders= placeholders[:-1]
        insert_query = f'INSERT INTO user_response ({columns}) VALUES ({placeholders})'
        cursor.execute(insert_query)
        connection.commit()
        bmi_text = users[current_user]['new_response']['answer25']
        if bmi_text != '':
            result = []
            for i in bmi_text.split(','):
                result.append(int(i.split()[0]))
            info_query = f"INSERT INTO pain_study.user_data (username, weight_lbs, height_feet, height_inches) VALUES('{current_user}',{result[2]}, {result[0]}, {result[1]});"
            cursor.execute(info_query)
            connection.commit()
        cursor.close()
    elif answer.question_id == 35:
        if "Yes" in answer.response[0]:
            message = "That’s great. "
            next_question_id = 36
        else:
            message = "No problem. Let me suggest one based on our conversation. How about aiming for 10 minutes of stretching each day to help reduce your pain? "
            next_question_id = 34
    elif answer.question_id == 36:
        message = "That’s a great goal! Let’s schedule some reminders to keep you on track. "
        next_question_id = 33
    if answer.question_id != 4:
        users[current_user]['new_response'][f"answer{answer.question_id}"] = ",".join(answer.response)
    else:
        users[current_user]['new_response'][f"answer{answer.question_id}"] = str(answer.response[0])
    return {"message": message, "next_question_id": next_question_id}

