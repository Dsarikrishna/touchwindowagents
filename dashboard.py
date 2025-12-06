import streamlit as st
import requests
import os
from datetime import datetime
import time

# Configuration
FUNCTIONS_URL = os.getenv("FUNCTIONS_URL", "http://localhost:7071")

# Initialize session state for performance metrics
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {
        'total_executions': 0,
        'successful_executions': 0,
        'failed_executions': 0,
        'total_execution_time': 0,
        'agent_metrics': {},
        'last_execution_times': [],
        'execution_history': []  # Store execution history with timestamps
    }

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
status_col1, status_col2 = st.columns(2)

with status_col1:
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

with status_col2:
    # Display overall performance metrics
    metrics = st.session_state.performance_metrics
    if metrics['total_executions'] > 0:
        success_rate = (metrics['successful_executions'] / metrics['total_executions']) * 100
        avg_time = metrics['total_execution_time'] / metrics['total_executions']
        st.metric("Success Rate", f"{success_rate:.1f}%", 
                 delta=f"{metrics['successful_executions']}/{metrics['total_executions']} runs")
        st.metric("Avg Execution Time", f"{avg_time:.2f}s")
    else:
        st.info("📊 No execution data yet - trigger agents to see metrics")

st.markdown("---")

# Performance Metrics Dashboard
st.subheader("📊 Performance Metrics")

perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

with perf_col1:
    st.metric("Total Executions", st.session_state.performance_metrics['total_executions'])

with perf_col2:
    st.metric("Successful", st.session_state.performance_metrics['successful_executions'], 
             delta_color="normal")

with perf_col3:
    st.metric("Failed", st.session_state.performance_metrics['failed_executions'], 
             delta_color="inverse")

with perf_col4:
    if st.session_state.performance_metrics['last_execution_times']:
        last_time = st.session_state.performance_metrics['last_execution_times'][-1]
        st.metric("Last Run Time", f"{last_time:.2f}s")
    else:
        st.metric("Last Run Time", "N/A")

# Agent-specific metrics
if st.session_state.performance_metrics['agent_metrics']:
    with st.expander("🔍 Agent-Specific Metrics"):
        agent_cols = st.columns(3)
        for idx, (agent_name, metrics) in enumerate(st.session_state.performance_metrics['agent_metrics'].items()):
            with agent_cols[idx % 3]:
                st.markdown(f"**{agent_name}**")
                st.caption(f"Runs: {metrics['runs']}")
                st.caption(f"Success: {metrics['success']}/{metrics['runs']}")
                if metrics['runs'] > 0:
                    agent_success_rate = (metrics['success'] / metrics['runs']) * 100
                    avg_agent_time = metrics['total_time'] / metrics['runs']
                    st.caption(f"Success Rate: {agent_success_rate:.1f}%")
                    st.caption(f"Avg Time: {avg_agent_time:.2f}s")
                if 'last_execution' in metrics and metrics['last_execution']:
                    st.caption(f"🕒 Last run: {metrics['last_execution']}")

st.markdown("---")

# Agent controls
st.subheader("🎮 Agent Controls")

