import streamlit as st
import mysql.connector
import pandas as pd


#Sql connection
connection = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "FkKihxumjnFVNpL.root",
  password = "PMAzpxzEEwMxG83X",
  database = "test"
)
cursor = connection.cursor(buffered=True)



#sidebar option
with st.sidebar:
    st.header("**EXPLORE**")

    option_menu=st.radio("Menu",['HOME','SELECT BUS'])
    # Custom CSS to add an image background to the sidebar
    st.markdown(
    """
    <style>
    .stSidebar {
        background-image: url('https://wallpapers.ispazio.net/wp-content/uploads/2018/03/UnderSea-X-400x866.jpg');
        background-size: cover;
        background-position: center;
        color: white; /* Adjust text color for visibility */
    }
    </style>
    """,
    unsafe_allow_html=True  
    )

#first option:
if option_menu=='HOME':
    # Background image CSS
    pg_bg_image = """
    <style>
    .stApp {
        background-image: url("https://wallpapercave.com/wp/wp7642340.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """
    # Apply the background image
    st.markdown(pg_bg_image, unsafe_allow_html=True)


    #welcome message for home page


    # Set the title of the app
    st.title("Welcome To REDBUS Data Project")

    # Add a subtitle
    st.subheader("Your one-stop solution for bus travel information")

    # Add a brief description
    st.write("""
    Welcome to the REDBUS application! 🚍

    This platform provides users with comprehensive bus travel information, including routes, schedules. Whether you're planning a trip or looking for the best bus services, we've got you covered.

    ### Features:
    - **Search for Bus Routes:** Easily find buses between cities.
    - **View Schedules:** Check departure and arrival times.
    - **Book Tickets:** Simple and secure booking process in https://www.redbus.in/

    Feel free to explore and enjoy your journey with REDBUS!
    """)


#second option:
if option_menu=='SELECT BUS':
    
    # Background image CSS
    pg_bg_image = """
    <style>
    .stApp {
        background-image: url("https://cdn.wallpapersafari.com/39/90/30FIeP.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """

    # Apply the background image
    st.markdown(pg_bg_image, unsafe_allow_html=True)

    # Title of the PAGE
    st.title("Find Your Bus Via Category !")
    
    # Column initialize
    col1, col2 = st.columns(2)
    
    # Selectbox for select route
    with col1:
        cursor.execute("SELECT DISTINCT ROUTENAME AS ROUTE FROM redbus ORDER BY ROUTENAME ASC")
        data=cursor.fetchall()
        option_menu_1=[i[0]for i in data]
    
        selected_option_1 = st.selectbox(
            "SELECT THE ROUTE:",
            options=option_menu_1
        )

    # Selectbox for bustype
    with col2:
        cursor.execute(f"SELECT DISTINCT bustype AS bustype FROM redbus WHERE routename='{selected_option_1}' ORDER BY bustype ASC")
        data=cursor.fetchall()
        option_menu_2=[i[0]for i in data]
        selected_option_2 = st.selectbox(
            "BUSTYPE:",
            options=option_menu_2,
        )
    #column initialize
    col3,col4,col5=st.columns(3)
    
    # Selectbox for Departing time 
    with col3:
        cursor.execute(f"SELECT DISTINCT departingtime AS departingtime FROM redbus WHERE routename='{selected_option_1}' AND bustype='{selected_option_2}' ORDER BY departingtime ASC")
        data=cursor.fetchall()
        option_menu_3=[i[0] for i in data]
        selected_option_3 = st.selectbox(
            "DEPARTING TIME:",
            options=option_menu_3
        )
    
        # Selectbox for Star Rating 
    with col4:
        cursor.execute(f"SELECT DISTINCT starrating as starRating FROM redbus WHERE routename='{selected_option_1}' AND bustype='{selected_option_2}' AND departingtime='{selected_option_3}' ORDER BY starrating ASC")
        data=cursor.fetchall()
        option_menu_4=[i[0] for i in data]
        selected_option_4 = st.selectbox(
            "STAR RATING:",
            options=option_menu_4
        )

    # Selectbox for price 
    with col5:
        cursor.execute(f"SELECT DISTINCT price as price FROM redbus WHERE routename='{selected_option_1}' AND bustype='{selected_option_2}' AND departingtime='{selected_option_3}' AND starrating='{selected_option_4}' ORDER BY price ASC")
        data=cursor.fetchall()
        option_menu_5=[i[0] for i in data]
        selected_option_5 = st.selectbox(
            "SELECT PRICE:",
            options=option_menu_5
        )
    
    #All filter applied
    st.header(" ")
    st.subheader("FILTER APPLIED (ALL) :")
    cursor.execute(f"SELECT * FROM redbus WHERE routename='{selected_option_1}' AND bustype='{selected_option_2}' AND departingtime='{selected_option_3}' AND starrating='{selected_option_4}' AND price='{selected_option_5}'")
    data=cursor.fetchall()
    df=pd.DataFrame(data,columns=["State", "routeName", "routeLink", "busName", "busType", "departingTime", "Duration", "ReachingTime", "StarRating", "Price", "SeatAvailability"])
    # Convert timedelta to a string format showing only hours and minutes
    df['departingTime'] = (pd.to_timedelta(df['departingTime']).dt.components.hours.astype(str).str.zfill(2) + ':' + 
                       pd.to_timedelta(df['departingTime']).dt.components.minutes.astype(str).str.zfill(2))

    df['ReachingTime'] = (pd.to_timedelta(df['ReachingTime']).dt.components.hours.astype(str).str.zfill(2) + ':' + 
                      pd.to_timedelta(df['ReachingTime']).dt.components.minutes.astype(str).str.zfill(2))
    st.write(df)


    #Route only selcted
    st.header(" ")
    st.subheader("ALL BUSSES IN SELECTED ROUTE :")
    cursor.execute(f"SELECT * FROM redbus WHERE routename='{selected_option_1}' AND seatavailability != 0")
    data=cursor.fetchall()
    df=pd.DataFrame(data,columns=["State", "routeName", "routeLink", "busName", "busType", "departingTime", "Duration", "ReachingTime", "StarRating", "Price", "SeatAvailability"])
    # Convert timedelta to a string format showing only hours and minutes
    df['departingTime'] = (pd.to_timedelta(df['departingTime']).dt.components.hours.astype(str).str.zfill(2) + ':' + 
                       pd.to_timedelta(df['departingTime']).dt.components.minutes.astype(str).str.zfill(2))

    df['ReachingTime'] = (pd.to_timedelta(df['ReachingTime']).dt.components.hours.astype(str).str.zfill(2) + ':' + 
                      pd.to_timedelta(df['ReachingTime']).dt.components.minutes.astype(str).str.zfill(2))
    st.write(df)