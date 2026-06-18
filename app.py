import streamlit as st
import requests
from config import get_smart_links

# Page configurations
st.set_page_config(page_title="AICreator Flow", page_icon="⚡", layout="wide")

# Header section
st.title("⚡ AICreator Flow: Wardrobe & Vacation Planner")
st.caption("Mix Your Clothes, Map Your Trip, and Instantly Order Missing Accessories")

# Sidebar for API Validation
st.sidebar.header("🔑 Authentication")
gemini_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

# Main user input form
st.subheader("👗 Scan & Optimize Your Look")
with st.container(border=True):
    occasion = st.text_input("1. Where are you going / What is the occasion?", 
                             placeholder="e.g., 3-Day Beach Vacation to Goa, Corporate Presentation, Evening Party...")
    
    clothes = st.text_area("2. What clothes are you carrying right now?", 
                           placeholder="e.g., White linen shirt, black cargo pants, denim jacket, casual blue jeans...")
    
    submit_button = st.button("Generate My Outfit Flow", type="primary")

# Execution running logic
if submit_button:
    if not gemini_key:
        st.error("Please provide your Google Gemini API key in the sidebar!")
    elif not occasion or not clothes:
        st.warning("Please fill out both fields to plan your look!")
    else:
        # Centralized endpoint configuration
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        # --- STAGE 1: THE MIX & MATCH PAIRS ---
        st.subheader("🗺️ STAGE 1: Your Personalized Outfit Matchings")
        with st.spinner("Gemini is analyzing your items and mapping out configurations..."):
            pair_prompt = f"You are an expert travel stylist. A user is packing these clothing items: [{clothes}] for this specific trip/occasion: '{occasion}'. Generate a clean, realistic pair schedule making the best use of these items. Group them logically (e.g., Day 1 Look, Day 2 Look). Keep it conversational and highly practical."
            
            try:
                response = requests.post(api_url, headers=headers, json={"contents": [{"parts": [{"text": pair_prompt}]}]})
                pair_result = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.info(pair_result)
                
                # --- STAGE 2: ACCESSORY UPGRADES ---
                st.subheader("🕶️ STAGE 2: Recommended Missing Accessories")
                with st.spinner("Calculating missing accents and syncing delivery portals..."):
                    accessory_prompt = f"Looking at these planned outfit matches:\n'{pair_result}'\n\nIdentify 2 to 3 specific accessory items (like a particular type of watch, sunglasses, belt, or statement socks) that are missing but absolutely vital to make these looks stand out. Explain clearly why each accessory elevates the vibe."
                    
                    response_acc = requests.post(api_url, headers=headers, json={"contents": [{"parts": [{"text": accessory_prompt}]}]})
                    accessory_result = response_acc.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success(accessory_result)
                
                # --- STAGE 3: INSTANT DELIVERY LINKS ---
                st.subheader("📦 STAGE 3: Instant Affiliate Delivery Portals")
                links = get_smart_links(occasion)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("🛒 Order Accessories on Amazon", links["amazon"], use_container_width=True)
                with col2:
                    st.link_button("⚡ Instant Delivery via Zepto", links["zepto"], use_container_width=True)
                    
            except Exception as e:
                st.error("An error occurred during pipeline scheduling. Verify your API credentials.")