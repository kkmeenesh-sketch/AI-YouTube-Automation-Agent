# AI YouTube Automation Agent

A fully automated AI-powered system for creating, optimizing, and publishing YouTube videos from start to finish.

## 🎯 Features

- **Automated Research & Script Generation** - Uses OpenAI ChatGPT to research topics and generate engaging video scripts
- **AI Video Generation** - Integrates with Google's AI video generation services
- **Automatic Subtitle Generation** - Generates captions and subtitles automatically
- **Smart Metadata Generation** - Auto-generates titles, descriptions, tags, and hashtags
- **Thumbnail Generation** - AI-powered thumbnail creation (optional)
- **YouTube Publishing** - Direct integration with YouTube Data API for uploading and scheduling
- **Fully Modular Architecture** - Each service can be connected separately and replaced as needed

## 📋 Workflow

```
Topic Research → ChatGPT Script → Video Generation → Download
    ↓
Subtitle Generation → Metadata Generation → Thumbnail (Optional)
    ↓
YouTube Upload → Scheduling → Auto-Publish
```

## 🏗️ Project Structure

```
AI-YouTube-Automation-Agent/
├── config/
│   ├── settings.py                 # Configuration management
│   ├── credentials_template.json   # API credentials template
│   └── requirements.txt            # Python dependencies
├── src/
│   ├── __init__.py
│   ├── main.py                     # Main orchestration agent
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── research.py             # Topic research module
│   │   ├── script_generator.py     # ChatGPT script generation
│   │   ├── video_generator.py      # Video generation (Google Flow)
│   │   ├── subtitle_generator.py   # Subtitle/caption generation
│   │   ├── metadata_generator.py   # Title, description, tags, hashtags
│   │   ├── thumbnail_generator.py  # AI thumbnail creation
│   │   ├── youtube_uploader.py     # YouTube upload & publishing
│   │   └── scheduler.py            # Video scheduling
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py               # Logging utilities
│   │   ├── file_handler.py         # File operations
│   │   ├── api_client.py           # Base API client
│   │   └── validators.py           # Input validation
│   └── database/
│       ├── __init__.py
│       └── db_manager.py           # Database operations
├── tests/
│   ├── __init__.py
│   ├── test_script_generator.py
│   ├── test_youtube_uploader.py
│   └── test_metadata_generator.py
├── logs/                           # Application logs (git-ignored)
├── temp/                           # Temporary files (git-ignored)
├── .env.example                    # Environment variables template
├── .gitignore
├── requirements.txt                # Main dependencies
├── setup.py                        # Package setup
└── README.md                       # This file
```

## 🔑 Required Credentials & API Keys

To run this agent, you'll need the following:

### 1. **OpenAI API (ChatGPT)**
   - **Get it from:** https://platform.openai.com/api-keys
   - **Required:** API Key
   - **Used for:** Script generation, metadata generation, title/description creation

### 2. **YouTube Data API v3**
   - **Get it from:** https://console.cloud.google.com/
   - **Required:** 
     - OAuth 2.0 Client Credentials (for channel access)
     - API Key (for basic operations)
   - **Scopes needed:**
     - `youtube.upload` - Upload videos
     - `youtube.readonly` - Read channel data
     - `youtube.force-ssl` - SSL communications
   - **Used for:** Video upload, scheduling, publishing

### 3. **Google AI Video Generation** ⚠️
   - **Status:** Currently investigating official APIs
   - **Potential Options:**
     - Google Cloud Vertex AI (for text-to-video/video AI)
     - Alternative: D-ID, Synthesia, or Runway ML APIs
   - **Will be confirmed** in video_generator.py documentation

### 4. **Speech-to-Text Service** (for subtitles)
   - **Option A:** Google Cloud Speech-to-Text API
   - **Option B:** AssemblyAI API
   - **Get it from:**
     - Google: https://cloud.google.com/speech-to-text
     - AssemblyAI: https://www.assemblyai.com/
   - **Used for:** Automatic subtitle/caption generation

### 5. **Thumbnail Generation** (Optional)
   - **Option A:** OpenAI DALL-E API (via OpenAI account)
   - **Option B:** Stability AI (Stable Diffusion)
   - **Used for:** AI-generated thumbnails

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kkmeenesh-sketch/AI-YouTube-Automation-Agent.git
   cd AI-YouTube-Automation-Agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

5. **Configure API keys:**
   ```bash
   cp config/credentials_template.json config/credentials.json
   # Edit credentials.json with your API keys
   ```

## 🚀 Quick Start

```python
from src.main import YouTubeAutomationAgent

# Initialize the agent
agent = YouTubeAutomationAgent(config_path="config/settings.py")

# Run the complete workflow
result = agent.automate_video_creation(
    topic="The Future of AI in 2025",
    video_style="educational",
    publish_time="2025-01-15 14:00:00",
    schedule=True
)

print(f"Video published: {result['youtube_url']}")
```

## 📚 Module Documentation

Each module has detailed documentation:
- `src/modules/script_generator.py` - ChatGPT integration
- `src/modules/video_generator.py` - Video generation services
- `src/modules/subtitle_generator.py` - Subtitle automation
- `src/modules/metadata_generator.py` - SEO & metadata
- `src/modules/youtube_uploader.py` - YouTube API integration
- `src/modules/scheduler.py` - Publishing schedule

## ⚙️ Configuration

All configuration is managed through:
- `.env` - Environment variables and API keys
- `config/settings.py` - Application settings
- `config/credentials.json` - API credentials

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## ⚠️ Important Notes

- **API Costs:** Running this agent will incur costs for OpenAI, YouTube, Google Cloud, and other services. Monitor your usage.
- **Rate Limits:** Be aware of API rate limits for each service.
- **Video Quality:** The final video quality depends on the video generation service used.
- **YouTube Guidelines:** Ensure all generated content complies with YouTube's Community Guidelines.

## 📧 Support

For issues, questions, or suggestions, please open a GitHub issue.

---

**Last Updated:** 2025
**Version:** 1.0.0
