from tools.tavily_tool import f_tavily_search
from tools.flight_tool import f_search_flights
from backend import f_run_travel_agent

# output = f_tavily_search("Top 5 hotels in Calangute(Goa)")
# print(output)

# flight_output = f_search_flights("Plan a 5 days Mumbai trip from Kolkata")
# print(flight_output)

inpt = "Plan a 5 days Darjeeling Trip from Bengaluru including flight, hotels and sightseeing under 1 lakhs"

resp = f_run_travel_agent(
    user_input=inpt,
    thread_id="test_user_1"
)

print("Final Response")
print(resp['answer'])