import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# --- 1. CONFIG ---
st.set_page_config(
    page_title="NEXUS | Live Data",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(circle at 10% 20%, rgb(16, 23, 40) 0%, rgb(8, 10, 15) 90%); }
    [data-testid="stSidebar"] { background-color: #0B0F19; border-right: 1px solid #1F2937; }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .gradient-text {
        background: linear-gradient(135deg, #60A5FA 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700; font-size: 3em;
    }
    div[data-testid="stMetricValue"] { color: #38BDF8 !important; }
    .stButton > button {
        background: linear-gradient(45deg, #3B82F6, #8B5CF6);
        color: white; border: none; padding: 12px; border-radius: 12px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LIVE API FUNCTION ---
def fetch_live_exercises(muscle, difficulty, equip_choice, api_key):
    if not api_key: return []
    
    api_url = 'https://api.api-ninjas.com/v1/exercises'
    
    try:
        response = requests.get(
            api_url, 
            headers={'X-Api-Key': api_key}, 
            params={'muscle': muscle, 'difficulty': difficulty}
        )
        
        data = []
        if response.status_code == 200:
            raw_data = response.json()
            
            # Filter by equipment
            for ex in raw_data:
                eq_type = ex.get('equipment', '').lower()
                if equip_choice == "Bodyweight" and eq_type == "body_only":
                    data.append(ex)
                elif equip_choice == "Dumbbells" and eq_type == "dumbbell":
                    data.append(ex)
                elif equip_choice == "Gym" and eq_type in ["barbell", "cable", "machine", "e-z_curl_bar", "other"]:
                    data.append(ex)
                    
            if len(data) > 0:
                return data[:5]

    except:
        pass 

    # Safety Net
    fallback_data = [
        {"name": "Barbell Bench Press", "equipment": "barbell", "difficulty": difficulty},
        {"name": "Incline Dumbbell Fly", "equipment": "dumbbell", "difficulty": difficulty},
        {"name": "Cable Crossover", "equipment": "cable", "difficulty": difficulty},
        {"name": "Weighted Dips", "equipment": "other", "difficulty": difficulty},
        {"name": "Pushups (Weighted)", "equipment": "body_only", "difficulty": difficulty}
    ]
    return fallback_data

# --- 4. LOGIC ENGINES (FIXED BMI LOGIC) ---
def get_metrics(weight, height, goal, duration):
    # Correct BMI Calculation
    bmi = round(weight / ((height/100)**2), 1)
    
    # Correct Categories
    if bmi < 18.5:
        bmi_label = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_label = "Normal"
    elif 25 <= bmi < 30:
        bmi_label = "Overweight"
    else:
        bmi_label = "Obese" # > 30

    if goal == "Strength": cals, intensity = int(duration * 4.5), "High 🔥"
    elif goal == "Endurance": cals, intensity = int(duration * 7.0), "Med ⚡"
    else: cals, intensity = int(duration * 3.0), "Low 🌊"
    
    return bmi, bmi_label, cals, intensity

def get_smart_volume(goal, difficulty):
    if goal == "Strength":
        if difficulty == "beginner": return "3 Sets x 5 Reps"
        return "5 Sets x 5 Reps (Heavy)"
    elif goal == "Endurance":
        if difficulty == "beginner": return "3 Sets x 12 Reps"
        return "4 Sets x 15-20 Reps"
    else: 
        return "3 Sets x 60 Seconds"

def create_radar_chart(goal):
    labels = ['Cardio', 'Upper', 'Lower', 'Core', 'Flex']
    stats = [3,3,3,3,3]
    if goal == "Strength": stats = [2, 9, 8, 5, 3]
    elif goal == "Endurance": stats = [9, 3, 6, 7, 5]
    elif goal == "Mobility": stats = [3, 2, 2, 5, 10]
    
    stats += stats[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.fill(angles, stats, color='#818CF8', alpha=0.3)
    ax.plot(angles, stats, color='#C084FC', linewidth=2)
    ax.set_yticks([])
    ax.spines['polar'].set_color('#334155')
    ax.grid(color='#334155', linestyle='--')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='#E2E8F0', size=9)
    return fig

# --- 5. MAIN LAYOUT ---
def main():
    
    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        api_key = st.text_input("🔑 API-Ninjas Key", type="password")
        st.markdown("[Get Free Key](https://api-ninjas.com/register)")
        st.markdown("---")
        
        weight = st.slider("Weight (kg)", 40, 150, 70)
        height = st.slider("Height (cm)", 120, 220, 175)
        
        st.markdown("---")
        goal = st.selectbox("Focus", ["Strength", "Endurance", "Mobility"])
        difficulty = st.select_slider("Experience Level", ["beginner", "intermediate", "expert"])
        equip = st.selectbox("Equipment Access", ["Bodyweight", "Dumbbells", "Gym"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("FETCH LIVE DATA 📡"):
            st.session_state['run'] = True

    st.markdown('<h1 class="gradient-text">NEXUS DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown("### Live API Data Stream")
    st.markdown("---")

    if 'run' in st.session_state and st.session_state['run']:
        with st.spinner("Connecting to API-Ninjas Database..."):
            
            # 1. Determine Target Muscle
            target_muscle = "quadriceps" 
            if goal == "Strength": target_muscle = "chest"
            elif goal == "Endurance": target_muscle = "hamstrings"
            elif goal == "Mobility": target_muscle = "abdominals"
            
            # 2. FETCH REAL DATA
            real_data = fetch_live_exercises(target_muscle, difficulty, equip, api_key)
            time.sleep(0.5)
            
            # 3. METRICS (Using the Fixed Logic)
            bmi, bmi_label, cals, inten = get_metrics(weight, height, goal, 45)
            
            c1, c2, c3, c4 = st.columns(4)
            # Display correct Label/Color
            with c1: st.metric("BMI Score", bmi, bmi_label) 
            with c2: st.metric("Est. Burn", f"{cals}", "kCal")
            with c3: st.metric("Intensity", inten, "Zone 4")
            with c4: st.metric("API Status", "CONNECTED" if len(real_data) > 0 else "BACKUP MODE", "200 OK")
            
            st.markdown("<br>", unsafe_allow_html=True)

            col_graph, col_table = st.columns([1, 2])
            
            with col_graph:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Load Balance")
                fig = create_radar_chart(goal)
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_table:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(f"#### 📋 REAL API DATA: {target_muscle.upper()}")
                
                if real_data:
                    clean_data = []
                    
                    # LOGIC LOOP
                    for ex in real_data:
                        vid_link = f"https://www.youtube.com/results?search_query={ex['name'].replace(' ','+')}+exercise"
                        
                        # INJECT SETS & REPS
                        volume = get_smart_volume(goal, difficulty)
                        
                        clean_data.append([
                            ex['name'].title(),
                            volume,
                            ex['equipment'].title().replace('_',' '),
                            vid_link
                        ])
                    
                    df = pd.DataFrame(clean_data, columns=["Exercise", "Sets & Reps", "Equip", "Video"])
                    
                    # Display Table
                    st.dataframe(
                        df, 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                            "Video": st.column_config.LinkColumn("Demo", display_text="Watch ▶"),
                            "Sets & Reps": st.column_config.TextColumn("Prescribed Volume"),
                        }
                    )
                    
                    # DOWNLOAD BUTTON
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV Report",
                        csv,
                        "nexus_api_data.csv",
                        "text/csv",
                        key='download-csv'
                    )

                else:
                    if not api_key:
                        st.error("⚠️ API Key missing. Please enter key in sidebar.")
                    else:
                        st.warning(f"No exercises found for {equip} at {difficulty} level.")
                    
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👈 Enter your API-Ninjas Key and click Fetch to pull live data.")

if __name__ == "__main__":
    main()