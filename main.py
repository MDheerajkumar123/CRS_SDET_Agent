from crewai import Agent


def main():
    agent = Agent(
        role="SDET Assistant",
        goal="Assist with software testing activities",
        backstory="You are a senior software testing engineer.",
        verbose=True,
    )

    print("CrewAI initialized successfully.")
    print(f"Agent role: {agent.role}")


if __name__ == "__main__":
    main()