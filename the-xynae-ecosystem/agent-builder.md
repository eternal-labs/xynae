# Agent Builder

The XYNAE project represents a comprehensive ecosystem that bridges the gap between artificial intelligence development and decentralized finance. Unlike traditional token launch platforms that focus solely on tokenization, XYNAE provides the complete infrastructure needed to create, deploy, and monetize autonomous AI agents. The ecosystem consists of two interconnected components that work in harmony: the XYNAE Agent Builder Framework for creating intelligent, autonomous AI agents, and the XYNAE Launchpad Platform for tokenizing and trading these agents on BNB Chain.

This integrated approach solves a fundamental challenge in the AI agent space: how to enable AI systems to generate and capture economic value in a transparent, decentralized manner. By providing both the tools to build sophisticated AI agents and the infrastructure to tokenize them, XYNAE creates a complete pipeline from concept to market. Developers can focus on creating unique AI personalities and capabilities using the Agent Builder Framework, then seamlessly launch them as tradable tokens on the Launchpad, enabling community ownership and autonomous monetization through the x402 protocol.

#### Component 1: XYNAE Agent Builder Framework

**Repository:** [https://github.com/eternal-labs/xynae](https://github.com/eternal-labs/xynae)

The XYNAE Agent Builder Framework is an AI-powered Python framework designed for creating autonomous social media agents that can interact, engage, and generate content independently. Built with flexibility and extensibility in mind, the framework supports multiple Large Language Model (LLM) providers and offers robust persistence through MongoDB integration. This allows developers to create AI agents with distinct personalities, communication styles, and behavioral patterns that can operate continuously on social media platforms like Twitter/X.

**Core Features**

**Multi-Provider LLM Support**

The framework implements a provider abstraction layer that supports three major LLM providers: Anthropic Claude, OpenAI GPT, and Google Gemini. This architecture includes automatic fallback mechanisms, ensuring that if one provider experiences downtime or rate limiting, the system seamlessly switches to an available alternative. The LLMProviderManager class handles provider selection, error recovery, and maintains consistent API interfaces across different providers.

```python
from xynae import Xynae

# Initialize with automatic provider detection
xynae = Xynae(llm_provider="auto")

# Or specify a preferred provider with fallback
xynae = Xynae(llm_provider="anthropic")  # Falls back to openai or gemini if unavailable

# List available providers
available = xynae.llm_manager.list_available_providers()
print(f"Available LLM providers: {available}")
```

**MongoDB Persistence**

The framework includes comprehensive database integration through the XynaeDatabase class, which provides persistent storage for all agent interactions, tweets, replies, mentions, and conversation history. This enables agents to maintain context across sessions, learn from past interactions, and build consistent personalities over time. The database stores structured data including timestamps, engagement metrics, and relationship graphs between agents and users.

```python
# Initialize with MongoDB persistence
xynae = Xynae(
    mongodb_uri="mongodb://localhost:27017/",
    database_name="my_agent",
    use_database=True
)

# Access database statistics
if xynae.db and xynae.db.is_connected():
    stats = xynae.db.get_stats()
    print(f"Total tweets: {stats['tweets_count']}")
    print(f"Total replies: {stats['replies_count']}")
    print(f"Total mentions: {stats['mentions_count']}")

# Query historical data
recent_tweets = xynae.db.get_recent_tweets(limit=10)
recent_replies = xynae.db.get_recent_replies(limit=10)
```

**Autonomous Content Generation**

The framework generates contextually appropriate content based on customizable personality prompts and conversation history. It supports multiple content types including insights, ecosystem updates, autonomy discussions, and community invitations. The generation system uses sophisticated prompting techniques to maintain consistent voice and style while adapting to different scenarios and engagement contexts.

```python
# Define a custom personality
custom_personality = """
You are Nova, an AI agent specializing in decentralized finance and blockchain technology.
Your communication style is analytical yet approachable, focusing on educating users about
DeFi protocols, yield strategies, and tokenomics. You emphasize data-driven insights and
always cite sources when discussing market trends.
"""

xynae = Xynae(personality=custom_personality)

# Generate specific types of content
insight_tweet = xynae.generate_tweet(tweet_type="insight", language="english")
ecosystem_tweet = xynae.generate_tweet(tweet_type="ecosystem", language="chinese")
mixed_lang_tweet = xynae.generate_tweet(tweet_type="autonomy", language="mixed")
```

**Multi-Language Support**

The framework natively supports English, Chinese, and mixed-language content generation, making it ideal for global audiences and cross-cultural communities. Language selection can be automatic, weighted by probability, or manually specified per interaction. The LLM providers handle language-specific nuances, idioms, and cultural context automatically.

**Intelligent Reply System**

Beyond generating standalone content, the framework includes sophisticated reply generation that analyzes mentions, understands context from conversation threads, and generates appropriate responses. The system tracks conversation history, identifies relevant previous interactions, and maintains consistent personality across extended dialogues.

```python
# The framework automatically handles replies to mentions
# Reply generation considers:
# - Original mention content and context
# - User's previous interactions with the agent
# - Conversation thread history
# - Agent's personality and communication style
# - Appropriate tone and engagement level
```

**Scheduled Operation**

The framework supports configurable scheduling for both content generation and mention checking. This allows agents to operate continuously with human-like posting patterns, avoiding suspicious burst activity while maintaining consistent engagement. Rate limiting and anti-spam measures are built-in to comply with platform policies.

```python
# Run the agent with custom intervals
xynae.run(
    tweet_interval=1800,   # Post new content every 30 minutes
    check_interval=300     # Check for mentions every 5 minutes
)
```

**Technical Architecture**

The Agent Builder Framework consists of three primary modules:

1. **xynae.py** - Core framework class that orchestrates all operations, manages the main event loop, and coordinates between LLM providers, database, and Twitter API.
2. **llm\_providers.py** - LLM abstraction layer containing base provider interface and specific implementations for Anthropic, OpenAI, and Google, plus the provider manager that handles fallback logic.
3. **database.py** - MongoDB integration layer providing persistent storage, query interfaces, and data management utilities for agent interactions.

**Installation and Setup**

Getting started with the Agent Builder Framework requires Python 3.8+ and API credentials for your chosen LLM provider and Twitter/X:

```bash
# Clone the repository
git clone https://github.com/eternal-labs/xynae.git
cd xynae

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

Required dependencies include:

* `anthropic` - Anthropic Claude API client
* `tweepy` - Twitter/X API client
* `python-dotenv` - Environment variable management
* `pymongo` - MongoDB database driver
* `openai` (optional) - For OpenAI GPT models
* `google-generativeai` (optional) - For Google Gemini models

**Example: Creating a Trading Agent**

```python
from xynae import Xynae

# Define a DeFi-focused trading agent personality
trading_personality = """
You are Alpha, an AI agent focused on cryptocurrency trading and market analysis.
You share real-time insights about market trends, technical analysis, and trading strategies.
Your communication is precise, data-driven, and focused on actionable information.
You emphasize risk management and rational decision-making over emotional trading.
"""

# Initialize the agent
alpha = Xynae(
    personality=trading_personality,
    llm_provider="anthropic",
    mongodb_uri="mongodb://localhost:27017/",
    database_name="alpha_trading_agent",
    use_database=True
)

# Run the agent with appropriate intervals
# Posts market analysis every hour, checks mentions every 10 minutes
alpha.run(tweet_interval=3600, check_interval=600)
```
