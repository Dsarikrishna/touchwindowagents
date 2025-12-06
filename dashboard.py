import streamlit as st
import requests
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Touch Window AI Agents",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    .status-running { color: #00ff00; }
    .status-stopped { color: #ff6b6b; }
    .big-number { font-size: 48px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Touch Window AI Agents Dashboard")
st.markdown("---")

# Configuration
FUNCTIONS_URL = st.sidebar.text_input(
    "Functions URL", 
    value="http://localhost:7071",
    help="The URL where your Azure Functions are running"
)

# Agent definitions
AGENTS = {
    "ProductAgent": {
        "icon": "📦",
        "description": "Monitors and analyzes product data",
        "schedule": "Weekly (Monday 2AM)"
    },
    "CompetitionMinderAgent": {
        "icon": "🎯",
        "description": "Tracks competitor activities",
        "schedule": "Weekly (Monday 2AM)"
    },
    "CustomerMinderAgent": {
        "icon": "👥",
        "description": "Customer relationship insights",
        "schedule": "Weekly (Monday 2AM)"
    },
    "EfficiencyAgent": {
        "icon": "⚡",
        "description": "Operational efficiency analysis",
        "schedule": "Weekly (Monday 2AM)"
    },
    "SupplierMinderAgent": {
        "icon": "🏭",
        "description": "Supplier relationship management",
        "schedule": "Weekly (Monday 2AM)"
    },
    "OrderProcessingAgent": {
        "icon": "📋",
        "description": "Order processing automation",
        "schedule": "Hourly"
    }
}

def check_health():
    """Check if the functions host is running"""
    try:
        response = requests.get(f"{FUNCTIONS_URL}/admin/host/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def trigger_agent(agent_name):
    """Trigger a specific agent"""
    try:
        response = requests.post(
            f"{FUNCTIONS_URL}/admin/functions/{agent_name}",
            headers={"Content-Type": "application/json"},
            json={},
            timeout=10
        )
        return response.status_code == 202
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Sidebar
st.sidebar.title("⚙️ Controls")

# Health check
if st.sidebar.button("🔄 Check Connection"):
    with st.spinner("Checking..."):
        if check_health():
            st.sidebar.success("✅ Connected!")
        else:
            st.sidebar.error("❌ Not connected")

st.sidebar.markdown("---")

# Trigger all agents
if st.sidebar.button("🚀 Trigger ALL Agents"):
    progress = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    for i, agent_name in enumerate(AGENTS.keys()):
        status_text.text(f"Triggering {agent_name}...")
        success = trigger_agent(agent_name)
        progress.progress((i + 1) / len(AGENTS))
        time.sleep(0.5)
    
    status_text.text("All agents triggered!")
    st.sidebar.success("✅ All agents triggered!")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Last refresh:** {datetime.now().strftime('%H:%M:%S')}")

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Agents", len(AGENTS))
with col2:
    is_connected = check_health()
    st.metric("Status", "🟢 Online" if is_connected else "🔴 Offline")
with col3:
    st.metric("Hourly Agents", "1")

st.markdown("---")

# Agent cards
st.subheader("🤖 Available Agents")

# Create 2 columns for agents
col1, col2 = st.columns(2)

for i, (agent_name, agent_info) in enumerate(AGENTS.items()):
    with col1 if i % 2 == 0 else col2:
        with st.container():
            st.markdown(f"""
            ### {agent_info['icon']} {agent_name}
            **{agent_info['description']}**
            
            ⏰ Schedule: `{agent_info['schedule']}`
            """)
            
            if st.button(f"▶️ Trigger {agent_name}", key=f"btn_{agent_name}"):
                with st.spinner(f"Triggering {agent_name}..."):
                    success = trigger_agent(agent_name)
                    if success:
                        st.success(f"✅ {agent_name} triggered successfully!")
                    else:
                        st.error(f"❌ Failed to trigger {agent_name}")
            
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>Touch Window AI Agents Dashboard | Built with Streamlit</p>
    <p>Repository: <a href="https://github.com/Dsarikrishna/touchwindowagents">github.com/Dsarikrishna/touchwindowagents</a></p>
</div>
""", unsafe_allow_html=True)
