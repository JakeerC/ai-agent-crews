# %% [markdown]
# ## Init env
#

# %%
from dotenv import load_dotenv

load_dotenv()

# %% [markdown]
# ## Init llm
#

# %%
from crewai import LLM

llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.1)

# %% [markdown]
# ## Create Agents
#

# %%
from crewai import Agent, Task, Crew

research_agent = Agent(
    role="Research Specialist",
    goal="Research interesting facts about the topic: {topic}",
    backstory="you are an expert at finding relevant and factual data.",
    verbose=True,
    llm=llm,
)

writer_agent = Agent(
    role="Creative writer",
    goal="Write a short blog summary using the research",
    backstory="You are skilled at writing engaging summary provided content",
    llm=llm,
    verbose=True,
)


# %%
research_topic_task = Task(
    description="Find 3-5 interesting and recent facts about {topic}.",
    expected_output="A bullet list of 3-5 facts",
    agent=research_agent,
)

write_summary_task = Task(
    description="Write a 100 word blog post summary  about {topic} using the facts from the research.",
    expected_output="A blog post summary",
    agent=writer_agent,
    context=[research_topic_task],
)

# %%
crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_topic_task, write_summary_task],
    verbose=True,
)

crew.kickoff(inputs={"topic": "the future of ev"})

# %%
