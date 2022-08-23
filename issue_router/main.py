from datetime import datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import os

from .models import CreateIssueRequest, CreateIssueResponse

load_dotenv()

app = FastAPI(
    title='Translator Issue Router',
    description='Post GitHub issues to Translator services.',
    version='0.1.0',
    contact={
        'email': 'max@covar.com',
        'name': 'Max',
    },
)


def upload_screenshots(screenshots):
    """Upload screenshots to github repo."""
    screenshot_urls = []
    for screenshot in screenshots:
        try:
            now = datetime.now()
            current_time = now.strftime('%Y%m%d%H%M%S%f')
            filename = f'screenshot_{current_time}.jpeg'
            response = requests.request(
                'PUT',
                f'{os.getenv("SCREENSHOT_URL")}/{filename}',
                json={
                    'message': f'Uploading {filename}',
                    'content': screenshot,
                },
                headers={
                    'accept': 'application/vnd.github+json',
                    'content-type': 'application/json',
                    'authorization': f'token {os.getenv("TOKEN")}',
                }
            )
            response.raise_for_status()
            response_json = response.json()
            screenshot_url = response_json['content']['download_url']
            screenshot_url = f'![screenshot]({screenshot_url})'
            screenshot_urls.append(screenshot_url)
        except Exception as e:
            screenshot_urls.append('Failed to upload screenshot.')
    return (' ').join(screenshot_urls)



@app.post('/create_issue', response_model=CreateIssueResponse)
async def create_issue(request: CreateIssueRequest):
    """Create a github ticket."""
    try:
        screenshots = upload_screenshots(request.screenshots)
        data = {
            'title': request.description,
            'body': f"""
## Type: {request.type}
## URL: {request.url}
## ARS PK: {request.ars_pk}

## Steps to reproduce:
{request.reproduction_steps}

## Screenshots:
{screenshots}
    """
        }
        response = requests.request(
            'POST',
            os.getenv('GITHUB_URL'),
            json=data,
            headers={
                'accept': 'application/vnd.github+json',
                'content-type': 'application/json',
                'authorization': f'token {os.getenv("TOKEN")}',
            }
        )
        response.raise_for_status()
        response_json = response.json()
        url = response_json['html_url']
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {
        'url': url
    }
