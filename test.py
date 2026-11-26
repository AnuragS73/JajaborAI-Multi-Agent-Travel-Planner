from tools.tavily_tool import f_tavily_search
from tools.flight_tool import f_search_flights

# output = f_tavily_search("Top 5 hotels in Calangute(Goa)")
# print(output)

flight_output = f_search_flights("Plan a 5 days Mumbai trip from Kolkata")
print(flight_output)