import json
import argparse
from crewai import LLM
from crewai import Task, Crew
from parsers.groww_parser import GrowwParser
from pipeline import generate_symbol_candidates, normalize_portfolio
from market.prices import fetch_prices
from market.indicators import compute_indicators
from market.news import fetch_news
from dotenv import load_dotenv

from agents.portfolio_interpreter import create_portfolio_interpreter
from agents.market_agent import create_market_agent
from agents.analyst_agent import create_financial_analyst
from agents.report_agent import create_report_agent
from symbol_resolver import SymbolResolver

load_dotenv()
resolver = SymbolResolver("data/symbol_master_list.csv")
#OLLAMA_LLM = LLM(
#    model="ollama/llama3.2:3b",
#    temperature=0.2
#)

runningllm = LLM(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_tokens=512
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Portfolio Analysis using CrewAI"
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to broker holdings file (Excel / CSV)"
    )

    parser.add_argument(
        "--broker",
        required=True,
        choices=["groww"],
        help="Broker format of the holdings file"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    # ---- Broker selection (extensible) ----
    if args.broker == "groww":
        parser = GrowwParser()
    else:
        raise ValueError(f"Unsupported broker: {args.broker}")

    # ---- Parse holdings ----
    df = parser.parse(args.file)
    portfolio = normalize_portfolio(df)

    print
    # ---- Market enrichment ----
    for stock in portfolio:
        resolved_symbol = resolver.resolve(stock["isin"])

        stock["resolved_symbol"] = resolved_symbol or "unresolved"
        price_df = fetch_prices(resolved_symbol) if resolved_symbol else None
        stock["indicators"] = compute_indicators(price_df)
        stock["news"] = fetch_news(resolved_symbol) if resolved_symbol else []
    # ---- Agents ----
    print("\n🤖 Initializing agents...\n")
    portfolio_agent = create_portfolio_interpreter(runningllm)
    print("Portfolio Interpreter Agent initialized.")
    market_agent = create_market_agent(runningllm)
    print("Market Analysis Agent initialized.")
    analyst_agent = create_financial_analyst(runningllm)
    print("Financial Analyst Agent initialized.")
    report_agent = create_report_agent(runningllm)

    # ---- Tasks ----
    task1 = Task(
        description=f"Analyze portfolio structure:\n{json.dumps(portfolio, indent=2)}",
        expected_output="Portfolio risks, concentration, and allocation assessment",
        agent=portfolio_agent
    )

    task2 = Task(
        description=f"Analyze market trends and news:\n{json.dumps(portfolio, indent=2)}",
        expected_output="Trend and sentiment summary per stock",
        agent=market_agent
    )

    task3 = Task(
        description="Based on portfolio and market insights, give Buy/Hold/Reduce recommendations",
        expected_output="Buy/Hold/Reduce per holding with reasoning",
        agent=analyst_agent
    )

    task4 = Task(
        description="Create a clean investment report from all insights",
        expected_output="Readable investment report",
        agent=report_agent
    )

    print("\n🤖 Starting CrewAI workflow...\n")
    crew = Crew(
        agents=[portfolio_agent, market_agent, analyst_agent, report_agent],
        tasks=[task1, task2, task3, task4],
        verbose=False
    )

    result = crew.kickoff()
    print("\n📊 FINAL INVESTMENT REPORT:\n")
    print(result)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()    
