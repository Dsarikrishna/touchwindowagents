"""
Touch Window AI Agents Dashboard
Enhanced dashboard showing real-time agent data and results.
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

# Custom CSS
st.markdown('''
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 5px 0;
    }
    .alert-high { background-color: #ff4b4b; color: white; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .alert-medium { background-color: #ffa726; color: white; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .alert-low { background-color: #66bb6a; color: white; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .success-box { background-color: #4caf50; color: white; padding: 15px; border-radius: 10px; }
    .info-box { background-color: #2196f3; color: white; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; 
        border-radius: 5px; 
        padding: 10px 20px;
    }
</style>
''', unsafe_allow_html=True)

# Header
st.title(" Touch Window AI Agents Dashboard")
st.markdown("Real-time monitoring and analytics from your AI agents")
st.markdown("---")

# Sidebar
st.sidebar.title(" Dashboard Controls")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Agent function mapping
AGENT_FUNCTIONS = {
    "OrderProcessingAgent": (" Order Processing", run_order_processing_agent if AGENTS_AVAILABLE else None),
    "ProductAgent": (" Product Analysis", run_product_agent if AGENTS_AVAILABLE else None),
    "EfficiencyAgent": (" System Efficiency", run_efficiency_agent if AGENTS_AVAILABLE else None),
    "CompetitionMinderAgent": (" Competition Monitor", run_competition_minder_agent if AGENTS_AVAILABLE else None),
    "CustomerMinderAgent": (" Customer Analytics", run_customer_minder_agent if AGENTS_AVAILABLE else None),
    "SupplierMinderAgent": (" Supplier Monitor", run_supplier_minder_agent if AGENTS_AVAILABLE else None),
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
    
    name, func = AGENT_FUNCTIONS[agent_key]
    if func:
        result = func()
        st.session_state.agent_results[agent_key] = result
        st.session_state.last_run[agent_key] = datetime.now().strftime('%H:%M:%S')
        return result
    return None

def run_all_agents():
    """Run all agents and store results"""
    results = {}
    for agent_key in AGENT_FUNCTIONS.keys():
        results[agent_key] = run_agent(agent_key)
    return results

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
st.sidebar.markdown("###  Quick Stats")

# Show quick stats in sidebar if we have results
if st.session_state.agent_results:
    order_result = st.session_state.agent_results.get("OrderProcessingAgent", {})
    if order_result.get("status") == "success":
        st.sidebar.metric("Total Revenue", f"")
    
    product_result = st.session_state.agent_results.get("ProductAgent", {})
    if product_result.get("status") == "success":
        st.sidebar.metric("Products Tracked", product_result.get('total_products', 0))
    
    supplier_result = st.session_state.agent_results.get("SupplierMinderAgent", {})
    if supplier_result.get("status") == "success":
        st.sidebar.metric("Suppliers", supplier_result.get('suppliers_monitored', 0))

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Repository:** [GitHub](https://github.com/Dsarikrishna/touchwindowagents)
""")

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
    st.header(" Order Processing Agent")
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
            st.metric("Total Revenue", f"")
        with m3:
            avg_margin = 0
            if result.get("order_details"):
                margins = [o.get("margin_pct", 0) for o in result["order_details"]]
                avg_margin = sum(margins) / len(margins) if margins else 0
            st.metric("Avg Margin", f"{avg_margin:.1f}%")
        with m4:
            st.metric("Alerts", len(result.get("alerts", [])))
        
        # Order details table
        st.subheader(" Order Details")
        if result.get("order_details"):
            order_data = result["order_details"][:10]  # Show first 10
            st.dataframe(order_data, use_container_width=True)
        
        # Alerts
        if result.get("alerts"):
            st.subheader(" Alerts")
            for alert in result["alerts"]:
                st.warning(f"Order #{alert.get('order_id')}: {alert.get('issue')} ({alert.get('margin')})")
    else:
        st.info(" Click 'Run Agent' to fetch order data from DummyJSON API")

# Tab 2: Product Agent
with tabs[1]:
    st.header(" Product Analysis Agent")
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
            st.metric("Price Range", f" - ")
        with m4:
            st.metric("Categories", len(result.get("categories", {})))
        
        # Categories breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(" Products by Category")
            categories = result.get("categories", {})
            if categories:
                st.bar_chart(categories)
        
        with col2:
            st.subheader(" Top Rated Products")
            top_rated = result.get("top_rated", [])[:5]
            for product in top_rated:
                st.markdown(f"**{product.get('title', 'N/A')}**")
                st.markdown(f"Rating:  {product.get('rating')} | Price: ")
                st.markdown("---")
    else:
        st.info(" Click 'Run Agent' to analyze products from FakeStoreAPI")

# Tab 3: Efficiency Agent
with tabs[2]:
    st.header(" System Efficiency Agent")
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
        st.subheader(" Endpoint Health")
        for endpoint in result.get("endpoints_checked", []):
            status_icon = "" if endpoint.get("healthy") else ""
            response_time = endpoint.get("response_time_ms", 0)
            time_color = "green" if response_time < 500 else "orange" if response_time < 1000 else "red"
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"{status_icon} **{endpoint.get('name')}**")
            with col2:
                st.markdown(f"Status: {endpoint.get('status_code')}")
            with col3:
                st.markdown(f" {response_time:.0f}ms")
        
        # Alerts
        if result.get("alerts"):
            st.subheader(" Performance Alerts")
            for alert in result["alerts"]:
                st.error(f"{alert.get('endpoint')}: {alert.get('issue')}")
    else:
        st.info(" Click 'Run Agent' to check system health across APIs")

