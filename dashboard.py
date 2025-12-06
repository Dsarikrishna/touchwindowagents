"""
Touch Window AI Agents Dashboard
Enhanced dashboard with colorful theme and real-time agent data.
"""
import streamlit as st
import requests
import time
import json
import sys
import os
from datetime import datetime

# Add shared folder to path for direct agent imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import agents directly
try:
    from shared.agents import (
        run_order_processing_agent,
        run_product_agent,
        run_efficiency_agent,
        run_competition_minder_agent,
        run_customer_minder_agent,
        run_supplier_minder_agent
    )
    AGENTS_AVAILABLE = True
except ImportError as e:
    AGENTS_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Page config
st.set_page_config(
    page_title="Touch Window AI Agents",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Dark Theme and Colorful Accents
st.markdown('''
<style>
    /* Main background - dark theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #e94560;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Metric cards with gradient backgrounds */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    [data-testid="stMetric"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: bold;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #ffd700 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(26, 26, 46, 0.8);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #16213e;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid #e94560;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e94560;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.6);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.4);
    }
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(33, 150, 243, 0.2);
        border-left: 4px solid #2196f3;
        color: #ffffff;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4caf50;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: rgba(255, 152, 0, 0.2);
        border-left: 4px solid #ff9800;
    }
    
    /* Error boxes */
    .stError {
        background-color: rgba(244, 67, 54, 0.2);
        border-left: 4px solid #f44336;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
    }
    
    [data-testid="stDataFrame"] {
        background-color: rgba(26, 26, 46, 0.9);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Cards for content sections */
    .content-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(233, 69, 96, 0.3);
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Colored accent cards */
    .card-blue {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .card-green {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .card-red {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .card-orange {
        background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .card-purple {
        background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .card-teal {
        background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    /* Alert styling */
    .alert-high {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 4px 10px rgba(231, 76, 60, 0.3);
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #f39c12 0%, #d35400 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 4px 10px rgba(243, 156, 18, 0.3);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 4px 10px rgba(39, 174, 96, 0.3);
    }
    
    /* Divider */
    hr {
        border-color: rgba(233, 69, 96, 0.3);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(26, 26, 46, 0.8);
        color: #ffffff;
        border-radius: 10px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
    }
    
    /* Text input */
    .stTextInput input {
        background-color: rgba(26, 26, 46, 0.8);
        color: #ffffff;
        border: 1px solid #e94560;
        border-radius: 8px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #e94560 !important;
    }
</style>
''', unsafe_allow_html=True)

# Header with gradient text effect
st.markdown('''
<h1 style="text-align: center; background: linear-gradient(135deg, #e94560, #ff6b6b, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem;">
 Touch Window AI Agents Dashboard
</h1>
<p style="text-align: center; color: #b0b0b0; font-size: 1.1rem;">
Real-time monitoring and analytics from your AI agents
</p>
''', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.markdown('''
<h2 style="color: #e94560;"> Dashboard Controls</h2>
''', unsafe_allow_html=True)
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Agent function mapping
AGENT_FUNCTIONS = {
    "OrderProcessingAgent": (" Order Processing", run_order_processing_agent if AGENTS_AVAILABLE else None, "#667eea"),
    "ProductAgent": (" Product Analysis", run_product_agent if AGENTS_AVAILABLE else None, "#00b894"),
    "EfficiencyAgent": (" System Efficiency", run_efficiency_agent if AGENTS_AVAILABLE else None, "#f39c12"),
    "CompetitionMinderAgent": (" Competition Monitor", run_competition_minder_agent if AGENTS_AVAILABLE else None, "#e94560"),
    "CustomerMinderAgent": (" Customer Analytics", run_customer_minder_agent if AGENTS_AVAILABLE else None, "#9b59b6"),
    "SupplierMinderAgent": (" Supplier Monitor", run_supplier_minder_agent if AGENTS_AVAILABLE else None, "#1abc9c"),
}

# Initialize session state for results
if 'agent_results' not in st.session_state:
    st.session_state.agent_results = {}
if 'last_run' not in st.session_state:
    st.session_state.last_run = {}

def run_agent(agent_key):
    """Run an agent and store results"""
    if not AGENTS_AVAILABLE:
        return {"status": "error", "error": IMPORT_ERROR}
    
    name, func, color = AGENT_FUNCTIONS[agent_key]
    if func:
        result = func()
        st.session_state.agent_results[agent_key] = result
        st.session_state.last_run[agent_key] = datetime.now().strftime('%H:%M:%S')
        return result
    return None

# Sidebar controls
if st.sidebar.button(" Run ALL Agents", type="primary", use_container_width=True):
    with st.spinner("Running all agents..."):
        progress = st.sidebar.progress(0)
        for i, agent_key in enumerate(AGENT_FUNCTIONS.keys()):
            run_agent(agent_key)
            progress.progress((i + 1) / len(AGENT_FUNCTIONS))
            time.sleep(0.3)
    st.sidebar.success(" All agents completed!")

st.sidebar.markdown("---")
st.sidebar.markdown('''
<h3 style="color: #00b894;"> Quick Stats</h3>
''', unsafe_allow_html=True)

# Show quick stats in sidebar if we have results
if st.session_state.agent_results:
    order_result = st.session_state.agent_results.get("OrderProcessingAgent", {})
    if order_result.get("status") == "success":
        st.sidebar.metric("Total Revenue", f"\")
    
    product_result = st.session_state.agent_results.get("ProductAgent", {})
    if product_result.get("status") == "success":
        st.sidebar.metric("Products Tracked", product_result.get('total_products', 0))
    
    supplier_result = st.session_state.agent_results.get("SupplierMinderAgent", {})
    if supplier_result.get("status") == "success":
        st.sidebar.metric("Suppliers", supplier_result.get('suppliers_monitored', 0))

st.sidebar.markdown("---")
st.sidebar.markdown('''
<div style="text-align: center; padding: 10px;">
<a href="https://github.com/Dsarikrishna/touchwindowagents" style="color: #e94560; text-decoration: none;">
 GitHub Repository
</a>
</div>
''', unsafe_allow_html=True)

# Main content - Tabs for each agent
tabs = st.tabs([
    " Orders", 
    " Products", 
    " Efficiency", 
    " Competition", 
    " Customers", 
    " Suppliers",
    " Overview"
])

# Tab 1: Order Processing Agent
with tabs[0]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #667eea;"> Order Processing Agent</h2>
    <p style="color: #b0b0b0;">Fetches and analyzes orders from DummyJSON API</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_order"):
            with st.spinner("Processing orders..."):
                run_agent("OrderProcessingAgent")
    
    result = st.session_state.agent_results.get("OrderProcessingAgent")
    if result and result.get("status") == "success":
        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Orders Processed", result.get("orders_processed", 0))
        with m2:
            st.metric("Total Revenue", f"\")
        with m3:
            avg_margin = 0
            if result.get("order_details"):
                margins = [o.get("margin_pct", 0) for o in result["order_details"]]
                avg_margin = sum(margins) / len(margins) if margins else 0
            st.metric("Avg Margin", f"{avg_margin:.1f}%")
        with m4:
            st.metric("Alerts", len(result.get("alerts", [])))
        
        # Order details table
        st.markdown('<h3 style="color: #667eea;"> Order Details</h3>', unsafe_allow_html=True)
        if result.get("order_details"):
            order_data = result["order_details"][:10]
            st.dataframe(order_data, use_container_width=True)
        
        # Alerts
        if result.get("alerts"):
            st.markdown('<h3 style="color: #f39c12;"> Alerts</h3>', unsafe_allow_html=True)
            for alert in result["alerts"]:
                st.markdown(f'''
                <div class="alert-medium">
                 Order #{alert.get('order_id')}: {alert.get('issue')} ({alert.get('margin')})
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info(" Click 'Run Agent' to fetch order data from DummyJSON API")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Product Agent
with tabs[1]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #00b894;"> Product Analysis Agent</h2>
    <p style="color: #b0b0b0;">Analyzes product catalog from FakeStoreAPI</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_product"):
            with st.spinner("Analyzing products..."):
                run_agent("ProductAgent")
    
    result = st.session_state.agent_results.get("ProductAgent")
    if result and result.get("status") == "success":
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Products", result.get("total_products", 0))
        with m2:
            st.metric("Avg Rating", f" {result.get('avg_rating', 0):.2f}")
        with m3:
            price_range = result.get("price_range", {})
            st.metric("Min Price", f"\")
        with m4:
            st.metric("Max Price", f"\")
        
        # Categories breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<h3 style="color: #00b894;"> Products by Category</h3>', unsafe_allow_html=True)
            categories = result.get("categories", {})
            if categories:
                st.bar_chart(categories)
        
        with col2:
            st.markdown('<h3 style="color: #ffd700;"> Top Rated Products</h3>', unsafe_allow_html=True)
            top_rated = result.get("top_rated", [])[:5]
            for product in top_rated:
                st.markdown(f'''
                <div class="card-green" style="padding: 10px; margin: 5px 0;">
                <strong>{product.get('title', 'N/A')}</strong><br/>
                 {product.get('rating')} | \
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info(" Click 'Run Agent' to analyze products from FakeStoreAPI")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Efficiency Agent
with tabs[2]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #f39c12;"> System Efficiency Agent</h2>
    <p style="color: #b0b0b0;">Monitors API health and response times</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_efficiency"):
            with st.spinner("Checking system health..."):
                run_agent("EfficiencyAgent")
    
    result = st.session_state.agent_results.get("EfficiencyAgent")
    if result and result.get("status") == "success":
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Endpoints Checked", result.get("checks_performed", 0))
        with m2:
            st.metric("Avg Response Time", f"{result.get('avg_response_time_ms', 0):.0f}ms")
        with m3:
            healthy = sum(1 for e in result.get("endpoints_checked", []) if e.get("healthy"))
            st.metric("Healthy Endpoints", f"{healthy}/{result.get('checks_performed', 0)}")
        
        # Endpoint status
        st.markdown('<h3 style="color: #f39c12;"> Endpoint Health</h3>', unsafe_allow_html=True)
        for endpoint in result.get("endpoints_checked", []):
            is_healthy = endpoint.get("healthy")
            response_time = endpoint.get("response_time_ms", 0)
            
            if is_healthy and response_time < 500:
                card_class = "alert-success"
                status_icon = ""
            elif is_healthy:
                card_class = "alert-medium"
                status_icon = ""
            else:
                card_class = "alert-high"
                status_icon = ""
            
            st.markdown(f'''
            <div class="{card_class}">
            {status_icon} <strong>{endpoint.get('name')}</strong> | 
            Status: {endpoint.get('status_code')} | 
             {response_time:.0f}ms
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info(" Click 'Run Agent' to check system health across APIs")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Competition Minder Agent
with tabs[3]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #e94560;"> Competition Monitor Agent</h2>
    <p style="color: #b0b0b0;">Compares prices across different sources</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_competition"):
            with st.spinner("Analyzing competition..."):
                run_agent("CompetitionMinderAgent")
    
    result = st.session_state.agent_results.get("CompetitionMinderAgent")
    if result and result.get("status") == "success":
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Products Compared", result.get("products_compared", 0))
        with m2:
            avg_diff = result.get("avg_price_diff_pct", 0)
            st.metric("Avg Price Difference", f"{avg_diff:+.1f}%")
        with m3:
            st.metric("Price Alerts", len(result.get("alerts", [])))
        
        # Price comparison
        st.markdown('<h3 style="color: #e94560;"> Price Comparison</h3>', unsafe_allow_html=True)
        price_diffs = result.get("price_differences", [])
        if price_diffs:
            for diff in price_diffs:
                diff_pct = diff.get('difference_pct', 0)
                if diff_pct < -10:
                    card_class = "alert-high"
                elif diff_pct > 10:
                    card_class = "alert-success"
                else:
                    card_class = "alert-medium"
                
                st.markdown(f'''
                <div class="{card_class}">
                <strong>{diff.get('our_product')}</strong><br/>
                Our Price: \ | Competitor: \ | 
                Difference: {diff_pct:+.1f}%
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info(" Click 'Run Agent' to compare prices with competitors")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Customer Minder Agent
with tabs[4]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #9b59b6;"> Customer Analytics Agent</h2>
    <p style="color: #b0b0b0;">Analyzes customer data and order patterns</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_customer"):
            with st.spinner("Analyzing customers..."):
                run_agent("CustomerMinderAgent")
    
    result = st.session_state.agent_results.get("CustomerMinderAgent")
    if result and result.get("status") == "success":
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Customers", result.get("total_customers", 0))
        with m2:
            st.metric("Regions", len(result.get("customers_by_region", {})))
        with m3:
            top_customers = result.get("top_customers", [])
            total_top_spent = sum(c.get("total_spent", 0) for c in top_customers)
            st.metric("Top Customer Value", f"\")
        
        # Top customers
        st.markdown('<h3 style="color: #9b59b6;"> Top Customers by Spending</h3>', unsafe_allow_html=True)
        top_customers = result.get("top_customers", [])[:5]
        if top_customers:
            for i, customer in enumerate(top_customers, 1):
                st.markdown(f'''
                <div class="card-purple" style="margin: 8px 0;">
                <strong>#{i} {customer.get('name')}</strong><br/>
                 {customer.get('email')}<br/>
                 Total Spent: \
                </div>
                ''', unsafe_allow_html=True)
        
        # Region breakdown
        st.markdown('<h3 style="color: #9b59b6;"> Customers by Region</h3>', unsafe_allow_html=True)
        regions = result.get("customers_by_region", {})
        if regions:
            sorted_regions = dict(sorted(regions.items(), key=lambda x: x[1], reverse=True)[:10])
            st.bar_chart(sorted_regions)
    else:
        st.info(" Click 'Run Agent' to analyze customer data")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Supplier Minder Agent
with tabs[5]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="color: #1abc9c;"> Supplier Monitor Agent</h2>
    <p style="color: #b0b0b0;">Monitors supplier activity and inventory</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Run Agent", key="run_supplier"):
            with st.spinner("Monitoring suppliers..."):
                run_agent("SupplierMinderAgent")
    
    result = st.session_state.agent_results.get("SupplierMinderAgent")
    if result and result.get("status") == "success":
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Suppliers Monitored", result.get("suppliers_monitored", 0))
        with m2:
            st.metric("Products Tracked", result.get("products_tracked", 0))
        with m3:
            st.metric("Inventory Alerts", len(result.get("inventory_alerts", [])))
        
        # Supplier status table
        st.markdown('<h3 style="color: #1abc9c;"> Supplier Performance</h3>', unsafe_allow_html=True)
        supplier_status = result.get("supplier_status", [])[:10]
        if supplier_status:
            st.dataframe(supplier_status, use_container_width=True)
        
        # Inventory alerts
        alerts = result.get("inventory_alerts", [])
        if alerts:
            st.markdown('<h3 style="color: #f39c12;"> Inventory Alerts</h3>', unsafe_allow_html=True)
            for alert in alerts:
                priority = alert.get("priority", "medium")
                card_class = "alert-high" if priority == "high" else "alert-medium"
                icon = "" if priority == "high" else ""
                st.markdown(f'''
                <div class="{card_class}">
                {icon} <strong>{alert.get('supplier')}</strong>: {alert.get('issue')}
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info(" Click 'Run Agent' to monitor supplier inventory")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 7: Overview
with tabs[6]:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('''
    <h2 style="background: linear-gradient(135deg, #e94560, #ff6b6b, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
     Dashboard Overview
    </h2>
    ''', unsafe_allow_html=True)
    
    if not st.session_state.agent_results:
        st.info(" Run agents from individual tabs or click 'Run ALL Agents' in the sidebar to see the overview")
    else:
        # Summary cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('''
            <div class="card-blue">
            <h3> Financial Summary</h3>
            ''', unsafe_allow_html=True)
            order_result = st.session_state.agent_results.get("OrderProcessingAgent", {})
            if order_result.get("status") == "success":
                st.metric("Total Revenue", f"\")
                st.metric("Orders Processed", order_result.get("orders_processed", 0))
            else:
                st.info("Run Order Processing Agent")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="card-green">
            <h3> Inventory Summary</h3>
            ''', unsafe_allow_html=True)
            product_result = st.session_state.agent_results.get("ProductAgent", {})
            supplier_result = st.session_state.agent_results.get("SupplierMinderAgent", {})
            if product_result.get("status") == "success":
                st.metric("Products", product_result.get("total_products", 0))
                st.metric("Avg Rating", f" {product_result.get('avg_rating', 0):.2f}")
            if supplier_result.get("status") == "success":
                st.metric("Suppliers", supplier_result.get("suppliers_monitored", 0))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('''
            <div class="card-purple">
            <h3> Competition & Customers</h3>
            ''', unsafe_allow_html=True)
            comp_result = st.session_state.agent_results.get("CompetitionMinderAgent", {})
            cust_result = st.session_state.agent_results.get("CustomerMinderAgent", {})
            if comp_result.get("status") == "success":
                st.metric("Price Diff vs Competition", f"{comp_result.get('avg_price_diff_pct', 0):+.1f}%")
            if cust_result.get("status") == "success":
                st.metric("Customers Analyzed", cust_result.get("total_customers", 0))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # All alerts summary
        st.markdown("---")
        st.markdown('<h3 style="color: #e94560;"> All Active Alerts</h3>', unsafe_allow_html=True)
        
        all_alerts = []
        for agent_key, result in st.session_state.agent_results.items():
            if result and result.get("status") == "success":
                alerts = result.get("alerts", []) + result.get("inventory_alerts", [])
                for alert in alerts:
                    alert["source"] = agent_key
                    all_alerts.append(alert)
        
        if all_alerts:
            for alert in all_alerts[:10]:
                st.markdown(f'''
                <div class="alert-medium">
                 <strong>{alert.get('source')}</strong>: {alert.get('issue', alert.get('error', 'Unknown'))}
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="alert-success">
             No critical alerts at this time
            </div>
            ''', unsafe_allow_html=True)
        
        # Last run times
        st.markdown("---")
        st.markdown('<h3 style="color: #00b894;"> Agent Run Times</h3>', unsafe_allow_html=True)
        if st.session_state.last_run:
            for agent, run_time in st.session_state.last_run.items():
                name, _, color = AGENT_FUNCTIONS.get(agent, (agent, None, "#ffffff"))
                st.markdown(f'''
                <p style="color: {color};"> <strong>{name}</strong>: Last run at {run_time}</p>
                ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('''
<div style="text-align: center; padding: 20px;">
    <p style="color: #b0b0b0;">Touch Window AI Agents Dashboard | Powered by Streamlit</p>
    <p style="color: #666;">Data Sources: DummyJSON, FakeStoreAPI, JSONPlaceholder</p>
    <p><a href="https://github.com/Dsarikrishna/touchwindowagents" style="color: #e94560;"> GitHub Repository</a></p>
</div>
''', unsafe_allow_html=True)
