from django.shortcuts import render
from .forms import ResumeForm
from groq import Groq
from dotenv import load_dotenv
import os
import fitz
import re
import ast

load_dotenv()
key = os.getenv("GROQ_API_KEY")
model = Groq(api_key=key)

# Create your views here.
def home(request):
    if request.method == 'POST':
        answer = None
        form = ResumeForm(request.POST, request.FILES)
        if (form.is_valid()):
            form.save()
            file = request.FILES['document']
            comment = form.cleaned_data['comment']
            doc = fitz.open(f'media/pdfs/{file}')
            npages = len(doc)
            resume = ''
            for page_num in range(npages):
                page = doc[page_num]
                text = page.get_text()
                resume += text
            smfb = model.chat.completions.create(
                messages=[
                    {"role":"system","content":"You are a professional Resume Summarizer and feedback and improvement giver"},
                    {"role":"user","content":resume+comment+"summarize and give feedback and give improvement in dictionary format of three keys 'summary' and 'feedback' and 'improvement' containing those as values respectively as list of strings and dont mention this method in the answer also just return the dictionary only please"}
                ],
                model="llama3-70b-8192",
                temperature=0.5
            )
            answer = smfb.choices[0].message.content
            answer = re.sub(r'\*\*(.*?)\*\*', r'<p><b>\1</b></p>', answer)
            answer  = ast.literal_eval(answer)
    else:
        form = ResumeForm()
        answer = None
    return render(request, 'home.html',{'form':form,'answer':answer})