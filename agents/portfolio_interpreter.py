from crewai import Agent

def create_portfolio_interpreter(llm):
    return Agent(
        role="Portfolio Interpreter",
        goal="Identify portfolio structure, concentration, and allocation risks",
        backstory="Expert at portfolio diagnostics and risk identification",
        llm=llm,
        verbose=False
    )
