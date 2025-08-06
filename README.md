## 🚀 One-Click Deploy Everything

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2FCopilot-Agent-365%2Fmain%2Fazuredeploy.json)

Click once. Enter OpenAI credentials. Everything deploys automatically - resources AND code!

## ✨ Features

- 🧠 **Azure OpenAI GPT-4** - Advanced AI responses with context understanding
- 💾 **Persistent Memory System** - User-specific and shared memory storage
- 🔐 **Enterprise Security** - Function-level authentication and HTTPS only
- 📊 **Full Monitoring** - Application Insights integration
- ⚡ **Serverless Architecture** - Auto-scaling Azure Functions
- 🎯 **Agent System** - Extensible architecture for custom capabilities
- 🎨 **Beautiful Web UI** - Modern chat interface included

## 🚀 Quick Start - 2 Ways to Use

### Option 1: Direct Deploy to Azure (Easiest)
1. Click the **"Deploy to Azure"** button above
2. Fill in:
   - Resource Group (create new or use existing)
   - Your Azure OpenAI API Key
   - Your Azure OpenAI Endpoint
3. Click **"Review + Create"** then **"Create"**
4. Wait 5-10 minutes for deployment
5. Deploy the code using instructions below

### Option 2: Use as Template (For Developers)
1. Click **"Use this template"** button above
2. Name your new repository
3. Clone your new repo locally
4. Customize the code as needed
5. Deploy using your own Azure resources

## 📋 Prerequisites

Before deploying, you need:

- ✅ **Azure Account** - [Get free trial](https://azure.microsoft.com/free/)
- ✅ **Azure OpenAI Service Access** - [Request access here](https://azure.microsoft.com/products/cognitive-services/openai-service)
- ✅ **Azure OpenAI API Key** - From your Azure OpenAI resource
- ✅ **Azure OpenAI Endpoint** - Format: `https://your-resource.openai.azure.com/`

## 🔧 Deployment Instructions

### Step 1: Deploy Azure Resources
Click the "Deploy to Azure" button and fill in your OpenAI credentials. This creates:
- Azure Function App (Linux, Python 3.11)
- Storage Account with File Share
- Application Insights
- Consumption Plan (pay-per-use)

### Step 2: Deploy the Function Code

After Azure resources are created, deploy the code:

#### Option A: ZIP Deployment (Recommended)
```bash
# Clone this repository
git clone https://github.com/kody-w/Copilot-Agent-365.git
cd Copilot-Agent-365/azure-function-app

# Create deployment package
zip -r ../deploy.zip . -x "*.git*" -x "local.settings.json"

# Deploy to your Function App
az functionapp deployment source config-zip \
    --resource-group <your-resource-group> \
    --name <your-function-app-name> \
    --src ../deploy.zip
```

#### Option B: VS Code Deployment
1. Install [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
2. Open the `azure-function-app` folder in VS Code
3. Sign in to Azure (Ctrl+Shift+P → "Azure: Sign In")
4. Right-click on your Function App in Azure panel
5. Select "Deploy to Function App..."

#### Option C: GitHub Actions (CI/CD)
1. Get publish profile from Azure Portal (Function App → Download publish profile)
2. Add as GitHub Secret: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
3. Add Function App name as secret: `AZURE_FUNCTIONAPP_NAME`
4. Push to main branch to trigger deployment

### Step 3: Get Your Function URL & Key

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Function App
3. Go to **Functions** → **businessinsightbot_function**
4. Click **Get Function URL**
5. Copy the URL (it includes the function key)

### Step 4: Test Your Chatbot

1. Open `client/index.html` in a web browser
2. Enter your Function URL and Key
3. Click "Save Config"
4. Start chatting with your AI assistant!

## 📁 Repository Structure

```
Copilot-Agent-365/
├── azuredeploy.json                # Azure ARM deployment template
├── azure-function-app/             # Main application code
│   ├── function_app.py            # Azure Function entry point
│   ├── requirements.txt           # Python dependencies
│   ├── host.json                  # Function host configuration
│   ├── businessinsightbot_function/
│   │   └── function.json          # Function bindings
│   ├── agents/                    # AI agent modules
│   │   ├── __init__.py
│   │   ├── basic_agent.py        # Base agent class
│   │   ├── context_memory_agent.py # Memory recall agent
│   │   └── manage_memory_agent.py  # Memory management agent
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       └── azure_file_storage.py  # Azure Files integration
├── client/                         # Web interface (optional)
│   └── index.html                 # Complete chat UI
└── .github/
    └── workflows/
        └── deploy.yml             # GitHub Actions deployment
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
Edit these environment variables in Azure Portal:
```
ASSISTANT_NAME=YourBotName
CHARACTERISTIC_DESCRIPTION=Your bot's personality description
```

### Add Custom Agents
1. Create new file in `agents/` folder:
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

2. The agent auto-loads on function restart!

### Modify the UI
Edit `client/index.html` to customize:
- Colors and branding
- Layout and design
- Additional features

## 🔍 Monitoring & Troubleshooting

### View Logs
```bash
# Stream live logs
az webapp log tail \
    --resource-group <your-rg> \
    --name <your-function-app>

# View in Application Insights
# Azure Portal → Your Function App → Application Insights → Live Metrics
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Connection Failed" in UI | Check Function URL and Key are correct |
| 500 Internal Server Error | Verify OpenAI credentials in App Settings |
| Memory not persisting | Check Azure Files share exists and is accessible |
| Agent not found | Ensure agent file follows naming pattern `*_agent.py` |

## 📊 Cost Estimation

Running this solution typically costs:
- **Function App**: ~$0 (free grant covers most usage)
- **Storage**: ~$5/month (5GB file share)
- **Application Insights**: ~$0 (free tier sufficient)
- **OpenAI API**: Based on usage (GPT-4 pricing applies)

Total: **~$5/month + OpenAI usage**

## 🤝 Contributing

Contributions are welcome! Please:
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