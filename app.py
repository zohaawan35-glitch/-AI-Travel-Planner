import os
import gradio as gr
from groq import Groq

# ---------------- AI Client ---------------- #
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# ---------------- Static Places ---------------- #
country_places = {
    
  "United States": [
    {"name": "New York City", "desc": "Known for Times Square, Statue of Liberty, and skyscrapers.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg/330px-View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg"},
    {"name": "Los Angeles", "desc": "Famous for Hollywood, beaches, and entertainment.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Los_Angeles_with_Mount_Baldy.jpg/330px-Los_Angeles_with_Mount_Baldy.jpg"},
    {"name": "Las Vegas", "desc": "City of casinos, nightlife, and mega shows.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/WorldMarketCenter1.jpg/250px-WorldMarketCenter1.jpg"},
    {"name": "San Francisco", "desc": "Famous for Golden Gate Bridge and tech culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/San_Francisco%2C_CA_USA_-_Mission_San_Francisco_de_Asis_%281776%29_and_Mission_Dolores_Basilica_%281918%29_-_panoramio_%285%29.jpg/250px-San_Francisco%2C_CA_USA_-_Mission_San_Francisco_de_Asis_%281776%29_and_Mission_Dolores_Basilica_%281918%29_-_panoramio_%285%29.jpg"},
    {"name": "Chicago", "desc": "Known for architecture, museums, and deep-dish pizza.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Navy_Pier_NW.jpg/250px-Navy_Pier_NW.jpg"}
  ],

  "Canada": [
    {"name": "Toronto", "desc": "Known for CN Tower and multicultural life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Scarborough_bluffs_-b.jpg/250px-Scarborough_bluffs_-b.jpg"},
    {"name": "Vancouver", "desc": "Mountains, beaches, and modern architecture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Vancouver_Art_Gallery_%2846588958915%29.jpg/250px-Vancouver_Art_Gallery_%2846588958915%29.jpg"},
    {"name": "Montreal", "desc": "French culture, festivals, and heritage.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Montreal_NDame1_tango7174.jpg/120px-Montreal_NDame1_tango7174.jpg"},
    {"name": "Banff", "desc": "National park with lakes and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Town_of_Banff_viewed_from_Sulphur_Mountain.jpg/250px-Town_of_Banff_viewed_from_Sulphur_Mountain.jpg"},
    {"name": "Quebec City", "desc": "Historic old town with European feel.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Place_Royale_at_night%2C_Vieux-Qu%C3%A9bec%2C_Quebec_ville%2C_Canada.jpg/250px-Place_Royale_at_night%2C_Vieux-Qu%C3%A9bec%2C_Quebec_ville%2C_Canada.jpg"}
  ],

  "United Kingdom": [
    {"name": "London", "desc": "Home to Big Ben, museums, and royal palaces.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/London_Skyline_%28125508655%29.jpeg/330px-London_Skyline_%28125508655%29.jpeg"},
    {"name": "Edinburgh", "desc": "Famous for Edinburgh Castle and old town.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Skyline_of_Edinburgh.jpg/330px-Skyline_of_Edinburgh.jpg"},
    {"name": "Manchester", "desc": "Known for football and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Manchester_Cathedral_-_Aerial_-_2024-06-16_01.jpg/250px-Manchester_Cathedral_-_Aerial_-_2024-06-16_01.jpg"},
    {"name": "Liverpool", "desc": "Birthplace of The Beatles and port city.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Pier_Head%2C_Liverpool_-_geograph.org.uk_-_3059094.jpg/330px-Pier_Head%2C_Liverpool_-_geograph.org.uk_-_3059094.jpg"},
    {"name": "Birmingham", "desc": "Known for canals, museums, and shopping.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Selfridges_Birmingham_from_Park_Street_car_park.jpg/250px-Selfridges_Birmingham_from_Park_Street_car_park.jpg"}
  ],

  "Germany": [
    {"name": "Berlin", "desc": "Historic city known for the Wall and museums.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Panorama_Gendarmenmarkt-Berlin-Huntke-2008.jpg/330px-Panorama_Gendarmenmarkt-Berlin-Huntke-2008.jpg"},
    {"name": "Munich", "desc": "Oktoberfest and Bavarian culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Stadtbild_M%C3%BCnchen.jpg/250px-Stadtbild_M%C3%BCnchen.jpg"},
    {"name": "Hamburg", "desc": "Port city with nightlife and lakes.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/HamburgSpeicherstadt.jpg/250px-HamburgSpeicherstadt.jpg"},
    {"name": "Frankfurt", "desc": "Financial hub with modern skyline.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Europ%C3%A4ische_Zentralbank_-_European_Central_Bank_%2819190136328%29_%28cropped%29.jpg/120px-Europ%C3%A4ische_Zentralbank_-_European_Central_Bank_%2819190136328%29_%28cropped%29.jpg"},
    {"name": "Cologne", "desc": "Famous for the Cologne Cathedral.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Kranh%C3%A4user_Cologne%2C_April_2018_-01.jpg/330px-Kranh%C3%A4user_Cologne%2C_April_2018_-01.jpg"}
  ],

  "France": [
    {"name": "Paris", "desc": "Eiffel Tower, Louvre, romantic streets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg/330px-La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg"},
    {"name": "Nice", "desc": "Mediterranean beaches and old town.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Promenade_des_Anglais_Nice_IMG_1255.jpg/250px-Promenade_des_Anglais_Nice_IMG_1255.jpg"},
    {"name": "Lyon", "desc": "Known for food and Roman history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Lyon-part-dieu-2023.jpg/330px-Lyon-part-dieu-2023.jpg"},
    {"name": "Marseille", "desc": "Port city with coastal views.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Notre-Dame_de_la_Garde_aerial_view_2020.jpeg/330px-Notre-Dame_de_la_Garde_aerial_view_2020.jpeg"},
    {"name": "Bordeaux", "desc": "Wine region with historic charm.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Bordeaux_Place_de_la_Bourse_de_nuit.jpg/330px-Bordeaux_Place_de_la_Bourse_de_nuit.jpg"}
  ],

  "Spain": [
    {"name": "Barcelona", "desc": "Architecture, beaches, and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Torre_Gl%C3%B2ries_nocturna.jpg/120px-Torre_Gl%C3%B2ries_nocturna.jpg"},
    {"name": "Madrid", "desc": "Capital city with museums and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Plaza_Mayor_De_Madrid_%28215862629%29_edited.jpeg/250px-Plaza_Mayor_De_Madrid_%28215862629%29_edited.jpeg"},
    {"name": "Seville", "desc": "Flamenco, cathedral, and old streets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Monumental_Plaza_de_Espa%C3%B1a_de_Sevilla_retouched.jpg/330px-Monumental_Plaza_de_Espa%C3%B1a_de_Sevilla_retouched.jpg"},
    {"name": "Valencia", "desc": "Futuristic buildings and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_at_night%2C_May_2017.jpg/330px-Ciutat_de_les_Arts_i_les_Ci%C3%A8ncies_at_night%2C_May_2017.jpg"},
    {"name": "Granada", "desc": "Famous for the Alhambra palace.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Alhambra_evening_panorama_Mirador_San_Nicolas_sRGB-1_%28cropped%29.jpg/330px-Alhambra_evening_panorama_Mirador_San_Nicolas_sRGB-1_%28cropped%29.jpg"}
  ],

  "Italy": [
    {"name": "Rome", "desc": "Colosseum, Vatican, and ancient history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Rom_Colosseum_Sept_2021_3.jpg/250px-Rom_Colosseum_Sept_2021_3.jpg"},
    {"name": "Venice", "desc": "Canals, gondolas, and romantic streets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Venezia_aerial_view.jpg/330px-Venezia_aerial_view.jpg"},
    {"name": "Florence", "desc": "Birthplace of Renaissance art.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/FirenzeDec092023_01.jpg/330px-FirenzeDec092023_01.jpg"},
    {"name": "Milan", "desc": "Fashion capital and modern vibes.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Milan_skyline_skyscrapers_of_Porta_Nuova_business_district_%28cropped%29.jpg/330px-Milan_skyline_skyscrapers_of_Porta_Nuova_business_district_%28cropped%29.jpg"},
    {"name": "Naples", "desc": "Historic city near Pompeii and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Centro_Direzionale_di_Napoli_%28cropped%29.jpg/330px-Centro_Direzionale_di_Napoli_%28cropped%29.jpg"}
  ],

  "Turkey": [
    {"name": "Istanbul", "desc": "Historic mosques, bazaars, and Bosphorus views.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Historical_peninsula_and_modern_skyline_of_Istanbul.jpg/330px-Historical_peninsula_and_modern_skyline_of_Istanbul.jpg"},
    {"name": "Cappadocia", "desc": "Rock formations and hot air balloons.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Cappadocia_balloon_trip%2C_Ortahisar_Castle_%2811893715185%29.jpg/330px-Cappadocia_balloon_trip%2C_Ortahisar_Castle_%2811893715185%29.jpg"},
    {"name": "Antalya", "desc": "Resorts, beaches, and ancient ruins.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Falezlerden_Antalya_Konyaalt%C4%B1_Plaj%C4%B1na_do%C4%9Fru_bir_g%C3%B6r%C3%BCn%C3%BCm.jpg/330px-Falezlerden_Antalya_Konyaalt%C4%B1_Plaj%C4%B1na_do%C4%9Fru_bir_g%C3%B6r%C3%BCn%C3%BCm.jpg"},
    {"name": "Ankara", "desc": "Capital city with museums.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/ANKARA_KOCATEPE_CAM%C4%B0%C4%B0.jpg/250px-ANKARA_KOCATEPE_CAM%C4%B0%C4%B0.jpg"},
    {"name": "Izmir", "desc": "Coastal city with markets and history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bayrakl%C4%B1_Sahil.jpg/330px-Bayrakl%C4%B1_Sahil.jpg"}
  ],

  "UAE":[
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

  "China": [
    {"name": "Beijing", "desc": "Great Wall and Forbidden City.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Skyline_of_Beijing_CBD_from_the_southeast_%2820210907094201%29.jpg/330px-Skyline_of_Beijing_CBD_from_the_southeast_%2820210907094201%29.jpg"},
    {"name": "Shanghai", "desc": "Skyscrapers and modern city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Huangpu_Park_20124-Shanghai_%2832208802494%29.jpg/330px-Huangpu_Park_20124-Shanghai_%2832208802494%29.jpg"},
    {"name": "Guangzhou", "desc": "Food and markets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Canton_Tower_20241027.jpg/330px-Canton_Tower_20241027.jpg"},
    {"name": "Shenzhen", "desc": "Tech hub near Hong Kong.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Commercial_area_of_futian_to_east2020.jpg/330px-Commercial_area_of_futian_to_east2020.jpg"},
    {"name": "Xi'an", "desc": "Terracotta Army and history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/City_wall_of_Xi%27an_51550-Xian_%2827959363326%29.jpg/250px-City_wall_of_Xi%27an_51550-Xian_%2827959363326%29.jpg"}
  ],

  "India": [
    {"name": "Delhi", "desc": "Historic sites and markets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Tomb_of_Humayun%2C_Delhi.jpg/250px-Tomb_of_Humayun%2C_Delhi.jpg"},
    {"name": "Mumbai", "desc": "Bollywood and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/%E0%A6%93%E0%A6%B0%E0%A6%B2%E0%A6%BF%E0%A6%B0_%E0%A6%97%E0%A6%97%E0%A6%A8%E0%A6%B0%E0%A7%88%E0%A6%96%E0%A6%BF%E0%A6%95_%E0%A6%A6%E0%A7%83%E0%A6%B6%E0%A7%8D%E0%A6%AF.jpg/330px-%E0%A6%93%E0%A6%B0%E0%A6%B2%E0%A6%BF%E0%A6%B0_%E0%A6%97%E0%A6%97%E0%A6%A8%E0%A6%B0%E0%A7%88%E0%A6%96%E0%A6%BF%E0%A6%95_%E0%A6%A6%E0%A7%83%E0%A6%B6%E0%A7%8D%E0%A6%AF.jpg"},
    {"name": "Jaipur", "desc": "Palaces and forts.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg/330px-East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg"},
    {"name": "Goa", "desc": "Beaches and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/BeachFun.jpg/330px-BeachFun.jpg"},
    {"name": "Agra", "desc": "Home of the Taj Mahal.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Taj_Mahal%2C_Agra%2C_India.jpg/330px-Taj_Mahal%2C_Agra%2C_India.jpg"}
  ],

  "Pakistan": [
    {"name": "Lahore", "desc": "Historic forts and food.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Lahore_Fort_view_from_Baradari.jpg/330px-Lahore_Fort_view_from_Baradari.jpg"},
    {"name": "Karachi", "desc": "Beaches and city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Dolmen_Towers_Karachi.jpg/330px-Dolmen_Towers_Karachi.jpg"},
    {"name": "Islamabad", "desc": "Mountains and modern architecture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Faisal_Mosque%2C_Islamabad_III.jpg/330px-Faisal_Mosque%2C_Islamabad_III.jpg"},
    {"name": "Hunza", "desc": "Valleys and scenic nature.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Rakaposhi%2C_Nagar_GB_%28Pakistan%29.jpg/330px-Rakaposhi%2C_Nagar_GB_%28Pakistan%29.jpg"},
    {"name": "Skardu", "desc": "Mountains and lakes.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Shangrila_resort_skardu.jpg/330px-Shangrila_resort_skardu.jpg"}
  ],

  "Thailand": [
    {"name": "Bangkok", "desc": "Temples, markets, nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Bangkok_Montage_2024_2.jpg/250px-Bangkok_Montage_2024_2.jpg"},
    {"name": "Phuket", "desc": "Beaches and islands.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Phuket_Aerial.jpg/250px-Phuket_Aerial.jpg"},
    {"name": "Chiang Mai", "desc": "Culture and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/0020-%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%AA%E0%B8%B4%E0%B8%87%E0%B8%AB%E0%B9%8C%E0%B8%A7%E0%B8%A3%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%A7%E0%B8%B4%E0%B8%AB%E0%B8%B2%E0%B8%A3.jpg/250px-0020-%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%AA%E0%B8%B4%E0%B8%87%E0%B8%AB%E0%B9%8C%E0%B8%A7%E0%B8%A3%E0%B8%A1%E0%B8%AB%E0%B8%B2%E0%B8%A7%E0%B8%B4%E0%B8%AB%E0%B8%B2%E0%B8%A3.jpg"},
    {"name": "Pattaya", "desc": "Beaches and entertainment.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Pattaya_beach_from_view_point.jpg/250px-Pattaya_beach_from_view_point.jpg"},
    {"name": "Krabi", "desc": "Cliffs, beaches, islands.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Wat_Tham_Sua_18.jpg/250px-Wat_Tham_Sua_18.jpg"}
  ],

  "Indonesia": [
    {"name": "Bali", "desc": "Beaches, temples, and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/1906_Puputan_monument_in_Denpasar.jpg/250px-1906_Puputan_monument_in_Denpasar.jpg"},
    {"name": "Jakarta", "desc": "Capital with modern city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Jakarta_CBD.jpg/330px-Jakarta_CBD.jpg"},
    {"name": "Yogyakarta", "desc": "Temples and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Jogja_-_Tugu_Monument_%282025%29_-_img_06.jpg/330px-Jogja_-_Tugu_Monument_%282025%29_-_img_06.jpg"},
    {"name": "Bandung", "desc": "Mountains and cool weather.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Bandung_View_dari_Gedung_Wisma_HSBC_Asia_Afrika_4.jpg/330px-Bandung_View_dari_Gedung_Wisma_HSBC_Asia_Afrika_4.jpg"},
    {"name": "Lombok", "desc": "Beaches and adventure.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/South_Lombok.jpg/330px-South_Lombok.jpg"}
  ],

  "Malaysia": [
    {"name": "Kuala Lumpur", "desc": "Petronas Towers and modern life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Kl-skyline-at-night-2022.jpg/330px-Kl-skyline-at-night-2022.jpg"},
    {"name": "Penang", "desc": "Food, culture, and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/KITLV_-_80020_-_Kleingrothe%2C_C.J._-_Medan_-_Quay_in_Penang_-_circa_1910.tif/lossy-page1-250px-KITLV_-_80020_-_Kleingrothe%2C_C.J._-_Medan_-_Quay_in_Penang_-_circa_1910.tif.jpg"},
    {"name": "Langkawi", "desc": "Islands and resorts.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Eagle_square_at_Kuah_Langkawi.jpg/250px-Eagle_square_at_Kuah_Langkawi.jpg"},
    {"name": "Malacca", "desc": "Historic streets and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Malacca_Sultanate_Palace.JPG/250px-Malacca_Sultanate_Palace.JPG"},
    {"name": "Sabah", "desc": "Mountains and wildlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Madai_Sabah_Madai-Cave-01.jpg/250px-Madai_Sabah_Madai-Cave-01.jpg"}
  ],

  "Singapore": [
    {"name": "Marina Bay", "desc": "Skyscrapers and city views.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Marina_Bay_Sands_%28I%29.jpg/330px-Marina_Bay_Sands_%28I%29.jpg"},
    {"name": "Sentosa", "desc": "Resorts and entertainment.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/1_sentosa_aerial_2016.jpg/330px-1_sentosa_aerial_2016.jpg"},
    {"name": "Gardens by the Bay", "desc": "Futuristic garden parks.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Supertree_Grove%2C_Gardens_by_the_Bay%2C_Singapore_-_20120712-02.jpg/330px-Supertree_Grove%2C_Gardens_by_the_Bay%2C_Singapore_-_20120712-02.jpg"},
    {"name": "Chinatown", "desc": "Culture and markets.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Chinatown_-_East_Broadway.jpg/250px-Chinatown_-_East_Broadway.jpg"},
    {"name": "Little India", "desc": "Colorful streets and temples.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/India_Square_JC_jeh.JPG/330px-India_Square_JC_jeh.JPG"}
  ],

  "Australia": [
    {"name": "Sydney", "desc": "Opera House and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019-06-21.jpg/330px-Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019-06-21.jpg"},
    {"name": "Melbourne", "desc": "Culture, food, and sports.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Melburnian_Skyline_b.jpg/330px-Melburnian_Skyline_b.jpg"},
    {"name": "Brisbane", "desc": "Riverside city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Brisbane_CBD_seen_from_Kangaroo_Point%2C_2024%2C_01_%282%29.jpg/330px-Brisbane_CBD_seen_from_Kangaroo_Point%2C_2024%2C_01_%282%29.jpg"},
    {"name": "Perth", "desc": "Beaches and sunny weather.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Perth_CBD_skyline_from_State_War_Memorial_Lookout%2C_2023%2C_04_b.jpg/330px-Perth_CBD_skyline_from_State_War_Memorial_Lookout%2C_2023%2C_04_b.jpg"},
    {"name": "Gold Coast", "desc": "Waves, beaches, and theme parks.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Gold_Coast_skyline_%28Unsplash%29.jpg/330px-Gold_Coast_skyline_%28Unsplash%29.jpg"}
  ],

  "New Zealand": [
    {"name": "Auckland", "desc": "Harbors and city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Auckland_skyline_-_May_2024_%282%29.jpg/330px-Auckland_skyline_-_May_2024_%282%29.jpg"},
    {"name": "Queenstown", "desc": "Adventure sports.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Queenstown_1_%288168013172%29.jpg/250px-Queenstown_1_%288168013172%29.jpg"},
    {"name": "Wellington", "desc": "Coastal capital with culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Wellington_Panorama_View.jpg/330px-Wellington_Panorama_View.jpg"},
    {"name": "Rotorua", "desc": "Geothermal attractions.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Rotorua_museum.jpg/250px-Rotorua_museum.jpg"},
    {"name": "Christchurch", "desc": "Garden city and nature.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Panorama_of_northern_parts_of_Christchurch_Central_City%2C_New_Zealand.jpg/330px-Panorama_of_northern_parts_of_Christchurch_Central_City%2C_New_Zealand.jpg"}
  ],

  "Brazil": [
    {"name": "Rio de Janeiro", "desc": "Beaches and Christ the Redeemer.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Cidade_Maravilhosa.jpg/330px-Cidade_Maravilhosa.jpg"},
    {"name": "São Paulo", "desc": "Modern city and food.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Marginal_Pinheiros_e_Jockey_Club.jpg/330px-Marginal_Pinheiros_e_Jockey_Club.jpg"},
    {"name": "Salvador", "desc": "Culture and beaches.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Salvador_BA_%28cropped%29_2.jpg/330px-Salvador_BA_%28cropped%29_2.jpg"},
    {"name": "Brasília", "desc": "Modern architecture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Planalto_Central_%28cropped%29.jpg/330px-Planalto_Central_%28cropped%29.jpg"},
    {"name": "Fortaleza", "desc": "Beaches and nightlife.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Fortaleza%2C_Brazil_%284%29_%28cropped%29.jpg/330px-Fortaleza%2C_Brazil_%284%29_%28cropped%29.jpg"}
  ],

  "Mexico": [
    {"name": "Mexico City", "desc": "Museums and history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Sobrevuelos_CDMX_HJ2A4913_%2825514321687%29_%28cropped%29.jpg/330px-Sobrevuelos_CDMX_HJ2A4913_%2825514321687%29_%28cropped%29.jpg"},
    {"name": "Cancún", "desc": "Beaches and resorts.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Cancun_Strand_Luftbild_%2822143397586%29.jpg/330px-Cancun_Strand_Luftbild_%2822143397586%29.jpg"},
    {"name": "Guadalajara", "desc": "Culture and food.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Panor%C3%A1mica_Guadalajara_desde_edificio_Bansi_hacia_norte_%28cropped%29.jpg/330px-Panor%C3%A1mica_Guadalajara_desde_edificio_Bansi_hacia_norte_%28cropped%29.jpg"},
    {"name": "Monterrey", "desc": "Mountains and city life.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Skyline_de_Monterrey_%28cropped%29.jpg/330px-Skyline_de_Monterrey_%28cropped%29.jpg"},
    {"name": "Tulum", "desc": "Beaches and Mayan ruins.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tulum_2.jpg/250px-Tulum_2.jpg"}
  ],

  "Argentina": [
    {"name": "Buenos Aires", "desc": "Dance, food, and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Puerto_Madero%2C_Buenos_Aires_%2840689219792%29_%28cropped%29.jpg/330px-Puerto_Madero%2C_Buenos_Aires_%2840689219792%29_%28cropped%29.jpg"},
    {"name": "Córdoba", "desc": "Historic buildings and nature.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/C%C3%B3rdoba_aerial_2.jpg/330px-C%C3%B3rdoba_aerial_2.jpg"},
    {"name": "Mendoza", "desc": "Wine region and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Downtown_Mendoza.jpg/250px-Downtown_Mendoza.jpg"},
    {"name": "Rosario", "desc": "Riverside attractions.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/J30_869_Rosario.jpg/330px-J30_869_Rosario.jpg"},
    {"name": "Bariloche", "desc": "Lakes and mountains.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Vista_a%C3%A9rea_de_Bariloche_y_la_Catedral.jpg/330px-Vista_a%C3%A9rea_de_Bariloche_y_la_Catedral.jpg"}
  ],

  "Egypt": [
    {"name": "Cairo", "desc": "Pyramids and museums.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Cairo_From_Tower_%28cropped%29.jpg/330px-Cairo_From_Tower_%28cropped%29.jpg"},
    {"name": "Giza", "desc": "Great Pyramids and Sphinx.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Giza-Nile.JPG/330px-Giza-Nile.JPG"},
    {"name": "Luxor", "desc": "Temples and ancient history.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Luxor_11.jpg/330px-Luxor_11.jpg"},
    {"name": "Aswan", "desc": "Nile views and culture.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/%D9%85%D8%B9%D8%A8%D8%AF_%D9%81%D9%8A%D9%84%D8%A9_..%D8%A7%D8%B3%D9%88%D8%A7%D9%86.jpg/120px-%D9%85%D8%B9%D8%A8%D8%AF_%D9%81%D9%8A%D9%84%D8%A9_..%D8%A7%D8%B3%D9%88%D8%A7%D9%86.jpg"},
    {"name": "Sharm El Sheikh", "desc": "Beaches and diving.", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Sharm_El_Sheikh_-_panoramio_%2815%29.jpg/330px-Sharm_El_Sheikh_-_panoramio_%2815%29.jpg"}
  ]
}

# ---------------- Trip Planner ---------------- #
def render_trip_html(ai_text):
    days = ai_text.split("Day ")
    html = "<div style='display:flex; flex-direction:column; gap:15px; max-height:500px; overflow-y:auto;'>"
    for d in days:
        if d.strip() == "":
            continue
        day_title, *rest = d.split(":")
        activities = ":".join(rest).strip().replace("\n","<br>")
        html += f"""
        <div style='border-radius:10px; box-shadow:0 4px 15px rgba(0,0,0,0.1); padding:15px; background-color:#f9f9f9;'>
            <h3 style='margin:0; color:#2c3e50;'>Day {day_title.strip()}</h3>
            <p style='margin-top:5px; font-size:14px; color:#34495e;'>{activities}</p>
        </div>
        """
    html += "</div>"
    return html

def generate_trip(country, days):
    places = [p["name"] for p in country_places[country]]
    prompt = f"""
Create a {days}-day trip plan for {country}.
Include:
- Daily schedule
- Best tourist places from: {places}
- Bus routes (fictional but realistic)
- Bus timings
- Hotels to stay each day
- Tips
Return as plain text in Day-wise format.
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}]
        )
        text = response.choices[0].message.content
        return render_trip_html(text)
    except Exception as e:
        return f"Error generating trip plan: {e}"

# ---------------- Show Places Professional ---------------- #
def show_places_professional(country):
    html = "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:20px;'>"
    for p in country_places[country]:
        html += f"""
        <div style='border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15); overflow:hidden; background:#fff;'>
            
            <div style="width:100%; height:160px; overflow:hidden;">
                <img src="{p['img']}" 
                     style='width:100%; height:160px; object-fit:cover; border-radius:0;' />
            </div>

            <div style='padding:12px;'>
                <h3 style='margin:0 0 6px 0; font-size:20px;'>{p['name']}</h3>
                <p style='margin:0; font-size:14px; color:#555;'>{p['desc']}</p>
            </div>

        </div>
        """
    html += "</div>"
    return html

# ---------------- Custom Trip ---------------- #
def generate_custom_trip(country_name, places_str, days):
    places = [p.strip() for p in places_str.split(",") if p.strip()]
    prompt = f"""
Create a {days}-day trip plan for {country_name}.
Include only these places: {places}.
Include bus routes, hotels, tips.
Return as plain text in Day-wise format.
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}]
        )
        text = response.choices[0].message.content
        return render_trip_html(text)
    except Exception as e:
        return f"Error generating custom trip plan: {e}"

# ---------------- Gradio UI ---------------- #
with gr.Blocks() as demo:
    gr.Markdown("## 🌍 AI Travel Planner")

    with gr.Tab("Pre-defined Countries"):
        country = gr.Dropdown(list(country_places.keys()), label="Select Country")
        show_btn = gr.Button("Show Tourist Places")
        places_output = gr.HTML()
        days = gr.Slider(1, 30, value=5, step=1, label="Number of Days")
        trip_btn = gr.Button("Generate Trip Plan")
        trip_output = gr.HTML()

        show_btn.click(show_places_professional, inputs=country, outputs=places_output)
        trip_btn.click(generate_trip, inputs=[country, days], outputs=trip_output)

    with gr.Tab("Custom Trip"):
        custom_country = gr.Textbox(label="Enter Country Name")
        custom_places = gr.Textbox(label="Enter Places (comma separated)")
        custom_days = gr.Slider(1, 30, value=5, step=1, label="Number of Days")
        custom_btn = gr.Button("Generate Custom Trip Plan")
        custom_output = gr.HTML()

        custom_btn.click(generate_custom_trip,
                         inputs=[custom_country, custom_places, custom_days],
                         outputs=custom_output)

demo.launch()
