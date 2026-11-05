from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_email(email):

    prompt = f"""
    You are an executive assistant.
    Summarize this email.
    Subject:{email["subject"]}
    Sender:{email["sender"]}
    Body:{email["body"]}

    
    Return ONLY raw JSON.

    Do not wrap the response in markdown.
    
    Do not use ```json.
    
    Do not explain your answer.
    
    Return only the JSON object.
    {{
      "message_id": ""
      "category": "",
      "priority_score": 0,      
      "priority_reason": "",
      "summary": "",
      "action_items": []
    }}
    
    
    
    Priority score must be an integer from 0 to 100.
    Possible categories: work, security, personal, promotional, job search, social media, financial, golf
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": prompt}
        ]
    )

    analyses = json.loads(response.choices[0].message.content)

    return analyses