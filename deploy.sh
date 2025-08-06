#!/bin/bash

# Check if resource group and function app name are provided
if [ $# -ne 2 ]; then
    echo "Usage: ./deploy.sh <resource-group> <function-app-name>"
    exit 1
fi

RESOURCE_GROUP=$1
FUNCTION_APP=$2

echo "🚀 Deploying to Azure Function App..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Function App: $FUNCTION_APP"

# Create deployment package
echo "📦 Creating deployment.zip..."
zip -r deployment.zip . -x "*.git*" -x "*.vscode*" -x "local.settings.json" -x "deployment.zip" -x "*.sh"

# Deploy to Azure
echo "☁️ Deploying to Azure..."
az functionapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $FUNCTION_APP \
    --src deployment.zip

# Check deployment status
if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🔗 Your function endpoint: https://$FUNCTION_APP.azurewebsites.net/api/businessinsightbot_function"
    
    # Clean up
    echo "🧹 Cleaning up..."
    rm deployment.zip
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi
