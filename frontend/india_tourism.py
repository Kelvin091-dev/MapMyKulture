import streamlit as st
import folium
from streamlit_folium import folium_static

# ---- Page Configuration ----
st.set_page_config(
    page_title="MapMy Kulture",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- State Data ----
STATE_DATA = {
    "Rajasthan": {
        "description": "The Land of Kings, where desert sands whisper tales of valor and vibrant hues dance in palace corridors.",
        "heritage": [
            {"name": "Amber Fort", "lat": 26.9855, "lon": 75.8513,
             "image": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Amer_Fort_%28Amber_Fort%29.jpg",
             "desc": "Majestic hilltop fortress with intricate mirror work"},
            {"name": "Stepwells of Abhaneri", "lat": 27.0074, "lon": 76.6076,
             "image": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Stepwell_Abhaneri.jpg",
             "desc": "Ancient architectural marvel for water conservation"}
        ],
        "festivals": [
            {"name": "Pushkar Camel Fair", "lat": 26.4897, "lon": 74.5517,
             "image": "https://upload.wikimedia.org/wikipedia/commons/4/49/Pushkar_Cattle_Fair_2009.jpg",
             "desc": "Vibrant desert carnival with camel races"},
            {"name": "Desert Festival", "lat": 26.9124, "lon": 70.9122,
             "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Jaisalmer_Desert_Festival_2018.jpg",
             "desc": "Cultural extravaganza under golden sands"}
        ],
        "foods": [
            {"name": "Dal Baati Churma",
             "image": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Dal_Bati_Churma.jpg",
             "desc": "Traditional meal served in brass utensils"},
            {"name": "Ghevar",
             "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Ghevar.jpg",
             "desc": "Honeycomb-shaped sweet delicacy"}
        ],
        "artifacts": [
            {"name": "Blue Pottery",
             "image": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Blue_Pottery_Jaipur.jpg",
             "desc": "Turquoise-hued ceramic art with Persian influences"},
            {"name": "Bandhani Sarees",
             "image": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Bandhani_saree.jpg",
             "desc": "Traditional tie-dye textile art"}
        ]
    },
    "Kerala": {
        "description": "God's Own Country, where emerald backwaters meet spice-scented hills and ancient traditions.",
        "heritage": [
            {"name": "Padmanabhapuram Palace", "lat": 8.2443, "lon": 77.3258,
             "image": "https://upload.wikimedia.org/wikipedia/commons/0/06/Padmanabhapuram_Palace_%2836%29.jpg",
             "desc": "Wooden architectural masterpiece"},
            {"name": "Bekal Fort", "lat": 12.3895, "lon": 75.0308,
             "image": "https://upload.wikimedia.org/wikipedia/commons/3/34/Bekal_Fort.jpg",
             "desc": "Seaside fortress with panoramic views"}
        ],
        "festivals": [
            {"name": "Onam", "lat": 10.8505, "lon": 76.2711,
             "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Onam_Sadya.jpg",
             "desc": "Harvest festival with floral carpets"},
            {"name": "Vishu", "lat": 9.9816, "lon": 76.2999,
             "image": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Vishu_kani.jpg",
             "desc": "New Year festival with ceremonial viewing"}
        ],
        "foods": [
            {"name": "Sadya",
             "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Onam_Sadya.jpg",
             "desc": "Grand vegetarian feast on banana leaf"},
            {"name": "Karimeen Pollichathu",
             "image": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Karimeen_Pollichathu.jpg",
             "desc": "Pearl spot fish cooked in banana leaf"}
        ],
        "artifacts": [
            {"name": "Kathakali Masks",
             "image": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Kathakali_BNC.jpg",
             "desc": "Traditional dance-drama face art"},
            {"name": "Coir Crafts",
             "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Coir_products.jpg",
             "desc": "Eco-friendly coconut fiber creations"}
        ]
    }
}

# ---- Enhanced Styles ----
def inject_style():
    banner_url = "https://t4.ftcdn.net/jpg/11/02/86/89/360_F_1102868968_To7xQ8HffJwpKD6rz6LogPeAWmJeOWfX.jpg"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,165,0,0.2), rgba(255,255,255,0.3)),
                    url('{banner_url}');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Palatino Linotype', 'Book Antiqua', serif;
    }}
    .card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        backdrop-filter: blur(5px);
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    .section-title {{
        color: #d35400;
        border-left: 5px solid #e67e22;
        padding-left: 15px;
        margin: 30px 0 20px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
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
    h1 {{
        color: #c0392b !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- Home Page ----
def home_page():
    inject_style()
    st.markdown("<h1 style='text-align:center;'>MapMy Kulture</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#16a085;'>Discover India's Cultural Tapestry</h4>", unsafe_allow_html=True)

    # Centered button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🌿 Responsible Tourism Guide", key="responsible_tourism_btn"):
            st.session_state.page = "responsible_tourism_guide"
            st.rerun()

    # State selection
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        selected_state = st.selectbox("Select a State to Explore", list(STATE_DATA.keys()))
        if st.button("🗺️ Show on Map"):
            st.session_state.page = "state_map"
            st.session_state.selected_state = selected_state
            st.rerun()
# ---- State Map Page ----
def state_map_page():
    inject_style()
    selected_state = st.session_state.selected_state
    data = STATE_DATA[selected_state]
    
    st.markdown(f"<h2 style='color:#c0392b;'>{selected_state} Cultural Map</h2>", unsafe_allow_html=True)
    
    m = folium.Map(location=[data['heritage'][0]['lat'], data['heritage'][0]['lon']], zoom_start=7)
    
    # Heritage Markers
    for site in data["heritage"]:
        folium.Marker(
            location=[site["lat"], site["lon"]],
            tooltip=folium.Tooltip(
                f"<b>🏰 {site['name']}</b>",
                sticky=True,
                permanent=False
            ),
            icon=folium.Icon(color="beige", icon="university", prefix="fa")
        ).add_to(m)
    
    # Festival Markers
    for festival in data["festivals"]:
        folium.Marker(
            location=[festival["lat"], festival["lon"]],
            tooltip=folium.Tooltip(
                f"<b>🎉 {festival['name']}</b>",
                sticky=True,
                permanent=False
            ),
            icon=folium.Icon(color="orange", icon="music", prefix="fa")
        ).add_to(m)

    with st.container():
        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        folium_static(m, width=1000, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,4])
    with col1:
        if st.button("← Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Explore Cultural Details →"):
            st.session_state.page = "state_description"
            st.rerun()

# ---- State Description Page ----
def state_description_page():
    inject_style()
    selected_state = st.session_state.selected_state
    data = STATE_DATA[selected_state]
    
    st.markdown(f"<h1 style='color:#c0392b; text-align:center;'>{selected_state} Cultural Odyssey</h1>", unsafe_allow_html=True)
    
    # State Intro
    with st.container():
        st.markdown(f"<div class='card'><h3 style='color:#16a085;'>🌄 Land of Wonders</h3><h4>{data['description']}</h4></div>", unsafe_allow_html=True)
    
    # Main Content Columns
    col1, col2 = st.columns([1,1])
    
    with col1:
        # Heritage Section
        with st.expander("🏛️ Hidden Heritage Gems", expanded=True):
            for site in data["heritage"]:
                st.markdown(f"""
                <div class='card'>
                    <h4>{site['name']}</h4>
                    <img src="{site['image']}" class='culture-img' width="100%">
                    <p>{site['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        # Artifacts Section
        st.markdown("<h2 class='section-title'>🛍️ Artisan Treasures</h2>", unsafe_allow_html=True)
        for artifact in data["artifacts"]:
            st.markdown(f"""
            <div class='card'>
                <h4>🎨 {artifact['name']}</h4>
                <img src="{artifact['image']}" class='culture-img' width="100%">
                <p>{artifact['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Festivals Section
        with st.expander("🎭 Cultural Extravaganza", expanded=True):
            for festival in data["festivals"]:
                st.markdown(f"""
                <div class='card'>
                    <h4>{festival['name']}</h4>
                    <img src="{festival['image']}" class='culture-img' width="100%">
                    <p>{festival['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Foods Section
        st.markdown("<h2 class='section-title'>🍴 Culinary Treasures</h2>", unsafe_allow_html=True)
        for food in data["foods"]:
            st.markdown(f"""
            <div class='card'>
                <h4>🥘 {food['name']}</h4>
                <img src="{food['image']}" class='culture-img' width="100%">
                <p>{food['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1,4])
    with c1:
        if st.button("🗺️ Back to Map"):
            st.session_state.page = "state_map"
            st.rerun()
    with c2:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.rerun()

# ---- Responsible Tourism Guide ----
def responsible_tourism_guide_page():
    inject_style()
    st.markdown("<h1 style='color:#c0392b; text-align:center;'>🌱 Responsible Tourism Guide</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3 style='color:#16a085;'>Travel with Respect</h3>
            <div class='columns'>
                <div class='column'>
                    <h4>🛑 Do's</h4>
                    <ul>
                        <li>Respect local customs and dress codes</li>
                        <li>Support local artisans and businesses</li>
                        <li>Use eco-friendly transportation</li>
                        <li>Preserve historical sites</li>
                    </ul>
                </div>
                <div class='column'>
                    <h4>🚫 Don'ts</h4>
                    <ul>
                        <li>Avoid single-use plastics</li>
                        <li>Don't disturb wildlife</li>
                        <li>Never remove artifacts</li>
                        <li>Avoid over-tourism spots</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---- Main App ----
if "page" not in st.session_state:
    st.session_state.page = "home"

pages = {
    "home": home_page,
    "state_map": state_map_page,
    "state_description": state_description_page,
    "responsible_tourism_guide": responsible_tourism_guide_page
}

pages[st.session_state.page]()