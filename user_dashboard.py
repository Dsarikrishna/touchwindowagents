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

# Custom CSS for a clean, modern look with good contrast
st.markdown("""
<style>
    /* Main app background - light gradient */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ffffff;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #ecf0f1 !important;
    }
    
    .agent-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    .agent-card h3 {
        color: #2c3e50 !important;
    }
    
    .agent-card strong {
        color: #34495e;
    }
    
    .agent-card p {
        color: #555555;
    }
    
    .status-online {
        color: #27ae60;
        font-weight: bold;
    }
    
    .status-offline {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* Buttons with high contrast */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: #ffffff !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #1f638a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.5);
    }
    
    /* Headings with dark text on light background */
    h1, h2, h3, h4 {
        color: #2c3e50 !important;
    }
    
    /* Regular text - dark on light background */
    .stMarkdown, p, li {
        color: #34495e !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        color: #2c3e50 !important;
        border: 1px solid #dfe6e9;
        border-radius: 8px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f8f9fa;
        border-color: #3498db;
    }
    
    /* Success/Error/Warning messages */
    .stSuccess {
        background-color: #d4edda;
        color: #155724 !important;
        border-left: 4px solid #28a745;
    }
    
    .stError {
        background-color: #f8d7da;
        color: #721c24 !important;
        border-left: 4px solid #dc3545;
    }
    
    .stWarning {
        background-color: #fff3cd;
        color: #856404 !important;
        border-left: 4px solid #ffc107;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460 !important;
        border-left: 4px solid #17a2b8;
    }
    
    /* Metrics - clean and readable */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #3498db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetric"] label {
        color: #7f8c8d !important;
        font-weight: 600;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background-color: #3498db;
    }
    
    /* Footer styling */
    .footer-text {
        color: #7f8c8d !important;
        text-align: center;
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
    
    # Initialize session state for reports
    if 'reports_loaded' not in st.session_state:
        st.session_state.reports_loaded = False
        st.session_state.reports_data = {}
    
    # Auto-load reports on first visit
    if not st.session_state.reports_loaded:
        with st.spinner("Loading latest reports..."):
            agents = [
                ("ProductAgent", "📦 Product Inventory"),
                ("CompetitionMinderAgent", "🎯 Competition Analysis"),
                ("CustomerMinderAgent", "👥 Customer Insights"),
                ("EfficiencyAgent", "⚡ System Efficiency"),
                ("SupplierMinderAgent", "🚚 Supplier Status"),
                ("OrderProcessingAgent", "📋 Order Processing")
            ]
            
            for agent_name, display_name in agents:
                try:
                    url = f"{FUNCTIONS_URL}/api/Trigger{agent_name}"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        st.session_state.reports_data[agent_name] = {
                            "status": "success",
                            "data": response.json(),
                            "display_name": display_name
                        }
                    else:
                        st.session_state.reports_data[agent_name] = {
                            "status": "error",
                            "display_name": display_name
                        }
                except Exception:
                    st.session_state.reports_data[agent_name] = {
                        "status": "error",
                        "display_name": display_name
                    }
            
            st.session_state.reports_loaded = True
    
    # Refresh button
    if st.button("� Refresh Reports", key="refresh_reports", use_container_width=True):
        with st.spinner("Refreshing reports..."):
            agents = [
                ("ProductAgent", "📦 Product Inventory"),
                ("CompetitionMinderAgent", "🎯 Competition Analysis"),
                ("CustomerMinderAgent", "� Customer Insights"),
                ("EfficiencyAgent", "⚡ System Efficiency"),
                ("SupplierMinderAgent", "🚚 Supplier Status"),
                ("OrderProcessingAgent", "📋 Order Processing")
            ]
            
            for agent_name, display_name in agents:
                try:
                    url = f"{FUNCTIONS_URL}/api/Trigger{agent_name}"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        st.session_state.reports_data[agent_name] = {
                            "status": "success",
                            "data": response.json(),
                            "display_name": display_name
                        }
                    else:
                        st.session_state.reports_data[agent_name] = {
                            "status": "error",
                            "display_name": display_name
                        }
                except Exception:
                    st.session_state.reports_data[agent_name] = {
                        "status": "error",
                        "display_name": display_name
                    }
        st.success("✅ Reports refreshed!")
        st.rerun()
    
    # Display reports summary
    if st.session_state.reports_loaded and st.session_state.reports_data:
        st.markdown("#### 📊 Latest Reports Summary")
        
        for agent_name, report in st.session_state.reports_data.items():
            if report["status"] == "success":
                data = report["data"]
                with st.expander(f"✅ {report['display_name']}", expanded=False):
                    # Custom summaries for each agent
                    if agent_name == "ProductAgent" and data.get("status") == "success":
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Products", data.get("total_products", 0))
                        col2.metric("Avg Rating", f"⭐ {data.get('avg_rating', 0):.1f}")
                        col3.metric("Categories", len(data.get("categories", {})))
                    
                    elif agent_name == "OrderProcessingAgent" and data.get("status") == "success":
                        col1, col2 = st.columns(2)
                        col1.metric("Orders", data.get("orders_processed", 0))
                        col2.metric("Revenue", f"${data.get('total_revenue', 0):,.2f}")
                    
                    elif agent_name == "CustomerMinderAgent" and data.get("status") == "success":
                        col1, col2 = st.columns(2)
                        col1.metric("Customers", data.get("total_customers", 0))
                        col2.metric("Regions", len(data.get("customers_by_region", {})))
                    
                    elif agent_name == "SupplierMinderAgent" and data.get("status") == "success":
                        col1, col2 = st.columns(2)
                        col1.metric("Suppliers", data.get("suppliers_monitored", 0))
                        col2.metric("Products", data.get("products_tracked", 0))
                    
                    elif agent_name == "EfficiencyAgent" and data.get("status") == "success":
                        col1, col2 = st.columns(2)
                        col1.metric("Checks", data.get("checks_performed", 0))
                        col2.metric("Avg Response", f"{data.get('avg_response_time_ms', 0):.0f}ms")
                    
                    elif agent_name == "CompetitionMinderAgent" and data.get("status") == "success":
                        col1, col2 = st.columns(2)
                        col1.metric("Products Compared", data.get("products_compared", 0))
                        col2.metric("Price Difference", f"{data.get('avg_price_diff_pct', 0):+.1f}%")
            else:
                with st.expander(f"❌ {report['display_name']}", expanded=False):
                    st.error("Unable to load report data")

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
<div class="footer-text" style="padding: 1rem;">
    <p style="color: #7f8c8d;">Touch Window AI Assistant | Last updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}</p>
    <p style="font-size: 0.9rem; color: #95a5a6;">Powered by Azure Functions & Streamlit</p>
</div>
""", unsafe_allow_html=True)
