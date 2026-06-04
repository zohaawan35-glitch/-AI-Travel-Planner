import streamlit as st
from groq import Groq

# ---------------- Page Config ---------------- #
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ---------------- Custom CSS ---------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hero Header */
.hero {
    text-align: center;
    padding: 40px 20px 20px;
}
.hero h1 {
    font-size: 3.5rem;
    background: linear-gradient(90deg, #f7971e, #ffd200, #f7971e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.hero p {
    color: #a0aec0;
    font-size: 1.1rem;
}

/* Place Card */
.place-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 16px;
    transition: transform 0.2s;
}
.place-card:hover { transform: translateY(-4px); }
.place-card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
}
.place-card-body {
    padding: 12px 14px;
}
.place-card-body h4 {
    color: #ffd200;
    margin: 0 0 4px 0;
    font-size: 1rem;
    font-family: 'Playfair Display', serif;
}
.place-card-body p {
    color: #cbd5e0;
    font-size: 0.82rem;
    margin: 0;
}

/* Day Card */
.day-card {
    background: rgba(255,255,255,0.06);
    border-left: 4px solid #ffd200;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.day-card h3 {
    color: #ffd200;
    margin: 0 0 8px 0;
    font-size: 1.1rem;
}
.day-card p {
    color: #e2e8f0;
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #a0aec0 !important;
    border-radius: 8px;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #f7971e, #ffd200) !important;
    color: #1a1a2e !important;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #f7971e, #ffd200);
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-size: 1rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

/* Selectbox / Textbox / Slider labels */
label, .stSlider label {
    color: #e2e8f0 !important;
    font-weight: 500;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: #fff !important;
}
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: #fff !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.1); }

/* Section headers */
.section-title {
    color: #ffd200;
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    margin: 20px 0 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- AI Client ---------------- #
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# ---------------- Static Places ---------------- #
country_places = {
    "United States": [
        {"name": "New York City", "desc": "Times Square, Statue of Liberty, and skyscrapers.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg/330px-View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg"},
        {"name": "Los Angeles", "desc": "Famous for Hollywood, beaches, and entertainment.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Los_Angeles_with_Mount_Baldy.jpg/330px-Los_Angeles_with_Mount_Baldy.jpg"},
        {"name": "Las Vegas", "desc": "City of casinos, nightlife, and mega shows.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/WorldMarketCenter1.jpg/250px-WorldMarketCenter1.jpg"},
        {"name": "San Francisco", "desc": "Famous for Golden Gate Bridge and tech culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/San_Francisco%2C_CA_USA_-_Mission_San_Francisco_de_Asis_%281776%29_and_Mission_Dolores_Basilica_%281918%29_-_panoramio_%285%29.jpg/250px-San_Francisco%2C_CA_USA_-_Mission_San_Francisco_de_Asis_%281776%29_and_Mission_Dolores_Basilica_%281918%29_-_panoramio_%285%29.jpg"},
        {"name": "Chicago", "desc": "Architecture, museums, and deep-dish pizza.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Navy_Pier_NW.jpg/250px-Navy_Pier_NW.jpg"}
    ],
    "Canada": [
        {"name": "Toronto", "desc": "Known for CN Tower and multicultural life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Scarborough_bluffs_-b.jpg/250px-Scarborough_bluffs_-b.jpg"},
        {"name": "Vancouver", "desc": "Mountains, beaches, and modern architecture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Vancouver_Art_Gallery_%2846588958915%29.jpg/250px-Vancouver_Art_Gallery_%2846588958915%29.jpg"},
        {"name": "Montreal", "desc": "French culture, festivals, and heritage.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Montreal_NDame1_tango7174.jpg/120px-Montreal_NDame1_tango7174.jpg"},
        {"name": "Banff", "desc": "National park with lakes and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Town_of_Banff_viewed_from_Sulphur_Mountain.jpg/250px-Town_of_Banff_viewed_from_Sulphur_Mountain.jpg"},
        {"name": "Quebec City", "desc": "Historic old town with European feel.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Place_Royale_at_night%2C_Vieux-Qu%C3%A9bec%2C_Quebec_ville%2C_Canada.jpg/250px-Place_Royale_at_night%2C_Vieux-Qu%C3%A9bec%2C_Quebec_ville%2C_Canada.jpg"}
    ],
    "United Kingdom": [
        {"name": "London", "desc": "Big Ben, museums, and royal palaces.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/London_Skyline_%28125508655%29.jpeg/330px-London_Skyline_%28125508655%29.jpeg"},
        {"name": "Edinburgh", "desc": "Edinburgh Castle and old town.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Skyline_of_Edinburgh.jpg/330px-Skyline_of_Edinburgh.jpg"},
        {"name": "Manchester", "desc": "Known for football and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Manchester_Cathedral_-_Aerial_-_2024-06-16_01.jpg/250px-Manchester_Cathedral_-_Aerial_-_2024-06-16_01.jpg"},
        {"name": "Liverpool", "desc": "Birthplace of The Beatles and port city.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Pier_Head%2C_Liverpool_-_geograph.org.uk_-_3059094.jpg/330px-Pier_Head%2C_Liverpool_-_geograph.org.uk_-_3059094.jpg"},
        {"name": "Birmingham", "desc": "Canals, museums, and shopping.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Selfridges_Birmingham_from_Park_Street_car_park.jpg/250px-Selfridges_Birmingham_from_Park_Street_car_park.jpg"}
    ],
    "Pakistan": [
        {"name": "Lahore", "desc": "Historic forts and food.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Lahore_Fort_view_from_Baradari.jpg/330px-Lahore_Fort_view_from_Baradari.jpg"},
        {"name": "Karachi", "desc": "Beaches and city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Dolmen_Towers_Karachi.jpg/330px-Dolmen_Towers_Karachi.jpg"},
        {"name": "Islamabad", "desc": "Mountains and modern architecture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Faisal_Mosque%2C_Islamabad_III.jpg/330px-Faisal_Mosque%2C_Islamabad_III.jpg"},
        {"name": "Hunza", "desc": "Valleys and scenic nature.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Rakaposhi%2C_Nagar_GB_%28Pakistan%29.jpg/330px-Rakaposhi%2C_Nagar_GB_%28Pakistan%29.jpg"},
        {"name": "Skardu", "desc": "Mountains and lakes.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Shangrila_resort_skardu.jpg/330px-Shangrila_resort_skardu.jpg"}
    ],
    "UAE": [
        {"name": "Dubai", "desc": "Skyscrapers, malls, and luxury lifestyle.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Artificial_Archipelagos%2C_Dubai%2C_United_Arab_Emirates_ISS022-E-024940_lrg.jpg/250px-Artificial_Archipelagos%2C_Dubai%2C_United_Arab_Emirates_ISS022-E-024940_lrg.jpg"},
        {"name": "Abu Dhabi", "desc": "Sheikh Zayed Mosque and cultural spots.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Abu_dhabi_skylines_2014.jpg/330px-Abu_dhabi_skylines_2014.jpg"},
        {"name": "Sharjah", "desc": "Museums and family attractions.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Al_Khan_Lagoon_by_Night.jpg/330px-Al_Khan_Lagoon_by_Night.jpg"},
        {"name": "Ras Al Khaimah", "desc": "Mountains and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Aerial_view_of_RAK_City_from_Al_Qawasim_Corniche_flagpole.jpg/330px-Aerial_view_of_RAK_City_from_Al_Qawasim_Corniche_flagpole.jpg"},
        {"name": "Fujairah", "desc": "Beaches and historic forts.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Al_Bithnah_Fort%2C_Fujairah%2C_UAE.jpg/250px-Al_Bithnah_Fort%2C_Fujairah%2C_UAE.jpg"}
    ],
    "Saudi Arabia": [
        {"name": "Riyadh", "desc": "Modern skyline and museums.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Riyadh_Skyline.jpg/330px-Riyadh_Skyline.jpg"},
        {"name": "Jeddah", "desc": "Coastal city with Corniche.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Jeddah_Waterfront_2025_%28cropped%29.jpg/330px-Jeddah_Waterfront_2025_%28cropped%29.jpg"},
        {"name": "Medina", "desc": "Islamic holy sites.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Al-Masjid_An-Nabawi_%28Bird%27s_Eye_View%29.jpg/330px-Al-Masjid_An-Nabawi_%28Bird%27s_Eye_View%29.jpg"},
        {"name": "Mecca", "desc": "Holiness and pilgrimage site.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/The_Kabah_in_the_Grand_Mosque_of_Makkah%2C_Saudi_Arabia_%2852501405646%29.jpg/120px-The_Kabah_in_the_Grand_Mosque_of_Makkah%2C_Saudi_Arabia_%2852501405646%29.jpg"},
        {"name": "Al Ula", "desc": "Ancient Nabatean rock tombs.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Al_Ula_%286748577917%29.jpg/330px-Al_Ula_%286748577917%29.jpg"}
    ],
    "Japan": [
        {"name": "Tokyo", "desc": "Modern city with culture and food.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Skyscrapers_of_Shinjuku_2009_January.jpg/330px-Skyscrapers_of_Shinjuku_2009_January.jpg"},
        {"name": "Kyoto", "desc": "Temples, gardens, and traditions.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Kinkaku3402CBcropped.jpg/250px-Kinkaku3402CBcropped.jpg"},
        {"name": "Osaka", "desc": "Street food and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Osaka_Castle_03bs3200.jpg/330px-Osaka_Castle_03bs3200.jpg"},
        {"name": "Hokkaido", "desc": "Snow festivals and nature.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Satellite_image_of_Hokkaido%2C_Japan_in_May_2001.jpg/250px-Satellite_image_of_Hokkaido%2C_Japan_in_May_2001.jpg"},
        {"name": "Nara", "desc": "Temples and friendly deer park.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/T%C5%8Ddai-ji_Kon-d%C5%8D.jpg/330px-T%C5%8Ddai-ji_Kon-d%C5%8D.jpg"}
    ],
    "India": [
        {"name": "Delhi", "desc": "Historic sites and markets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Tomb_of_Humayun%2C_Delhi.jpg/250px-Tomb_of_Humayun%2C_Delhi.jpg"},
        {"name": "Mumbai", "desc": "Bollywood and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/%E0%A6%93%E0%A6%B0%E0%A6%B2%E0%A6%BF%E0%A6%B0_%E0%A6%97%E0%A6%97%E0%A6%A8%E0%A6%B0%E0%A7%88%E0%A6%96%E0%A6%BF%E0%A6%95_%E0%A6%A6%E0%A7%83%E0%A6%B6%E0%A7%8D%E0%A6%AF.jpg/330px-%E0%A6%93%E0%A6%B0%E0%A6%B2%E0%A6%BF%E0%A6%B0_%E0%A6%97%E0%A6%97%E0%A6%A8%E0%A6%B0%E0%A7%88%E0%A6%96%E0%A6%BF%E0%A6%95_%E0%A6%A6%E0%A7%83%E0%A6%B6%E0%A7%8D%E0%A6%AF.jpg"},
        {"name": "Jaipur", "desc": "Palaces and forts.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg/330px-East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg"},
        {"name": "Goa", "desc": "Beaches and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/BeachFun.jpg/330px-BeachFun.jpg"},
        {"name": "Agra", "desc": "Home of the Taj Mahal.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Taj_Mahal%2C_Agra%2C_India.jpg/330px-Taj_Mahal%2C_Agra%2C_India.jpg"}
    ],
    "Turkey": [
        {"name": "Istanbul", "desc": "Historic mosques, bazaars, and Bosphorus views.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Historical_peninsula_and_modern_skyline_of_Istanbul.jpg/330px-Historical_peninsula_and_modern_skyline_of_Istanbul.jpg"},
        {"name": "Cappadocia", "desc": "Rock formations and hot air balloons.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Cappadocia_balloon_trip%2C_Ortahisar_Castle_%2811893715185%29.jpg/330px-Cappadocia_balloon_trip%2C_Ortahisar_Castle_%2811893715185%29.jpg"},
        {"name": "Antalya", "desc": "Resorts, beaches, and ancient ruins.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Falezlerden_Antalya_Konyaalt%C4%B1_Plaj%C4%B1na_do%C4%9Fru_bir_g%C3%B6r%C3%BCn%C3%BCm.jpg/330px-Falezlerden_Antalya_Konyaalt%C4%B1_Plaj%C4%B1na_do%C4%9Fru_bir_g%C3%B6r%C3%BCn%C3%BCm.jpg"},
        {"name": "Ankara", "desc": "Capital city with museums.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/ANKARA_KOCATEPE_CAM%C4%B0%C4%B0.jpg/250px-ANKARA_KOCATEPE_CAM%C4%B0%C4%B0.jpg"},
        {"name": "Izmir", "desc": "Coastal city with markets and history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bayrakl%C4%B1_Sahil.jpg/330px-Bayrakl%C4%B1_Sahil.jpg"}
    ],
    "France": [
        {"name": "Paris", "desc": "Eiffel Tower, Louvre, romantic streets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/330px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg"},
        {"name": "Nice", "desc": "Mediterranean beaches and old town.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Promenade_des_Anglais_Nice_IMG_1255.jpg/250px-Promenade_des_Anglais_Nice_IMG_1255.jpg"},
        {"name": "Lyon", "desc": "Known for food and Roman history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Lyon-part-dieu-2023.jpg/330px-Lyon-part-dieu-2023.jpg"},
        {"name": "Marseille", "desc": "Port city with coastal views.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Notre-Dame_de_la_Garde_aerial_view_2020.jpeg/330px-Notre-Dame_de_la_Garde_aerial_view_2020.jpeg"},
        {"name": "Bordeaux", "desc": "Wine region with historic charm.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Bordeaux_Place_de_la_Bourse_de_nuit.jpg/330px-Bordeaux_Place_de_la_Bourse_de_nuit.jpg"}
    ],
    "Australia": [
        {"name": "Sydney", "desc": "Opera House and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019-06-21.jpg/330px-Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019-06-21.jpg"},
        {"name": "Melbourne", "desc": "Culture, food, and sports.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Melburnian_Skyline_b.jpg/330px-Melburnian_Skyline_b.jpg"},
        {"name": "Brisbane", "desc": "Riverside city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Brisbane_CBD_seen_from_Kangaroo_Point%2C_2024%2C_01_%282%29.jpg/330px-Brisbane_CBD_seen_from_Kangaroo_Point%2C_2024%2C_01_%282%29.jpg"},
        {"name": "Perth", "desc": "Beaches and sunny weather.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Perth_CBD_skyline_from_State_War_Memorial_Lookout%2C_2023%2C_04_b.jpg/330px-Perth_CBD_skyline_from_State_War_Memorial_Lookout%2C_2023%2C_04_b.jpg"},
        {"name": "Gold Coast", "desc": "Waves, beaches, and theme parks.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Gold_Coast_skyline_%28Unsplash%29.jpg/330px-Gold_Coast_skyline_%28Unsplash%29.jpg"}
    ],
    "Thailand": [
        {"name": "Bangkok", "desc": "Temples, markets, nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Bangkok_Montage_2024_2.jpg/250px-Bangkok_Montage_2024_2.jpg"},
        {"name": "Phuket", "desc": "Beaches and islands.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Phuket_Aerial.jpg/250px-Phuket_Aerial.jpg"},
        {"name": "Chiang Mai", "desc": "Culture and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/0020-%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%AA%E0%B8%B4%E0%B8%87%E0%B8%AB%E0%B9%8C%E0%B8%A7%E0%B8%A3%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%A7%E0%B8%B4%E0%B8%AB%E0%B8%B2%E0%B8%A3.jpg/250px-0020-%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%AA%E0%B8%B4%E0%B8%87%E0%B8%AB%E0%B9%8C%E0%B8%A7%E0%B8%A3%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%A7%E0%B8%B4%E0%B8%AB%E0%B8%B2%E0%B8%A3.jpg"},
        {"name": "Pattaya", "desc": "Beaches and entertainment.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Pattaya_beach_from_view_point.jpg/250px-Pattaya_beach_from_view_point.jpg"},
        {"name": "Krabi", "desc": "Cliffs, beaches, islands.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Wat_Tham_Sua_18.jpg/250px-Wat_Tham_Sua_18.jpg"}
    ],
}

# ---------------- Helper Functions ---------------- #
def render_places_grid(country):
    places = country_places[country]
    cols = st.columns(len(places))
    for i, place in enumerate(places):
        with cols[i]:
            st.markdown(f"""
            <div class="place-card">
                <img src="{place['img']}" alt="{place['name']}"/>
                <div class="place-card-body">
                    <h4>{place['name']}</h4>
                    <p>{place['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_trip_plan(ai_text):
    days = ai_text.split("Day ")
    for d in days:
        if not d.strip():
            continue
        parts = d.split(":", 1)
        day_title = parts[0].strip()
        activities = parts[1].strip().replace("\n", "<br>") if len(parts) > 1 else ""
        st.markdown(f"""
        <div class="day-card">
            <h3>🗓️ Day {day_title}</h3>
            <p>{activities}</p>
        </div>
        """, unsafe_allow_html=True)

def generate_trip(country, days):
    places = [p["name"] for p in country_places[country]]
    prompt = f"""
Create a {days}-day trip plan for {country}.
Include:
- Daily schedule
- Best tourist places from: {places}
- Transport routes and timings
- Hotels to stay each day
- Travel tips
Return as plain text in Day-wise format starting each day with "Day 1:", "Day 2:", etc.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_custom_trip(country_name, places_str, days):
    places = [p.strip() for p in places_str.split(",") if p.strip()]
    prompt = f"""
Create a {days}-day trip plan for {country_name}.
Include only these places: {places}.
Include transport routes, hotels, and travel tips.
Return as plain text in Day-wise format starting each day with "Day 1:", "Day 2:", etc.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---------------- UI ---------------- #
st.markdown("""
<div class="hero">
    <h1>🌍 AI Travel Planner</h1>
    <p>Discover the world with personalized AI-powered itineraries</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🗺️ Pre-defined Countries", "✏️ Custom Trip"])

# ---- Tab 1: Pre-defined ---- #
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        country = st.selectbox("Select a Country", list(country_places.keys()), key="country_select")
    with col2:
        days = st.slider("Number of Days", 1, 30, 5, key="days_slider")

    if st.button("🏙️ Show Tourist Places", key="show_places"):
        st.markdown('<p class="section-title">Top Places to Visit</p>', unsafe_allow_html=True)
        render_places_grid(country)

    st.markdown("")
    if st.button("🤖 Generate AI Trip Plan", key="gen_trip"):
        with st.spinner("✈️ Planning your trip..."):
            try:
                result = generate_trip(country, days)
                st.markdown('<p class="section-title">Your Personalized Itinerary</p>', unsafe_allow_html=True)
                render_trip_plan(result)
            except Exception as e:
                st.error(f"Error: {e}")

# ---- Tab 2: Custom Trip ---- #
with tab2:
    col1, col2 = st.columns([2, 1])
    with col1:
        custom_country = st.text_input("Enter Country Name", placeholder="e.g. Morocco")
    with col2:
        custom_days = st.slider("Number of Days", 1, 30, 5, key="custom_days_slider")

    custom_places = st.text_input(
        "Enter Places (comma separated)",
        placeholder="e.g. Marrakech, Fes, Casablanca"
    )

    if st.button("🤖 Generate Custom Trip Plan", key="gen_custom"):
        if not custom_country or not custom_places:
            st.warning("Please enter both country name and places.")
        else:
            with st.spinner("✈️ Planning your custom trip..."):
                try:
                    result = generate_custom_trip(custom_country, custom_places, custom_days)
                    st.markdown('<p class="section-title">Your Custom Itinerary</p>', unsafe_allow_html=True)
                    render_trip_plan(result)
                except Exception as e:
                    st.error(f"Error: {e}")
