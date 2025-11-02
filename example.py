"""
Example usage of Xynae framework
This file demonstrates different ways to use and customize Xynae
"""

from xynae import Xynae

# Example 1: Basic usage with environment variables
def basic_example():
    """Simple setup using .env file for API keys"""
    xynae = Xynae()
    xynae.run(tweet_interval=1200, check_interval=300)


# Example 2: Custom personality
def custom_personality_example():
    """Using a custom personality for your AI agent"""
    custom_personality = """You are a tech enthusiast AI focused on AI research and development.
    Share insights about machine learning, neural networks, and the future of AI.
    Be educational, inspiring, and genuine in your communications.
    Keep technical but accessible."""
    
    xynae = Xynae(personality=custom_personality)
    xynae.run()


# Example 3: Multiple LLM providers
def multiple_llm_example():
    """Use different LLM providers"""
    # Auto-select from available providers
    xynae = Xynae(llm_provider="auto")
    
    # Or specify a preferred provider
    xynae_openai = Xynae(llm_provider="openai")
    xynae_gemini = Xynae(llm_provider="gemini")
    
    # List available providers
    available = xynae.llm_manager.list_available_providers()
    print(f"Available providers: {available}")


# Example 4: MongoDB persistence
def mongodb_example():
    """Use MongoDB for persistence"""
    # With MongoDB (default)
    xynae = Xynae(
        mongodb_uri="mongodb://localhost:27017/",
        database_name="xynae",
        use_database=True
    )
    
    # Without database (memory-only)
    xynae_memory = Xynae(use_database=False)
    
    # Check database stats
    if xynae.db and xynae.db.is_connected():
        stats = xynae.db.get_stats()
        print(f"Database stats: {stats}")
        
        # Get recent tweets
        recent = xynae.db.get_recent_tweets(limit=10)
        print(f"Recent tweets: {len(recent)}")


# Example 5: Generate tweets without posting
def generate_only_example():
    """Generate tweets for review before posting"""
    xynae = Xynae()
    
    # Generate different types of tweets
    insight_tweet = xynae.generate_tweet(tweet_type="insight", language="english")
    print(f"Insight: {insight_tweet}\n")
    
    ecosystem_tweet = xynae.generate_tweet(tweet_type="ecosystem", language="chinese")
    print(f"Ecosystem: {ecosystem_tweet}\n")
    
    mixed_tweet = xynae.generate_tweet(tweet_type="autonomy", language="mixed")
    print(f"Mixed: {mixed_tweet}\n")


# Example 6: Custom intervals
def custom_intervals_example():
    """Run with custom posting and checking intervals"""
    xynae = Xynae()
    
    # Post every 30 minutes, check mentions every 2 minutes
    xynae.run(tweet_interval=1800, check_interval=120)


# Example 7: Full configuration
def full_config_example():
    """Complete configuration with all features"""
    xynae = Xynae(
        llm_provider="anthropic",  # Preferred LLM
        mongodb_uri="mongodb://localhost:27017/",
        database_name="my_bot",
        agent_count=10000,
        personality="""Your custom personality here...""",
        use_database=True
    )
    
    # Check what's available
    print(f"LLM Providers: {xynae.llm_manager.list_available_providers()}")
    print(f"Database connected: {xynae.db.is_connected() if xynae.db else False}")
    
    xynae.run(tweet_interval=1200, check_interval=300)


if __name__ == "__main__":
    # Uncomment the example you want to run:
    
    # basic_example()
    # custom_personality_example()
    # multiple_llm_example()
    # mongodb_example()
    # generate_only_example()
    # custom_intervals_example()
    # full_config_example()
    
    print("Please uncomment one of the examples above to run it.")
    print("Or create your own customization using Xynae class.")

