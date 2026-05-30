import streamlit as st
import datetime

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="GiggleBunny-K Sanctuary", page_icon="🐰")

# Custom CSS for the Black, Pink, and Wine Red theme
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #000000;
        color: #FFB6C1;
    }}
    .stButton>button {{
        width: 100%;
        height: 100px;
        border-radius: 20px;
        border: 4px solid #722F37;
        background-color: #722F37;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0px 0px 15px #FF69B4;
    }}
    .stButton>button:hover {{
        background-color: #FF69B4;
        border-color: #FFB6C1;
        color: black;
    }}
    .grievance-box {{
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FF69B4;
        margin-bottom: 10px;
    }}
    h1, h2, h3 {{
        color: #FF69B4 !important;
        font-family: 'Courier New', Courier, monospace;
    }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #722F37;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA STORAGE (Mock Database) ---
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
if 'buzzer_count' not in st.session_state:
    st.session_state.buzzer_count = 0

# --- APP LAYOUT ---

st.title("🐰 GiggleBunny-K's Sanctuary")
st.subheader("For the precious creature when the world is too loud.")

# Section 1: The Overstimulation Buzzer
st.markdown("---")
st.write("### 🚨 The 'Leave Me Alone' Buzzer")
st.write("Press this if you are overstimulated, irritated, or just done with everyone.")

if st.button("💢 ACTIVATE BUZZER 💢"):
    st.session_state.buzzer_count += 1
    st.balloons()
    st.error(f"ALERT: GiggleBunny-K is officially irritated! (Signal sent {st.session_state.buzzer_count} times today)")
    st.write("✨ *Instructions for the creature: Find a dark corner, grab a blanket, and breathe. This app has heard your scream.* ✨")

# Section 2: The Grievance Box
st.markdown("---")
st.write("### 📝 Official Grievance Filing")
st.write("What did the world do wrong this time? Launch a ticket for the Admin (your boyfriend) to review.")

with st.form("grievance_form", clear_on_submit=True):
    issue = st.text_area("Describe the irritation:")
    severity = st.select_slider("Severity Level", options=["Mildly Annoying", "Pissed Off", "Atomic Rage"])
    submitted = st.form_submit_button("Submit Ticket to Admin")
    
    if submitted and issue:
        ticket = {
            "id": len(st.session_state.tickets) + 1,
            "time": datetime.datetime.now().strftime("%H:%M"),
            "issue": issue,
            "severity": severity,
            "status": "Pending Review ⏳",
            "reply": ""
        }
        st.session_state.tickets.append(ticket)
        st.success("Ticket launched. The creature's voice has been logged.")

# Section 3: Admin Panel (For You)
st.sidebar.markdown("## 🔐 Admin Access")
admin_password = st.sidebar.text_input("Enter Admin Key", type="password")

# Only shows tickets if you enter the 'password' (you can change 'love' to whatever you want)
if admin_password == "love":
    st.sidebar.write("### Review Grievances")
    
    if not st.session_state.tickets:
        st.sidebar.write("No active grievances. The creature is currently chill.")
    
    for i, t in enumerate(st.session_state.tickets):
        with st.sidebar.expander(f"Ticket #{t['id']} - {t['severity']}"):
            st.write(f"**At {t['time']}, the creature said:**")
            st.write(f"*{t['issue']}*")
            
            reply_text = st.text_input(f"Reply to #{t['id']}", key=f"reply_{i}")
            if st.button(f"Send Reply", key=f"btn_{i}"):
                st.session_state.tickets[i]['reply'] = reply_text
                st.session_state.tickets[i]['status'] = "Resolved ✅"
                st.rerun()

# Section 4: Ticket Status (What she sees)
st.markdown("---")
st.write("### 📂 Ticket Status")
if not st.session_state.tickets:
    st.write("No open tickets. You are doing great, GiggleBunny-K.")
else:
    for t in reversed(st.session_state.tickets):
        color = "#FF69B4" if t['status'] == "Resolved ✅" else "#722F37"
        st.markdown(f"""
            <div class="grievance-box">
                <p><strong>Ticket #{t['id']}</strong> - Status: <span style="color:{color}">{t['status']}</span></p>
                <p><em>"{t['issue']}"</em></p>
                <p style="color: #FFB6C1;"><strong>Admin Reply:</strong> {t['reply'] if t['reply'] else "Waiting for Admin to stop being a loser and reply..."}</p>
            </div>
        """, unsafe_allow_html=True)
