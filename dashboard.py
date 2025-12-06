import streamlit as st
import requests
import os
from datetime import datetime

# Configuration
FUNCTIONS_URL = os.getenv("FUNCTIONS_URL", "http://localhost:7071")

# Page config
st.set_page_config(
    page_title="Touch Window AI Agents",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Touch Window AI Agents Dashboard")
st.markdown("---")

# Agent definitions
agents = [
    {
        "name": "ProductAgent",
        "description": "Monitors and analyzes product data",
        "icon": "📦",
        "schedule": "Weekly (Mon 2AM)"
    },
    {
        "name": "CompetitionMinderAgent",
        "description": "Tracks competitor activities",
        "icon": "🎯",
        "schedule": "Weekly (Mon 2AM)"
    },
    {
        "name": "CustomerMinderAgent",
        "description": "Analyzes customer behavior and feedback",
        "icon": "👥",
        "schedule": "Weekly (Mon 2AM)"
    },
    {
        "name": "EfficiencyAgent",
        "description": "Monitors operational efficiency metrics",
        "icon": "⚡",
        "schedule": "Weekly (Mon 2AM)"
    },
    {
        "name": "SupplierMinderAgent",
        "description": "Tracks supplier performance and issues",
        "icon": "🚚",
        "schedule": "Weekly (Mon 2AM)"
    },
    {
        "name": "OrderProcessingAgent",
        "description": "Processes and analyzes orders",
        "icon": "📋",
        "schedule": "Weekly (Mon 2AM)"
    }
]

# Status check
st.subheader("🔌 System Status")
try:
    # Test with a simple HTTP trigger endpoint
    response = requests.get(f"{FUNCTIONS_URL}/api/TriggerProductAgent", timeout=2)
    if response.status_code in [200, 202]:
        st.success("✅ AI Agents are online and ready!")
    else:
        st.warning(f"⚠️ Agents responded with status code: {response.status_code}")
except Exception as e:
    st.error(f"❌ Cannot connect to agents at {FUNCTIONS_URL}")
    st.info("💡 Make sure the functions container is running")

st.markdown("---")

# Agent controls
st.subheader("🎮 Agent Controls")

# Trigger All Agents button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Trigger All Agents", use_container_width=True, type="primary"):
        with st.spinner("Triggering all agents..."):
            results = {}
            for agent in agents:
                try:
                    url = f"{FUNCTIONS_URL}/api/Trigger{agent['name']}"
                    response = requests.post(url, json={}, timeout=30)
                    
                    if response.status_code == 200:
                        results[agent['name']] = {"status": "✅ Success", "data": response.json()}
                    else:
                        results[agent['name']] = {"status": f"❌ Failed ({response.status_code})", "error": response.text}
                except Exception as e:
                    results[agent['name']] = {"status": "❌ Error", "error": str(e)}
            
            # Display results
            st.success("All agents have been triggered!")
            st.balloons()
            
            for agent_name, result in results.items():
                with st.expander(f"{result['status']} - {agent_name}"):
                    if "data" in result:
                        st.json(result['data'])
                    else:
                        st.error(result.get('error', 'Unknown error'))

st.markdown("---")

col_count = 3
cols = st.columns(col_count)

for idx, agent in enumerate(agents):
    col = cols[idx % col_count]
    
    with col:
        with st.container():
            st.markdown(f"### {agent['icon']} {agent['name']}")
            st.caption(agent['description'])
            st.caption(f"📅 {agent['schedule']}")
            
            if st.button(f"▶️ Trigger", key=f"trigger_{agent['name']}", use_container_width=True):
                with st.spinner(f"Triggering {agent['name']}..."):
                    try:
                        url = f"{FUNCTIONS_URL}/api/Trigger{agent['name']}"
                        response = requests.post(url, json={}, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ {agent['name']} executed successfully!")
                            st.json(result)
                            st.balloons()
                        else:
                            st.error(f"❌ Failed: Status {response.status_code}")
                            st.code(response.text)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
### 📖 Quick Guide

**To trigger agents:**
- **Single Agent**: Click the "▶️ Trigger" button for any specific agent
- **All Agents**: Click the "🚀 Trigger All Agents" button at the top
- View results directly in the dashboard with detailed JSON responses

**Agent Functions:**
- **ProductAgent**: Analyzes product inventory and trends
- **CompetitionMinderAgent**: Monitors competitor pricing and strategies
- **CustomerMinderAgent**: Tracks customer satisfaction and feedback
- **EfficiencyAgent**: Identifies operational improvements
- **SupplierMinderAgent**: Evaluates supplier reliability
- **OrderProcessingAgent**: Manages order workflows

**Scheduled Execution:**
- Most agents run weekly on Mondays at 2:00 AM
- OrderProcessingAgent runs hourly
- Use the dashboard for manual execution anytime
""")

st.info(f"🔗 Functions API: {FUNCTIONS_URL}")
st.caption(f"⏰ Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
