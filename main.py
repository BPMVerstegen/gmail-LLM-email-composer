import requests
import json
import datetime
import os

class GmailEmailComposer:
    def __init__(self, api_key, api_secret, email_service_account, email_password):
        self.api_key = "YOUR_API_KEY"
        self.api_secret = "YOUR_API_SECRET"
        self.email_service_account = "YOUR_EMAIL"
        self.email_password = "YOUR_PASSWORD"
        self.api_url = 'https://gmail.googleapis.com/'
        
    def compose_email(self, subject, to, body, attachments=None, schedule=None):
        if schedule:
            if not isinstance(schedule, dict):
                raise ValueError("Schedule must be a dictionary")
            send_at = schedule['send_at']
        else:
            send_at = None
    
        payload = {
            "method": "POST",
            "url": "/messages",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer',  # bearer token must be replaced with actual token
                # 'User-Agent' should match that of Gmail
            },
            "json": {
                "requireCrf": False,
                "body": { 
                    "raw": "<html><body>Hello<br><br>B</body></html>",
                    "attachmentTypes": []
                },
                "labelIds": [],
                "labelName": [],
                "labels": [],
                "priorityVisibility": "person",
                "in_reply_to_message_id": None,
                "uuid": None,
                "threadId": None,
                "name": None,
                "signature": None,
                "fromEmail": to,
                "toRecipients": [{"email": to}],
                "ccRecipients": [],
                "bccRecipients": [],
                "additionalRecipientTypes": [
                    {"emailAddress": {"address": to, "labelIds": []}},
                ],
                "includeRecipientEmailTag": False,
                "includeRecipients": [],
                "threads": [],
                "addExtensions": [],

            }
        }

        if attachments:
            payload['json']['body']['attachments'] = attachments

        response = requests.post(f"{self.api_url}/v1/users/me/messages", json=payload)
    
        if response.status_code == 201:
            email_id = response.json()['id']
            return email_id
        else:
            return None

    def schedule_email(self, email_id, schedule):
        if not isinstance(email_id, str):
            raise ValueError("Email ID must be a string")
        payload = {
            "method": "POST",
            "url": "/messages/{email_id}/batch",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer',  # bearer token must be replaced with actual token
                # 'User-Agent' should match that of Gmail
            },
        
            "json": {
                "message": {
                    "batchManageLabelIds": [],
                    "flaggedLabelIds": [],
                    "labelIds": [],
                    "name": "",
                    "parentMessageId": email_id,
                    "sendToAll": {},
                    "sendToSome": {
                        "ids": [email_id]
                    },
                    "deleteFrom": {},

                }
            }
        }
        response = requests.post(self.api_url + str(email_id) + "/batch", json=payload)
        
        if response.status_code == 202:
            return "Email Scheduled Successfully"
        else:
            return None

    def send_email(self, email_id):
        if not isinstance(email_id, str):
            raise ValueError("Email ID must be a string")
        payload = {
            "method": "POST",
            "url": f"{self.api_url}/messages/{email_id}/send",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer',  # bearer token must be replaced with actual token
                # 'User-Agent' should match that of Gmail
            },
        }
        response = requests.post(self.api_url + str(email_id) + "/send", json=payload)
        if response.status_code == 200:
            return "Email Sent Successfully"
        else:
            return None

def generate_text(prompt):
    api_url = "https://api.llama.io/v1/models/generate_text"
    payload = {
        "prompt": prompt
    }
    response = requests.get(api_url, json=payload)
    if 'paragraphs' in response.json() and response.json()['paragraphs']:
        paragraph = response.json()['paragraphs'][0][0]
        return paragraph['text']
    else:
        return None

def main():
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    email_service_account = "YOUR_EMAIL_SERVICE_ACCOUNT"
    email_password = "YOUR_EMAIL_PASSWORD"
    
    composer = GmailEmailComposer(api_key, api_secret, email_service_account, email_password)
    
    subject = "subject_string"
    to = "recipient_email"
    body = ""
    attachments = ["attachment1.txt", "attachment2.pdf"]
    schedule = {"send_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    email_id = composer.compose_email(subject, to, body, attachments, schedule)
    
    if email_id:
        message = composer.schedule_email(email_id, schedule)
        if message:
            try:
                message = composer.send_email(email_id)
                print(message)
            except Exception as e:
                print(f"Error sending email: {e}")
        print("Email Composed Successfully")
    else:
        print("Failed to compose email")

if __name__ == "__main__":
    main()
