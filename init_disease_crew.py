import warnings
warnings.filterwarnings('ignore')
 
from dotenv import load_dotenv
load_dotenv()
 
import os
import yaml
from crewai import Agent, Task, Crew, LLM
from tools.tavily_search_tool import TavilySearchTool
from tools.DuckDuckGo_search_tool import DuckDuckGoSearchRunTool

files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)
 
agents_config = configs['agents']
tasks_config = configs['tasks']

import os
from crewai import LLM
groq_llm = LLM(
    model="gpt-4o-mini",
    # model="groq/llama3-8b-8192",
    temperature=0.3,
    # max_tokens=4096,
    # base_url="https://api.groq.com/openai/v1"
)

from crewai_tools import SerperDevTool
 
# Initialize the tool for internet searching capabilities
Serpertool = SerperDevTool(
    # search_url="https://google.serper.dev/scholar",
    # country="India",
    n_results=15,
)

###### Disease Research Crew
research_agent = Agent(
    config=agents_config['research_assistant_agent'],
    llm=groq_llm,
    tools=[Serpertool, TavilySearchTool(), DuckDuckGoSearchRunTool()],
)

reporting_agent = Agent(
    config=agents_config['research_reporting_agent'],
    llm=groq_llm,
)
 
serper_research_task = Task(
    config=tasks_config['serper_disease_research_task'],
    agent=research_agent,
    tools=[Serpertool]
)

tavily_research_task = Task(
    config=tasks_config['tavily_disease_research_task'],
    agent=research_agent,
    tools=[TavilySearchTool()]
)

duckduckgo_research_task = Task(
    config=tasks_config['duckduckgo_disease_research_task'],
    agent=research_agent,
    tools=[DuckDuckGoSearchRunTool()]
)

final_report_task = Task(
    config=tasks_config['final_research_report_task'],
    agent=reporting_agent,
    context=[serper_research_task, tavily_research_task, duckduckgo_research_task],
    output_file='disease_report.md',
)

Diseasecrew = Crew(
    agents=[research_agent,reporting_agent],
    tasks=[serper_research_task, tavily_research_task, duckduckgo_research_task,final_report_task],
    verbose=True
)

###### Diet Research Crew
diet_research_agent = Agent(
    config=agents_config['medical_dietician_research_agent'],
    llm=groq_llm,
    tools=[Serpertool, TavilySearchTool(), DuckDuckGoSearchRunTool()]
)

diet_reporting_agent = Agent(
    config=agents_config['diet_reporting_agent'],
    llm=groq_llm,
)

serper_diet_research= Task(
    config=tasks_config['serper_diet_research_task'],
    agent=diet_research_agent,
    tools=[Serpertool]
)

tavily_diet_research = Task(
    config=tasks_config['tavily_diet_research_task'],
    agent=diet_research_agent,
    tools=[TavilySearchTool()]
)

duckduck_diet_research = Task(
    config=tasks_config['duckduckgo_diet_research_task'],
    agent=diet_research_agent,
    tools=[DuckDuckGoSearchRunTool()]
)

final_diet_report = Task(
    config=tasks_config['final_diet_report_task'],
    agent=diet_reporting_agent,
    context=[serper_diet_research, tavily_diet_research, duckduck_diet_research],
    output_file='diet_report.md',
)

Dietcrew = Crew(
    agents=[diet_research_agent,diet_reporting_agent],
    tasks=[serper_diet_research, tavily_diet_research, duckduck_diet_research, final_diet_report],
    verbose=True
)

###### Exercise Research Crew
exercise_research_agent = Agent(
    config=agents_config['physiotherapist_agent'],
    llm=groq_llm,
    tools=[Serpertool, TavilySearchTool(), DuckDuckGoSearchRunTool()]
)

exercise_reporting_agent = Agent(
    config=agents_config['exercise_reporting_agent'],
    llm=groq_llm,
)
 
serper_exercise_research_task = Task(
    config=tasks_config['serper_exercise_research_task'],
    agent=research_agent,
    tools=[Serpertool]
)

tavily_exercise_research_task = Task(
    config=tasks_config['tavily_exercise_research_task'],
    agent=research_agent,
    tools=[TavilySearchTool()]
)

duckduckgo_exercise_research_task = Task(
    config=tasks_config['duckduckgo_exercise_research_task'],
    agent=research_agent,
    tools=[DuckDuckGoSearchRunTool()]
)

final_exercise_report_task = Task(
    config=tasks_config['final_exercise_report_task'],
    agent=reporting_agent,
    context=[serper_exercise_research_task, tavily_exercise_research_task, duckduckgo_exercise_research_task],
    output_file='exercise_report.md',
)

Exercisecrew = Crew(
    agents=[exercise_research_agent,exercise_reporting_agent],
    tasks=[serper_exercise_research_task, tavily_exercise_research_task, duckduckgo_exercise_research_task, final_exercise_report_task],
    verbose=True
)

print('#'*30 + 'INIT RUNS' + '#'*30)
