---
icon: gears
cover: .gitbook/assets/gitbook.png
coverY: 0
---

# XYNAE Setup

### 1. Clone the Agent Builder Repository

```bash
# Clone the repository
git clone https://github.com/eternal-labs/xynae.git
cd xynae

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import anthropic, tweepy, pymongo; print('Dependencies installed successfully!')"
```

#### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Open .env in your text editor
nano .env  # or use your preferred editor
```

Add your API keys to the `.env` file:

```env
# LLM Provider (set at least one)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
# or
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
# or
GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxxxxx

# Twitter/X API
TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxxx
TWITTER_BEARER_TOKEN=xxxxxxxxxxxxxxxxxxxxx

# MongoDB (optional - defaults to localhost if not set)
MONGODB_URI=mongodb://localhost:27017/

# Or for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

Save the file and ensure it's never committed to version control.

***
