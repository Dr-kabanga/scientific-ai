# ChatGPT Real-Time Sync Workflow

This repository includes an automated workflow for real-time code analysis and Slack notifications using GitHub Actions and OpenAI's GPT models.

## Features

- **Automatic Code Analysis:**  
  Triggers on pushes to `main`, new/synchronized/reopened PRs, or a `repository_dispatch` event named `chatgpt_sync`.  
  Uses OpenAI's GPT to summarize PR diffs, flag issues, and suggest improvements.

- **Slack Notifications:**  
  Notifies the team via Slack after workflow runs, highlighting repo, commit, and author.

## Setup Instructions

### 1. Add Required GitHub Secrets

Go to your repository **Settings → Secrets and variables → Actions** and add:

- `OPENAI_API_KEY` — Your OpenAI API key
- `GITHUB_TOKEN` — (Usually auto-injected by GitHub Actions, but add if using a custom token)
- `SLACK_WEBHOOK_URL` — Your Slack Incoming Webhook URL

### 2. Add Workflow and Scripts

- Place `.github/workflows/chatgpt_sync.yml` in your repo.
- Place `scripts/webhook_listener.py` in the `scripts/` directory.
- (Optional) Add the `Notify Slack` step to your workflows (see below).

### 3. Example Workflow Files

#### `.github/workflows/chatgpt_sync.yml`
```yaml
name: ChatGPT Real-Time Sync
on:
  push:
    branches: [ main ]
  pull_request:
    types: [opened, synchronize, reopened]
  repository_dispatch:
    types: [chatgpt_sync]

jobs:
  analyze-and-comment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install openai requests

      - name: Run ChatGPT analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/webhook_listener.py \
            --event ${{ toJson(github.event) }} \
            --repo ${{ github.repository }}
```

#### `scripts/webhook_listener.py`
```python
import os
import sys
import json
import requests
from openai import OpenAI

# Load environment
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Parse event payload
payload = json.loads(sys.argv[sys.argv.index('--event') + 1])
repo = sys.argv[sys.argv.index('--repo') + 1]

def analyze_code(diff_text):
    prompt = ("You are a knowledgeable AI. Analyze the following git diff and summarize key changes, potential issues, "
              "and suggestions for improvement:\n" + diff_text)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

# Example: extract diff and run analysis
diff_text = ''
if 'pull_request' in payload:
    # Fetch PR diff
    pr_number = payload['number']
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    pr_data = requests.get(url, headers=headers).json()
    diff_url = pr_data['diff_url']
    diff_text = requests.get(diff_url).text

# Run analysis
analysis = analyze_code(diff_text)
print("ChatGPT Analysis:\n", analysis)

# Post as PR comment
if analysis:
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(comment_url,
                  headers={'Authorization': f'token {GITHUB_TOKEN}'},
                  json={'body': analysis})
```

#### Slack Integration Step (Optional)
You can add this to any workflow job to notify your Slack channel:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    fields: repo,commit,author
    mention: 'here'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Next Steps

1. **Add required secrets** (see above).
2. **Commit the workflow and script** to your repository.
3. **Create additional workflows** for data simulation, policy drafts, and performance logging as needed.
4. **Build a dashboard** that consumes and displays workflow logs for real-time monitoring.

---

*Questions? Open an issue or discussion in this repository!*