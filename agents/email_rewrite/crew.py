from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

from tools.jargon_replacer import ReplaceJargonsTool

load_dotenv()


@CrewBase
class EmailCrew:
    """ "Enhance email professionally" """

    agents_config = "config/agents.yml"
    tasks_config = "config/tasks.yml"

    @agent
    def email_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["email_assistant"],
            tools=[ReplaceJargonsTool()],
            verbose=True,
        )

    @task
    def email_task(self) -> Task:
        return Task(
            config=self.tasks_config["email_task"], agent=self.email_assistant()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=[self.email_assistant()], tasks=[self.email_task()])


if __name__ == "__main__":
    email_crew = EmailCrew()
    email_crew.crew().kickoff(
        inputs={
            "original_email": """
                looping in Priya. TAS and PRX updates are in the deck. ETA for SDS integration is Friday.
                Let's sync up tomorrow if SYNCBOT allows 😄. ping me if any blockers.
            """
        }
    )
