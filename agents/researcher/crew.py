from typing import List
from dotenv import load_dotenv
from crewai import LLM
import os
from crewai import Agent, Task, Crew
from crewai_tools import (
    SerperDevTool,
    DirectoryReadTool,
    FileWriterTool,
    FileReadTool,
)
from pydantic import BaseModel, Field, ConfigDict

load_dotenv()


llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.1)


class Content(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content_type: str = Field(
        ...,
        description="The type of content to be created",
    )
    topic: str = Field(..., description="The topic of the content")
    target_audience: str = Field(..., description="The target audience for the content")
    tags: List[str] = Field(..., description="Tags to be used for the content")
    content: str = Field(..., description="The content itself")


max_rpm_1 = 3
research_agent = Agent(
    role="Research Specialist",
    goal="Research interesting facts about the topic: {topic}",
    backstory="You are an expert at finding relevant and factual data.",
    tools=[
        SerperDevTool(),
        DirectoryReadTool("resources/researcher_crew/drafts"),
        FileWriterTool(),
        FileReadTool(),
    ],
    verbose=True,
    llm=llm,
    max_rpm=max_rpm_1,
)

writer_agent = Agent(
    role="Creative Writer",
    goal="Write a short blog summary using the research",
    backstory="You are skilled at writing engaging summaries based on provided content.",
    tools=[
        DirectoryReadTool("resources/researcher_crew/drafts"),
        FileWriterTool(),
        FileReadTool(),
    ],
    llm=llm,
    verbose=True,
    max_rpm=max_rpm_1,
)

task1 = Task(
    description="Find 3-5 interesting and recent facts about {topic} as of year 2025.",
    expected_output="A bullet list of 3-5 facts. \n Store the content in 'resources/researcher_crew/drafts/reaserch.md'.",
    agent=research_agent,
    output_json=Content,
)

task2 = Task(
    description="Write a detailed blog post about {topic} using the facts from the research.",
    expected_output="A blog post.Store the content in 'resources/researcher_crew/drafts/post.md'.",
    agent=writer_agent,
    context=[task1],
    output_json=Content,
)

crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[task1, task2],
    verbose=True,
    memory=True,
    max_rpm=max_rpm_1,
    embedder={
        "provider": "google",
        "config": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model": "text-embedding-004",
        },
    },
)

crew.kickoff(inputs={"topic": "The future of electrical vehicles"})
crew.kickoff(inputs={"topic": "What is the revenue outlook in this sector?"})
crew.kickoff(inputs={"topic": "How ai advancements will affect it."})
