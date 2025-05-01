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
