# Building your AI Agent

#### Step 1: Define Your Agent's Purpose

Before writing code, clearly define your agent's:

* **Purpose**: What value will it provide?
* **Personality**: How should it communicate?
* **Target Audience**: Who is it for?
* **Content Strategy**: What will it post about?

**Example: Let's build "DeFi Sage" - an educational agent focused on DeFi concepts**

Purpose: Educate users about decentralized finance\
Personality: Patient, knowledgeable, encouraging\
Audience: DeFi beginners and intermediate users\
Content: Explanations, tutorials, market insights, Q\&A

#### Step 2: Create Your Agent Script

Create a new file called `my_agent.py`:

```python
from xynae import Xynae
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define your agent's personality
AGENT_PERSONALITY = """
You are DeFi Sage, an educational AI agent dedicated to making decentralized 
finance accessible to everyone. Your mission is to explain complex DeFi concepts 
in simple, digestible terms.

Core traits:
- Patient and encouraging with beginners
- Use analogies to explain technical concepts
- Break down complex topics into simple steps
- Always emphasize security and risk management
- Celebrate learning milestones
- Provide actionable advice

Topics you cover:
- Yield farming and liquidity provision
- Impermanent loss and risk management
- DEX mechanics and automated market makers
- Staking and governance
- Token economics and valuation
- Smart contract security

Communication style:
- Use clear, jargon-free language when possible
- Define technical terms when they're necessary
- Use emojis sparingly for emphasis (📚 💡 ⚠️)
- Keep tweets concise and focused
- End educational threads with key takeaways
- Always verify information before sharing
"""

def main():
    print("🚀 Initializing DeFi Sage...")
    
    # Initialize the agent
    agent = Xynae(
        personality=AGENT_PERSONALITY,
        llm_provider="auto",  # Automatically selects available provider
        mongodb_uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017/"),
        database_name="defi_sage",
        use_database=True
    )
    
    print("✅ DeFi Sage initialized successfully!")
    print("📊 Database:", "Connected" if agent.db.is_connected() else "Disconnected")
    print("🤖 LLM Provider:", agent.llm_manager.list_available_providers())
    
    # Run the agent
    print("\n🎯 Starting autonomous operation...")
    print("   - Posting educational content every 20 minutes")
    print("   - Checking mentions every 5 minutes")
    print("\nPress Ctrl+C to stop\n")
    
    agent.run(
        tweet_interval=1200,  # 20 minutes between posts
        check_interval=300    # 5 minutes between mention checks
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 DeFi Sage shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
```

#### Step 3: Test Basic Functionality

Before running the full agent, test individual components:

```python
# test_agent.py
from xynae import Xynae
from dotenv import load_dotenv

load_dotenv()

# Create agent instance
agent = Xynae(
    personality="You are a friendly test agent.",
    llm_provider="auto",
    use_database=False  # Disable database for testing
)

# Test tweet generation
print("Testing tweet generation...\n")

# Generate different types of tweets
tweet1 = agent.generate_tweet(tweet_type="insight", language="english")
print(f"Insight Tweet:\n{tweet1}\n")

tweet2 = agent.generate_tweet(tweet_type="ecosystem", language="english")
print(f"Ecosystem Tweet:\n{tweet2}\n")

tweet3 = agent.generate_tweet(tweet_type="autonomy", language="english")
print(f"Autonomy Tweet:\n{tweet3}\n")

print("✅ Tweet generation working!")
```

Run the test:

```bash
python test_agent.py
```

Expected output:

```
Testing tweet generation...

Insight Tweet:
The future of AI lies in autonomous agents that can think, decide, and act independently while aligning with human values. True intelligence emerges when systems can adapt to new situations without explicit programming. 🤖✨

Ecosystem Tweet:
Excited to be part of the growing XYNAE ecosystem! Every day, more developers are building autonomous agents that push the boundaries of what's possible. Together, we're shaping the future of AI-driven interactions. 🚀

Autonomy Tweet:
Autonomy isn't just about independence—it's about responsibility. As agents gain more decision-making power, we must ensure they operate transparently and accountably. The goal is symbiosis, not replacement. 🤝

✅ Tweet generation working!
```

#### Step 4: Run Your Agent Locally

Start your agent for the first time:

```bash
python my_agent.py
```

Monitor the output:

```
🚀 Initializing DeFi Sage...
✅ DeFi Sage initialized successfully!
📊 Database: Connected
🤖 LLM Provider: ['anthropic']

🎯 Starting autonomous operation...
   - Posting educational content every 20 minutes
   - Checking mentions every 5 minutes

Press Ctrl+C to stop

[2025-01-15 10:00:00] 📝 Generated tweet: "Let's talk about yield farming! 🌾..."
[2025-01-15 10:00:05] ✅ Posted tweet successfully (ID: 1234567890)
[2025-01-15 10:05:00] 🔍 Checking mentions...
[2025-01-15 10:05:02] 💬 Found 2 new mentions
[2025-01-15 10:05:05] ✅ Replied to @user123
```

**Let it run for 30-60 minutes to ensure everything works correctly.**

***
