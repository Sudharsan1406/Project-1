
# Project 1 :

# NASA Near-Earth Object (NEO) Tracking & Insights using Public API

# Data On Boarding

import requests

import datetime
from datetime import datetime

API_KEY = "cLJtmgRvl3Y65KUxylaQ74vekIleNPdtNjHhDCfh"

url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_KEY}"

response = requests.get(url)

data = response.json()  # dictionary format

data

data.keys()

data['near_earth_objects'].keys()

len(data['near_earth_objects'])

details = data['near_earth_objects']

data['near_earth_objects']['2024-01-02']

data['near_earth_objects']['2024-01-02'][0]['close_approach_data'][0]['orbiting_body']

data['near_earth_objects']['2024-01-02'][0]['close_approach_data'][0]['close_approach_date']

type(data['near_earth_objects']['2024-01-02'][0]['close_approach_data'][0]['close_approach_date'])

details.items()

details.keys()

data['links']

# ________________________________******__________________________________________
# Data Processing

asteroids_data = []
target = 10000
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_KEY}"
row1 = []
row2 = []

while len(asteroids_data) < target:
    response  = requests.get(url)
    data      = response.json()
    details   = data['near_earth_objects']
    for date, info in details.items():
        for i in info:

            asteroids_data.append(dict(
            id = i['id'],
            neo_reference_id = i['neo_reference_id'],
            name = i['name'],
            mag = float(i['absolute_magnitude_h']),
            dia_min = float(i['estimated_diameter']['kilometers']['estimated_diameter_min']),
            dia_max = float(i['estimated_diameter']['kilometers']['estimated_diameter_max']),
            hazar = bool(i['is_potentially_hazardous_asteroid']),
            date = datetime.strptime((i['close_approach_data'][0]['close_approach_date']),'%Y-%m-%d'),
            velocity = float(i['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
            astronomical = float(i['close_approach_data'][0]['miss_distance']['astronomical']),
            miss_dis_km = float(i['close_approach_data'][0]['miss_distance']['kilometers']),
            miss_dis_lunar = float(i['close_approach_data'][0]['miss_distance']['lunar']),
            orbiting_body = (i['close_approach_data'][0]['orbiting_body'])
                                  ))
            row1.append((
            i['id'],
            i['name'],
            float(i['absolute_magnitude_h']),
            float(i['estimated_diameter']['kilometers']['estimated_diameter_min']),
            float(i['estimated_diameter']['kilometers']['estimated_diameter_max']),
            bool(i['is_potentially_hazardous_asteroid'])
                                  ))
            row2.append((
            i['neo_reference_id'],
            datetime.strptime(i['close_approach_data'][0]['close_approach_date'],'%Y-%m-%d'),
            float(i['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
            float(i['close_approach_data'][0]['miss_distance']['astronomical']),
            float(i['close_approach_data'][0]['miss_distance']['kilometers']),
            float(i['close_approach_data'][0]['miss_distance']['lunar']),
            (i['close_approach_data'][0]['orbiting_body'])
                                  ))

            if len(asteroids_data) >= target:
                break
        if len(asteroids_data) >= target:
            break

    url = data['links'].get('next')

type(row2[0][1])

len(asteroids_data)

asteroids_data

len(row1)

# ________________________________******__________________________________________
# SQL Operations

import mysql.connector

conn = mysql.connector.connect(
    host      ="localhost",
    user      ="root",
    password  ="Sudhan140695@",
    database  = "nasa"

)
cursor = conn.cursor()
print("MySQL connection established!")

conn

cursor.execute("""
    CREATE TABLE IF NOT EXISTS asteroids (
          id int,
          name TEXT,
          absolute_magnitude_h FLOAT,
          estimated_diameter_min_km FLOAT,
          estimated_diameter_max_km FLOAT,
          is_potentially_hazardous_asteroid BOOLEAN
          );
""")
conn.commit()
print("Table 'asteroids' created successfully in MySQL!")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS close_approach (
            id int,
            close_approach_date DATE,
            relative_velocity_kmph FLOAT,
            astronomical FLOAT,
            miss_distance_km FLOAT,
            miss_distance_lunar FLOAT,
            orbiting_body TEXT
          );
""")
conn.commit()
print("Table 'close_approach' created successfully in MySQL!")

insert1 = """

    INSERT INTO  asteroids
    values
    (%s,%s,%s,%s,%s,%s)

    """

cursor.executemany(insert1,row1)
conn.commit()
print("Table 'asteroids' created successfully in MySQL!")

insert2 = """

    INSERT INTO  close_approach
    values
    (%s,%s,%s,%s,%s,%s,%s)

    """

cursor.executemany(insert2,row2)
conn.commit()
print("Table 'close_approach' created successfully in MySQL!")

# ________________________________******__________________________________________
# SQL Queries

from tabulate import tabulate

query_1 = """
select a.name as asteroids_name,
count(c.id) as approach_count
from asteroids a
join close_approach c
on a.id = c.id
where c.orbiting_body = 'Earth'
group by a.name
order by approach_count desc;
"""
cursor.execute(query_1)
result_1 = cursor.fetchall()
print("query 1 : Count how many times each asteroid has approached Earth")

# Define table headers
headers = ["asteroids_name", "approach_count"]

# Print the result as a table
print(tabulate(result_1, headers=headers, tablefmt="grid"))

query_2 = """
select a.name as Asteroids_name,
avg(c.relative_velocity_kmph) as Avg_Velocity
from asteroids a
join close_approach c
on a.id = c.id
group by a.name
order by Avg_Velocity desc; """
cursor.execute(query_2)
result_2 = cursor.fetchall()
print("query 2 : Average velocity of each asteroid over multiple approaches")

# Define table headers
headers = ["asteroids_name", "Avg_Velocity"]

# Print the result as a table
print(tabulate(result_2, headers=headers, tablefmt="grid"))

query_3 = """
select a.name as Asteroid_Name,
c.relative_velocity_kmph as Relative_Velocity_kmph,
c.close_approach_date as Close_app_date
from asteroids a
join close_approach c
on a.id = c.id
order by Relative_Velocity_kmph desc
limit 10; """
cursor.execute(query_3)
result_3 = cursor.fetchall()
print("query 3 : List top 10 fastest asteroids")

# Define table headers
headers = ["asteroids_name", "Avg_Velocity","Close_app_date"]

# Print the result as a table
print(tabulate(result_3, headers=headers, tablefmt="grid"))

query_4 = """
select a.name as asteroids_name,
count(c.id) as approach_count
from asteroids a
join close_approach c
on a.id = c.id
where a.is_potentially_hazardous_asteroid = 0
and c.orbiting_body = 'Earth'
group by a.name
having count(c.id) > 3
order by approach_count desc; """
cursor.execute(query_4)
result_4 = cursor.fetchall()
print("query 4 : Find potentially hazardous asteroids that have approached Earth more than 3 times")

# Define table headers
headers = ["asteroids_name", "approach_count"]

# Print the result as a table
print(tabulate(result_4, headers=headers, tablefmt="grid"))

query_5 = """
select
month(c. close_approach_date) 'Most Approach Month',
count(*) as Toatl_Approaches
from close_approach c
group by month(c.close_approach_date)
order by(Toatl_Approaches) Desc
limit 1;
 """
cursor.execute(query_5)
result_5 = cursor.fetchall()
print("query 5 : Find the month with the most asteroid approaches ")

# Define table headers
headers = ["asteroids_name", "approach_count"]

# Print the result as a table
print(tabulate(result_5, headers=headers, tablefmt="grid"))

query_5 = """
select
month(c. close_approach_date) 'Most Approach Month',
count(*) as Toatl_Approaches
from close_approach c
group by month(c.close_approach_date)
order by(Toatl_Approaches) Desc
limit 1;
 """
cursor.execute(query_5)
result_5 = cursor.fetchall()
print("query 5 : Find the month with the most asteroid approaches ")

# Define table headers
headers = ["Most Approach Month", "Toatl_Approaches"]

# Print the result as a table
print(tabulate(result_5, headers=headers, tablefmt="grid"))

query_6 = """
select a.name,
c.close_approach_date,
c.relative_velocity_kmph
from asteroids a
join close_Approach c
on a.id = c.id
order by c.relative_velocity_kmph desc
limit 1;
 """
cursor.execute(query_6)
result_6 = cursor.fetchall()
print("query 6 : Get the asteroid with the fastest ever approach speed ")

# Define table headers
headers = ["name", "close_approach_date","relative_velocity_kmph"]

# Print the result as a table
print(tabulate(result_6, headers=headers, tablefmt="grid"))

query_7 = """
select a.name, a.estimated_diameter_max_km
from asteroids a
order by a.estimated_diameter_max_km desc;
 """
cursor.execute(query_7)
result_7 = cursor.fetchall()
print("query 7 : Sort asteroids by maximum estimated diameter (descending) ")

# Define table headers
headers = ["name", "estimated_diameter_max_km"]

# Print the result as a table
print(tabulate(result_7, headers=headers, tablefmt="grid"))

query_8 = """
SELECT id
FROM (SELECT id, close_approach_date, miss_distance_km,
LAG(miss_distance_km) OVER (PARTITION BY id ORDER BY close_approach_date) AS prev_distance
FROM close_approach)t
WHERE prev_distance IS NOT NULL AND miss_distance_km < prev_distance GROUP BY id;
 """
cursor.execute(query_8)
result_8 = cursor.fetchall()
print("query 8 : Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)")

# Define table headers
headers = ["id"]

# Print the result as a table
print(tabulate(result_8, headers=headers, tablefmt="grid"))

query_9 = """
select a.name, c.close_approach_date, c.miss_distance_km
from asteroids a join close_approach c
on a.id = c.id
where c.orbiting_body = 'Earth'
order by c.close_approach_date, c.miss_distance_km desc;
 """
cursor.execute(query_9)
result_9 = cursor.fetchall()
print("query 9 : Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.")

# Define table headers
headers = ["name", "close_approach_date","miss_distance_km"]

# Print the result as a table
print(tabulate(result_9, headers=headers, tablefmt="grid"))

query_10 = """
select a.name, c.relative_velocity_kmph
from asteroids a join close_approach c
on a.id = c.id
where c.orbiting_body = 'Earth' and (c.relative_velocity_kmph  > 50000)
order by (c.relative_velocity_kmph) desc;
 """
cursor.execute(query_10)
result_10 = cursor.fetchall()
print("query 10 : List names of asteroids that approached Earth with velocity > 50,000 km/h ")

# Define table headers
headers = ["name", "relative_velocity_kmph"]

# Print the result as a table
print(tabulate(result_10, headers=headers, tablefmt="grid"))

query_11 = """
select month(c.close_approach_date),
count(*) as Toatl_Count
from close_approach c
group by month(c.close_approach_date)
order by(Toatl_Count) Desc;
 """
cursor.execute(query_11)
result_11 = cursor.fetchall()
print("query 11 : Count how many approaches happened per month")

# Define table headers
headers = ["month", "relative_velocity_kmph"]

# Print the result as a table
print(tabulate(result_11, headers=headers, tablefmt="grid"))

query_12 = """
select a.name, a.absolute_magnitude_h
from asteroids a
order by a.absolute_magnitude_h asc
limit 1;
 """
cursor.execute(query_12)
result_12 = cursor.fetchall()
print("query 12 : Find asteroid with the highest brightness (lowest magnitude value)")

# Define table headers
headers = ["Name", "absolute_magnitude_h"]

# Print the result as a table
print(tabulate(result_12, headers=headers, tablefmt="grid"))

query_13 = """
select is_potentially_hazardous_asteroid as Hazard_Status,
count(*) as Total_Asteroids
from asteroids
group by is_potentially_hazardous_asteroid;
 """
cursor.execute(query_13)
result_13 = cursor.fetchall()
print("query 13 :  Get number of hazardous vs non-hazardous asteroids")

# Define table headers
headers = ["Hazard_Status", "Total_Asteroids"]

# Print the result as a table
print(tabulate(result_13, headers=headers, tablefmt="grid"))

query_14 = """
select a.name, c.close_approach_date, c.miss_distance_lunar
from asteroids a join close_approach c
on a.id = c.id
where c.miss_distance_lunar < 1 and c.orbiting_body = 'Earth'
order by c.miss_distance_lunar asc;
 """
cursor.execute(query_14)
result_14 = cursor.fetchall()
print("query 14 :  Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance.")

# Define table headers
headers = ["Name", "close_approach_date","miss_distance_lunar"]

# Print the result as a table
print(tabulate(result_14, headers=headers, tablefmt="grid"))

query_15 = """
select a.name, c.astronomical
from asteroids a join close_approach c
on a.id = c.id
where c.astronomical <= 0.05
order by c.astronomical asc;
 """
cursor.execute(query_15)
result_15 = cursor.fetchall()
print("query 15 :  Find asteroids that came within 0.05 AU(astronomical distance)")

# Define table headers
headers = ["Name", "astronomical"]

# Print the result as a table
print(tabulate(result_15, headers=headers, tablefmt="grid"))

query_16 = """
SELECT name, estimated_diameter_max_km
FROM asteroids
ORDER BY estimated_diameter_max_km
DESC LIMIT 5;
"""
cursor.execute(query_16)
result_16 = cursor.fetchall()
print("query 16 :  Find the 5 largest asteroids by maximum estimated diameter")

# Define table headers
headers = ["Name", "estimated_diameter_max_km"]

# Print the result as a table
print(tabulate(result_16, headers=headers, tablefmt="grid"))

query_17 = """SELECT a.name, AVG(c.relative_velocity_kmph) AS avg_velocity
FROM asteroids a JOIN close_approach c ON a.id = c.id
GROUP BY a.name ORDER BY avg_velocity DESC LIMIT 1;"""
cursor.execute(query_17)
result_17 = cursor.fetchall()
print("query 17 :  Which asteroid had the highest average velocity in all its approaches?")

# Define table headers
headers = ["Name", "Avg_velocity"]

# Print the result as a table
print(tabulate(result_17, headers=headers, tablefmt="grid"))

query_18 = """
SELECT COUNT(DISTINCT a.id) AS count
FROM asteroids a JOIN close_approach c
ON a.id = c.id
WHERE a.estimated_diameter_max_km > 1
AND c.relative_velocity_kmph > 50000;
"""
cursor.execute(query_18)
result_18 = cursor.fetchall()
print("query 18 : How many asteroids have both large size (diameter > 1 km) and high speed (> 50,000 kmph)?")

# Define table headers
headers = ["Count"]

# Print the result as a table
print(tabulate(result_18, headers=headers, tablefmt="grid"))

query_19 = """
SELECT close_approach_date, COUNT(*) AS approaches
FROM close_approach
GROUP BY close_approach_date
HAVING COUNT(*) > 1 ORDER BY approaches DESC;
 """
cursor.execute(query_19)
result_19 = cursor.fetchall()
print("Find dates where more than 1 asteroid approached Earth on the same day ")

# Define table headers
headers = ["close_approach_date", "approaches"]

# Print the result as a table
print(tabulate(result_19, headers=headers, tablefmt="grid"))

query_20 = """
SELECT name, (estimated_diameter_max_km - estimated_diameter_min_km) as 'Diameter_Variation'
FROM asteroids Order by Diameter_Variation desc LIMIT 10;
 """
cursor.execute(query_20)
result_20 = cursor.fetchall()
print("query 20 :  List the asteroids with most varying diameter estimates")

# Define table headers
headers = ["Name", "Diameter_Variation"]

# Print the result as a table
print(tabulate(result_20, headers=headers, tablefmt="grid"))




# ________________________________******__________________________________________
# StreamLit

%%writefile Project.py
import streamlit as st
#st.set_page_config(layout = 'wide')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Set page config (optional)
st.set_page_config(page_title="Asteroid App", layout="wide")

# Function to load and encode local jpg image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Local image filename (same folder)
image_file = 'Earth.jpg'

# Get base64 string
img_base64 = get_base64_of_bin_file(image_file)

# Inject HTML + CSS for background
page_bg_img = f"""
<style>
.stApp {{
  background-image: url("data:image/jpg;base64,{img_base64}");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}}
</style>
"""

# Load CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

import mysql.connector

conn = mysql.connector.connect(
    host      ="localhost",
    user      ="root",
    password  ="Sudhan140695@",
    database  = "nasa"
    
)
cursor = conn.cursor()
print("MySQL connection established!")


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Filter Criteria", "SQL Queries", "Creator Info"])

# -------------------------------- PAGE 1: Introduction --------------------------------
if page == "Project Introduction":
    st.title("🚀 NASA Near-Earth Object (NEO) Tracking & Insights using Public API")
    st.subheader("📊 A Streamlit App for Exploring NASA Near-Earth Object (NEO) Tracking & Insights")
    st.write("""
    **This project analyzes NASA Near-Earth Object (NEO) Tracking & Insights data from different months using an MySQL database :-**

    ● Threat Monitoring: Analyze which asteroids are potentially hazardous based on
    velocity, size, and proximity.\n
    ● Date-Based Exploration: Understand patterns of asteroid occurrences and visits by
    date.\n
    ● Filtering for Insight: Help researchers or educators filter based on custom conditions
    like approach distance, size, or orbiting body.\n
    ● Space Data Democratization: Deliver an intuitive interface for non-technical users to
    explore astronomical data.  

    **Features:**
    - View and filter NEO data by id, Velocity, Month, etc,.
    - Generate dynamic visualizations.
    - Run predefined SQL queries to explore insights.

    **Database Used:** `nasa_neo`
    """)
    st.image(r"C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Earth2.jpg", width=350)

# -------------------------------- PAGE 2: Filter Criteria --------------------------------
elif page == "Filter Criteria":
    st.title("🚀 NASA (NEO) Tracking & Insights using Public API")


    cursor.execute("""
    SELECT 
    a.name, 
    a.absolute_magnitude_h, 
    a.estimated_diameter_min_km,
    a.estimated_diameter_max_km, 
    a.is_potentially_hazardous_asteroid, 
    c.close_approach_date, 
    c.relative_velocity_kmph, 
    c.astronomical
    FROM asteroids a 
    JOIN close_approach c 
    ON a.id = c.id; 
    """)
    

    row = cursor.fetchall()
    
    df = pd.DataFrame(row, columns = ["name", 'absolute_magnitude_h','estimated_diameter_min_km', 'estimated_diameter_max_km',
                                      'is_potentially_hazardous_asteroid', 'close_approach_date', 'relative_velocity_kmph', 'astronomical'])
    
    df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])

    st.markdown ("## Asteroids Filtering Dashboard")

    c1,c2,c3 = st.columns([1,1,1], gap = 'large')
    c4,c5,c6 = st.columns([1,1,1], gap = 'large')
    c7,c8 = st.columns([1,1], gap = 'large')

    with c1 :
        # Magnitude slider
        mag_min, mag_max = st.slider("select Maximum Magnitude ",float(df['absolute_magnitude_h'].min()),float(df['absolute_magnitude_h'].max()),
                                     (float(df['absolute_magnitude_h'].min()),float(df['absolute_magnitude_h'].max())))
    with c2 :
        # Velocity slider
        vel_min, vel_max = st.slider(
            "Select Velocity Range (km/h)",
            float(df['relative_velocity_kmph'].min()),
            float(df['relative_velocity_kmph'].max()),
            (float(df['relative_velocity_kmph'].min()), float(df['relative_velocity_kmph'].max()))
    )
    
    with c3 :
        # Astronomical Unit slider
        au_min, au_max = st.slider(
            "Select Astronomical Unit (AU) Range",
            float(df['astronomical'].min()),
            float(df['astronomical'].max()),
            (float(df['astronomical'].min()), float(df['astronomical'].max()))
        )
        
    with c4 :
        # Estimated Diameter sliders
        diameter_min, diameter_max = st.slider(
            "Select Minimum Estimated Diameter (km)",
            float(df['estimated_diameter_min_km'].min()),
            float(df['estimated_diameter_min_km'].max()),
            (float(df['estimated_diameter_min_km'].min()), float(df['estimated_diameter_min_km'].max()))
        )

    with c5 :
        max_diameter_min, max_diameter_max = st.slider(
            "Select Maximum Estimated Diameter (km)",
            float(df['estimated_diameter_max_km'].min()),
            float(df['estimated_diameter_max_km'].max()),
            (float(df['estimated_diameter_max_km'].min()), float(df['estimated_diameter_max_km'].max()))
        )
        
    with c6 :
        # Date range selector
        start_date, end_date = st.date_input(
            "Select Close Approach Date Range",
            (df['close_approach_date'].min(), df['close_approach_date'].max())
        )
        
    with c7 :
        # Hazardous checkbox
        hazardous_only = st.checkbox("Show only Potentially Hazardous Asteroids")
    
    with c8 :
        # Hazardous checkbox
        Non_hazardous_only = st.checkbox("Show only Potentially Non-Hazardous Asteroids")
    
    # Step 5: Apply Filters
    filtered_df = df[
        (df['absolute_magnitude_h'] >= mag_min) & (df['absolute_magnitude_h'] <= mag_max) &
        (df['relative_velocity_kmph'] >= vel_min) & (df['relative_velocity_kmph'] <= vel_max) &
        (df['astronomical'] >= au_min) & (df['astronomical'] <= au_max) &
        (df['estimated_diameter_min_km'] >= diameter_min) & (df['estimated_diameter_min_km'] <= diameter_max) &
        (df['estimated_diameter_max_km'] >= max_diameter_min) & (df['estimated_diameter_max_km'] <= max_diameter_max) &
        (df['close_approach_date'] >= pd.to_datetime(start_date)) & (df['close_approach_date'] <= pd.to_datetime(end_date))
    ]
    
    if hazardous_only:
        filtered_df = filtered_df[filtered_df['is_potentially_hazardous_asteroid'] == 1]
    if Non_hazardous_only:
        filtered_df = filtered_df[filtered_df['is_potentially_hazardous_asteroid'] == 0]
    
    # Step 6: Show the filtered data
    st.markdown("## Filtered Asteroids")
    st.dataframe(filtered_df)
# -------------------------------- PAGE 3: SQL Queries --------------------------------
elif page == "SQL Queries":
    st.title("📋 SQL Query Results")

    def get_data(query, params=None):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sudhan140695@",
            database="nasa"
        )
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df

    queries = {
        
        "1. Count how many times each asteroid has approached Earth " : " select a.name as asteroids_name, count(c.id) as approach_count from asteroids a join close_approach c on a.id = c.id where c.orbiting_body = 'Earth' group by a.name order by approach_count desc;" ,
        "2. Average velocity of each asteroid over multiple approaches " : " select a.name as Asteroids_name, avg(c.relative_velocity_kmph) as Avg_Velocity from asteroids a join close_approach c on a.id = c.id group by a.name order by Avg_Velocity desc;",
        "3. List top 10 fastest asteroids " : "select a.name as Asteroid_Name, c.relative_velocity_kmph as Relative_Velocity_kmph, c.close_approach_date as Close_app_date from asteroids a join close_approach c on a.id = c.id order by Relative_Velocity_kmph desc limit 10;",
        "4. Find potentially hazardous asteroids that have approached Earth more than 3 times " : "select a.name as asteroids_name, count(c.id) as approach_count from asteroids a join close_approach c on a.id = c.id where a.is_potentially_hazardous_asteroid = 0  and c.orbiting_body = 'Earth' group by a.name having count(c.id) > 3 order by approach_count desc;",
        "5. Find the month with the most asteroid approaches " : "select month(c. close_approach_date) 'Most Approach Month', count(*) as Toatl_Approaches from close_approach c group by month(c.close_approach_date) order by(Toatl_Approaches) Desc limit 1;",
        "6. Get the asteroid with the fastest ever approach speed " : "select a.name, c.close_approach_date, c.relative_velocity_kmph from asteroids a join close_approach c on a.id = c.id order by c.relative_velocity_kmph desc limit 1;",
        "7. Sort asteroids by maximum estimated diameter (descending) " : "select a.name, a.estimated_diameter_max_km from asteroids a order by a.estimated_diameter_max_km desc;",
        "8. Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)" : "SELECT id FROM (SELECT id, close_approach_date, miss_distance_km, LAG(miss_distance_km) OVER (PARTITION BY id ORDER BY close_approach_date) AS prev_distance FROM close_approach)t WHERE prev_distance IS NOT NULL AND miss_distance_km < prev_distance GROUP BY id;",
        "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth" : "select a.name, c.close_approach_date, c.miss_distance_km from asteroids a join close_approach c on a.id = c.id  where c.orbiting_body = 'Earth' order by c.close_approach_date, c.miss_distance_km desc;",
        "10. List names of asteroids that approached Earth with velocity > 50,000 km/h " : "select a.name, c.relative_velocity_kmph from asteroids a join close_approach c on a.id = c.id where c.orbiting_body = 'Earth' and (c.relative_velocity_kmph  > 50000) order by (c.relative_velocity_kmph) desc;",
        "11. Count how many approaches happened per month " : "select month(c.close_approach_date), count(*) as Toatl_Count from close_approach c group by month(c.close_approach_date) order by(Toatl_Count) Desc;",
        "12. Find asteroid with the highest brightness (lowest magnitude value) " :  "select a.name, a.absolute_magnitude_h from asteroids a order by a.absolute_magnitude_h asc limit 1;",
        "13. Get number of hazardous vs non-hazardous asteroids " : "select is_potentially_hazardous_asteroid as Hazard_Status, count(*) as Total_Asteroids from asteroids group by is_potentially_hazardous_asteroid;",
        "14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance" : "select a.name, c.close_approach_date, c.miss_distance_lunar from asteroids a join close_approach c on a.id = c.id  where c.miss_distance_lunar < 1 and c.orbiting_body = 'Earth' order by c.miss_distance_lunar asc;",
        "15. Find asteroids that came within 0.05 AU(astronomical distance) " : "select a.name, c.astronomical from asteroids a join close_approach c on a.id = c.id  where c.astronomical <= 0.05 order by c.astronomical asc;" ,
        "16. Find the 5 largest asteroids by maximum estimated diameter" : "SELECT name, estimated_diameter_max_km FROM asteroids ORDER BY estimated_diameter_max_km DESC LIMIT 5;",  
        "17. Which asteroid had the highest average velocity in all its approaches?" : "SELECT a.name, AVG(c.relative_velocity_kmph) AS avg_velocity FROM asteroids a JOIN close_approach c ON a.id = c.id GROUP BY a.name ORDER BY avg_velocity DESC LIMIT 1;",
        "18. How many asteroids have both large size (diameter > 1 km) and high speed (> 50,000 kmph)?" : "SELECT COUNT(DISTINCT a.id) AS count FROM asteroids a JOIN close_approach c ON a.id = c.id WHERE a.estimated_diameter_max_km > 1 AND c.relative_velocity_kmph > 50000;",
        "19. Find dates where more than 1 asteroid approached Earth on the same day ":"SELECT close_approach_date, COUNT(*) AS approaches FROM close_approach GROUP BY close_approach_date HAVING COUNT(*) > 1 ORDER BY approaches DESC;",
        "20. List the asteroids with most varying diameter estimates " : "SELECT name, (estimated_diameter_max_km - estimated_diameter_min_km) as 'Diameter_Variation' FROM asteroids Order by Diameter_Variation desc LIMIT 10;"
    }
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))
    query_result = get_data(queries[selected_query])

    st.write("### Query Result:")
    st.dataframe(query_result)

# -------------------------------- PAGE 4: Creator Info --------------------------------
elif page == "Creator Info":
    st.title("👩‍💻 Creator of this Project")
    st.write("""
#    **Developed by:** Sudharsan M S
#    **Skills:** Python, Pandas, MySQL, Streamlit
    """)
    st.image(r"C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\RC.jpg", width=150)
