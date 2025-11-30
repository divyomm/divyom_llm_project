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
    h4 { color: #A78BFA !important; } 
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ENGINES ---

def get_metrics(weight, height, goal, duration):
    bmi = round(weight / ((height/100)**2), 1)
    if bmi < 18.5: bmi_label = "Underweight"
    elif 18.5 <= bmi < 25: bmi_label = "Normal"
    elif 25 <= bmi < 30: bmi_label = "Overweight"
    else: bmi_label = "Obese"

    if goal == "Strength": cals, intensity = int(duration * 4.5), "High 🔥"
    elif goal == "Endurance": cals, intensity = int(duration * 7.0), "Med ⚡"
    else: cals, intensity = int(duration * 3.0), "Low 🌊"
    
    return bmi, bmi_label, cals, intensity

def get_smart_volume(goal, difficulty, bmi):
    if bmi >= 30: return "3 Sets x 10 Reps (Low Impact)"
    if goal == "Strength": return "4 Sets x 6-8 Reps" if difficulty != "beginner" else "3 Sets x 10 Reps"
    elif goal == "Endurance": return "3 Sets x 15 Reps"
    else: return "3 Sets x 60 Seconds"

def generate_diet_plan(goal, weight):
    if goal == "Strength":
        p, c, f = int(weight * 2.2), int(weight * 3.0), int(weight * 0.8)
        meals = [["Breakfast", "Oats + Whey"], ["Lunch", "Chicken + Rice"], ["Dinner", "Lean Beef + Veg"]]
    elif goal == "Endurance":
        p, c, f = int(weight * 1.6), int(weight * 5.0), int(weight * 0.8)
        meals = [["Breakfast", "Banana + Toast"], ["Lunch", "Pasta + Turkey"], ["Dinner", "Fish + Quinoa"]]
    else:
        p, c, f = int(weight * 2.0), int(weight * 1.5), int(weight * 0.9)
        meals = [["Breakfast", "Eggs + Spinach"], ["Lunch", "Chicken Salad"], ["Dinner", "White Fish + Greens"]]
    return meals, p, c, f

# --- 4. VISUALIZATION ---

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
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    ax.fill(angles, stats, color='#818CF8', alpha=0.3)
    ax.plot(angles, stats, color='#C084FC', linewidth=2)
    ax.set_yticks([]); ax.spines['polar'].set_color('#334155')
    ax.grid(color='#334155', linestyle='--'); ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='#E2E8F0', size=9)
    return fig

def create_donut_chart(p, c, f):
    labels = ['Pro', 'Carb', 'Fat']
    sizes = [p, c, f]
    colors = ['#38BDF8', '#C084FC', '#34D399']
    
    # Chart with explicit size to fit card
    fig, ax = plt.subplots(figsize=(4, 2))
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%', 
                                      colors=colors, startangle=90, 
                                      textprops={'color':"white", 'fontsize': 8}, pctdistance=0.80)
    centre_circle = plt.Circle((0,0),0.60,fc='#1E2530') # Match card background
    fig.gca().add_artist(centre_circle)
    return fig

# --- 5. LIVE API FUNCTION ---
def fetch_live_exercises(muscle, difficulty, equip_choice, api_key):
    if not api_key: return []
    api_url = 'https://api.api-ninjas.com/v1/exercises'
    try:
        response = requests.get(
            api_url, 
            headers={'X-Api-Key': api_key}, 
            params={'muscle': muscle, 'difficulty': difficulty}
        )
        if response.status_code == 200:
            data = response.json()
            filtered = []
            for ex in data:
                eq = ex.get('equipment', '').lower()
                if equip_choice == "Bodyweight" and eq == "body_only": filtered.append(ex)
                elif equip_choice == "Dumbbells" and eq == "dumbbell": filtered.append(ex)
                elif equip_choice == "Gym": filtered.append(ex) # Gym accepts all
            
            if not filtered: return data[:3] # Fallback to top 3 if filter is too strict
            return filtered[:3] 
        return []
    except: return []

