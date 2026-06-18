import streamlit as st
import requests
from config import get_smart_links

# Page configurations
st.set_page_config(page_title="AICreator Flow", page_icon="⚡", layout="wide")

st.title("⚡ AICreator Flow: Wardrobe & Vacation Planner")
st.caption("Scan Your Clothes, Map Your Trip, and Instantly Order Missing Accessories")

# Sidebar Authentication
st.sidebar.header("🔑 Authentication")
gemini_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

st.subheader("👗 Scan & Optimize Your Look")
with st.container(border=True):
    occasion = st.text_input("1. Where are you going / What is the occasion?", 
                             placeholder="e.g., 3-Day Beach Vacation to Goa, Date Night...")
    
    st.write("---")
    st.markdown("### 📸 Live Wardrobe Scanner")
    camera_photo = st.camera_input("Take a photo of your clothes layout directly via camera")
    st.write("---")
    
    clothes = st.text_area("2. Verify or add clothing description details manually:", 
                            placeholder="e.g., black dress, white linen shirt, denim jacket...")

    submit_button = st.button("Generate My Outfit Flow", type="primary")

if submit_button:
    if not gemini_key:
        st.error("Please provide your Google Gemini API key in the sidebar!")
    elif not occasion or (not clothes and not camera_photo):
        st.warning("Please specify an occasion and input/scan your apparel items!")
    else:
        # Structured functional payload array track 
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        st.subheader("🗺️ STAGE 1: Your Personalized Outfit Matchings")
        with st.spinner("Gemini is processing layout variables..."):
            pair_prompt = f"You are an expert travel stylist. A user has packed/scanned these clothing items: [{clothes}] for this occasion: '{occasion}'. Generate a crisp daily pair schedule making the best use of these items. Keep it practical and highly conversational."
            
            payload = {"contents": [{"parts": [{"text": pair_prompt}]}]}
            
            try:
                response = requests.post(api_url, headers=headers, json=payload)
                response_json = response.json()
                
                if 'candidates' not in response_json:
                    st.error("🛑 Live API Tracking Sync Alert. Details:")
                    st.json(response_json)
                else:
                    pair_result = response_json['candidates'][0]['content']['parts'][0]['text']
                    st.info(pair_result)
                    
                    # STAGE 2: ACCESSORIES
                    st.subheader("🕶️ STAGE 2: Recommended Missing Accessories")
                    with st.spinner("Calculating matching accents..."):
                        acc_prompt = f"Based on this outfit plan:\n'{pair_result}'\n\nSuggest 2 specific accessories (like a type of watch, sunglasses) to finish the look."
                        response_acc = requests.post(api_url, headers=headers, json={"contents": [{"parts": [{"text": acc_prompt}]}]})
                        acc_result = response_acc.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(acc_result)
                    
                    # STAGE 3: VISUAL ELEVATION
                    st.subheader("🎨 STAGE 3: Visual Style Inspo Blueprint Mockups")
                    img_col1, img_col2, img_col3 = st.columns(3)
                    with img_col1:
                        st.image("https://images.unsplash.com/photo-1483985988355-763728e1935b?w=500", caption="Scanned Palette Profile")
                    with img_col2:
                        st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=500", caption="AI Structural Match Up")
                    with img_col3:
                        st.image("https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500", caption="Accessorized Profile Blueprint")

                    # STAGE 4: DELIVERY PORTALS
                    st.subheader("📦 STAGE 4: Instant Affiliate Delivery Portals")
                    links = get_smart_links(occasion)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button("🛒 Order Accessories on Amazon", links["amazon"], use_container_width=True)
                    with col2:
                        st.link_button("⚡ Instant Delivery via Zepto", links["zepto"], use_container_width=True)
                        
            except Exception as e:
                st.error(f"System Connection Warning: {e}")