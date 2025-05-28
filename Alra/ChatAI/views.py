import os
import json
import together
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Set your API key as environment variable
os.environ["TOGETHER_API_KEY"] = "05236ba11d5ed04d5d3fad11bd5a786901d21fe3f6012215fc1882dfd5e74c3d"

def index(request):
    return render(request, 'ChatAI/index.html')

def generate_response(question):
    prompt = (
        "You are a helpful assistant. "
        "Answer the following question clearly and briefly. "
        "Do not ask any questions or continue the conversation:\n\n"
        f"Q: {question}\nA:"
    )
    response = together.Complete.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.7,
        max_tokens=256,
        prompt=prompt,
    )
    text = response["choices"][0]["text"]

    # Stream word by word
    for word in text.split():
        yield word + ' '

@csrf_exempt
def answer(request):
    data = json.loads(request.body)
    message = data.get("message", "")
    response = StreamingHttpResponse(generate_response(message), status=200, content_type="text/plain")
    return response
