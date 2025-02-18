import os
import json
import time
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint = "https://milan-m3zxey01-swedencentral.cognitiveservices.azure.com",
    api_key = "xxx",
    api_version = "2024-05-01-preview"
)

# Create an assistant with file search capability
assistant = client.beta.assistants.create(
    name="Document Assistant",
    instructions="You are an AI assistant that uses file search to retrieve information from uploaded documents when answering user questions.",
    model="gpt-4o", # replace with your model deployment name
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": ["vs_SVdXtKA16zg6jsGHYyvXyDTm"]}},
    temperature=1,
    top_p=1
)

# Create a thread
thread = client.beta.threads.create()

# Add a message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=input("Enter your question: ")
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Poll for the run to complete
while run.status in ["queued", "in_progress", "cancelling"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {run.status}")

if run.status == "completed":
    # Get messages from the thread
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    
    # Print the assistant's response
    for message in messages.data:
        if message.role == "assistant":
            print("\nAssistant's response:")
            print(message.content[0].text.value)

elif run.status == "requires_action":
    # Handle file search tool outputs
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []
    
    for tool_call in tool_calls:
        if tool_call.type == "file_search":
            # The file search is handled automatically by Azure OpenAI
            # We just need to submit an empty output
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps({"results": []})
            })
    
    # Submit tool outputs
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )
    
    # Continue polling for completion
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status after tool outputs: {run.status}")
    
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Print the assistant's response
        for message in messages.data:
            if message.role == "assistant":
                print("\nAssistant's response:")
                print(message.content[0].text.value)
    else:
        print(f"Run ended with status: {run.status}")
        if hasattr(run, 'last_error'):
            print(f"Error: {run.last_error}")

else:
    print(f"Run failed with status: {run.status}")
    if hasattr(run, 'last_error'):
        print(f"Error: {run.last_error}")
