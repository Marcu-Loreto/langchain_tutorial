
#Como importar os deiversos modleos de LLMs no langchain é o mesmo padrão

from langchain_openai import ChatOpenAI
# from langchain_antrropic import ChatAnthropic
# from langchain_gemini import ChatGemini

#Como carregar os modelos
#model_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
# model_antrropic = ChatAnthropic(model="claude-3-5-sonnet", temperature=0.3)
# model_gemini = ChatGemini(model="gemini-1.5-flash", temperature=0.3)

#como criar as credencias das LLM e chamar no modo de variavel de ambiente, sem expor as chaves no codigo

import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()    
openai_api_key=os.getenv("OPENAI_API_KEY")
#Precisa criar um arquivo .env na raiz do projeto e colocar as chaves de API OPENAI_API_KEY // Antrropic_API_KEY // Gemini_API_KEY
model_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, openai_api_key=openai_api_key)     
# model_antrropic = ChatAnthropic(model="claude-3-5-sonnet", temperature=0.3, anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))     
# model_gemini = ChatGemini(model="gemini-1.5-flash", temperature=0.3, gemini_api_key=os.getenv("GEMINI_API_KEY"))     

#Como usar os modelos usar o INVOKE
resposta = model_openai.invoke("Qual é a capital do Brasil?")
# print(resposta.content) #Imprime apenas  resposta [0] que é o texto da resposta 
# print(resposta.response_metadata) #Imprime toda informacao de metadados : Tokens, modelo,

 #Outros metodos para usar os modelos

# model_antrropic.invoke("Qual é a capital do Brasil?")
# model_gemini.invoke("Qual é a capital do Brasil?")


#Como criar uma saida estruturada 

from pydantic import BaseModel, Field # pip install pydantic
 #criar um modelo de saida estruturada - Precisa criar uma classe que herda de BaseModel

class RespostaUsuario(BaseModel):
    response: str = Field(description="Resposta do usuario")
    mentioned_name :bool = Field(description="indica se algum nome foi mencionado")  
    token_usage: int = Field(description="quantidade de tokens usados")   
    logprobs: float = Field(description="logprobs")
# Agora preciso criar um modelo que vai usar esta saida estruturada, um modelo customizado

model_customizado = model_openai.with_structured_output(RespostaUsuario)

# Agora posso usar o modelo customizado para fazer uma chamada
resposta_customizada = model_customizado.invoke("ola, aqui é o joao, sabe qual a capital do Brasil?")
#print(resposta_customizada.logprobs)
print(resposta_customizada.response)
print(f"Mencioanou algum nome ? : {resposta_customizada.mentioned_name}")
print(f"quantidade de tokens usados: {resposta_customizada.token_usage}")

#Adicionando ferramentas  ao modelo

#1 instalar o langgraph ( pip install -q langgraph)

#Chamar o ReAct (create_react_agent) - Existe uma viso de deprecate
# CHECKPOINT: Tenta importar da nova localização (langchain.agents) primeiro
# Se falhar, usa a localização antiga (langgraph.prebuilt) como fallback
try:
    from langchain.agents import create_react_agent
    print("✅ Usando create_react_agent de langchain.agents (nova versão)")
except ImportError:
    from langgraph.prebuilt import create_react_agent
    print("⚠️ Usando create_react_agent de langgraph.prebuilt (versão antiga - será descontinuada no futuro)")
#Veja artigo_ReAct.md para mais detalhes

#Para ser um ReAct_Agente ele precisa de ferramentas. Vamso criar uma Calculadora ( Funcao_calculator)

def old_calculator(num1:float, num2:float, operator:str): # esta seria o basico, mas a operacao é restrita a soma, subtrair,dividir e multiplicar
    if operator == "add":
        return num1 + num2
    elif operator == "subtract":
        return num1 - num2
    elif operator == "multiply":
        return num1 * num2
    elif operator == "divide":
        return num1 / num2
    else:
        return "Operador invalido"

# Agora vem a engenharia de contexto para montar esta ferramenta para IA
# Os tipos de dados a IA recebe como Contexto, os Numeros ela recebe correto, mas a operacao é restrita a 4 operaçoes, logo o operator deve ser LITERAL. Como fazer?
from typing import Literal
def calculator(num1:float, num2:float, operator:Literal["add", "subtract", "multiply", "divide"]):    
    # PRECISO COLOCAR UMA DOCSTRING PARA A IA LER PARA QUE SERVE A FERRAMENTA 
    """
    Util para reallizae os calculos matematicos de 2 numeros.
    inputs:
    num1: float
    num2: float
    operator: Literal["add", "subtract", "multiply", "divide"]
    outputs:
    result: float
    """
    if operator == "add":
        return num1 + num2
    elif operator == "subtract":
        return num1 - num2
    elif operator == "multiply":
        return num1 * num2
    elif operator == "divide":
        return num1 / num2
    else:
        raise ValueError("Operador invalido")
 # Definindo o System prompt para o ReAct_Agente e o modelo a ser usado
model = model_openai
system_prompt = """
Voce e um assistente que pode usar ferramentas para resolver problemas.
"""
agent = create_react_agent(
    model = model, 
    prompt = system_prompt, 
    tools=[calculator],
    
    )

from langchain_core.messages import HumanMessage, SystemMessage # definindo o dicionario de mensagens systemMessage = SystemPrompt , pode ser descartado

# Executando a pergunta do José e capturando a resposta
resposta_jose = agent.invoke(
     {"messages": [SystemMessage(content=system_prompt),
     HumanMessage(content="Ola, meu nome é jose, Qual e a soma de 2 e 2?")]
     }
    )

# Imprimindo a resposta do agente
# resposta_jose é um dict com estrutura: {"messages": [SystemMessage, HumanMessage, AIMessage, ToolMessage, AIMessage]}
# A última mensagem (AIMessage) contém a resposta final

print("🤖 RESPOSTA DO AGENTE REACT PARA JOSÉ:")

resposta_final = resposta_jose["messages"][-1].content
print(f"\n{resposta_final}")


#Colocando Memoria no Agente LOCALMENTE 
from langgraph.checkpoint.memory import InMemorySaver

agent2 = create_react_agent(
    model = model, 
    prompt = system_prompt, 
    tools=[calculator],
    checkpointer = InMemorySaver()
    )

config = {"configurable": {"thread_id": "1234rt"}}

resposta_jose2 = agent2.invoke(
    {"messages": [HumanMessage(content="Ola, meu nome é jose, Qual e a soma de 12 e 256?")]},
    config=config
    )

print(resposta_jose2["messages"][-1].content)

resposta_jose3 = agent2.invoke(
    {"messages": [HumanMessage(content="Ola, qual o meu nome?")]},
    config=config
    )

print(resposta_jose3["messages"][-1].content)


#Criando uma funçao de extrair informaçoes de um texto - usando saida estruturada

class pessoa(BaseModel):
    nome: str = Field(description="Nome da pessoa")
    idade: int = Field(description="Idade da pessoa")
    genero: Literal["Masculino", "Feminino", "Outro"] = Field(description="Genero da pessoa")
    cidade: str = Field(description="Cidade da pessoa")
    pais: str = Field(description="Pais da pessoa")
    
model_pessoa = model_openai.with_structured_output(pessoa)

resposta_pessoa = model_pessoa.invoke("Ola, meu nome é jose,  sou homen, alto , moro em Recife, Brasil e tenho 25 anos")
print(resposta_pessoa)
