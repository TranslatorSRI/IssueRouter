# IssueRouter
Route issues from Translator UI to Translator Services

## How to:
POST to `/create_issue` with the following values:
- `url`: url where issue happened
- `ars_pk`: pk given from ARS
- `description`: a short summary of the issue
- `reproduction_steps`: a list of steps one could do to reproduce the issue
- `screenshots`: a list of base64 encoded images that show the issue
- `type`: bug or feature request

You will get back a response containing the following values:
- `url`: the github url of the created issue

## Development:
### Locally
- Create a virtual environment and activate
- In the root directory, `pip install -r requirements-lock.txt`
- Run `uvicorn issue_router.main.app --host 0.0.0.0 --port 4007 --reload`

### Docker:
- `docker-compose up --build`
