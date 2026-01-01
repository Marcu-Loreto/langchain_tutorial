

# Instalar as dependencias no Python

 pip install langchain_openai
 pip install langchain_antrropic
 pip install langchain_gemini
 pip install python-dotenv - Para usar as chaves de PAI sem expor no codigo
  
 
 # Como importar os deiversos modleos de LLMs no langchain é o mesmo padrão

from langchain_openai import ChatOpenAI
from langchain_antrropic import ChatAnthropic
from langchain_gemini import ChatGemini
 # Como importar as chaves da variavel de ambiente .env 
import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()    
openai_api_key=os.getenv("OPENAI_API_KEY")

# Como carregar os modelos
model_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=openai_api_key)
model_antrropic = ChatAnthropic(model="claude-3-5-sonnet", temperature=0.3)
model_gemini = ChatGemini(model="gemini-1.5-flash", temperature=0.3)

# Como usar os modelos usar o INVOKE
model_openai.invoke("Qual é a capital do Brasil?")
model_antrropic.invoke("Qual é a capital do Brasil?")
model_gemini.invoke("Qual é a capital do Brasil?")

# exemplo de uma saida estruturada atribuida a um modelo 
 Precisa criar uma classe para definir a saida estruturada...veja abaixo: 
  1 - precisa instalar o basemodel e field
  from pydantic import BaseModel, Field 
  
# Criar a classe que vai receber a saida estruturada 

class RespostaUsuario(BaseModel):
    response: str = Field(description="Resposta do usuario")
    mentioned_name :bool = Field(description="indica se algum nome foi mencionado")  
    token_usage: int = Field(description="quantidade de tokens usados")   
    logprobs: float = Field(description="logprobs")
# Agora preciso criar um modelo que vai usar esta saida estruturada, um modelo customizado

model_customizado = model_openai.with_structured_output(RespostaUsuario)

# Agora posso usar o modelo customizado para fazer uma chamada
resposta_customizada = model_customizado.invoke("ola, aqui é o joao, sabe qual a capital do Brasil?")


# Posso definir uma lista especifica de respostas para mostra na tela
print(resposta_customizada.logprobs)
print(resposta_customizada.response)
print(resposta_customizada.mentioned_name)
print(resposta_customizada.token_usage)


# Como adicionar MEMORIA ao modelo ?
Adiconar o langgraph ( pip install langgraph)