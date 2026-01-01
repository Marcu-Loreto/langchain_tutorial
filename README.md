Tutorial sobre Langchai
Biblioteca de IA para Python
comandos e estrutura de dados

Tutorial Básico: O que é o LangChain?
O LangChain é um framework criado para simplificar o desenvolvimento de aplicações baseadas em modelos de linguagem (LLMs), como o GPT da OpenAI, o Claude da Anthropic ou o Gemini do Google,.
Pense nele não apenas como uma biblioteca que você usa dentro do seu código, mas como uma estrutura sobre a qual você constrói a sua solução de Inteligência Artificial. Ele serve como uma "ponte" que padroniza a comunicação entre o seu código e diferentes inteligências artificiais.
Por que usar o LangChain?
A principal vantagem é a abstração. Sem o LangChain, para trocar do GPT-4 para o Claude, você teria que reescrever a parte do código que conecta à API, pois cada uma tem suas regras. Com o LangChain, a linguagem é padronizada:
• Se você usa llm.invoke() para o GPT, você usa o mesmo comando para o Claude ou para um modelo rodando localmente (Ollama). Basta mudar a definição do modelo em uma linha.

--------------------------------------------------------------------------------
A Hierarquia do LangChain (Desenhada)
O ecossistema do LangChain é modular. Isso significa que ele é dividido em vários pacotes independentes para que você não precise instalar tudo se for usar apenas uma parte,.
Existe uma ordem de dependência (quem precisa de quem para funcionar), conhecida tecnicamente como ordenação topológica. Abaixo está o desenho dessa hierarquia baseada nas fontes:
      [ SEU CÓDIGO / APLICAÇÃO ]
                  |
                  v
    +-----------------------------+
    |   Bibliotecas de Nível Alto |
    |                             |
    |  [LangChain Community]      |  <-- Integrações feitas pela comunidade (ex: Chroma, Quadrant) 
    |  [LangGraph]                |  <-- Para criar Agentes e fluxos complexos 
    |  [LangChain OpenAI/Anthropic]| <-- Integrações oficiais dedicadas 
    +-----------------------------+
                  |
                  v
    +-----------------------------+
    |        LangChain            |  <-- O pacote principal (Orquestração de "chains") 
    +-----------------------------+
                  |
                  v
    +-----------------------------+
    |      LangChain Core         |  <-- A BASE DE TUDO (Abstrações fundamentais) 
    +-----------------------------+
Explicando a Hierarquia:
1. LangChain Core: É a base. Todas as outras bibliotecas dependem dele. Ele contém as regras fundamentais e a linguagem padrão do framework,.
2. LangChain (Pacote Principal): Fica acima do Core. Contém as lógicas de encadeamento (chains).
3. LangChain Community & Integrações: São pacotes específicos. Por exemplo, o langchain-openai permite conectar especificamente com a OpenAI, mas ele depende do Core para funcionar,.
4. LangGraph: Uma biblioteca da mesma família usada para criar agentes que interagem entre si e mantêm estado (memória) de forma cíclica,.

--------------------------------------------------------------------------------
Conceitos Chave para Iniciantes
1. Modelos (LLMs)
No LangChain, você define um objeto que representa a IA.
• Exemplo: Você importa ChatOpenAI e define que quer usar o modelo "gpt-4o-mini". Se quiser mudar para o Claude, basta trocar a importação para ChatAnthropic e manter o resto do código igual.
2. Chains (Correntes)
O nome "LangChain" vem da ideia de criar correntes de raciocínio. Você conecta:
• Um Prompt (o que você pede) -> Um Modelo (quem processa) -> Uma Saída (a resposta).
3. Agentes e Ferramentas (Tools)
Os agentes são sistemas que usam o raciocínio da IA para decidir quais ferramentas chamar.
• O LangChain utiliza um conceito chamado ReAct (Reasoning + Acting). A IA pensa: "Preciso responder quanto é 50 x 50. Eu não sei calcular bem, então vou chamar a ferramenta 'Calculadora'". Ela executa a ação, pega o resultado e devolve a resposta final ao usuário,,.
4. LangSmith
É uma ferramenta essencial do ecossistema para monitoramento e debug. Ele permite ver exatamente o que está acontecendo dentro da sua aplicação (quantos tokens gastou, quanto tempo demorou, onde ocorreu um erro),.

