from flask import Flask, render_template, request, jsonify
import requests  # or use your LLM library directly
from dotenv import load_dotenv
import os

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

load_dotenv()

REGION_NAME = os.getenv("REGION_NAME")
AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_SESSION_TOKEN= os.getenv("AWS_SESSION_TOKEN")

app = Flask(__name__)
try:
    model = ChatBedrock(model_id="meta.llama3-1-8b-instruct-v1:0",
                        region_name=REGION_NAME,
                        aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY,
                        aws_session_token=AWS_SESSION_TOKEN)
except Exception as e:
    print(f"Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = get_bot_response(user_message) # Replace with your function
    
    return jsonify({'reply': bot_response})

def get_bot_response(message):
    # Simulated response for demonstration
    response = model.invoke([HumanMessage(content=message)])
    return response.content  # Replace with your LLM interaction logic

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)