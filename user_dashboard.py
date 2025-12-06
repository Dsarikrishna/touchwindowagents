"""
Touch Window AI Agents - User Dashboard
Simple, intuitive interface for non-technical users
"""
import streamlit as st
import requests
import os
from datetime import datetime
import time

# Configuration
FUNCTIONS_URL = os.getenv("FUNCTIONS_URL", "http://localhost:7071")

# Page config with friendly settings
st.set_page_config(
    page_title="Touch Window AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean, modern look
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    h3 {
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Touch Window AI Assistant</h1>
    <p>Your intelligent business automation dashboard</p>
</div>
""", unsafe_allow_html=True)

# System Status Section
st.markdown("### 📊 System Status")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    status_container = st.empty()
    try:
        response = requests.get(f"{FUNCTIONS_URL}/api/TriggerProductAgent", timeout=2)
        if response.status_code in [200, 202]:
            status_container.success("✅ All systems operational")
        else:
            status_container.warning("⚠️ System check needed")
    except Exception:
        status_container.error("❌ System offline - Please contact support")

st.markdown("---")

# Quick Actions Section
st.markdown("### ⚡ Quick Actions")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="agent-card">
        <h3>🚀 Run All Business Checks</h3>
        <p>Execute all AI agents to get a complete business overview including inventory, 
        customers, competition, suppliers, efficiency, and orders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("▶️ Run All Checks", key="run_all", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()
        
        agents = [
            ("ProductAgent", "📦 Product Inventory"),
            ("CompetitionMinderAgent", "🎯 Competition Analysis"),
            ("CustomerMinderAgent", "👥 Customer Insights"),
            ("EfficiencyAgent", "⚡ System Efficiency"),
            ("SupplierMinderAgent", "🚚 Supplier Status"),
            ("OrderProcessingAgent", "📋 Order Processing")
        ]
        
        all_success = True
        
        for idx, (agent_name, display_name) in enumerate(agents):
            status_text.text(f"Running {display_name}...")
            try:
                url = f"{FUNCTIONS_URL}/api/Trigger{agent_name}"
                response = requests.post(url, json={}, timeout=30)
                
                if response.status_code == 200:
                    with results_container:
                        st.success(f"✅ {display_name} - Completed")
                else:
                    all_success = False
                    with results_container:
                        st.error(f"❌ {display_name} - Failed")
            except Exception as e:
                all_success = False
                with results_container:
                    st.error(f"❌ {display_name} - Error")
            
            progress_bar.progress((idx + 1) / len(agents))
            time.sleep(0.5)
        
        status_text.empty()
        progress_bar.empty()
        
        if all_success:
            st.balloons()
            st.success("🎉 All business checks completed successfully!")
        else:
            st.warning("⚠️ Some checks encountered issues. Please review the results above.")

with col2:
    st.markdown("""
    <div class="agent-card">
        <h3>📈 View Latest Reports</h3>
        <p>Access detailed insights from each AI agent. Get comprehensive data on your 
        business operations, market position, and opportunities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 View Reports", key="view_reports", use_container_width=True):
        st.info("📄 Report viewing feature coming soon. For now, use the individual agent buttons below to see detailed results.")

st.markdown("---")

# Individual Agents Section
st.markdown("### 🤖 Individual Business Tools")

# Define agents with user-friendly descriptions
agents_info = [
    {
        "name": "ProductAgent",
        "icon": "📦",
        "title": "Product Inventory Check",
        "description": "Monitor your product catalog, pricing, ratings, and categories",
        "benefits": "Track inventory health, identify top performers, monitor ratings"
    },
    {
        "name": "CompetitionMinderAgent",
        "icon": "🎯",
        "title": "Competition Monitor",
        "description": "Compare your prices and offerings against competitors",
        "benefits": "Stay competitive, identify pricing opportunities, market positioning"
    },
    {
        "name": "CustomerMinderAgent",
        "icon": "👥",
        "title": "Customer Analytics",
        "description": "Understand customer behavior, preferences, and spending patterns",
        "benefits": "Improve satisfaction, identify VIP customers, regional insights"
    },
    {
        "name": "EfficiencyAgent",
        "icon": "⚡",
        "title": "System Efficiency Monitor",
        "description": "Check system health, API performance, and response times",
        "benefits": "Ensure smooth operations, prevent downtime, optimize performance"
    },
    {
        "name": "SupplierMinderAgent",
        "icon": "🚚",
        "title": "Supplier Performance",
        "description": "Monitor supplier reliability, inventory levels, and delivery times",
        "benefits": "Avoid stockouts, ensure quality, maintain good relationships"
    },
    {
        "name": "OrderProcessingAgent",
        "icon": "📋",
        "title": "Order Analysis",
        "description": "Process and analyze orders, revenue, and profit margins",
        "benefits": "Track revenue, identify issues, optimize order processing"
    }
]

# Display agents in a 2-column grid
col_left, col_right = st.columns(2)

for idx, agent in enumerate(agents_info):
    col = col_left if idx % 2 == 0 else col_right
    
    with col:
        with st.expander(f"{agent['icon']} {agent['title']}", expanded=False):
            st.markdown(f"**What it does:**\n{agent['description']}")
            st.markdown(f"**Why it matters:**\n{agent['benefits']}")
            
            if st.button(f"Run {agent['title']}", key=f"run_{agent['name']}", use_container_width=True):
                with st.spinner(f"Running {agent['title']}..."):
                    try:
                        url = f"{FUNCTIONS_URL}/api/Trigger{agent['name']}"
                        response = requests.post(url, json={}, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ {agent['title']} completed successfully!")
                            
                            # Display key metrics in a friendly way
                            if result.get("status") == "success":
                                st.markdown("**📊 Quick Summary:**")
                                
                                # Custom summaries for each agent
                                if agent['name'] == "ProductAgent":
                                    col1, col2, col3 = st.columns(3)
                                    col1.metric("Products", result.get("total_products", 0))
                                    col2.metric("Avg Rating", f"⭐ {result.get('avg_rating', 0):.1f}")
                                    col3.metric("Categories", len(result.get("categories", {})))
                                
                                elif agent['name'] == "OrderProcessingAgent":
                                    col1, col2 = st.columns(2)
                                    col1.metric("Orders", result.get("orders_processed", 0))
                                    col2.metric("Revenue", f"${result.get('total_revenue', 0):,.2f}")
                                
                                elif agent['name'] == "CustomerMinderAgent":
                                    col1, col2 = st.columns(2)
                                    col1.metric("Customers", result.get("total_customers", 0))
                                    col2.metric("Regions", len(result.get("customers_by_region", {})))
                                
                                elif agent['name'] == "SupplierMinderAgent":
                                    col1, col2 = st.columns(2)
                                    col1.metric("Suppliers", result.get("suppliers_monitored", 0))
                                    col2.metric("Products", result.get("products_tracked", 0))
                                
                                elif agent['name'] == "EfficiencyAgent":
                                    col1, col2 = st.columns(2)
                                    col1.metric("Checks", result.get("checks_performed", 0))
                                    col2.metric("Avg Response", f"{result.get('avg_response_time_ms', 0):.0f}ms")
                                
                                elif agent['name'] == "CompetitionMinderAgent":
                                    col1, col2 = st.columns(2)
                                    col1.metric("Products Compared", result.get("products_compared", 0))
                                    col2.metric("Price Difference", f"{result.get('avg_price_diff_pct', 0):+.1f}%")
                                
                                # Show detailed results in an expander
                                with st.expander("📄 View Detailed Results"):
                                    st.json(result)
                        else:
                            st.error(f"❌ Failed to run {agent['title']}")
                    except Exception as e:
                        st.error(f"❌ Error: Unable to connect to the system")

st.markdown("---")

# Help Section
with st.expander("❓ Help & Information"):
    st.markdown("""
    ### How to Use This Dashboard
    
    **Quick Start:**
    1. Click "Run All Checks" to get a complete business overview
    2. Or select individual tools to focus on specific areas
    3. Results appear immediately with key insights
    
    **What Each Tool Does:**
    - **Product Inventory:** Monitors your product catalog and performance
    - **Competition Monitor:** Keeps track of competitor pricing
    - **Customer Analytics:** Analyzes customer behavior and trends
    - **System Efficiency:** Ensures all systems are running smoothly
    - **Supplier Performance:** Tracks supplier reliability
    - **Order Analysis:** Processes and analyzes order data
    
    **Automated Checks:**
    Most tools run automatically every week on Monday at 2:00 AM.
    Order processing runs every hour automatically.
    
    **Need Help?**
    Contact your system administrator if you see error messages.
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Touch Window AI Assistant | Last updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}</p>
    <p style="font-size: 0.9rem;">Powered by Azure Functions & Streamlit</p>
</div>
""", unsafe_allow_html=True)
