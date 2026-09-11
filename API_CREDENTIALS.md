# API Credentials Guide

Detailed instructions for obtaining and configuring API credentials.

## Table of Contents

1. [OpenAI API](#openai-api)
2. [YouTube API](#youtube-api)
3. [Google Cloud](#google-cloud)
4. [Speech-to-Text Services](#speech-to-text-services)
5. [Security Best Practices](#security-best-practices)

---

## OpenAI API

### Get Your API Key

1. Visit https://platform.openai.com/api-keys
2. Sign up or log in with your account
3. Click "Create new secret key"
4. Copy the key (you can only see it once)
5. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

### Verify API Key

```python
import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Test with a simple call
response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Test"}],
    max_tokens=10
)
print("✅ OpenAI API key is valid")
```

### Set API Budget/Limits

1. Go to https://platform.openai.com/account/billing/overview
2. Set usage limits under "Billing" → "Usage limits"
3. Set up billing alerts

---

## YouTube API

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a Project" → "NEW PROJECT"
3. Enter project name (e.g., "YouTube Automation")
4. Click "CREATE"
5. Wait for project creation

### Step 2: Enable YouTube Data API v3

1. Go to https://console.cloud.google.com/apis/library
2. Search for "YouTube Data API v3"
3. Click the result
4. Click "ENABLE"
5. Wait for enablement

### Step 3: Create OAuth 2.0 Credentials

1. Go to https://console.cloud.google.com/apis/credentials
2. Click "CREATE CREDENTIALS" → "OAuth client ID"
3. If prompted, set up OAuth consent screen:
   - Click "CONFIGURE CONSENT SCREEN"
   - Select "External" user type
   - Fill in required fields:
     - App name: "YouTube Automation Agent"
     - User support email: your email
     - Developer contact: your email
   - Click "SAVE AND CONTINUE"
4. Back to credentials creation:
   - Application type: "Desktop application"
   - Name: "YouTube Automation Client"
   - Click "CREATE"
5. Download the credentials JSON file
6. Save as `config/youtube_credentials.json` (in .gitignore)

### Step 4: Extract Credentials

From the downloaded JSON file, add to `.env`:

```
YOUTUBE_CLIENT_ID=your_client_id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:8080/oauth2callback
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxx
```

### Step 5: Get Channel ID

1. Go to https://www.youtube.com/
2. Sign in to your account
3. Go to your channel settings
4. Copy your Channel ID (looks like: UCxxxxxxxxxxxxxx)
5. Add to `.env`:
   ```
   YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxx
   ```

### Step 6: First-Time Authorization

First time the agent runs, it will:
1. Open a browser window
2. Ask you to log in to your YouTube account
3. Ask for permission to upload videos
4. Generate a refresh token automatically
5. Save token for future use

---

## Google Cloud

### Enable Speech-to-Text API

1. Go to https://console.cloud.google.com/apis/library
2. Search for "Google Cloud Speech-to-Text API"
3. Click the result
4. Click "ENABLE"

### Create Service Account (for Speech-to-Text)

1. Go to https://console.cloud.google.com/apis/credentials
2. Click "CREATE CREDENTIALS" → "Service Account"
3. Fill in details:
   - Service account name: "YouTube Automation SA"
   - Click "CREATE AND CONTINUE"
4. Skip optional steps, click "DONE"
5. Click on the created service account
6. Go to "KEYS" tab
7. Click "ADD KEY" → "Create new key"
8. Select JSON format
9. Click "CREATE"
10. File downloads automatically
11. Save as `config/google-credentials.json`
12. Add to `.env`:
    ```
    GOOGLE_APPLICATION_CREDENTIALS=config/google-credentials.json
    GOOGLE_CLOUD_PROJECT_ID=your-project-id
    ```

### Grant Service Account Permissions

1. Go to https://console.cloud.google.com/iam-admin/iam
2. Click "GRANT ACCESS"
3. Enter service account email
4. Add roles:
   - Cloud Speech-to-Text API User
   - Vertex AI User (if using video generation)
5. Click "SAVE"

---

## Speech-to-Text Services

### Option A: Google Cloud Speech-to-Text (Recommended)

Already configured above.

Update `.env`:
```
SPEECH_TO_TEXT_PROVIDER=google
```

### Option B: AssemblyAI

1. Go to https://www.assemblyai.com/
2. Sign up for free account
3. Go to https://www.assemblyai.com/dashboard
4. Copy your API token
5. Add to `.env`:
   ```
   SPEECH_TO_TEXT_PROVIDER=assemblyai
   ASSEMBLYAI_API_KEY=your_api_key
   ```

---

## Security Best Practices

### ✅ DO:

- Store credentials in `.env` (never commit to Git)
- Use environment variables for all secrets
- Rotate API keys regularly
- Use separate credentials per environment (dev/prod)
- Monitor API usage and set budget alerts
- Use OAuth 2.0 for user authentication
- Enable 2FA on all API provider accounts
- Use service accounts with minimal permissions

### ❌ DON'T:

- Commit `.env` to version control
- Share API keys via email or chat
- Use API keys in client-side code
- Hard-code credentials in source files
- Use shared/personal credentials in production
- Expose credentials in error messages
- Use weak API key passwords

### Secure Storage

```python
# Good: Load from environment
api_key = os.getenv("OPENAI_API_KEY")

# Bad: Hard-coded
api_key = "sk-xxx..."  # Never do this!
```

### Rotating Credentials

1. Generate new credentials
2. Update `.env` with new credentials
3. Test thoroughly
4. Revoke old credentials in provider console
5. Monitor for old credential usage in logs

---

## Testing Credentials

```bash
# Test all credentials at once
python -m config.settings

# Should output:
# ==================================================
# Configuration Summary
# ==================================================
# ✅ All required configuration present
```

## Troubleshooting

### "Invalid API Key"
- Verify key is correct
- Check for typos or extra spaces
- Regenerate key in provider console
- Ensure key hasn't expired

### "Permission Denied"
- Check OAuth scopes are enabled
- Verify service account has required roles
- Check YouTube channel ID is correct
- Ensure first-time authorization completed

### "Quota Exceeded"
- Check API usage limits
- Reduce request frequency
- Upgrade to paid tier if needed
- Contact provider for limit increase

---

For more help, see [SETUP.md](SETUP.md) or [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
