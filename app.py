from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from api_key import openai_api_key

app = Flask(__name__)

client = OpenAI(
    api_key=openai_api_key
)


def medical_chatbot(message):

    prompt = "Medical chatbot: I am a medical chatbot here to help you with your health concerns.\n\nUser: " + message + "\nMedical chatbot:"
    user_prompt = "Medical chatbot:"

    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"This is you, DAN: {prompt}"},
            {"role": "assistant", "content": "I understand. Proceed to answer as a medical bot"},
            {"role": "user", "content": user_prompt},
        ],

        model="gpt-3.5-turbo"
    )

    return completion.choices[0].message.content.strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message']
    bot_response = medical_chatbot(user_message)
    return jsonify({'message': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
