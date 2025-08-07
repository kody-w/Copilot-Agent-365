# Copilot Agent 365 - Enterprise AI Assistant

## 🚀 One-Click Deploy to Azure

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2FCopilot-Agent-365%2Fmain%2Fazuredeploy.json)

Click once. Azure creates everything. Copy the deployment command. Done!

## ✨ Features

- 🧠 **Azure OpenAI GPT-4** - Advanced AI responses with context understanding
- 💾 **Persistent Memory System** - User-specific and shared memory storage
- 🔐 **Enterprise Security** - Function-level authentication and HTTPS only
- 📊 **Full Monitoring** - Application Insights integration
- ⚡ **Serverless Architecture** - Auto-scaling Azure Functions
- 🎯 **Agent System** - Extensible architecture for custom capabilities
- 🎨 **Beautiful Web UI** - Modern chat interface included

## 📋 Prerequisites

- ✅ **Azure Account** - [Get free trial](https://azure.microsoft.com/free/)
- ✅ **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- ✅ **Python 3.11** - [Download Python](https://www.python.org/downloads/)
- ✅ **Azure Functions Core Tools** - Install with: `npm install -g azure-functions-core-tools@4`

## 🎯 Quick Start Guide

### Step 1: Deploy Azure Resources
1. Click the **"Deploy to Azure"** button above
2. Fill in required parameters (or use defaults)
3. Click **"Review + Create"** then **"Create"**
4. Wait 5-10 minutes for deployment to complete
5. Go to **Outputs** tab and copy the `quickDeployCommand`

### Step 2: Deploy the Function Code
Run the command from Step 1 outputs, or manually:

```bash
# Clone and deploy
git clone https://github.com/kody-w/Copilot-Agent-365.git
cd Copilot-Agent-365
zip -r deploy.zip . -x "*.git*"
az functionapp deployment source config-zip \
    --resource-group <your-rg> \
    --name <your-function-app> \
    --src deploy.zip
```

### Step 3: Test Your Function
Use the `testCommandWithKey` from outputs or get your function URL with key from the `functionUrlWithKey` output.

## 💻 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kody-w/Copilot-Agent-365.git
cd Copilot-Agent-365
```

### 2. Set Up Python Environment
```bash
# Create virtual environment with Python 3.11
python3.11 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Fix Dependencies (if needed)
```bash
# If you encounter Pydantic errors, fix with:
pip uninstall pydantic openai -y
pip install pydantic==1.10.13 openai==1.12.0
```

### 4. Create local.settings.json
After deploying to Azure, copy the `localSettingsJson` output from the ARM template, or create manually:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_OPENAI_API_KEY": "your-key-here",
    "AZURE_OPENAI_ENDPOINT": "https://your-resource.openai.azure.com/",
    "AZURE_OPENAI_API_VERSION": "2024-02-01",
    "AZURE_FILES_SHARE_NAME": "azfbusinessbot3c92ab",
    "ASSISTANT_NAME": "Copilot Agent 365",
    "CHARACTERISTIC_DESCRIPTION": "Enterprise AI assistant"
  }
}
```

### 5. Start Local Development
```bash
# Ensure you're in the project root with activated venv
func start

# For verbose output:
func start --verbose

# To use a different port:
func start --port 7072
```

### 6. Test Locally
```bash
# Test with curl
curl -X POST http://localhost:7071/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "conversation_history": []}'

# Or open client/index.html and point to localhost:7071
```

## 🛠️ Command Line Reference

### Essential Commands

#### Setup Commands
```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Install Azure CLI (macOS)
brew update && brew install azure-cli

# Login to Azure
az login

# Set default subscription
az account set --subscription "Your Subscription Name"
```

#### Development Commands
```bash
# Create Python virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Fix Pydantic issues
pip install pydantic==1.10.13 openai==1.12.0

# Start function locally
func start

# Start with debugging
func start --verbose

# Start on different port
func start --port 7072
```

#### Deployment Commands
```bash
# Create deployment package
zip -r deploy.zip . -x "*.git*" -x ".venv/*" -x "local.settings.json"

# Deploy to Azure Function App
az functionapp deployment source config-zip \
    --resource-group <resource-group> \
    --name <function-app-name> \
    --src deploy.zip

# Deploy directly from GitHub
az functionapp deployment source config \
    --resource-group <resource-group> \
    --name <function-app-name> \
    --repo-url https://github.com/kody-w/Copilot-Agent-365 \
    --branch main \
    --manual-integration

# Restart Function App
az functionapp restart \
    --resource-group <resource-group> \
    --name <function-app-name>
```

#### Testing Commands
```bash
# Test local function
curl -X POST http://localhost:7071/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "conversation_history": []}'

# Test deployed function (with key)
curl -X POST "https://<your-app>.azurewebsites.net/api/businessinsightbot_function?code=<your-key>" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "conversation_history": []}'

# Get function URL with key
az functionapp function show \
    --resource-group <resource-group> \
    --name <function-app-name> \
    --function-name main \
    --query "invokeUrlTemplate" -o tsv

# List function keys
az functionapp function keys list \
    --resource-group <resource-group> \
    --name <function-app-name> \
    --function-name main
