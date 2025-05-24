import streamlit as st
from datetime import date

# ---- Page Configuration ----
st.set_page_config(
    page_title="MapMy Kulture",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- Inject Custom Styles ----
def inject_style():
    banner_url = "https://t4.ftcdn.net/jpg/11/02/86/89/360_F_1102868968_To7xQ8HffJwpKD6rz6LogPeAWmJeOWfX.jpg"

    st.markdown(f"""
    <style>
    @keyframes scroll-left {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}

    .stApp {{
        background: 
            linear-gradient(
                rgba(255,165,0,0.1), 
                rgba(255,255,255,0.3), 
                rgba(0,128,0,0.1)
            );
        font-family: 'Segoe UI', sans-serif;
        padding-bottom: 100px;
        min-height: 100vh;
    }}

    .marquee {{
        background: #fff7e6;
        color: #cc6600;
        font-weight: bold;
        font-size: 1.2rem;
        padding: 10px;
        border-radius: 8px;
        margin: 10px auto 30px auto;
        overflow: hidden;
        max-width: 90%;
        white-space: nowrap;
        position: relative;
        height: 2rem;
    }}

    .marquee span {{
        display: inline-block;
        padding-left: 100%;
        animation: scroll-left 12s linear infinite;
    }}

    .explore-btn {{
        background: #138808 !important;
        color: white !important;
        border: 3px solid #FF9933 !important;
        padding: 0.6rem 2rem !important;
        border-radius: 30px;
        font-size: 1.2rem;
        margin: 2rem auto 1rem auto;
        display: block;
        animation: pulse 2.5s ease-in-out infinite;
        transition: transform 0.3s ease;
    }}

    .explore-btn:hover {{
        transform: scale(1.08);
    }}

    .footer-img {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        z-index: -1;
    }}

    h1 {{
        text-align: center;
        font-weight: bold;
        color: #000000;
        margin-top: 1.5rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(50, 50, 50, 0.2) !important;
        backdrop-filter: blur(5px);
    }}

    .date-text {{
        text-align: center;
        color: #0b3d0b;
        font-weight: 600;
        font-size: 16px;
        margin-top: 30px;
        margin-bottom: 10px;
    }}

    .date-inputs {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 15px;
    }}

    .date-inputs > div {{
        width: 150px;
    }}

    .submit-btn-container {{
        text-align: center;
        margin-bottom: 20px;
    }}
    </style>

    <div class="footer-img">
        <img src="{banner_url}" style="width:100%;">
    </div>
    """, unsafe_allow_html=True)


# ---- Home Page ----
def home_page():
    inject_style()

    st.markdown("<h1>MapMy Kulture</h1>", unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="marquee">
            <span>Discover Indian Tourism, Traditional Food, Handicrafts & Colorful Festivals – Experience the Heart of India!</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if st.button("Discover India →", key="explore", help="Explore India"):
        st.session_state.page = "main"
        st.rerun()

    st.markdown('<div class="date-text">Pick your dates to know what\'s going on in India</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today(), key="start_date")
    with col2:
        end_date = st.date_input("End Date", value=date.today(), key="end_date")

    st.markdown('<div class="submit-btn-container">', unsafe_allow_html=True)
    if st.button("Submit Dates →", key="submit_dates"):
        st.session_state.page = "events"
        st.session_state.start = start_date
        st.session_state.end = end_date
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ---- Main Page ----
def main_page():
    inject_style()

    st.markdown("### Welcome to Incredible India")
    st.write("Discover the heart of India — from breathtaking landscapes to flavorful cuisines, traditional crafts, and spectacular festivals. Stay connected to every corner of the nation, one state at a time.")

    st.sidebar.title("Explore India")
    states = ["Rajasthan", "Kerala", "Goa", "Himachal Pradesh", "Tamil Nadu"]
    selected_state = st.sidebar.selectbox("Choose State", states)

    st.header(f"Discover {selected_state}")
    tabs = st.tabs(["Tourism", "Cuisine", "Handicrafts", "Festivals", "Govt Schemes"])

    with tabs[0]:
        st.subheader("Top Attractions")
        st.write(f"Explore {selected_state}'s famous landmarks...")

    with tabs[1]:
        st.subheader("Local Food")
        st.write(f"Taste {selected_state}'s signature dishes...")

    with tabs[2]:
        st.subheader("Traditional Crafts")
        st.write(f"Discover {selected_state}'s artisanal heritage...")

    with tabs[3]:
        st.subheader("Cultural Festivals")
        st.write(f"Experience {selected_state}'s vibrant celebrations...")

    with tabs[4]:
        st.subheader("Government Schemes")
        st.write(f"Learn about welfare and development schemes in {selected_state}...")

    if st.sidebar.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---- Events Page ----
def events_page():
    inject_style()

    st.markdown("### Upcoming Events in India")
    st.write(f"Showing events between **{st.session_state.get('start')}** and **{st.session_state.get('end')}**:")

    sample_events = [
        {"state": "Rajasthan", "event": "Desert Festival", "date": "2025-02-14"},
        {"state": "Goa", "event": "Goa Carnival", "date": "2025-03-01"},
        {"state": "Punjab", "event": "Baisakhi", "date": "2025-04-13"},
        {"state": "Kerala", "event": "Onam", "date": "2025-08-28"},
    ]

    for event in sample_events:
        st.markdown(f"**{event['event']}** in *{event['state']}* — {event['date']}")

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---- Page Routing ----
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "main":
    main_page()
elif st.session_state.page == "events":
    events_page()
