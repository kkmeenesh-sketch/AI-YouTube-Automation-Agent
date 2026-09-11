# Setup and Installation Guide

Complete step-by-step guide to set up the AI YouTube Automation Agent.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- FFmpeg (for video processing)
- A text editor or IDE

## Step 1: Clone the Repository

```bash
git clone https://github.com/kkmeenesh-sketch/AI-YouTube-Automation-Agent.git
cd AI-YouTube-Automation-Agent
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements.txt[dev]
```

## Step 4: Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API credentials
# Use your preferred editor:
nano .env          # Linux/Mac
# or
code .env          # VS Code
# or
gedit .env         # GNOME
```

## Step 5: Obtain API Credentials

### 5.1 OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key and add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

### 5.2 YouTube API Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Add to `.env`:
   ```
   YOUTUBE_CLIENT_ID=your_client_id
   YOUTUBE_CLIENT_SECRET=your_client_secret
   YOUTUBE_CHANNEL_ID=your_channel_id
   ```

### 5.3 Google Cloud Configuration

1. In Google Cloud Console, enable Speech-to-Text API
2. Download service account credentials
3. Save as `config/google-credentials.json`
4. Update `.env`:
   ```
   GOOGLE_CLOUD_PROJECT_ID=your_project_id
   GOOGLE_APPLICATION_CREDENTIALS=config/google-credentials.json
   ```

### 5.4 Speech-to-Text Provider (Choose One)

**Option A: Google Cloud Speech-to-Text**
```
SPEECH_TO_TEXT_PROVIDER=google
GOOGLE_SPEECH_API_KEY=your_api_key
```

**Option B: AssemblyAI**
```
SPEECH_TO_TEXT_PROVIDER=assemblyai
ASSEMBLYAI_API_KEY=your_api_key
```

## Step 6: Verify Installation

```bash
# Run configuration validation
python -m config.settings

# Should show:
# ==================================================
# Configuration Summary
# ==================================================
# ...
# ✅ All required configuration present
```

## Step 7: Test the Agent

```bash
# Run example workflow
python examples.py

# Or start interactive mode
python -m src.main
```

## Configuration Files

### .env

Main configuration file with all API keys and settings.
Never commit this file to version control.

### config/settings.py

Application settings and configuration management.
Loads from `.env` automatically.

### config/credentials.json

Optional: Centralized credentials file.
Template: `config/credentials_template.json`

## Directory Structure

After installation, your project should look like:

```
AI-YouTube-Automation-Agent/
├── .env                       # Your API credentials (git-ignored)
├── .env.example              # Template
├── config/
│   ├── settings.py           # Configuration
│   ├── credentials.json      # Credentials (git-ignored)
│   └── google-credentials.json # Google creds (git-ignored)
├── src/
│   ├── main.py              # Main agent
│   ├── modules/             # Feature modules
│   ├── utils/               # Utilities
│   └── database/            # Database manager
├── logs/                     # Application logs (auto-created)
├── data/                     # Data storage (auto-created)
├── output/                   # Output files (auto-created)
└── temp/                     # Temporary files (auto-created)
```

## Troubleshooting

### Missing OpenAI API Key

**Error:** `ValueError: OpenAI API key not configured`

**Solution:**
1. Check `.env` file has `OPENAI_API_KEY`
2. Verify the key is valid at https://platform.openai.com/api-keys
3. Check you have API credits available

### YouTube Authentication Issues

**Error:** `googleapiclient.errors.HttpError`

**Solution:**
1. Ensure OAuth credentials are properly downloaded
2. Verify `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` in `.env`
3. First run requires browser authentication

### FFmpeg Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution:**

Linux:
```bash
sudo apt-get install ffmpeg
```

Mac:
```bash
brew install ffmpeg
```

Windows:
```bash
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

## Next Steps

1. Review [USAGE.md](USAGE.md) for detailed usage instructions
2. Check [examples.py](examples.py) for code examples
3. Read module documentation in `src/modules/`
4. Set up scheduling (optional)
5. Configure webhook integrations (optional)

## Support

For issues or questions:
1. Check the [README.md](README.md)
2. Review error logs in `logs/`
3. Open a GitHub issue

---

**Installation complete!** You're ready to automate YouTube video creation.
