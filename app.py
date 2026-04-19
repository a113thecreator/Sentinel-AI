import streamlit as st
import requests
import time

# --- CEO AURA STYLING ---
st.set_page_config(page_title="SENTINEL AI", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white; font-weight: bold; border: none;
    }
    .stTextInput>div>div>input { 
        background-color: #12161d; color: #00ffc3; 
        border: 1px solid #1f2937; border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SENTINEL AI")
st.caption("Founder Edition v1.1 | Professional Intelligence")

# --- CORE ENGINE ---
API_KEY = "# --- CORE ENGINE ---
# This line tells the app to look in the "Cloud Vault" for your key
API_KEY = st.secrets["VT_API_KEY"]" # Put your key back here!

url_input = st.text_input("Enter Target URL for Diagnostic", placeholder="https://")

if st.button("EXECUTE SCAN"):
    if url_input:
        with st.status("Initializing Sentinel Protocols...", expanded=True) as status:
            st.write("🛰️ Connecting to Global Database...")
            headers = {"x-apikey": API_KEY}
            data = {"url": url_input}
            
            try:
                response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
                
                if response.status_code == 200:
                    st.write("🔎 Deep-Scanning Vendor Data...")
                    time.sleep(10) 
                    
                    analysis_id = response.json()['data']['id']
                    report = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=headers).json()
                    
                    attributes = report['data']['attributes']
                    stats = attributes['stats']
                    results = attributes['results']
                    
                    status.update(label="Scan Complete!", state="complete", expanded=False)
                    
                    st.divider()
                    c1, c2 = st.columns(2)
                    c1.metric("CLEAN RATING", f"{stats['harmless']}/70")
                    c2.metric("THREATS DETECTED", stats['malicious'], delta_color="inverse")

                    if stats['malicious'] > 0:
                        st.error(f"🚨 SENTINEL WARNING: Malicious activity detected.")
                        
                        # NEW: The Expert Intelligence List
                        with st.expander("VIEW THREAT VENDORS"):
                            st.write("The following engines flagged this URL:")
                            for vendor, details in results.items():
                                if details['category'] == 'malicious':
                                    st.write(f"- 🔴 **{vendor}**: {details['result']}")
                    else:
                        st.success("🛡️ SENTINEL VERDICT: No threats found in global database.")
                else:
                    st.error("API Connection Error.")
            except Exception as e:
                st.error(f"System Offline: {e}")