--------------------------------------------------------------------------------
Como começar (O Fluxo Básico)
Se você fosse escrever um código simples usando LangChain (em Python), o fluxo seria:
1. Instalação: Você instala o pacote necessário, por exemplo, pip install langchain-openai. Ao fazer isso, ele automaticamente instala o langchain-core porque depende dele,.
2. Configuração: Você define sua chave de API (ex: OPENAI_API_KEY) como uma variável de ambiente,.
3. Execução: Você cria o modelo e usa o método .invoke("Sua pergunta"). O LangChain envia isso para a IA, recebe a resposta e te entrega o conteúdo.
Analogia para Fixação
Para entender a hierarquia de dependências do LangChain, imagine que você vai se vestir. Existe uma ordem lógica que não pode ser quebrada:
Você não pode calçar o tênis antes de colocar a meia. Da mesma forma, o LangChain Community (o tênis) não funciona sem o LangChain Core (a meia) já estar instalado. O Core é a peça fundamental de roupa íntima que você precisa vestir antes de colocar qualquer outra camada de roupa (outros pacotes) por cima


1. Configurando a API Key com Variáveis de Ambiente
O método recomendado nas fontes é definir a chave como uma variável de ambiente. Isso permite que o LangChain detecte automaticamente a chave sem que você precise passá-la repetidamente como parâmetro,.
import os
from langchain_openai import ChatOpenAI

# 1. Defina a chave na variável de ambiente padrão que o LangChain procura
# Substitua 'sua-chave-aqui' pela sua API Key real da OpenAI
os.environ["OPENAI_API_KEY"] = "sk-..." 

# 2. Ao instanciar o modelo, ele encontra a chave automaticamente
# O tutorial sugere o uso de modelos como o "gpt-4o-mini"
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3) 

# Teste simples
response = model.invoke("Opa, tudo bom?")
print(response.content)
Nota: Se você não definir a variável de ambiente OPENAI_API_KEY, o código dará erro de autenticação ao tentar chamar o modelo,.

--------------------------------------------------------------------------------
2. Criando uma Classe para Saída Estruturada (JSON)
Para garantir que a IA responda em um formato JSON específico, o tutorial utiliza a biblioteca Pydantic. Você cria uma class (que herda de BaseModel) e define os campos com tipagem e descrição. O LangChain usa essas descrições como contexto para a IA saber exatamente o que preencher,.
Aqui está o exemplo de como criar uma estrutura para extrair informações de um usuário:
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. Definição da Classe (O "Molde" dos dados)
class RespostaUsuario(BaseModel):
    response: str = Field(
        description="A resposta gerada para o usuário em linguagem natural"
    )
    mentioned_name: bool = Field(
        description="Indica se o usuário mencionou algum nome próprio na conversa (True/False)"
    )
    # Exemplo extra baseado na fonte [6] para extração de dados
    age: int | None = Field(
        default=None, 
        description="A idade da pessoa, se mencionada"
    )

# 2. Configuração do Modelo
llm = ChatOpenAI(model="gpt-4o-mini")

# 3. 'Amarrar' a estrutura ao modelo usando o método .with_structured_output()
# Isso força o modelo a seguir a classe que criamos acima
model_structured = llm.with_structured_output(RespostaUsuario)

# 4. Execução (Invoke)
# Exemplo 1: Onde o nome É mencionado
resultado1 = model_structured.invoke("Olá, meu nome é Anwar e tenho 25 anos.")
print(f"Resultado 1: {resultado1}")
# Saída esperada (objeto): response='...' mentioned_name=True age=25

# Exemplo 2: Onde o nome NÃO É mencionado
resultado2 = model_structured.invoke("Qual é a capital do Brasil?")
print(f"Resultado 2: {resultado2}")
# Saída esperada (objeto): response='Brasília...' mentioned_name=False age=None
Pontos Importantes do Código:
• BaseModel e Field: São importados do Pydantic. O Field é crucial porque a description funciona como um prompt para a IA entender o que aquele campo significa,.
• with_structured_output: Esse método transforma o modelo padrão em um modelo que retorna um objeto da classe que você definiu, em vez de apenas texto solto,.
• Tipagem: Ao definir mentioned_name: bool, a IA entende que só pode retornar True ou False, evitando alucinações de formato,.
Analogia para Fixação
Imagine que o Modelo de IA (GPT) é uma massa de modelar disforme. A Classe Pydantic (RespostaUsuario) funciona como uma forminha de biscoito. Quando você usa o comando .with_structured_output(), você está forçando a massa (IA) a passar por essa forminha. O resultado não é mais uma massa aleatória (texto solto), mas sim um biscoito com formato perfeitamente definido (JSON Estruturado)