# Trigger All Agents button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Trigger All Agents", use_container_width=True, type="primary"):
        with st.spinner("Triggering all agents..."):
            results = {}
            start_time = time.time()
            
            for agent in agents:
                try:
                    agent_start = time.time()
                    url = f"{FUNCTIONS_URL}/api/Trigger{agent['name']}"
                    response = requests.post(url, json={}, timeout=30)
                    agent_duration = time.time() - agent_start
                    
                    # Update agent-specific metrics
                    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if agent['name'] not in st.session_state.performance_metrics['agent_metrics']:
                        st.session_state.performance_metrics['agent_metrics'][agent['name']] = {
                            'runs': 0, 'success': 0, 'total_time': 0, 'last_execution': None
                        }
                    
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['runs'] += 1
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['total_time'] += agent_duration
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['last_execution'] = execution_time
                    
                    if response.status_code == 200:
                        results[agent['name']] = {"status": "✅ Success", "data": response.json(), "time": agent_duration, "executed_at": execution_time}
                        st.session_state.performance_metrics['successful_executions'] += 1
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['success'] += 1
                        # Store in execution history
                        st.session_state.performance_metrics['execution_history'].append({
                            'agent': agent['name'], 'timestamp': execution_time, 'status': 'success', 'duration': agent_duration
                        })
                    else:
                        results[agent['name']] = {"status": f"❌ Failed ({response.status_code})", "error": response.text, "time": agent_duration, "executed_at": execution_time}
                        st.session_state.performance_metrics['failed_executions'] += 1
                        st.session_state.performance_metrics['execution_history'].append({
                            'agent': agent['name'], 'timestamp': execution_time, 'status': 'failed', 'duration': agent_duration
                        })
                except Exception as e:
                    agent_duration = time.time() - agent_start
                    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    results[agent['name']] = {"status": "❌ Error", "error": str(e), "time": agent_duration, "executed_at": execution_time}
                    st.session_state.performance_metrics['failed_executions'] += 1
                    
                    if agent['name'] not in st.session_state.performance_metrics['agent_metrics']:
                        st.session_state.performance_metrics['agent_metrics'][agent['name']] = {
                            'runs': 0, 'success': 0, 'total_time': 0, 'last_execution': None
                        }
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['runs'] += 1
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['total_time'] += agent_duration
                    st.session_state.performance_metrics['agent_metrics'][agent['name']]['last_execution'] = execution_time
                    st.session_state.performance_metrics['execution_history'].append({
                        'agent': agent['name'], 'timestamp': execution_time, 'status': 'error', 'duration': agent_duration
                    })
            
            total_duration = time.time() - start_time
            st.session_state.performance_metrics['total_executions'] += len(agents)
            st.session_state.performance_metrics['total_execution_time'] += total_duration
            st.session_state.performance_metrics['last_execution_times'].append(total_duration)
            
            # Keep only last 10 execution times
            if len(st.session_state.performance_metrics['last_execution_times']) > 10:
                st.session_state.performance_metrics['last_execution_times'].pop(0)
            
            # Display results
            st.success(f"All agents have been triggered! Total time: {total_duration:.2f}s")
            st.balloons()
            
            for agent_name, result in results.items():
                executed_at = result.get('executed_at', 'N/A')
                status_text = f"{result['status']} - {agent_name} ({result.get('time', 0):.2f}s) - 🕒 {executed_at}"
                with st.expander(status_text):
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
            
            # Show agent-specific metrics if available
            if agent['name'] in st.session_state.performance_metrics['agent_metrics']:
                agent_metrics = st.session_state.performance_metrics['agent_metrics'][agent['name']]
                if agent_metrics['runs'] > 0:
                    success_rate = (agent_metrics['success'] / agent_metrics['runs']) * 100
                    avg_time = agent_metrics['total_time'] / agent_metrics['runs']
                    st.caption(f"⚡ Success: {success_rate:.0f}% | Avg: {avg_time:.1f}s")
            
            if st.button(f"▶️ Trigger", key=f"trigger_{agent['name']}", use_container_width=True):
                with st.spinner(f"Triggering {agent['name']}..."):
                    agent_start = time.time()
                    try:
                        url = f"{FUNCTIONS_URL}/api/Trigger{agent['name']}"
                        response = requests.post(url, json={}, timeout=30)
                        agent_duration = time.time() - agent_start
                        
                        # Update metrics
                        execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if agent['name'] not in st.session_state.performance_metrics['agent_metrics']:
                            st.session_state.performance_metrics['agent_metrics'][agent['name']] = {
                                'runs': 0, 'success': 0, 'total_time': 0, 'last_execution': None
                            }
                        
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['runs'] += 1
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['total_time'] += agent_duration
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['last_execution'] = execution_time
                        st.session_state.performance_metrics['total_executions'] += 1
                        st.session_state.performance_metrics['total_execution_time'] += agent_duration
                        st.session_state.performance_metrics['last_execution_times'].append(agent_duration)
                        
                        if len(st.session_state.performance_metrics['last_execution_times']) > 10:
                            st.session_state.performance_metrics['last_execution_times'].pop(0)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.performance_metrics['successful_executions'] += 1
                            st.session_state.performance_metrics['agent_metrics'][agent['name']]['success'] += 1
                            st.session_state.performance_metrics['execution_history'].append({
                                'agent': agent['name'], 'timestamp': execution_time, 'status': 'success', 'duration': agent_duration
                            })
                            st.success(f"✅ {agent['name']} executed successfully in {agent_duration:.2f}s! 🕒 {execution_time}")
                            st.json(result)
                            st.balloons()
                        else:
                            st.session_state.performance_metrics['failed_executions'] += 1
                            st.session_state.performance_metrics['execution_history'].append({
                                'agent': agent['name'], 'timestamp': execution_time, 'status': 'failed', 'duration': agent_duration
                            })
                            st.error(f"❌ Failed: Status {response.status_code} (took {agent_duration:.2f}s) 🕒 {execution_time}")
                            st.code(response.text)
                    except Exception as e:
                        agent_duration = time.time() - agent_start
                        st.session_state.performance_metrics['failed_executions'] += 1
                        st.session_state.performance_metrics['total_executions'] += 1
                        st.session_state.performance_metrics['total_execution_time'] += agent_duration
                        
                        execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if agent['name'] not in st.session_state.performance_metrics['agent_metrics']:
                            st.session_state.performance_metrics['agent_metrics'][agent['name']] = {
                                'runs': 0, 'success': 0, 'total_time': 0, 'last_execution': None
                            }
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['runs'] += 1
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['total_time'] += agent_duration
                        st.session_state.performance_metrics['agent_metrics'][agent['name']]['last_execution'] = execution_time
                        st.session_state.performance_metrics['execution_history'].append({
                            'agent': agent['name'], 'timestamp': execution_time, 'status': 'error', 'duration': agent_duration
                        })
                        
                        st.error(f"❌ Error: {str(e)} (took {agent_duration:.2f}s) 🕒 {execution_time}")
            
            st.markdown("---")

# Execution History
st.markdown("---")
st.subheader("📊 Execution History")

if st.session_state.performance_metrics['execution_history']:
    # Show last 20 executions
    recent_history = st.session_state.performance_metrics['execution_history'][-20:]
    recent_history.reverse()  # Show most recent first
    
    for idx, execution in enumerate(recent_history):
        status_icon = "✅" if execution['status'] == 'success' else "❌"
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        with col1:
            st.text(execution['agent'])
        with col2:
            st.text(f"🕒 {execution['timestamp']}")
        with col3:
            st.text(f"{status_icon} {execution['status'].title()}")
        with col4:
            st.text(f"{execution['duration']:.2f}s")
else:
    st.info("No execution history yet. Trigger agents to see execution records.")

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
