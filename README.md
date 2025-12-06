# Touch Window AI Agents 🤖

Azure Functions-based AI Agents for Touch Window automation and intelligence.

**No Azure subscription required!** Run with Docker or GitHub Codespaces for free.

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed

### Run with One Command

```bash
# Clone the repository
git clone https://github.com/Dsarikrishna/touchwindowagents.git
cd touchwindowagents

# Start all agents with Docker
docker-compose up
```

That's it! Your agents are now running at `http://localhost:7071` 🎉

### Trigger All Agents

```bash
# In a new terminal
curl -X POST http://localhost:7071/admin/functions/ProductAgent -H "Content-Type: application/json" -d "{}"
curl -X POST http://localhost:7071/admin/functions/CompetitionMinderAgent -H "Content-Type: application/json" -d "{}"
curl -X POST http://localhost:7071/admin/functions/CustomerMinderAgent -H "Content-Type: application/json" -d "{}"
curl -X POST http://localhost:7071/admin/functions/EfficiencyAgent -H "Content-Type: application/json" -d "{}"
curl -X POST http://localhost:7071/admin/functions/SupplierMinderAgent -H "Content-Type: application/json" -d "{}"
curl -X POST http://localhost:7071/admin/functions/OrderProcessingAgent -H "Content-Type: application/json" -d "{}"
```

### Stop the Agents

```bash
docker-compose down
```

---

## 🤖 AI Agents

| Agent | Description | Schedule |
|-------|-------------|----------|
| **ProductAgent** | Monitors and analyzes product data | Weekly (Mon 2AM) |
| **CompetitionMinderAgent** | Tracks competitor activities | Weekly (Mon 2AM) |
| **CustomerMinderAgent** | Customer relationship insights | Weekly (Mon 2AM) |
| **EfficiencyAgent** | Operational efficiency analysis | Weekly (Mon 2AM) |
| **SupplierMinderAgent** | Supplier relationship management | Weekly (Mon 2AM) |
| **OrderProcessingAgent** | Order processing automation | Hourly |

---

## 🌐 Alternative: GitHub Codespaces (Cloud-based)

Run entirely in the cloud without installing anything:

1. Go to this repository on GitHub
2. Click the green **"Code"** button
3. Click **"Create codespace on main"**
4. Wait for setup (~2 min)
5. Run in terminal:
   ```bash
   func start
   ```

**Free tier**: 60 hours/month

---

## 💻 Alternative: Local Development (Windows)

### Prerequisites
- Python 3.12+
- Node.js (for Azurite)
- Azure Functions Core Tools

### Setup

1. **Install Azure Functions Core Tools**
   ```powershell
   winget install Microsoft.Azure.FunctionsCoreTools
   ```

2. **Install Azurite**
   ```powershell
   npm install -g azurite
   ```

3. **Clone and setup**
   ```powershell
   git clone https://github.com/Dsarikrishna/touchwindowagents.git
   cd touchwindowagents
   pip install -r requirements.txt
   ```

4. **Create local.settings.json**
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python"
     }
   }
   ```

5. **Run** (double-click or run in terminal)
   ```
   start-local.bat
   ```

---

## 📁 Project Structure

```
touchwindowagents/
├── .devcontainer/          # GitHub Codespaces config
├── .github/workflows/      # CI/CD with Docker
├── CompetitionMinderAgent/
├── CustomerMinderAgent/
├── EfficiencyAgent/
├── OrderProcessingAgent/
├── ProductAgent/
├── SupplierMinderAgent/
├── shared/                 # Shared agent utilities
├── docker-compose.yml      # 🐳 One-command deployment
├── Dockerfile
├── requirements.txt
├── start-local.bat         # Windows local runner
└── trigger-all-agents.bat  # Windows agent trigger
```

---

## 🔧 Configuration

Environment variables can be set in:
- `docker-compose.yml` for Docker
- `local.settings.json` for local development

---

## 📝 License

MIT License
