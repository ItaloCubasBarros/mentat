import os
import openai
import PyPDF2
from flask import Flask, render_template, request, redirect, url_for

# Configuração do OpenAI
openai.api_key = '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'  # Substitua pela sua chave real

# Inicializando o aplicativo Flask
app = Flask(__name__)

# Configuração do diretório para uploads de arquivos PDF
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Função para verificar se o arquivo tem a extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para extrair o texto do PDF
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in range(len(leitor.pages)):
            texto += leitor.pages[pagina].extract_text()
    return texto

# Função para gerar o resumo com o OpenAI
def gerar_resumo(texto):
    print("Gerando resumo...")  # Ponto de depuração
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",  # Usando o modelo GPT-4
            messages=[
                {"role": "system", "content": "Você é um assistente de IA que cria resumos concisos."},
                {"role": "user", "content": f"Resuma o seguinte texto:\n\n{texto}"}
            ],
            max_tokens=200,  # Ajuste o número de tokens conforme necessário
            temperature=0.7
        )
        resumo = resposta['choices'][0]['message']['content'].strip()
        print("Resumo gerado:", resumo)  # Ponto de depuração
        return resumo
    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return "Erro ao gerar resumo."

# Função para gerar o quiz com base no resumo
def gerar_quiz(resumo):
    print("Gerando quiz...")  # Ponto de depuração
    try:
        prompt = f"Crie um quiz de múltipla escolha com 3 perguntas baseadas no seguinte resumo:\n\n{resumo}"

        resposta = openai.ChatCompletion.create(
            model="gpt-4",  # Usando o modelo GPT-4
            messages=[
                {"role": "system", "content": "Você é um assistente de IA que cria quizzes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )

        quiz = resposta['choices'][0]['message']['content'].strip()
        print("Quiz gerado:", quiz)  # Ponto de depuração
        return quiz
    except Exception as e:
        print(f"Erro ao gerar quiz: {e}")
        return "Erro ao gerar quiz."

# Página principal (upload do PDF)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        arquivo = request.files['file']
        if arquivo and allowed_file(arquivo.filename):
            # Salvar o arquivo PDF na pasta uploads
            caminho_pdf = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
            arquivo.save(caminho_pdf)
            
            # Extrair o texto do PDF
            print(f"Extraindo texto do arquivo: {arquivo.filename}")  # Ponto de depuração
            texto_pdf = extrair_texto_pdf(caminho_pdf)
            print(f"Texto extraído: {texto_pdf[:500]}...")  # Imprimir os primeiros 500 caracteres do texto
            
            # Gerar o resumo e o quiz
            resumo = gerar_resumo(texto_pdf)
            quiz = gerar_quiz(resumo)
            
            # Passar o resumo e o quiz para a página
            return render_template('index.html', resumo=resumo, quiz=quiz)
    
    return render_template('index.html')

# Iniciar o servidor Flask
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