# Tab 4: Competition Minder Agent
with tabs[3]:
    st.header(" Competition Monitor Agent")
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
            st.metric("Avg Price Difference", f"{avg_diff:+.1f}%", 
                     delta=f"{'Cheaper' if avg_diff < 0 else 'More expensive'}")
        with m3:
            st.metric("Price Alerts", len(result.get("alerts", [])))
        
        # Price comparison table
        st.subheader(" Price Comparison")
        price_diffs = result.get("price_differences", [])
        if price_diffs:
            for diff in price_diffs:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"**{diff.get('our_product')}**")
                with col2:
                    st.markdown(f"Our: ")
                with col3:
                    st.markdown(f"Comp: ")
                with col4:
                    diff_pct = diff.get('difference_pct', 0)
                    color = "red" if diff_pct < -10 else "green" if diff_pct > 10 else "gray"
                    st.markdown(f":{color}[{diff_pct:+.1f}%]")
        
        # Alerts
        if result.get("alerts"):
            st.subheader(" Competitor Price Alerts")
            for alert in result["alerts"]:
                st.error(f" {alert.get('product')}: {alert.get('issue')}")
    else:
        st.info(" Click 'Run Agent' to compare prices with competitors")

# Tab 5: Customer Minder Agent
with tabs[4]:
    st.header(" Customer Analytics Agent")
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
            st.metric("Top Customer Value", f"")
        
        # Top customers
        st.subheader(" Top Customers by Spending")
        top_customers = result.get("top_customers", [])[:5]
        if top_customers:
            for i, customer in enumerate(top_customers, 1):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.markdown(f"### #{i}")
                with col2:
                    st.markdown(f"**{customer.get('name')}**")
                    st.markdown(f" {customer.get('email')}")
                with col3:
                    st.metric("Spent", f"")
        
        # Region breakdown
        st.subheader(" Customers by Region")
        regions = result.get("customers_by_region", {})
        if regions:
            # Show top 10 regions
            sorted_regions = dict(sorted(regions.items(), key=lambda x: x[1], reverse=True)[:10])
            st.bar_chart(sorted_regions)
    else:
        st.info(" Click 'Run Agent' to analyze customer data")

# Tab 6: Supplier Minder Agent
with tabs[5]:
    st.header(" Supplier Monitor Agent")
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
        st.subheader(" Supplier Performance")
        supplier_status = result.get("supplier_status", [])[:10]
        if supplier_status:
            st.dataframe(supplier_status, use_container_width=True)
        
        # Inventory alerts
        alerts = result.get("inventory_alerts", [])
        if alerts:
            st.subheader(" Inventory Alerts")
            for alert in alerts:
                priority = alert.get("priority", "medium")
                if priority == "high":
                    st.error(f" {alert.get('supplier')}: {alert.get('issue')}")
                else:
                    st.warning(f" {alert.get('supplier')}: {alert.get('issue')}")
    else:
        st.info(" Click 'Run Agent' to monitor supplier inventory")

# Tab 7: Overview
with tabs[6]:
    st.header(" Dashboard Overview")
    
    if not st.session_state.agent_results:
        st.info(" Run agents from individual tabs or click 'Run ALL Agents' in the sidebar to see the overview")
    else:
        # Summary cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("###  Financial Summary")
            order_result = st.session_state.agent_results.get("OrderProcessingAgent", {})
            if order_result.get("status") == "success":
                st.metric("Total Revenue", f"")
                st.metric("Orders Processed", order_result.get("orders_processed", 0))
            else:
                st.info("Run Order Processing Agent")
        
        with col2:
            st.markdown("###  Inventory Summary")
            product_result = st.session_state.agent_results.get("ProductAgent", {})
            supplier_result = st.session_state.agent_results.get("SupplierMinderAgent", {})
            if product_result.get("status") == "success":
                st.metric("Products", product_result.get("total_products", 0))
                st.metric("Avg Rating", f" {product_result.get('avg_rating', 0):.2f}")
            if supplier_result.get("status") == "success":
                st.metric("Suppliers", supplier_result.get("suppliers_monitored", 0))
        
        with col3:
            st.markdown("###  Competition & Customers")
            comp_result = st.session_state.agent_results.get("CompetitionMinderAgent", {})
            cust_result = st.session_state.agent_results.get("CustomerMinderAgent", {})
            if comp_result.get("status") == "success":
                st.metric("Price Diff vs Competition", f"{comp_result.get('avg_price_diff_pct', 0):+.1f}%")
            if cust_result.get("status") == "success":
                st.metric("Customers Analyzed", cust_result.get("total_customers", 0))
        
        # All alerts summary
        st.markdown("---")
        st.subheader(" All Active Alerts")
        
        all_alerts = []
        for agent_key, result in st.session_state.agent_results.items():
            if result and result.get("status") == "success":
                alerts = result.get("alerts", []) + result.get("inventory_alerts", [])
                for alert in alerts:
                    alert["source"] = agent_key
                    all_alerts.append(alert)
        
        if all_alerts:
            for alert in all_alerts[:10]:
                st.warning(f"**{alert.get('source')}**: {alert.get('issue', alert.get('error', 'Unknown'))}")
        else:
            st.success(" No critical alerts at this time")
        
        # Last run times
        st.markdown("---")
        st.subheader(" Agent Run Times")
        if st.session_state.last_run:
            for agent, run_time in st.session_state.last_run.items():
                name, _ = AGENT_FUNCTIONS.get(agent, (agent, None))
                st.markdown(f"- **{name}**: Last run at {run_time}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Touch Window AI Agents Dashboard | Powered by Streamlit</p>
    <p>Data Sources: DummyJSON, FakeStoreAPI, JSONPlaceholder</p>
    <p><a href='https://github.com/Dsarikrishna/touchwindowagents'>GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
