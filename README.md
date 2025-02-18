# Azure OpenAI Chat Assistant

This Python script provides an interface to interact with Azure OpenAI's Assistants API, specifically designed to handle document-based queries using file search capabilities.

## Features

- Connects to Azure OpenAI service
- Creates an AI assistant with file search capabilities
- Allows users to input questions about uploaded documents
- Displays real-time status updates during processing
- Handles file search operations automatically

## Requirements

- Python 3.x
- `openai` Python package

## Setup

1. Install the required package:
```bash
pip install openai
```

2. Configure your Azure OpenAI credentials in the script:
- Azure Endpoint
- API Key
- API Version
- Model deployment name

## Usage

1. Run the script:
```bash
python azure_openai_chat.py
```

2. When prompted, enter your question about the uploaded documents.

3. The script will:
   - Create an assistant instance
   - Create a new thread
   - Submit your question
   - Process the response
   - Display the assistant's answer

4. The status of the request will be displayed in real-time as it processes.

## Error Handling

The script includes comprehensive error handling for:
- Run status monitoring
- File search operations
- API communication issues

Any errors encountered during execution will be displayed with relevant details.
