# 🚀 Touch Window AI Agents

Enterprise-grade AI automation system powered by Azure Functions with dual dashboards for technical and business users.

## ✨ Features

### 🤖 Six Intelligent AI Agents

1. **📦 ProductAgent** - Analyzes product catalog, pricing, ratings, and inventory
2. **🎯 CompetitionMinderAgent** - Monitors competitor pricing and market positioning
3. **👥 CustomerMinderAgent** - Tracks customer behavior, spending patterns, and regional insights
4. **⚡ EfficiencyAgent** - Monitors system health, API performance, and response times
5. **🚚 SupplierMinderAgent** - Evaluates supplier reliability and inventory levels
6. **📋 OrderProcessingAgent** - Processes orders, calculates margins, and identifies issues

### 📊 Dual Dashboard System

#### Admin Dashboard (Port 8501)
- **Technical Interface** - Full control panel for developers and system administrators
- **Detailed JSON Responses** - Complete data access for debugging and analysis
- **Individual & Batch Execution** - Run agents one at a time or all together
- **System Monitoring** - Real-time status checks and error tracking

#### User Dashboard (Port 8502)
- **Business-Friendly Interface** - Simplified view for non-technical users
- **Visual Summaries** - Key metrics and insights at a glance
- **Progress Tracking** - Real-time feedback on agent execution
- **Help Documentation** - Built-in guidance and explanations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Environment                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Azurite   │  │   Functions  │  │   Dashboards  │  │
│  │   Storage   │←─│  (12 Total)  │←─│   Admin/User  │  │
│  │  Emulator   │  │              │  │               │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│   Ports:          Port: 7071         Ports: 8501/8502  │
│   10000-10002                                           │
└─────────────────────────────────────────────────────────┘
```

### Function Types
- **6 Timer-Triggered Functions** - Scheduled automatic execution
- **6 HTTP-Triggered Functions** - Manual execution via API/Dashboard

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (for cloning the repository)
- 2GB free RAM
- Ports 7071, 8501, 8502, 10000-10002 available

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Dsarikrishna/touchwindowagents.git
cd touchwindowagents
```

2. **Start all services**
```bash
docker-compose up --build
```

3. **Access the dashboards**
- **Admin Dashboard**: http://localhost:8501
- **User Dashboard**: http://localhost:8502
- **Functions API**: http://localhost:7071

## 📖 Usage Guide

### For Administrators

1. Open Admin Dashboard at http://localhost:8501
2. Check system status at the top
3. Use "🚀 Trigger All Agents" for full system check
4. Or trigger individual agents for specific analysis
5. View detailed JSON responses for debugging

### For Business Users

1. Open User Dashboard at http://localhost:8502
2. Click "Run All Checks" for complete business overview
3. Or use individual tools for specific insights
4. View summaries with key metrics
5. Expand for detailed results when needed

### Via API (Advanced)

```bash
# Trigger individual agents
curl -X POST http://localhost:7071/api/TriggerProductAgent

# Get results
curl http://localhost:7071/api/TriggerProductAgent
```

## 🔧 Configuration

### Environment Variables

```bash
# Functions URL (for dashboards)
FUNCTIONS_URL=http://localhost:7071

# Azure Storage (automatically configured for local dev)
AzureWebJobsStorage=UseDevelopmentStorage=true
```

### Scheduling

Agents run automatically on schedule:
- **Weekly Agents** (Mon 2:00 AM): Product, Competition, Customer, Efficiency, Supplier
- **Hourly Agent**: Order Processing

## 🏛️ Project Structure

```
touchwindowagents/
├── ProductAgent/              # Product analysis timer function
├── CompetitionMinderAgent/    # Competition monitoring timer function
├── CustomerMinderAgent/       # Customer analytics timer function
├── EfficiencyAgent/           # System efficiency timer function
├── SupplierMinderAgent/       # Supplier monitoring timer function
├── OrderProcessingAgent/      # Order processing timer function
├── TriggerProductAgent/       # HTTP trigger wrapper
├── TriggerCompetitionMinderAgent/
├── TriggerCustomerMinderAgent/
├── TriggerEfficiencyAgent/
├── TriggerOrderProcessingAgent/
├── TriggerSupplierMinderAgent/
├── shared/
│   └── agents.py              # Core agent logic
├── dashboard.py               # Admin dashboard
├── user_dashboard.py          # User-friendly dashboard
├── docker-compose.yml         # Multi-container orchestration
├── Dockerfile                 # Azure Functions container
├── Dockerfile.dashboard       # Admin dashboard container
├── Dockerfile.user_dashboard  # User dashboard container
├── requirements.txt           # Python dependencies
└── README-USAGE.md           # This file
```

## 🔌 API Endpoints

### HTTP Trigger Endpoints (POST/GET)
- `/api/TriggerProductAgent`
- `/api/TriggerCompetitionMinderAgent`
- `/api/TriggerCustomerMinderAgent`
- `/api/TriggerEfficiencyAgent`
- `/api/TriggerSupplierMinderAgent`
- `/api/TriggerOrderProcessingAgent`

All endpoints return JSON with:
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "..."
}
```

## 📊 Data Sources

Agents fetch data from public APIs:
- **DummyJSON** - Order and cart data
- **FakeStoreAPI** - Product catalog
- **JSONPlaceholder** - User and customer data

## 🛠️ Development

### Running Locally (Without Docker)

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Install Python dependencies
pip install -r requirements.txt

# Start Functions
func start

# Start Admin Dashboard (separate terminal)
streamlit run dashboard.py

# Start User Dashboard (separate terminal)
streamlit run user_dashboard.py --server.port=8502
```

### Adding New Agents

1. Create timer-triggered function directory
2. Add HTTP trigger wrapper
3. Implement agent logic in `shared/agents.py`
4. Update dashboards to include new agent
5. Rebuild containers

## 🐛 Troubleshooting

### Dashboard Shows "System Offline"
- Check if Docker containers are running: `docker ps`
- Restart: `docker-compose restart`

### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :8501

# Stop containers and restart
docker-compose down
docker-compose up
```

### Agents Return Errors
- Check logs: `docker-compose logs functions`
- Verify internet connection (agents fetch from APIs)
- Restart: `docker-compose restart functions`

## 📦 Deployment

### Deploy to Azure

1. Create Azure Function App
2. Configure Application Settings
3. Deploy using Azure Functions extension or CLI
4. Deploy dashboards to Azure App Service

### Environment Variables for Production
```
FUNCTIONS_URL=https://your-function-app.azurewebsites.net
AzureWebJobsStorage=<your-storage-connection-string>
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- **Dsarikrishna** - [GitHub](https://github.com/Dsarikrishna)

## 🙏 Acknowledgments

- Azure Functions team for the Python runtime
- Streamlit for the amazing dashboard framework
- Public API providers (DummyJSON, FakeStoreAPI, JSONPlaceholder)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

---

**Repository**: https://github.com/Dsarikrishna/touchwindowagents

**Last Updated**: December 2025
