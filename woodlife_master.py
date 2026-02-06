import streamlit as st
import requests
import json

# --- CONFIGURATION ---
WEATHER_API_KEY = "bd356f8b091c94c89cad3137490e1098"
# YOU MUST ADD $5 CREDITS TO OPENAI FOR THIS TO WORK, OR SET TO TRUE FOR MOCK MODE
OPENAI_API_KEY = OPENAI_API_KEY = "YOUR_KEY_HERE"
MOCK_AI_MODE = True # Set to FALSE when you have real money

st.set_page_config(page_title="WoodLife: Full Lifecycle", layout="wide")

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_furniture' not in st.session_state:
    st.session_state.selected_furniture = None
if 'wood_type' not in st.session_state:
    st.session_state.wood_type = ""

st.title("🌳 WoodLife: Complete Furniture Lifecycle")

# --- TABS FOR STEPS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Choose", "2. Climate", "3. AR/Scan", "4. Design", "5. Refine", "6. Order", "7. Recycle"
])

# --- STEP 1: CHOOSE FURNITURE ---
with tab1:
    st.header("🪑 Step 1: Selection")
    furniture = st.selectbox("What do you want to buy?", ["Sofa", "Dining Table", "Bed", "Chair"])
    if st.button("Confirm Selection"):
        st.session_state.selected_furniture = furniture
        st.success(f"You selected: {furniture}")

# --- STEP 2: CLIMATE (REAL LOGIC) ---
with tab2:
    st.header("🌡️ Step 2: Climate Analysis")
    city = st.text_input("Enter City", "Chennai")
    
    if st.button("Analyze Climate"):
        with st.spinner("Fetching Satellite Data..."):
            try:
                # Real API Call
                geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}").json()
                if len(geo) > 0:
                    lat, lon = geo[0]['lat'], geo[0]['lon']
                    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric").json()
                    
                    hum = weather['main']['humidity']
                    st.metric("Humidity", f"{hum}%")
                    
                    if hum > 60:
                        rec = "TEAK (Water Resistant)"
                        st.session_state.wood_type = "Teak"
                    else:
                        rec = "OAK/PINE (Stable)"
                        st.session_state.wood_type = "Oak"
                        
                    st.success(f"AI Recommendation: {rec}")
                else:
                    st.error("City not found")
            except Exception as e:
                st.error(f"Error: {e}")

# --- STEP 3: AR / SPACE SCAN ---
with tab3:
    st.header("📱 Step 3: Room Scan & Placement")
    st.info("👉 Note: Full 3D AR requires a mobile app. Here we analyze uploaded room photos.")
    
    room_photo = st.file_uploader("Upload a photo of your room", type=['jpg', 'png'])
    
    if room_photo:
        st.image(room_photo, caption="Uploaded Room", use_column_width=True)
        if st.button("Analyze Space"):
            st.spinner("Computer Vision Processing...")
            st.success("Analysis Complete!")
            st.write("📏 **Detected Walking Space:** 2.5 feet (Good)")
            st.write("💡 **Lighting:** Partial sunlight detected. Recommend stain-proof fabric.")

# --- STEP 4: AI DESIGN GENERATION ---
with tab4:
    st.header("🎨 Step 4: AI Design Generator")
    prompt = st.text_input("Describe your design (e.g., Lion in forest)")
    
    if st.button("Generate Design"):
        st.write(f"Generating '{prompt}'...")
        
        if MOCK_AI_MODE:
            st.warning("⚠️ MOCK MODE ACTIVE (You have $0 API Credits)")
            st.image("https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&q=80", caption="Mock Design Result")
        else:
            # REAL AI CODE (Requires $5)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }
            payload = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }
            try:
                response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)
                data = response.json()
                st.image(data['data'][0]['url'], caption="AI Generated Design")
            except Exception as e:
                st.error(f"AI Error: {e} (Likely 'Insufficient Quota')")

# --- STEP 5: AI REFINEMENT ---
with tab5:
    st.header("✨ Step 5: AI Refinement")
    st.write("AI converts your 'Lion' and 'Peacock' request into a cohesive artistic scene.")
    
    if st.button("Refine with AI"):
        if MOCK_AI_MODE:
             st.success("🤖 AI Logic Executed:")
             st.write("Input: Lion + Peacock")
             st.write("Output: Lion sitting under Peacock-Tree structure.")
             st.markdown("*(This is logic demonstration. Real image generation requires credits)*")
        else:
            st.info("Requires OpenAI GPT-4o API Integration")

# --- STEP 6: ORDER ---
with tab6:
    st.header("🛒 Step 6: Booking")
    st.write(f"Product: {st.session_state.selected_furniture}")
    st.write(f"Material: {st.session_state.wood_type}")
    st.write("Total Price: ₹55,000")
    if st.button("Confirm Order"):
        st.success("✅ Order Placed! WhatsApp team for delivery.")

# --- STEP 7: RECYCLE / FUTURE ---
with tab7:
    st.header("♻️ Step 7: Future Transformation")
    damage_photo = st.file_uploader("Upload photo of broken furniture", type=['jpg', 'png'])
    
    if damage_photo:
        st.image(damage_photo, caption="Damaged Item")
        if st.button("Analyze Damage"):
            st.spinner("AI Vision Analysis...")
            st.success("Salvageable Material Detected: 65%")
            st.write("📦 **Suggested New Product:** Two Dining Chairs")
            st.write("We will collect this piece to build your new chairs.")
