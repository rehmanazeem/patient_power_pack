from flask import Flask, render_template, request, jsonify
import requests  # or use your LLM library directly
from dotenv import load_dotenv
import os

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

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

parser = StrOutputParser()

chain = model | parser

systemPrompt = """You are an AI assitant that can help with medical questions. Your user is a patient named Anna. 

Here is a doctor report about Anna's condition:

---
We report about the patient Anna Kumari, 45 years old, who was treated in our clinic.

Main diagnoses:
Stage I early breast cancer, cT1c N0 M0
Luminal B type, ductal invasive carcinoma
ER 90%, PR 60%, HER2neu negativ
G3, Ki67 20%
Other relevant diagnoses:
Osteoporosis
Low Vitamin D levels

History:
The patient presented for an infrared camera breast cancer screening in May 2024. The
infrared imaging highlighted a small, suspicious area that wasn't palpable. Further
diagnostic tests confirmed the small area as a stage I breast cancer. Staging diagnostics
did not display any metastases. The recommendation of the tumor board was to
perform a neoadjuvant chemotherapy, followed by a breast-conserving surgery of the
breast and axilla and an adjuvant radiotherapy as well as endocrine treatment.

Dianostics:
Infrared camera (02.05.24): abmormal region of the right breast
Sonography (04.06.24): right side BI-RADs IV (17mm), left side BI-RADS II
Mammography (04.06.24): right side BI-RADs IV (17mm), left side BI-RADS II
Histology (04.06.24): ductal invasive carcinoma, G3,
Immunohistochemistry: ER 90%, PR 60%, HER2neu negativ, Ki67 20%

Staging diagnostics:
Sonography of the liver (26.06.24): not suspicious
X-ray of the chest (30.06.24): not suspicious
Tumor board recommendation (14.07.24):
- Neoadjuvant chemotherapy with 4 cycles of Epirubicin and Cylophosphamide
followed by 12 cycles of weekly Paclitaxel
- Breast-conserving surgery of the breast and axilla
- Radiotherapy
- Adjuvant endocrine treatment with tamoxifen

---
"""

messages = [
    SystemMessage(content=systemPrompt)
]

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
    messages.append(HumanMessage(content=message))
    response = chain.invoke(messages)
    messages.append(SystemMessage(content=response))
    return response  # Replace with your LLM interaction logic

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)