
from crewai import Agent, LLM
from app.core.config import get_settings


def create_llm():
    settings = get_settings()

    return LLM(
        model=f"groq/{settings.groq_model_name}",
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_completion_tokens=4096,
    )


def create_data_analyst():
    return Agent(
        role="Financial Data Analyst",
        goal=(
            "Analyze supplied market data, price trends, volume, "
            "indicators, financial information and news context. "
            "Identify data quality issues and produce factual insights."
        ),
        backstory=(
            "You specialize in financial data analysis, statistical "
            "reasoning and identifying uncertainty in market data."
        ),
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_strategy_agent():
    return Agent(
        role="Trading Strategy Analyst",
        goal=(
            "Develop and evaluate a hypothetical trading strategy "
            "using the Data Analyst findings."
        ),
        backstory=(
            "You specialize in technical strategies, entry and exit "
            "logic, trend analysis, momentum and backtesting."
        ),
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_execution_agent():
    return Agent(
        role="Paper Trade Execution Planner",
        goal=(
            "Create a hypothetical execution plan without placing "
            "real orders."
        ),
        backstory=(
            "You specialize in hypothetical order planning, position "
            "sizing, timing and order management."
        ),
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_risk_agent():
    return Agent(
        role="Risk Management Analyst",
        goal=(
            "Assess hypothetical portfolio risk and recommend "
            "appropriate risk controls and exposure limits."
        ),
        backstory=(
            "You specialize in risk management, capital preservation "
            "and identifying uncertainty."
        ),
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
    )
