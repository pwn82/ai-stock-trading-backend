from crewai import Task


def create_data_task(
    agent,
    stock_symbol,
    market_data,
    news_data,
    user_request
):

    return Task(

        description=f"""
Analyze the following stock data.

Stock:
{stock_symbol}

User request:
{user_request}

Market data:
{market_data}

News:
{news_data}

Perform:

1. Price trend analysis
2. Volume analysis
3. Technical indicator analysis
4. News sentiment assessment
5. Financial data observations
6. Data quality problems
7. Missing data
8. Key insights

Do not invent missing values.

Clearly distinguish:
- Observed data
- Calculated indicators
- Assumptions

Return a concise analytical report.
""",

        expected_output=(
            "A factual market analysis report containing "
            "price trends, indicators, sentiment, data "
            "quality and key insights."
        ),

        agent=agent
    )


def create_strategy_task(
    agent,
    stock_symbol,
    user_request
):

    return Task(

        description=f"""
Create a hypothetical trading strategy for:

Stock:
{stock_symbol}

User request:
{user_request}

Use the previous Data Analyst report.

Evaluate:

1. Strategy preference
2. Trend
3. Momentum
4. Entry conditions
5. Exit conditions
6. Hypothetical backtesting considerations
7. Expected scenario
8. Alternative scenario

Possible simulated recommendation:
BUY / SELL / HOLD

Do not claim certainty or guaranteed returns.

This is a paper-trading analysis only.
""",

        expected_output=(
            "A hypothetical trading strategy with entry "
            "conditions, exit conditions, assumptions and "
            "scenario analysis."
        ),

        agent=agent
    )


def create_execution_task(
    agent,
    stock_symbol,
    capital,
    risk_tolerance
):

    return Task(

        description=f"""
Create a hypothetical paper-trading execution plan.

Stock:
{stock_symbol}

Capital:
{capital}

Risk tolerance:
{risk_tolerance}

Use the previous Data Analyst and Strategy reports.

Calculate conceptually:

1. Hypothetical order type
2. Entry price
3. Exit price
4. Position size
5. Maximum exposure
6. Timing
7. Execution conditions

Never place a real order.

If required price information is unavailable,
say "insufficient data".
""",

        expected_output=(
            "A paper-trading execution plan with hypothetical "
            "position size, order type and entry/exit conditions."
        ),

        agent=agent
    )


def create_risk_task(
    agent,
    stock_symbol,
    capital,
    risk_tolerance
):

    return Task(

        description=f"""
Perform risk assessment for:

Stock:
{stock_symbol}

Capital:
{capital}

Risk tolerance:
{risk_tolerance}

Use all previous reports.

Assess:

1. Market risk
2. Volatility risk
3. Data quality risk
4. News risk
5. Portfolio exposure
6. Hypothetical stop loss
7. Hypothetical take profit
8. Maximum loss scenario
9. Overall risk level

Then provide a final educational/paper-trading
recommendation:

BUY / SELL / HOLD

Explain the rationale and uncertainty.

Never claim guaranteed returns.
Never place a real order.
""",

        expected_output=(
            "A risk report containing risk level, hypothetical "
            "stop loss, hypothetical take profit, maximum "
            "exposure and final paper-trading recommendation."
        ),

        agent=agent
    )