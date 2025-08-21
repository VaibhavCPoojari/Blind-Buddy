from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")  # Ensure
)

result = client.run_workflow(
    workspace_name="shri-2krws",
    workflow_id="custom-workflow-2",
    images={
        "image": "D:\IDP\pole.jpeg"
    },
    use_cache=True  
)

print(result)