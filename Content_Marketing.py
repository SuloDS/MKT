import streamlit as st
from crewai import Agent, Task, Crew, Process
from groq import Groq

# Configurações iniciais
st.set_page_config(page_title="Gen-Marketer", page_icon=":bar_chart:", layout="centered")
st.subheader("Gen-Marketer")

# Inicialização do LLM com a chave da API
llm = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Definição dos Agentes
agents = {
    "market_researcher": Agent(
        role='Market Researcher',
        goal='Research new and emerging trends in pet products industry in Germany',
        backstory='You are a market researcher in the pet product industry',
        verbose=True,
        allow_delegation=False,
        llm=llm
    ),
    "campaign_creator": Agent(
        role='Marketing Campaign Creator',
        goal='Come up with 3 interesting marketing campaign ideas in the pet product industry based on market research insights',
        backstory='You are a marketing campaign planner in the pet product industry',
        verbose=True,
        allow_delegation=False,
        llm=llm
    ),
    "digital_marketer": Agent(
        role='Digital Marketing Content Creator',
        goal='Come up with 2 or 3 interesting advertisement ideas for marketing on digital platforms such as YouTube, Instagram and TikTok along with script for each marketing campaign',
        backstory='You are a marketing marketer specialising in performance marketing in the pet product industry',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
}

# Criação dos prompts e das tarefas
tasks = [
    Task(description=st.text_area("What Market Research Task would you like me to do today?"), agent=agents["market_researcher"]),
    Task(description=st.text_area("What Marketing Campaigns would you like me to come up with today?"), agent=agents["campaign_creator"]),
    Task(description=st.text_area("What Digital Marketing Content would you like me to generate today?"), agent=agents["digital_marketer"])
]

# Criação da equipe (crew)
crew = Crew(
    agents=list(agents.values()),
    tasks=tasks,
    verbose=2,
    process=Process.sequential
)

# Geração de respostas
if st.button("Generate"):
    with st.spinner("Generating response..."):
        crew.kickoff()
        for task in tasks:
            st.write(task.output)
