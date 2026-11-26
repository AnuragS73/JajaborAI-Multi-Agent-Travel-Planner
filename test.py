from tools.tavily_tool import tavily_search
from tools.flight_tool import f_search_flights

# output = tavily_search("Top 5 hotels in Calangute(Goa)")
# print(output)

flight_output = f_search_flights("Plan a 5 days Mumbai trip from Kolkata")
print(flight_output)