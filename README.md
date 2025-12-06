# Touch Window AI Agents

Azure Functions-based AI Agents for Touch Window automation and intelligence.

## 🤖 Agents

| Agent | Description | Schedule |
|-------|-------------|----------|
| **ProductAgent** | Monitors and analyzes product data | Weekly (Mon 2AM) |
| **CompetitionMinderAgent** | Tracks competitor activities | Weekly (Mon 2AM) |
| **CustomerMinderAgent** | Customer relationship insights | Weekly (Mon 2AM) |
| **EfficiencyAgent** | Operational efficiency analysis | Weekly (Mon 2AM) |
| **SupplierMinderAgent** | Supplier relationship management | Weekly (Mon 2AM) |
| **OrderProcessingAgent** | Order processing automation | Hourly |

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Azure Functions Core Tools v4
- Azurite (for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dsarikrishna/touchwindowagents.git
   cd touchwindowagents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create local.settings.json**
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python"
     }
   }
   ```

4. **Start Azurite (Azure Storage Emulator)**
   ```bash
   npx azurite --silent --location ./azurite-data
   ```

5. **Run Azure Functions locally**
   ```bash
   func start
   ```

### Manual Trigger (for testing)

```powershell
# Trigger a specific agent
Invoke-WebRequest -Uri "http://localhost:7071/admin/functions/ProductAgent" -Method Post -ContentType "application/json" -Body '{"input":"test"}' -UseBasicParsing
```

## 📦 Deployment

### Deploy to Azure

1. Create an Azure Function App in the Azure Portal
2. Download the Publish Profile from the Function App
3. Add the publish profile as a GitHub Secret named `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
4. Update the `AZURE_FUNCTIONAPP_NAME` in `.github/workflows/azure-functions-deploy.yml`
5. Push to `main` branch to trigger deployment

### GitHub Actions

The repository includes a GitHub Actions workflow that automatically deploys to Azure Functions on push to the `main` branch.

## 📁 Project Structure

```
touchwindowagents/
├── .github/
│   └── workflows/
│       └── azure-functions-deploy.yml
├── CompetitionMinderAgent/
│   ├── __init__.py
│   └── function.json
├── CustomerMinderAgent/
│   ├── __init__.py
│   └── function.json
├── EfficiencyAgent/
│   ├── __init__.py
│   └── function.json
├── OrderProcessingAgent/
│   ├── __init__.py
│   └── function.json
├── ProductAgent/
│   ├── __init__.py
│   └── function.json
├── SupplierMinderAgent/
│   ├── __init__.py
│   └── function.json
├── shared/
│   ├── __init__.py
│   └── agents.py
├── host.json
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Each agent can be configured via environment variables in the Azure Function App settings or `local.settings.json` for local development.

## 📝 License

MIT License