```

#### Monitoring Commands
```bash
# Stream live logs
az functionapp log tail \
    --resource-group <resource-group> \
    --name <function-app-name>

# Check deployment status
az functionapp deployment list-publishing-profiles \
    --resource-group <resource-group> \
    --name <function-app-name>

# View app settings
az functionapp config appsettings list \
    --resource-group <resource-group> \
    --name <function-app-name>

# Update app setting
az functionapp config appsettings set \
    --resource-group <resource-group> \
    --name <function-app-name> \
    --settings "KEY=VALUE"
```

## 📁 Repository Structure

```
Copilot-Agent-365/
├── function_app.py            # Azure Function entry point with route handler
├── requirements.txt           # Python dependencies
├── host.json                  # Function host configuration
├── functions.json             # Function bindings configuration
├── agents/                    # AI agent modules
│   ├── __init__.py
│   ├── basic_agent.py        # Base agent class
│   ├── context_memory_agent.py # Memory recall agent
│   └── manage_memory_agent.py  # Memory management agent
├── utils/                     # Utility modules
│   ├── __init__.py
│   └── azure_file_storage.py  # Azure Files integration
├── client/                    # Web interface (optional)
│   └── index.html            # Complete chat UI
├── azuredeploy.json          # ARM template for Azure deployment
├── local.settings.json       # Local configuration (create this)
└── README.md                 # This file
```

## 🎯 Key Features Explained

### Memory System
- **User-Specific Memory**: Each user (identified by GUID) has isolated memory storage
- **Shared Memory**: Common knowledge accessible across all conversations
- **Persistent Storage**: Memories survive function restarts using Azure Files

### Agent Architecture
- **Extensible Design**: Easy to add new capabilities
- **Built-in Agents**:
  - `ContextMemory`: Recalls previous conversations
  - `ManageMemory`: Stores important information
- **Custom Agents**: Create your own by extending `BasicAgent`

### Security & Compliance
- **Function-Level Auth**: Requires function key for API access
- **HTTPS Only**: All communications encrypted
- **CORS Support**: Configurable cross-origin access
- **Azure AD Ready**: Can integrate with Azure Active Directory

## 🛠️ Customization Guide

### Change Assistant Identity
Edit environment variables in Azure Portal or local.settings.json:
```json
{
  "ASSISTANT_NAME": "YourBotName",
  "CHARACTERISTIC_DESCRIPTION": "Your bot's personality"
}
```

### Add Custom Agents
Create new file in `agents/` folder:
```python
from agents.basic_agent import BasicAgent

class MyCustomAgent(BasicAgent):
    def __init__(self):
        self.name = 'MyCustomAgent'
        self.metadata = {
            "name": self.name,
            "description": "What this agent does",
            "parameters": {
                "type": "object",
                "properties": {
                    # Define parameters
                }
            }
        }
        super().__init__(self.name, self.metadata)
    
    def perform(self, **kwargs):
        # Your agent logic here
        return "Agent result"
```

## 🔍 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "No job functions found" | Ensure `function_app.py` is in root with `@app.route` decorator |
| Pydantic import error | Run: `pip install pydantic==1.10.13 openai==1.12.0` |
| Invalid host.json | Recreate with content from this README |
| Port already in use | Use different port: `func start --port 7072` |
| Storage emulator issues | Install Azurite: `npm install -g azurite` then run `azurite` |
| Python version mismatch | Use Python 3.11: `python3.11 -m venv .venv` |

### Quick Fixes

#### Fix All Dependencies
```bash
pip uninstall pydantic openai azure-functions azure-storage-file -y
pip install pydantic==1.10.13 openai==1.12.0 azure-functions==1.18.0 azure-storage-file==2.1.0
```

#### Recreate host.json
```bash
cat > host.json << 'EOF'
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[3.*, 4.0.0)"
  },
  "functionTimeout": "00:10:00"
}
EOF
```

#### Complete Reset
```bash
# Clean everything and start fresh
rm -rf .venv deploy.zip
python3.11 -m venv .venv
source .venv/bin/activate
pip install pydantic==1.10.13 openai==1.12.0 azure-functions==1.18.0 azure-storage-file==2.1.0
func start
```

## 📊 Cost Estimation

Running this solution typically costs:
- **Function App**: ~$0 (free grant covers most usage)
- **Storage**: ~$5/month (5GB file share)
- **Application Insights**: ~$0 (free tier sufficient)
- **OpenAI API**: Based on usage (GPT-4 pricing applies)

**Total: ~$5/month + OpenAI usage**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Built with Azure Functions and Azure OpenAI
- Designed for Microsoft 365 integration
- Memory system inspired by conversational AI best practices

## 🆘 Support

- **Issues**: [Open an issue](https://github.com/kody-w/Copilot-Agent-365/issues)
- **Discussions**: [Start a discussion](https://github.com/kody-w/Copilot-Agent-365/discussions)
- **Documentation**: [Azure Functions Docs](https://docs.microsoft.com/azure/azure-functions/)

---

<p align="center">
  Made with ❤️ for the Azure and Microsoft 365 community
  <br>
  <a href="https://github.com/kody-w/Copilot-Agent-365">⭐ Star this repo</a> if you find it helpful!
</p>