import openai

# Definir chave da API do OpenAI
openai.api_key = 'sua-chave-da-api'

def gerar_resumo(texto):
    resposta = openai.Completion.create(
        model="gpt-4",  # Ou GPT-3, dependendo da sua necessidade
        prompt=f"Resuma o seguinte texto:\n\n{texto}",
        max_tokens=200,  # Ajuste o número de tokens conforme necessário
        temperature=0.7
    )
    return resposta['choices'][0]['text'].strip()
