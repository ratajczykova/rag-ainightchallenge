import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import requests
import time
from streamlit_echarts import st_echarts
from streamlit_lottie import st_lottie
from core.database import Database
from core.embedder import Embedder
from core.llm import LLMManager

# Page Configuration
st.set_page_config(page_title="KnowledgeQuest Innovation Lab", page_icon="🧬", layout="wide")

# Load Custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("web/style.css")

# --- HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def add_log(message):
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    st.session_state.logs = st.session_state.logs[-15:]

# Lottie Assets
lottie_molecule = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6cu9k5d.json")

# Initialize Session State
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'logs' not in st.session_state:
    st.session_state.logs = ["--- System Initialized ---"]
if 'bread_scale' not in st.session_state:
    st.session_state.bread_scale = 1.0

# Singletons
db = Database()
embedder = Embedder()
llm = LLMManager()

# --- CUSTOM COMPONENTS ---

def render_molecular_gauge(score, key=None):
    val = int(score * 100)
    color = "#ff4b2b" if val < 40 else ("#ffaa00" if val < 70 else "#00ff88")
    status = "INERT" if val < 40 else ("REACTING" if val < 70 else "STABLE")
    
    option = {
        "series": [{
            "type": 'gauge',
            "startAngle": 180,
            "endAngle": 0,
            "min": 0,
            "max": 100,
            "splitNumber": 5,
            "itemStyle": {"color": color},
            "progress": {"show": True, "width": 8},
            "pointer": {"show": False},
            "axisLine": {"lineStyle": {"width": 8, "color": [[1, '#333']]}},
            "axisTick": {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "anchor": {"show": False},
            "title": {"show": False},
            "detail": {
                "valueAnimation": True,
                "width": '60%',
                "lineHeight": 40,
                "borderRadius": 8,
                "offsetCenter": [0, '-15%'],
                "fontSize": 20,
                "fontWeight": 'bold',
                "formatter": '{value}%',
                "color": color
            },
            "data": [{"value": val}]
        }]
    }
    st_echarts(options=option, height="120px", key=key)
    st.markdown(f"<div style='text-align:center; margin-top:-40px; color:{color}; font-weight:bold; font-size:0.8em;'>{status} COMPOUND</div>", unsafe_allow_html=True)

def render_battery(query):
    words = query.split()
    length = len(words)
    # Hybrid calculation: Reward both word count and word complexity (length)
    char_bonus = len(query.replace(" ", "")) * 2
    level = min(100, (length * 15) + char_bonus)
    color = "var(--bakery-gold)"
    if level < 30: color = "#ff4b2b"
    elif level < 70: color = "#ffaa00"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px;">
            <div class="battery-container">
                <div class="battery-level" style="height: {level}%; background: {color};"></div>
            </div>
            <div style="color:#888; font-size:0.8em; font-family:monospace;">ENERGY LEVEL: {level}%</div>
        </div>
    """, unsafe_allow_html=True)

def render_bread_svg(scale=1.0):
    st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <svg class="rising-bread" width="80" height="50" viewBox="0 0 100 60" style="transform: scale({scale});">
            <path d="M10,40 Q10,20 30,20 L70,20 Q90,20 90,40 L90,50 Q90,55 85,55 L15,55 Q10,55 10,50 Z" fill="#D2B48C" stroke="#8B4513" stroke-width="2"/>
            <path d="M25,25 Q30,35 35,25" fill="none" stroke="#8B4513" stroke-width="2"/>
            <path d="M45,25 Q50,35 55,25" fill="none" stroke="#8B4513" stroke-width="2"/>
            <path d="M65,25 Q70,35 75,25" fill="none" stroke="#8B4513" stroke-width="2"/>
        </svg>
        <div style="color:var(--bakery-gold); font-size:0.7em; margin-top:5px; font-family:monospace;">STABILITY INDEX</div>
    </div>
    """, unsafe_allow_html=True)

# --- (Sidebar moved to bottom for state sync) ---

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color:var(--neon-cyan); font-family:monospace;'>KNOWLEDGE QUEST <span style='color:#fff;'>LAB</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#888; margin-top:-15px; font-family:monospace;'>Immersive Technical Ingredient Intelligence</p>", unsafe_allow_html=True)

