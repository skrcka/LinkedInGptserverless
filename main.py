import os
import json
import requests
from google.cloud import secretmanager
import urllib.request


url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
req = requests.get(url, headers={"Metadata-Flavor": "Google"})
project_id = req.text

client = secretmanager.SecretManagerServiceClient()
name = client.secret_version_path(project_id, 'gpt-key', 'latest')
request = secretmanager.AccessSecretVersionRequest(name=name)
response = client.access_secret_version(request=request)
api_key = response.payload.data.decode('UTF-8')

def linkedin_completion(request):
    try:
        request_json = request.get_json()
        message = request_json['message']
        thread = request_json['thread']
        userid = request_json['user']
        username = request_json['name']

        if message:
            text = f'Reply to this LinkedIn chat message thread by adjusting this LinkedIn message: "{message}" to something more appropriate and professional. But stay relevant to the point of the original message. Reply as {username}:\n{thread}'
        else:
            text = f'Reply to this LinkedIn chat message thread as {username}:\n\n{thread}'

        url = 'https://api.openai.com/v1/chat/completions'
        model = 'gpt-3.5-turbo'
        messages = [{'role': 'user', 'content': text}]

        request_json = {
            'model': model,
            'messages': messages,
            'user': userid,
        }
        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.post(url, json=request_json, headers=headers)
        response = response.json()
        response = response['choices'][0]['message']['content']
        response = response.strip()

        return response

    except Exception as e:
        return str(e), 500
