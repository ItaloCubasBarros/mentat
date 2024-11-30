import os
import openai
import PyPDF2
from flask import Flask, render_template, request, redirect, url_for


openai.api_key = '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'  # Substitua pela sua chave real

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in range(len(leitor.pages)):
            texto += leitor.pages[pagina].extract_text()
    return texto


def gerar_resumo(texto):
    resposta = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "Você é um assistente de IA que cria resumos concisos."},
            {"role": "user", "content": f"Resuma o seguinte texto:\n\n{texto}"}
        ],
        max_tokens=200, 
        temperature=0.7
    )
    return resposta['choices'][0]['message']['content'].strip()


def gerar_quiz(resumo):
    prompt = f"Crie um quiz de múltipla escolha com 5 perguntas baseadas no seguinte resumo:\n\n{resumo}"
    
    resposta = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "Você é um assistente de IA que cria quizzes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.7
    )
    
    return resposta['choices'][0]['message']['content'].strip()



