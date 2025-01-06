import warnings
warnings.filterwarnings('ignore')
 
from dotenv import load_dotenv
load_dotenv()
 
import os
import yaml
from crewai import Agent, Task, Crew, LLM

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
    n_results=20,
)

# Disease Research Crew
research_agent = Agent(
    config=agents_config['research_assistant_agent'],
    llm=groq_llm,
    tools=[Serpertool],
)
 
research_task = Task(
    config=tasks_config['research_disease'],
    agent=research_agent,
    output_file='disease_summary2.md',
)

Diseasecrew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True
)

# Diet Research Crew
diet_agent = Agent(
    config=agents_config['medical_dietician_agent'],
    llm=groq_llm,
    tools=[Serpertool]
)
 
diet_research_task= Task(
    config=tasks_config['diet_planning'],
    agent=research_agent,
    output_file='diet_summary2.md',
)

Dietcrew = Crew(
    agents=[diet_agent],
    tasks=[diet_research_task],
    verbose=True
)

# Exercise Research Crew
exercise_agent = Agent(
    config=agents_config['physiotherapist_agent'],
    llm=groq_llm,
    tools=[Serpertool]
)
 
exercise_research_task = Task(
    config=tasks_config['exercise_plan_for_disease_recovery'],
    agent=research_agent,
    output_file='exercise_summary2.md',
)

Exercisecrew = Crew(
    agents=[exercise_agent],
    tasks=[exercise_research_task],
    verbose=True
)

print('#'*30 + 'INIT RUNS' + '#'*30)
