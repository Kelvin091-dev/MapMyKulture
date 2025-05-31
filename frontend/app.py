import streamlit as st
import folium
from streamlit_folium import folium_static
import snowflake.connector
from dotenv import load_dotenv
import os

# ---- Page Configuration ----
st.set_page_config(
    page_title="MapMy Kulture",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Load Environment Variables ----
load_dotenv(".env")


# ---- Snowflake Connection ----
def get_snowflake_connection():
    try:
        return snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        return None


# ---- Data Fetching Functions ----
def fetch_states():
    conn = get_snowflake_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT NAME FROM MMK.STATES ORDER BY NAME ASC")
        states = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return states
    except Exception as e:
        st.error(f"🚨 Error fetching states: {str(e)}")
        return []
    finally:
        try:
            conn.close()
        except:
            pass


def get_state_details(state_name):
    conn = get_snowflake_connection()
    if not conn:
        return None, None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ID, NAME FROM MMK.STATES WHERE LOWER(NAME) = LOWER(%s)",
            (state_name,)
        )
        row = cursor.fetchone()
        return row if row else (None, None)
    except Exception as e:
        st.error(f"🚨 Error fetching state details: {str(e)}")
        return None, None
    finally:
        try:
            conn.close()
        except:
            pass


def fetch_map_data(state_id):
    conn = get_snowflake_connection()
    if not conn:
        return [], []

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT NAME, LATITUDE, LONGITUDE FROM MMK.TOURIST_PLACES "
            "WHERE STATE_ID = %s AND LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL",
            (state_id,)
        )
        heritage = [
            {"name": row[0], "lat": float(row[1]), "lon": float(row[2])}
            for row in cursor.fetchall()
        ]

        cursor.execute(
            "SELECT NAME, LATITUDE, LONGITUDE FROM MMK.FESTIVALS "
            "WHERE STATE_ID = %s AND LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL",
            (state_id,)
        )
        festivals = [
            {"name": row[0], "lat": float(row[1]), "lon": float(row[2])}
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()
        return heritage, festivals
    except Exception as e:
        st.error(f"🚨 Error fetching map data: {str(e)}")
        return [], []
    finally:
        try:
            conn.close()
        except:
            pass


# ---- Enhanced Styles ----
def inject_style():
    banner_url = "https://www.poojn.in/wp-content/uploads/2025/05/Maharashtras-UNESCO-World-Heritage-Sites-A-Complete-Guide-With-Photos.jpeg.jpg"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,165,0,0.2), rgba(255,255,255,0.5)),
                    url('{banner_url}');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Palatino Linotype', 'Book Antiqua', serif;
    }}
    .card {{
        background-color: white !important;
        color: black !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    .section-title {{
        color: black !important;
        border-left: 5px solid #e67e22;
        padding-left: 15px;
        margin: 30px 0 20px 0;
    }}
    .culture-img {{
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 10px 0;
        height: 250px;
        object-fit: cover;
        border: 2px solid #ffffff;
    }}
    .map-container {{
        border: 3px solid #e67e22;
        border-radius: 15px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.8);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: black!important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255,255,255,0.25) !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: white !important;
    }}
    .streamlit-expanderHeader {{
        color: white !important;
        background-color: white !important;
    }}
    .streamlit-expanderContent {{
        color: white  !important;
        background-color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ---- Page Components ----
def home_page():
    inject_style()
    st.markdown("<h1 style='text-align:center;'>MapMy Kulture</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#16a085;'>Discover India's Cultural Tapestry</h4>",
                unsafe_allow_html=True)

    states = fetch_states()
    if not states:
        st.warning("Could not load states. Please check Snowflake connection and tables.")
        return

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_state = st.selectbox("Select a State to Explore", states)
        if st.button("🗺 Show on Map"):
            st.session_state.page = "state_map"
            st.session_state.selected_state = selected_state
            st.rerun()


def state_map_page():
    inject_style()
    selected_state = st.session_state.selected_state
    state_id, _ = get_state_details(selected_state)

    if not state_id:
        st.error("Could not retrieve state details")
        return

    heritage, festivals = fetch_map_data(state_id)

    map_center = [20.5937, 78.9629]
    if heritage:
        map_center = [heritage[0]["lat"], heritage[0]["lon"]]
    elif festivals:
        map_center = [festivals[0]["lat"], festivals[0]["lon"]]

    m = folium.Map(location=map_center, zoom_start=7)

    for site in heritage:
        folium.Marker(
            location=[site["lat"], site["lon"]],
            tooltip=f"🏰 {site['name']}",
            icon=folium.Icon(color="Red", icon="monument", prefix="fa")
        ).add_to(m)

    for festival in festivals:
        folium.Marker(
            location=[festival["lat"], festival["lon"]],
            tooltip=f"🎉 {festival['name']}",
            icon=folium.Icon(color="blue", icon="guitar", prefix="fa")
        ).add_to(m)

    with st.container():
        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        folium_static(m, width=1000, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Explore Cultural Details →"):
            st.session_state.page = "state_details"
            st.rerun()


def state_details_page():
    inject_style()
    selected_state = st.session_state.selected_state
    state_id, state_name = get_state_details(selected_state)

    if not state_id:
        st.error("Could not retrieve state details")
        return

    st.markdown(f"""
    <style>
    .card-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}
    
    .card {{
        background-color: #FFF8DC !important;
        color: #000000 !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 10px 15px;
        
        border: none;
      display: inline-block; /* Shrinks to content size */
    text-align: center;
}}
    .card-title {{
        font-size: 1.3rem;
        font-weight: bold;
        margin: 0;
        color: #333333 !important;
        text-align: center;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 4px;
    }}
    
    .card-content {{
        font-size: 1.5rem;
        font-weight: bold;
        color: black!important;
        line-height: 1.6;
    }}
    
    .image-container {{
        width: 100%;
        margin: 0 auto;
        padding-bottom: 10px;
        text-align: center;
    }}
    
   
    .stImage img {{
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    @media (max-width: 768px) {{
        .card, .header-card {{
            width: 95%;
        }}
    }}
    </style>
    
    """, unsafe_allow_html=True)

    TABLE_CONFIG = {
        "festivals": {"title": "NAME", "desc": "DESCRIPTION", "img": "URL"},
        "tourist_places": {"title": "NAME", "desc": "DESCRIPTION", "img": "URL"},
        "local_foods": {"title": "DISH_NAME", "desc": "DESCRIPTION", "img": "URL"},
        "handicrafts": {"title": "CRAFT_NAME", "desc": "DESCRIPTION", "img": "URL"},
        "government_schemes": {"title": "SCHEME_NAME", "desc": "DESCRIPTION", "img": None}
    }

    cultural_data = fetch_state_details(state_id)

    st.markdown(f"<h2 style='color:#2c3e50 !important; text-align: center; margin-bottom: 30px;'>🏞 Cultural Heritage of {state_name}</h2>", unsafe_allow_html=True)

    tabs = st.tabs([tab.replace("_", " ").title() for tab in cultural_data.keys()])

    for tab, (table_name, items) in zip(tabs, cultural_data.items()):
        with tab:
            if not items:
                st.info(f"No {table_name.replace('_', ' ')} data available")
                continue

            config = TABLE_CONFIG[table_name]
            for item in items:
                title = item[config['title'].lower()]
                description = item[config['desc'].lower()]
                image_url = item.get(config['img'].lower()) if config['img'] else None

                with st.container():
                    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class='card'>
                        <div class='card-title'>{title}</div>
                    """, unsafe_allow_html=True)
                    
                    if image_url:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown("<div class='image-container'>", unsafe_allow_html=True)
                            st.image(
                                image_url,
                                width=250,  # Slightly larger fixed width
                                caption=title,
                                output_format="auto"
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div class='card-content'>
                                {description}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='card-content'>
                            {description}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if table_name == "government_schemes":
                        st.markdown("""
                        <div class='card-content'>
                            <strong>Implementation Status:</strong> Active
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)  # Close card
                    st.markdown("</div>", unsafe_allow_html=True)  # Close card-container

    if st.button("← Back to Map", key="back_button"):
        st.session_state.page = "state_map"
        st.rerun()

def fetch_state_details(state_id):
    conn = get_snowflake_connection()
    if not conn:
        return {}

    data = {}
    tables = {
        "festivals": {"title": "NAME", "desc": "DESCRIPTION", "img": "URL"},
        "tourist_places": {"title": "NAME", "desc": "DESCRIPTION", "img": "URL"},
        "local_foods": {"title": "DISH_NAME", "desc": "DESCRIPTION", "img": "URL"},
        "handicrafts": {"title": "CRAFT_NAME", "desc": "DESCRIPTION", "img": "URL"},
        "government_schemes": {"title": "SCHEME_NAME", "desc": "DESCRIPTION", "img": None},
    }

    try:
        cursor = conn.cursor()
        for table, cols in tables.items():
            columns = ["ID", cols['title'], cols['desc']]
            if cols['img']:
                columns.append(cols['img'])

            cursor.execute(
                f"SELECT {', '.join(columns)} FROM MMK.{table} WHERE STATE_ID = %s",
                (state_id,)
            )
            data[table] = [
                dict(zip([col.lower() for col in columns], row))
                for row in cursor.fetchall()
            ]
    except Exception as e:
        st.error(f"Error fetching {table} data: {str(e)}")
    finally:
        conn.close()

    return data



# ---- Main App Flow ----
if "page" not in st.session_state:
    st.session_state.page = "home"

pages = {
    "home": home_page,
    "state_map": state_map_page,
    "state_details": state_details_page
}

pages[st.session_state.page]()