# --- 6. MAIN LAYOUT ---
def main():
    
    with st.sidebar:
        st.markdown("## ⚙️ SETTINGS")
        api_key = st.text_input("🔑 API-Ninjas Key", type="password")
        st.markdown("[Get Free Key](https://api-ninjas.com/register)")
        st.markdown("---")
        
        weight = st.slider("Weight (kg)", 40, 150, 70)
        height = st.slider("Height (cm)", 120, 220, 175)
        goal = st.selectbox("Focus", ["Strength", "Endurance", "Mobility"])
        difficulty = st.select_slider("Level", ["beginner", "intermediate", "expert"])
        equip = st.selectbox("Equipment Access", ["Bodyweight", "Dumbbells", "Gym"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("RUN SIMULATION 📡"):
            st.session_state['run'] = True

    st.markdown('<h1 class="gradient-text">NEXUS DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown("### Live API Data Stream")
    st.markdown("---")

    if 'run' in st.session_state and st.session_state['run']:
        with st.spinner("Connecting to API & Analyzing Biomechanics..."):
            
            # 1. CALCULATE METRICS
            bmi, bmi_label, cals, inten = get_metrics(weight, height, goal, 45)
            meals, p, c, f = generate_diet_plan(goal, weight)
            
            time.sleep(0.5)
            
            # --- ROW 1: METRICS ---
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("BMI Score", f"{bmi}", bmi_label)
            with c2: st.metric("Est. Burn", f"{cals}", "kCal")
            with c3: st.metric("Target Protein", f"{p}g", "Daily")
            # We don't know API status yet, placeholder
            
            st.markdown("<br>", unsafe_allow_html=True)

            # --- ROW 2: VISUALS ---
            col_left, col_right = st.columns([1, 1])
            
            # Left Card: Radar Chart
            with col_left:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Training Vectors")
                fig1 = create_radar_chart(goal)
                st.pyplot(fig1)
                st.markdown('</div>', unsafe_allow_html=True)

            # Right Card: Nutrition (Stacked Layout)
            with col_right:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🥗 Nutrition Fuel")
                # Stacked: Chart Top, Table Bottom
                fig3 = create_donut_chart(p, c, f)
                st.pyplot(fig3, use_container_width=False)
                st.dataframe(pd.DataFrame(meals, columns=["Meal", "Plan"]), hide_index=True, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- ROW 3: FULL WEEKLY SPLIT GENERATOR ---
            st.markdown("### 🗓️ WEEKLY LIVE PROTOCOL")
            
            # Define the Split (Day Name, Muscle 1, Muscle 2)
            weekly_split = [
                ("MONDAY: PUSH (Chest + Triceps)", "chest", "triceps"),
                ("TUESDAY: PULL (Back + Biceps)", "middle_back", "biceps"),
                ("WEDNESDAY: LEGS (Quads + Hams)", "quadriceps", "hamstrings"),
                ("THURSDAY: SHOULDERS & CORE", "shoulders", "abdominals")
            ]
            
            api_status_ok = False 

            # Loop through days and generate cards
            for day_name, m1, m2 in weekly_split:
                
                with st.container():
                    st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"#### {day_name}")
                    
                    # Fetch data for both muscles
                    data_m1 = fetch_live_exercises(m1, difficulty, equip, api_key)
                    data_m2 = fetch_live_exercises(m2, difficulty, equip, api_key)
                    combined_day = data_m1 + data_m2
                    
                    if combined_day:
                        api_status_ok = True
                        clean_data = []
                        for ex in combined_day:
                            vid_link = f"https://www.youtube.com/results?search_query={ex['name'].replace(' ','+')}+exercise"
                            vol = get_smart_volume(goal, difficulty, bmi)
                            
                            clean_data.append([
                                ex['name'].title(),
                                ex['muscle'].upper(),
                                vol,
                                vid_link
                            ])
                        
                        df = pd.DataFrame(clean_data, columns=["Exercise", "Target", "Sets/Reps", "Video"])
                        st.dataframe(
                            df, use_container_width=True, hide_index=True,
                            column_config={"Video": st.column_config.LinkColumn("Demo", display_text="Watch ▶")}
                        )
                    else:
                        st.warning("⚠️ API Key missing or no exercises found.")
                        
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Update status metric based on loop result
            with c4: st.metric("System Status", "ONLINE" if api_status_ok else "OFFLINE", "200 OK")

    else:
        st.info("👈 Enter API Key and Click Run to Initialize.")

if __name__ == "__main__":
    main()