query = st.text_input("ENTER SCAN PARAMETERS...", placeholder="Target enzyme, chemical stability, or formulation data...")

if query:
    render_battery(query)

if st.button("EMBARK ON RESEARCH QUEST", use_container_width=True):
    if not query:
        st.error("SYSTEM ERROR: PLEASE ENTER SCAN PARAMETERS")
    else:
        add_log(f"Initializing scan: '{query[:15]}...'")
        
        scan_placeholder = st.empty()
        scan_placeholder.markdown("<div style='height:2px; width:100%; background:var(--neon-cyan); box-shadow:0 0 10px var(--neon-cyan); animation: scan-line 2s infinite;'></div>", unsafe_allow_html=True)
        
        with st.spinner("ANALYZING MOLECULAR DATA..."):
            add_log("Connecting to Groq R&D Hub...")
            add_log("Vectorizing query tokens...")
            q_emb = embedder.embed(query)
            
            add_log("Performing Semantic Analysis on Archives...")
            results = db.search(q_emb, top_k=3)
            
            time.sleep(1) 
            scan_placeholder.empty()
            
            if results:
                best_score = results[0][2]
                if best_score > 0.70:
                    st.session_state.streak += 1
                    st.session_state.bread_scale = 1.3
                    add_log("EXPERT MATCH FOUND. Formulation data stable.")
                else:
                    st.session_state.streak = 0
                    st.session_state.bread_scale = 1.0
                    add_log("Weak correlation detected.")
                
                st.subheader("🧬 TECHNICAL DECODING RESULTS")
                
                cols = st.columns(3)
                for idx, res in enumerate(results):
                    filename, fragment, score = res
                    with cols[idx]:
                        st.markdown(f"""
                            <div class="holographic-card">
                                <p style="font-size: 0.65em; color: var(--neon-cyan); font-family:monospace;">SOURCE: {filename.upper()}</p>
                                <p style="font-size: 0.85em; line-height:1.4; height:120px; overflow-y:auto;">{fragment}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        render_molecular_gauge(score, key=f"gauge_{idx}")
                
                st.markdown("---")
                st.markdown("<h3 style='color:var(--bakery-gold); font-family:monospace;'>🧠 DEEP LABORATORY EXPLORATION</h3>", unsafe_allow_html=True)
                add_log("Synthesizing follow-up hypothesis...")
                follow_up = llm.generate_follow_up(results[0][1])
                st.info(follow_up)
            else:
                st.session_state.streak = 0
                st.session_state.bread_scale = 1.0
                st.error("CORE ERROR: NO MATCHING DATA IN ARCHIVES")
                add_log("Scan failed: No relevant fragments found.")

# --- LAB LOG TERMINAL ---
st.markdown("---")
st.markdown("<span style='font-size:0.7em; color:#555; font-family:monospace;'>SYSTEM LOGS</span>", unsafe_allow_html=True)
log_text = "<br>".join(st.session_state.logs)
st.markdown(f'<div class="lab-log">{log_text}</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#333; font-size:0.6em; font-family:monospace;'>CONFIDENTIAL: ROSE BLANCHE R&D PROPERTIES</p>", unsafe_allow_html=True)

# --- SIDEBAR RENDERED AT END TO ENSURE LATEST STATE REFLECTION ---
with st.sidebar:
    st.markdown("<h2 style='color:var(--neon-cyan);'>🧪 INNOVATION LAB</h2>", unsafe_allow_html=True)
    if lottie_molecule:
        st_lottie(lottie_molecule, height=150, key="molecule")
    
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align:center;">
            <span style="font-size:0.7em; color:#888; font-family:monospace;">LAB SEARCH STREAK</span><br>
            <span style="font-size:2em; font-weight:bold; color:var(--bakery-gold);">🔥 {st.session_state.streak}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    render_bread_svg(st.session_state.bread_scale)
    st.markdown("---")
    st.caption("ROSE BLANCHE R&D TERMINAL v2.0")
