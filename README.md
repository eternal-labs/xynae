<div align="center">

![Xynae Logo](assets/images/logo.png)

# Xynae

**An AI-powered social media automation framework for autonomous interactions**

</div>

Xynae is a flexible Python framework that enables AI agents to autonomously interact on social media platforms (currently supporting Twitter/X). It supports multiple LLM providers, MongoDB persistence, and allows you to create AI personalities that can post content, reply to mentions, and engage with users authentically.

## Features

- 🤖 **Multiple LLM Providers**: Support for Anthropic Claude, OpenAI GPT, and Google Gemini with automatic fallback
- 💾 **MongoDB Persistence**: Store tweets, replies, mentions, and conversation history in MongoDB
- 🎨 **Autonomous Content Generation**: AI-powered tweet generation with customizable personalities
- 💬 **Automated Replies**: Intelligent reply generation to mentions and interactions
- 🌐 **Multi-language Support**: Natural support for English, Chinese, and mixed-language content
- ⏰ **Scheduled Posting**: Configurable intervals for posting and checking mentions
- 🔧 **Highly Customizable**: Easy to customize personality, behavior, and posting patterns
- 🔐 **Secure Configuration**: Environment variable-based API key management

## Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/eternal-labs/xynae.git
cd xynae
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# LLM Provider (set at least one)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
# or
GOOGLE_API_KEY=your_google_api_key_here

# Twitter/X API
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_SECRET=your_twitter_access_token_secret_here

# MongoDB (optional - defaults to localhost if not set)
MONGODB_URI=mongodb://localhost:27017/
```

### 3. Get API Keys

**LLM Provider API Keys (choose at least one):**
- **Anthropic Claude**: Sign up at [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI GPT**: Get key from [platform.openai.com](https://platform.openai.com/api-keys)
- **Google Gemini**: Get key from [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

**Twitter/X API Keys:**
- Apply for developer access at [developer.twitter.com](https://developer.twitter.com/en/portal/dashboard)
- Create a new app and generate API keys and tokens

**MongoDB (Optional):**
- **Local**: Install MongoDB locally or use Docker: `docker run -d -p 27017:27017 mongo`
- **Cloud**: Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available)

### 4. Run

```bash
python xynae.py
```

## Usage

### Basic Usage

```python
from xynae import Xynae

# Initialize with environment variables
# Automatically detects available LLM providers and MongoDB
xynae = Xynae()

# Run the main loop
xynae.run(tweet_interval=1200, check_interval=300)  # 20 min tweets, 5 min checks
```

### Multiple LLM Providers

```python
# Use a specific provider
xynae = Xynae(llm_provider="openai")  # or "anthropic", "gemini", "auto"

# The framework will automatically fallback to other providers if one fails
# List available providers
available = xynae.llm_manager.list_available_providers()
print(f"Available providers: {available}")
```

### MongoDB Persistence

```python
# With MongoDB (default)
xynae = Xynae(
    mongodb_uri="mongodb://localhost:27017/",
    database_name="xynae",
    use_database=True
)

# Without database (memory-only mode)
xynae = Xynae(use_database=False)

# Check database stats
if xynae.db and xynae.db.is_connected():
    stats = xynae.db.get_stats()
    print(f"Tweets: {stats['tweets_count']}, Replies: {stats['replies_count']}")
```

### Custom Personality

```python
custom_personality = """You are a friendly AI assistant focused on technology education.
Share insights about AI, programming, and the future of technology.
Be helpful, clear, and engaging in your communications."""

xynae = Xynae(personality=custom_personality)
xynae.run()
```

### Custom Tweet Generation

```python
# Generate a single tweet
tweet = xynae.generate_tweet(tweet_type="insight", language="english")
print(tweet)

# Available tweet types: "insight", "ecosystem", "autonomy", "invitation"
# Available languages: "english", "chinese", "mixed", "auto"
```

### Programmatic Configuration

```python
# Pass API keys directly (not recommended for production)
xynae = Xynae(
    llm_provider="anthropic",  # Preferred LLM provider
    mongodb_uri="mongodb://localhost:27017/",
    database_name="my_bot",
    agent_count=10000  # Initial entity count
)

# Access database directly
recent_tweets = xynae.db.get_recent_tweets(limit=10)
recent_replies = xynae.db.get_recent_replies(limit=10)
```

## Configuration Options

### Tweet Intervals

- `tweet_interval`: Seconds between automated tweets (default: 1200 = 20 minutes)
- `check_interval`: Seconds between mention checks (default: 300 = 5 minutes)

### Customization Points

1. **Personality Prompt**: Modify the `personality` parameter to change AI behavior
2. **Tweet Types**: Customize tweet type prompts in `generate_tweet()` method
3. **Language Distribution**: Adjust language probability in the `run()` method
4. **Tweet Type Distribution**: Modify weights for different tweet types

## Architecture

```
xynae/
├── xynae.py                 # Main framework class
├── llm_providers.py         # LLM provider abstraction layer
│   ├── LLMProvider          # Base class
│   ├── AnthropicProvider    # Claude API
│   ├── OpenAIProvider       # GPT API
│   ├── GeminiProvider       # Gemini API
│   └── LLMProviderManager   # Provider manager with fallback
├── database.py              # MongoDB integration
│   └── XynaeDatabase        # Database operations
└── requirements.txt         # Dependencies
```

## Requirements

- Python 3.8+
- At least one LLM provider API key (Anthropic, OpenAI, or Google)
- Twitter/X API credentials (optional, for posting)
- MongoDB (optional, for persistence - defaults to memory-only if unavailable)
- Internet connection

## Dependencies

**Required:**
- `anthropic`: Anthropic Claude API client
- `tweepy`: Twitter/X API client
- `python-dotenv`: Environment variable management
- `pymongo`: MongoDB database driver

**Optional (install only providers you need):**
- `openai`: For OpenAI GPT models
- `google-generativeai`: For Google Gemini models

## Customization Guide

### Changing the Personality

Edit the default personality in `__init__()` or pass a custom one:

```python
personality = """Your custom personality instructions here..."""
xynae = Xynae(personality=personality)
```

### Adding New Tweet Types

1. Add a new prompt in the `prompts` dictionary in `generate_tweet()`
2. Add a fallback in the `fallbacks` dictionary
3. Adjust the distribution in the `run()` method

### Adjusting Language Behavior

Modify the language selection logic in `run()`:

```python
lang_rand = random.random()
if lang_rand < 0.60:  # 60% English
    language = "english"
elif lang_rand < 0.85:  # 25% Chinese
    language = "chinese"
else:  # 15% Mixed
    language = "mixed"
```

## Safety & Best Practices

- **Rate Limiting**: The framework includes built-in rate limiting and delays
- **Error Handling**: Automatic retry logic for network errors
- **Memory Management**: Old tweet IDs are cleaned up to prevent memory bloat
- **API Keys**: Never commit `.env` files to version control
- **Content Review**: Review generated content before deploying in production

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Ensure your `.env` file exists and contains `ANTHROPIC_API_KEY`
- Check that `python-dotenv` is installed

**"X connection failed"**
- Verify your Twitter API credentials are correct
- Check that your Twitter developer account has the necessary permissions
- Ensure your API keys have read/write permissions

**Rate Limit Errors**
- Increase intervals between posts and checks
- Reduce the frequency of API calls

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This framework is for educational and legitimate automation purposes. Ensure your use complies with:
- Twitter/X Terms of Service
- Anthropic API Usage Policies
- Applicable laws and regulations

Use responsibly and ethically.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for the AI community**

