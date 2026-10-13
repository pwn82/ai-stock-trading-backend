from crewai import Crew, Process

from app.crew.agents import (
    create_data_analyst,
    create_strategy_agent,
    create_execution_agent,
    create_risk_agent
)

from app.crew.tasks import (
    create_data_task,
    create_strategy_task,
    create_execution_task,
    create_risk_task
)


class TradingCrew:

    def run(
        self,
        stock_symbol,
        capital,
        risk_tolerance,
        strategy_preference,
        news_impact,
        market_data,
        news_data,
        user_question
    ):

        data_agent = create_data_analyst()

        strategy_agent = create_strategy_agent()

        execution_agent = create_execution_agent()

        risk_agent = create_risk_agent()

        data_task = create_data_task(
            data_agent,
            stock_symbol,
            market_data,
            news_data,
            user_question
        )

        strategy_task = create_strategy_task(
            strategy_agent,
            stock_symbol,
            f"""
Capital: {capital}

Risk tolerance:
{risk_tolerance}

Strategy preference:
{strategy_preference}

News impact:
{news_impact}

Original question:
{user_question}
"""
        )

        execution_task = create_execution_task(
            execution_agent,
            stock_symbol,
            capital,
            risk_tolerance
        )

        risk_task = create_risk_task(
            risk_agent,
            stock_symbol,
            capital,
            risk_tolerance
        )

        crew = Crew(

            agents=[
                data_agent,
                strategy_agent,
                execution_agent,
                risk_agent
            ],

            tasks=[
                data_task,
                strategy_task,
                execution_task,
                risk_task
            ],

            process=Process.sequential,

            verbose=True
        )

        result = crew.kickoff()

        return {
            "result": str(result),

            "tasks": [
                {
                    "agent": "Data Analyst",
                    "output": str(
                        data_task.output
                    )
                },
                {
                    "agent": "Trading Strategy",
                    "output": str(
                        strategy_task.output
                    )
                },
                {
                    "agent": "Execution Planner",
                    "output": str(
                        execution_task.output
                    )
                },
                {
                    "agent": "Risk Manager",
                    "output": str(
                        risk_task.output
                    )
                }
            ]
        }


trading_crew = TradingCrew()