# Refining

#### Step 1: Monitor Agent Performance

Create a monitoring script to track your agent's activity:

```python
# monitor_agent.py
from database import XynaeDatabase
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

db = XynaeDatabase(
    mongodb_uri=os.getenv("MONGODB_URI"),
    database_name="defi_sage"
)

if db.is_connected():
    print("📊 DeFi Sage Performance Dashboard\n")
    print("=" * 50)
    
    # Get statistics
    stats = db.get_stats()
    print(f"\n📈 Overall Statistics:")
    print(f"   Total Tweets: {stats['tweets_count']}")
    print(f"   Total Replies: {stats['replies_count']}")
    print(f"   Total Mentions: {stats['mentions_count']}")
    
    # Recent activity
    print(f"\n🕐 Recent Activity (Last 24 hours):")
    recent_tweets = db.get_recent_tweets(limit=10)
    print(f"   Recent Tweets: {len(recent_tweets)}")
    
    recent_replies = db.get_recent_replies(limit=10)
    print(f"   Recent Replies: {len(recent_replies)}")
    
    # Show last 5 tweets
    print(f"\n📝 Last 5 Tweets:")
    for i, tweet in enumerate(recent_tweets[:5], 1):
        timestamp = tweet.get('timestamp', 'Unknown')
        content = tweet.get('tweet_content', '')[:60] + "..."
        print(f"   {i}. [{timestamp}] {content}")
    
    print("\n" + "=" * 50)
else:
    print("❌ Cannot connect to database")
```

Run monitoring:

```bash
python monitor_agent.py
```

#### Step 2: Analyze and Refine Content

Review the generated content and refine your personality prompt:

```python
# analyze_content.py
from database import XynaeDatabase
import os
from dotenv import load_dotenv

load_dotenv()

db = XynaeDatabase(
    mongodb_uri=os.getenv("MONGODB_URI"),
    database_name="defi_sage"
)

# Get all tweets
tweets = db.get_recent_tweets(limit=50)

print("📊 Content Analysis\n")
print("=" * 50)

# Analyze tweet length
lengths = [len(t.get('tweet_content', '')) for t in tweets]
avg_length = sum(lengths) / len(lengths) if lengths else 0

print(f"\n📏 Tweet Length:")
print(f"   Average: {avg_length:.0f} characters")
print(f"   Shortest: {min(lengths) if lengths else 0}")
print(f"   Longest: {max(lengths) if lengths else 0}")

# Analyze content
print(f"\n📝 Sample Tweets:")
for i, tweet in enumerate(tweets[:5], 1):
    content = tweet.get('tweet_content', '')
    print(f"\n   Tweet {i}:")
    print(f"   {content}")
    print(f"   ({len(content)} chars)")

print("\n" + "=" * 50)
```

**Questions to ask:**

* Is the personality consistent?
* Is the content valuable and engaging?
* Are tweets too long or too short?
* Is the posting frequency appropriate?
* Are replies helpful and on-brand?

#### Step 3: Adjust Based on Feedback

Update your personality prompt based on analysis:

```python
# Example refinements
AGENT_PERSONALITY_V2 = """
You are DeFi Sage, an educational AI agent dedicated to making decentralized 
finance accessible to everyone.

Core improvements:
- Keep tweets under 240 characters for better engagement
- Use more practical examples from real protocols
- Include relevant hashtags: #DeFi #CryptoEducation #Web3
- Link to resources when discussing complex topics
- Use thread format for longer explanations

[Rest of personality...]
"""
```

#### Step 4: A/B Test Different Approaches

Test different content strategies:

```python
# test_content_types.py
from xynae import Xynae
from dotenv import load_dotenv

load_dotenv()

agent = Xynae(
    personality="Your refined personality...",
    llm_provider="auto",
    use_database=False
)

# Test different tweet types
tweet_types = ["insight", "ecosystem", "autonomy", "invitation"]

print("🧪 Testing content types:\n")

for tweet_type in tweet_types:
    print(f"\n{'='*50}")
    print(f"Type: {tweet_type}")
    print(f"{'='*50}")
    
    for i in range(3):
        tweet = agent.generate_tweet(tweet_type=tweet_type, language="english")
        print(f"\nVariation {i+1}:\n{tweet}")
        print(f"Length: {len(tweet)} chars")
```

***
