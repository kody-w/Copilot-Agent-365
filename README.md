# Azure Function App - AI Chatbot with Memory

## 📁 File Structure

```
azure-function-app/
├── function_app.py                  # Main function code
├── requirements.txt                 # Python dependencies
├── host.json                       # Function configuration
├── businessinsightbot_function/
│   └── function.json              # Function bindings
├── agents/
│   ├── __init__.py
│   ├── basic_agent.py             # Base agent class
│   ├── context_memory_agent.py   # Memory recall agent
│   └── manage_memory_agent.py    # Memory management agent
└── utils/
    ├── __init__.py
    └── azure_file_storage.py      # Azure storage integration
```YOUR-USERNAME

## 🚀 Deployment Steps

1. Create a ZIP file:
   ```bash
   zip -r deployment.zip . -x "*.git*" -x "*.vscode*" -x "local.settings.json"
   ```

2. Deploy to Azure:
   ```bash
   az functionapp deployment source config-zip \
       --resource-group <your-resource-group> \
       --name <your-function-app-name> \
       --src deployment.zip
   ```

## 🔧 Configuration

Set these environment variables in your Azure Function App:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_VERSION
- AZURE_FILES_SHARE_NAME
- ASSISTANT_NAME
- CHARACTERISTIC_DESCRIPTION
