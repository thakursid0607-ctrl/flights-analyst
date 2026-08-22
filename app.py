import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to SQLite database
def get_data(query, params=None):
    conn = sqlite3.connect("flights_analyst.sqlite")
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

    # Streamlit App Title
st.set_page_config(page_title="airports flights analyst", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "airport Visualization", "SQL Queries", "Creator Info"])


# -------------------------------- PAGE 1: Introduction --------------------------------
if page == "Project Introduction":
    st.title(" flights Analysis")
    st.subheader("📊 A Streamlit App for Exploring flights analysis")
    st.write("""
    This project analyzes flights data from different airports using an SQLite database.
    It provides visualizations for flights, airports, and aircrafts parameters.

    **Features:**
    - View and filter airports by city, country, or continent.
    - Generate dynamic visualizations.
    - Run predefined SQL queries to explore insights.

    **Database Used:** `flights_analyst.sqlite`
    """)

    # -------------------------------- PAGE 2: Weather Data Visualization --------------------------------
    elif page == "airports Visualization":
        st.title("📊 airports Visualizer")

        # Fetch city list
         cities = get_data("SELECT DISTINCT city FROM airports")["city"].tolist()

         # Filters
        selected_city = st.selectbox("Select City", cities)
        airport_name = st.radio("Filter By:", ["city", "country"])

        if date_option == "name":
            selected_country = st.("Choose a country")
            query = "SELECT * FROM flight_analyst WHERE City = ? AND country = ?"
            df = get_data(query, params=(selected_city, selected_country))
         else:
            selected_iata = st.selectbox("Select iata_code")
            query = "SELECT * FROM airports WHERE City = ? AND country) = ?"
            df = get_data(query, params=(selected_city, f"{selected_iata}"))

        if not df.empty:
            st.write("### airports", df)

             # Visualization
             st.write("### aircrafts")
             plt.figure(figsize=(10, 5))
             sns.lineplot(data=df, x="origin_iata", y="flight_id")
             plt.xticks(rotation=45)
             st.pyplot(plt)
        else:
             st.warning("No data available for the selected filters.")


        # -------------------------------- PAGE 3: SQL Queries --------------------------------
        elif page == "SQL Queries":
            st.title("📋 SQL Query Results")

            queries = {
                 "1. Show the total number of flights for each aircraft model, listing the model and its count.": "SELECT a.aircraft_model,COUNT(f.flight_number) AS total_flights FROM aircraft a JOIN flights f ON a.aircraft_registration = f.aircraft_registration GROUP BY a.aircraft_model;",
                 "2. List all aircraft (registration, model) that have been assigned to more than 5 flights. ": " ",
                 "3. For each airport, display its name and the number of outbound flights, but only for airports with more than 5 flights.": "SELECT a.name, COUNT(f.flight_number) AS outbound_flights FROM airports a JOIN flights f ON a.iata_code = f.origin_iata GROUP BY a.name;",
                 "4. Find the top 3 destination airports (name, city) by number of arriving flights, sorted by count descending.": "SELECT a.name, a.city, COUNT(f.flight_number) AS arriving_flights FROM airports a JOIN flights f ON a.iata_code = f.destination_iata GROUP BY a.name, a.city;",
                 "5. Show for each flight: number, origin, destination, and a label 'Domestic' or 'International' using CASE WHEN on country match.": "SELECT f.flight_number, f.origin_iata, f.destination_iata, CASE WHEN a1.country = a2.country THEN 'Domestic' ELSE 'International' END AS flight_label FROM flights f JOIN airports a1 ON f.origin_iata = a1.iata_code JOIN airports a2 ON f.destination_iata = a2.iata_code;"
                 "6. Show the 5 most recent arrivals at “DEL” airport including flight number, aircraft, departure airport name, and arrival time, ordered by latest arrival.": "SELECT f.flight_number,f.aircraft_registration AS aircraft, a.name AS departure_airport_name,f.actual_arrival AS arrival_time FROM flights f JOIN airports a ON f.origin_iata = a.iata_code WHERE f.destination_iata = 'DEL' AND f.actual_arrival IS NOT NULL ORDER BY f.actual_arrival DESC LIMIT 5; "
                 "7. Find all airports with no arriving flights (never used as a destination in flights table)": "SELECT a.iata_code, a.name, a.city FROM airports a LEFT JOIN flights f ON a.iata_code = f.destination_iata WHERE f.destination_iata IS NULL;  -- Keeps only airports with zero matching flight records"
                 "8. For each airline, count the number of flights by status (e.g., 'On Time', 'Delayed', 'Cancelled') using CASE WHEN": " "
                 "9. Show all cancelled flights, with aircraft and both airports, ordered by departure time descending": " "
                 "10. List all city pairs (origin-destination) that have more than 2 different aircraft models operating flights between them": " "
                 "11. For each destination airport, compute the % of delayed flights (status='Delayed') among all arrivals, sorted by highest percentage": "SELECT f.destination_iata AS destination_airport,COUNT(CASE WHEN f.scheduled_departure < f.actual_departure THEN 1 END) AS delayed_arrivals,COUNT(f.flight_number) AS total_arrivals,ROUND((COUNT(CASE WHEN f.scheduled_departure < f.actual_departure THEN 1 END) * 100.0) / COUNT(f.flight_number)2) AS delay_percentage FROM flights f GROUP BY f.destination_iata ORDER BY delay_percentage DESC"

             }

             selected_query = st.selectbox("Choose a Query", list(queries.keys()))
             query_result = get_data(queries[selected_query])

            st.write("### Query Result:")
            st.dataframe(query_result)

    # -------------------------------- PAGE 4: Creator Info --------------------------------
    elif page == "Creator Info":
        st.title("👩‍💻 Creator of this Project")
        st.write("""
        **Developed by:** Sidharath Singh 
        **Skills:** Python, SQL, Data Analysis,Streamlit, Pandas    
        """)
        st.image("https://via.placeholder.com/150", caption="Your Profile Picture", width=150)


