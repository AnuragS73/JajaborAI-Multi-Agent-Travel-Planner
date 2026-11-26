import os
import certifi
from dotenv import load_dotenv


load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict,Annotated
import operator
import uuid

import psycopg
from psycopg.rows import dict_row

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import(
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_groq import ChatGroq

from tools.tavily_tool import f_tavily_search
from tools.flight_tool import f_search_flights

## get db with sslmode
def f_get_db_url():
    """
    This function is used to get the database (postgre SQL) url
    """
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError(
            "Database url is missing. Please add your Render PostgreSQL External DB"
        )

    if "sslmode=" not in db_url:
        separator = '&' if '?' in db_url else '?'
        db_url = f'{db_url}{separator}sslmode=require'

    return db_url

# url = f_get_db_url()
# print(url)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to .env file"
    )


# =========================
# ========= LLM ===========
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)


# =========================
# ======== State ==========
# =========================

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage],operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int


# ==================================
# ======== Agent1: Flight ==========
# ==================================

def f_agent_flight(state: TravelState):
    """
    This function creates flight agent
    """
    query = state["user_query"]
    flight_data = f_search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [AIMessage(content="Flight results fetched")],
        "llm_calls":  state.get("llm_calls",0) + 1
    }


# ==================================
# ======== Agent2: Hotel ===========
# ==================================

def f_agent_hotel(state: TravelState):
    """
    This function creates hotel agent
    """
    query = f"Best hotels for {state["user_query"]}"
    hotel_results = f_tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [AIMessage(content="Hotel info fetched")],
        "llm_calls":  state.get("llm_calls",0) + 1
    }

# ======================================
# ======== Agent3: Itinerary ===========
# ======================================



def f_agent_itinerary(state: TravelState):
    """
    This function creates itinerary agent
    """
    itinerary_prompt = f"""
Create a complete travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}

Make the itinerary practical, budget-aware, and easy to follow.
"""

    response = llm.invoke(
        [
            SystemMessage(content="You are an expert travel planner"),
            HumanMessage(content=itinerary_prompt)
        ]
    )

    return {
        "itinerary": response.content,
        "message": [response],
        "llm_calls":  state.get("llm_calls",0) + 1
    }


# ======================================
# ======== Agent4: Final Response ======
# ======================================

def f_agent_final(state: TravelState):
    """
    This function creates final response agent
    """
    final_prompt = f"""
Generate a final travel response for the use.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}

Itinerary:
{state['itinerary']}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel suggestion
4. Day to day itinerary
5. Estimated budget
6. Final recommendations

Important:
- Be clear and practical
- Mention that flight API may not provide the ticket prices if pricing is unavailable
- Keep response useful for real travel plan

"""
    response = llm.invoke(
        [
            SystemMessage(content="You are professional AI travel planner"),
            HumanMessage(content=final_prompt)
        ]
    )

    return {
        "messages": [response],
        "llm_calls":  state.get("llm_calls",0) + 1
    }