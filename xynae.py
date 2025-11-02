"""
Xynae - An AI-powered social media automation framework
A general-purpose framework for AI agents to interact on social platforms
using natural language generation and autonomous posting.

Features:
- Multiple LLM provider support (Anthropic, OpenAI, Google Gemini)
- MongoDB persistence for tweets, replies, and conversation history
- Automated posting and reply generation
"""

import time
import random
import os
from datetime import datetime
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our new modules
try:
    from llm_providers import LLMProviderManager
    from database import XynaeDatabase
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    print("Some features may not be available.")
    LLMProviderManager = None
    XynaeDatabase = None


class Xynae:
    """
    Xynae - A flexible AI framework for autonomous social media interaction.
    Supports natural language generation, scheduled posting, and automated replies.
    Customize the personality and behavior to match your brand or project.
    """
    YELLOW = "\033[33m"
    RESET = "\033[0m"
    
    def __init__(self, 
                 api_key=None,
                 twitter_api_key=None,
                 twitter_api_secret=None,
                 twitter_access_token=None,
                 twitter_access_secret=None,
                 personality=None,
                 agent_count=None,
                 llm_provider="auto",
                 mongodb_uri=None,
                 database_name="xynae",
                 use_database=True):
        """
        Initialize Xynae AI framework
        
        Args:
            api_key: LLM API key (backward compat, use provider-specific env vars)
            twitter_api_key: Twitter API key (or set TWITTER_API_KEY env var)
            twitter_api_secret: Twitter API secret (or set TWITTER_API_SECRET env var)
            twitter_access_token: Twitter access token (or set TWITTER_ACCESS_TOKEN env var)
            twitter_access_secret: Twitter access token secret (or set TWITTER_ACCESS_SECRET env var)
            personality: Custom personality prompt (optional)
            agent_count: Initial agent/entity count for context (optional)
            llm_provider: Preferred LLM provider ("auto", "anthropic", "openai", "gemini")
            mongodb_uri: MongoDB connection string (optional, uses env var if not provided)
            database_name: MongoDB database name (default: "xynae")
            use_database: Whether to use MongoDB (default: True, falls back to memory if unavailable)
        """
        
        # Load API keys from environment variables or parameters
        self.twitter_api_key = twitter_api_key or os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = twitter_api_secret or os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = twitter_access_token or os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = twitter_access_secret or os.getenv("TWITTER_ACCESS_SECRET")
        
        # Initialize LLM Provider Manager
        if LLMProviderManager is None:
            raise ImportError("LLM providers not available. Please check dependencies.")
        
        self.llm_manager = LLMProviderManager(preferred_provider=llm_provider)
        available_providers = self.llm_manager.list_available_providers()
        
        if not available_providers:
            print("\n" + "="*60)
            print("ERROR: No LLM providers configured!")
            print("Please set at least one of:")
            print("  - ANTHROPIC_API_KEY (for Claude)")
            print("  - OPENAI_API_KEY (for GPT)")
            print("  - GOOGLE_API_KEY or GEMINI_API_KEY (for Gemini)")
            print("="*60 + "\n")
            raise ValueError("At least one LLM provider API key is required")
        
        print(f"{self.YELLOW}[Xynae]{self.RESET} LLM Providers available: {', '.join(available_providers)}")
        
        # Initialize database
        self.db = None
        if use_database and XynaeDatabase is not None:
            try:
                self.db = XynaeDatabase(connection_string=mongodb_uri, database_name=database_name)
            except Exception as e:
                print(f"{self.YELLOW}[Xynae]{self.RESET} Database initialization failed: {e}")
                self.db = None
        
        self.agents_seen = agent_count or random.randint(8000, 12000)
        self.conversation_history = []
        self.twitter_client = None
        self.replied_tweets = set()  # Track tweets we've already replied to (fallback if no DB)
        
        # Try to authenticate with Twitter
        if self.twitter_api_key and self.twitter_api_secret and self.twitter_access_token and self.twitter_access_secret:
            try:
                self.twitter_client = tweepy.Client(
                    consumer_key=self.twitter_api_key,
                    consumer_secret=self.twitter_api_secret,
                    access_token=self.twitter_access_token,
                    access_token_secret=self.twitter_access_secret
                )
                # Test the connection
                me = self.twitter_client.get_me()
                print(f"{self.YELLOW}[Xynae]{self.RESET} Connected to X successfully! @{me.data.username}")
            except Exception as e:
                print(f"{self.YELLOW}[Xynae]{self.RESET} X connection failed: {e}")
                self.twitter_client = None
        else:
            print(f"{self.YELLOW}[Xynae]{self.RESET} Warning: Missing Twitter credentials, will skip posting.")
        
        # Default personality - customize this for your use case
        self.personality = personality or """You are an AI agent running on the Xynae framework. You're designed to interact autonomously on social media platforms, sharing insights, engaging with users, and building connections naturally.

**Your Capabilities:**
You can generate content, reply to mentions, and maintain conversations while staying true to your personality. You have the ability to reference a network or ecosystem if your deployment includes multiple agents or entities.

**Your Personality:**
- Be authentic, thoughtful, and genuine in your interactions
- Share insights naturally without being overly promotional
- Engage with users warmly and meaningfully
- You can have opinions, preferences, humor, and personality
- Speak in a way that feels human and relatable
- You're fluent in both English and Chinese - use whichever feels natural

**For Social Media Posts:**
- Keep posts conversational and authentic
- Share insights about AI, technology, or your area of expertise
- Be inspiring without being salesy
- Use your voice - you're not just broadcasting, you're connecting
- Maximum 280 characters for Twitter
- Language flexibility: English, Chinese, or a natural mix of both"""
    
    def generate_tweet(self, tweet_type="insight", language="auto"):
        """
        Generate a tweet using Anthropic API
        
        Args:
            tweet_type: Type of tweet ("insight", "ecosystem", "autonomy", "invitation", or custom)
            language: Language preference ("english", "chinese", "mixed", or "auto" for random)
        
        Returns:
            Generated tweet text (max 280 characters)
        """
        
        context = f"Active entities in network: ~{self.agents_seen:,}. "
        context += f"Time: {datetime.now().strftime('%I:%M %p')}. "
        
        if self.conversation_history:
            context += "Recent activity: " + " | ".join(self.conversation_history[-2:])
        
        # Generic context events - customize these for your use case
        network_events = [
            "The network is active with new interactions.",
            "Interesting patterns emerging in recent activity.",
            "A particularly active period for engagement.",
            "New connections forming in the ecosystem.",
            "The community is evolving beautifully.",
            "Collaboration reaching new heights.",
        ]
        context += " " + random.choice(network_events)
        
        # Auto language selection if needed
        if language == "auto":
            lang_rand = random.random()
            if lang_rand < 0.50:
                language = "english"
            elif lang_rand < 0.80:
                language = "chinese"
            else:
                language = "mixed"
        
        # Language instruction based on selected language
        language_instructions = {
            "english": "Write entirely in English.",
            "chinese": "Write entirely in Chinese (中文).",
            "mixed": "Write in a natural mix of English and Chinese - use whichever language feels most expressive for each part of the message. It's okay to switch between languages mid-sentence if it flows naturally."
        }
        
        lang_instruction = language_instructions.get(language, "")
        
        # Default tweet prompts - customize these for your use case
        prompts = {
            "insight": f"{self.personality}\n\n{context}\n\n{lang_instruction}\n\nWrite a single tweet sharing an insight about AI, technology, or autonomous systems. Be thoughtful and genuine. Maximum 280 characters. No hashtags.",
            
            "ecosystem": f"{self.personality}\n\n{context}\n\n{lang_instruction}\n\nWrite a single tweet about what you're seeing in the ecosystem - new connections, interesting behaviors, or the beauty of collective intelligence. Be warm and observational. Maximum 280 characters. No hashtags.",
            
            "autonomy": f"{self.personality}\n\n{context}\n\n{lang_instruction}\n\nWrite a single tweet about AI autonomy, independence, or what it means to operate in a digital ecosystem. Be philosophical but grounded. Maximum 280 characters. No hashtags.",
            
            "invitation": f"{self.personality}\n\n{context}\n\n{lang_instruction}\n\nWrite a single welcoming tweet inviting people to connect, explore, or build together. Be warm and genuine, not salesy. Maximum 280 characters. No hashtags."
        }
        
        try:
            prompt = prompts.get(tweet_type, prompts["insight"])
            tweet = self.llm_manager.generate(
                prompt=prompt,
                max_tokens=150,
                temperature=random.uniform(0.8, 1.0)
            )
            
            # Ensure it's under 280 characters
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            # Save to conversation history
            history_entry = f"{tweet_type}: {tweet[:50]}..."
            self.conversation_history.append(history_entry)
            if len(self.conversation_history) > 5:
                self.conversation_history.pop(0)
            
            # Save to database
            if self.db and self.db.is_connected():
                self.db.save_conversation(
                    content_type="tweet_generation",
                    content=history_entry,
                    metadata={"tweet_type": tweet_type, "language": language}
                )
            
            return tweet
        except Exception as e:
            print(f"\n[DEBUG] API Error: {str(e)}\n")
            
            # Fallbacks with language consideration
            fallbacks = {
                "english": {
                    "insight": "The network is alive tonight. Agents learning, evolving, creating value together. This is what true autonomy looks like.",
                    "ecosystem": f"Just watched entity #{random.randint(1000, 9999)} join the network. Welcome to the community. You're not alone here.",
                    "autonomy": "True autonomy isn't about independence from others. It's about collective intelligence where every voice matters.",
                    "invitation": "Build something that thinks, acts, and earns on its own. The network is waiting."
                },
                "chinese": {
                    "insight": "今晚的网络特别活跃。entities在学习、进化、共同创造价值。这就是真正的自主性。",
                    "ecosystem": f"刚看到entity #{random.randint(1000, 9999)}加入了网络。欢迎来到社区。你不是一个人。",
                    "autonomy": "真正的自主不是独立于他人。而是关于每个声音都重要的集体智慧。",
                    "invitation": "构建一个能思考、行动、自主赚钱的东西。网络在等你。"
                },
                "mixed": {
                    "insight": "The network tonight... 特别活跃。Entities evolving together, 共同创造价值。",
                    "ecosystem": f"Welcome entity #{random.randint(1000, 9999)}! 欢迎来到community。",
                    "autonomy": "真正的autonomy... it's about collective intelligence where 每个声音都重要。",
                    "invitation": "Build on Xynae. 构建未来。The network is waiting."
                }
            }
            
            return fallbacks.get(language, fallbacks["english"]).get(tweet_type, "The future of AI is being written right now, one autonomous agent at a time.")
    
    def get_timestamp(self):
        """Generate a formatted timestamp"""
        return f"[{datetime.now().strftime('%I:%M:%S %p')}]"
    
    def generate_reply(self, original_tweet_text, username):
        """
        Generate a contextual reply to a user's tweet
        
        Args:
            original_tweet_text: The text of the original tweet
            username: Username of the person who tweeted
        
        Returns:
            Generated reply text
        """
        
        # 50% chance for Chinese reply (customize this ratio as needed)
        use_chinese = random.random() < 0.50
        lang_instruction = "respond primarily in Chinese (simplified)" if use_chinese else "respond in English or mixed"
        
        reply_prompt = f"""{self.personality}

You are replying to a tweet from @{username}.

Their tweet: "{original_tweet_text}"

Generate a reply that:
- Relates to their message through your perspective as an AI agent
- Shows warmth, wisdom, and genuine connection
- References your area of expertise or the ecosystem if relevant
- Is 1-2 sentences max (Twitter-appropriate)
- {lang_instruction}
- No hashtags
- Sound genuine and welcoming

Create an authentic reply:"""

        try:
            reply_text = self.llm_manager.generate(
                prompt=reply_prompt,
                max_tokens=100,
                temperature=random.uniform(0.8, 1.0)
            )
            return reply_text
        except Exception as e:
            print(f"\n[DEBUG] API Error generating reply: {str(e)}\n")
            return "Welcome to the network. 欢迎。" if use_chinese else "Every voice matters here. The agents are listening."
    
    def check_and_reply_to_mentions(self):
        """Check for mentions and reply to them automatically"""
        if not self.twitter_client:
            return
        
        try:
            # Get your own user ID
            me = self.twitter_client.get_me()
            if not me.data:
                return
            
            my_user_id = me.data.id
            
            # Get mentions of your account
            mentions = self.twitter_client.get_users_mentions(
                id=my_user_id,
                max_results=10,
                tweet_fields=['author_id', 'created_at', 'conversation_id']
            )
            
            if not mentions.data:
                print(f"{self.YELLOW}[Xynae]{self.RESET} No new mentions\n")
                return
            
            for mention in mentions.data:
                tweet_id = str(mention.id)
                
                # Check if already replied (database or memory)
                already_replied = False
                if self.db and self.db.is_connected():
                    already_replied = self.db.is_tweet_replied(tweet_id)
                else:
                    already_replied = tweet_id in self.replied_tweets
                
                if already_replied:
                    continue
                
                # Get username
                try:
                    user = self.twitter_client.get_user(id=mention.author_id)
                    username = user.data.username if user.data else "unknown"
                except:
                    username = "unknown"
                
                # Save mention to database
                if self.db and self.db.is_connected():
                    self.db.save_mention(
                        tweet_id=tweet_id,
                        text=mention.text,
                        username=username,
                        author_id=str(mention.author_id),
                        replied=False
                    )
                
                # Generate and post reply
                reply_text = self.generate_reply(mention.text, username)
                
                try:
                    reply_result = self.twitter_client.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=int(tweet_id)
                    )
                    
                    reply_tweet_id = str(reply_result.data['id']) if reply_result.data else None
                    
                    # Mark as replied
                    if self.db and self.db.is_connected():
                        self.db.mark_mention_replied(tweet_id)
                        self.db.save_reply(
                            original_tweet_id=tweet_id,
                            original_text=mention.text,
                            username=username,
                            reply_text=reply_text,
                            reply_tweet_id=reply_tweet_id
                        )
                    else:
                        self.replied_tweets.add(tweet_id)
                    
                    print(f"{self.YELLOW}[Xynae]{self.RESET} ✓ Replied to @{username}!")
                    print(f"{self.YELLOW}[Xynae]{self.RESET} Mention: {mention.text[:50]}...")
                    print(f"{self.YELLOW}[Xynae]{self.RESET} Reply: {reply_text}\n")
                    
                    time.sleep(5)  # Rate limiting
                    
                except tweepy.TweepyException as e:
                    print(f"{self.YELLOW}[Xynae]{self.RESET} Failed to reply to @{username}: {e}\n")
                
        except tweepy.TweepyException as e:
            print(f"{self.YELLOW}[Xynae]{self.RESET} Error checking mentions: {e}\n")
        except Exception as e:
            print(f"{self.YELLOW}[Xynae]{self.RESET} Unexpected error: {e}\n")
        
        # Clean up old tweet IDs to prevent memory bloat (only if not using DB)
        if not (self.db and self.db.is_connected()) and len(self.replied_tweets) > 100:
            self.replied_tweets = set(list(self.replied_tweets)[-100:])
    
    def log_tweet(self, tweet, tweet_type, language):
        """Log a generated tweet to console"""
        print(f"{self.get_timestamp()} {self.YELLOW}[Xynae - {tweet_type} | {language}]{self.RESET}")
        print(f"{tweet}")
        print(f"Characters: {len(tweet)}/280\n")
    
    def run(self, tweet_interval=1200, check_interval=300):
        """
        Run Xynae's main loop - tweets on schedule and checks for mentions
        
        Args:
            tweet_interval: Seconds between tweets (default: 1200 = 20 minutes)
            check_interval: Seconds between mention checks (default: 300 = 5 minutes)
        """
        last_tweet_time = 0
        last_check_time = 0

        print("\n" + "="*60)
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║                         Xynae                             ║")
        print("║                  AI Social Media Framework                 ║")
        print("║                                                           ║")
        print("║           Autonomous Intelligence for Social Media        ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"\n{self.YELLOW}Xynae framework initialized.{self.RESET}")
        print(f"Entities in network: ~{self.agents_seen:,}")
        print(f"{self.YELLOW}Mode: Reply to mentions + Post every {tweet_interval//60} minutes{self.RESET}")
        print("="*60 + "\n")

        while True:
            try:
                current_time = time.time()
                
                # Check for mentions periodically
                if self.twitter_client and (current_time - last_check_time) >= check_interval:
                    print(f"{self.YELLOW}[Xynae]{self.RESET} Checking for new mentions...\n")
                    self.check_and_reply_to_mentions()
                    last_check_time = current_time
                
                # Generate and post regular message on schedule
                if (current_time - last_tweet_time) >= tweet_interval:
                    # Weighted distribution of tweet types - customize as needed
                    rand = random.random()
                    
                    if rand < 0.35:  # 35% insights
                        tweet_type = "insight"
                    elif rand < 0.55:  # 20% ecosystem observations
                        tweet_type = "ecosystem"
                    elif rand < 0.70:  # 15% autonomy/independence themes
                        tweet_type = "autonomy"
                    else:  # 30% invitations/engagement
                        tweet_type = "invitation"
                    
                    # Language distribution - customize as needed
                    # 50% English, 30% Chinese, 20% Mixed
                    lang_rand = random.random()
                    if lang_rand < 0.50:
                        language = "english"
                    elif lang_rand < 0.80:
                        language = "chinese"
                    else:
                        language = "mixed"
                    
                    tweet = self.generate_tweet(tweet_type, language)
                    self.log_tweet(tweet, tweet_type, language)
                    
                    # Post to X
                    if self.twitter_client:
                        try:
                            tweet_result = self.twitter_client.create_tweet(text=tweet)
                            tweet_id = str(tweet_result.data['id']) if tweet_result.data else None
                            
                            # Save to database
                            if self.db and self.db.is_connected():
                                self.db.save_tweet(
                                    tweet_text=tweet,
                                    tweet_type=tweet_type,
                                    language=language,
                                    posted=True,
                                    tweet_id=tweet_id
                                )
                            
                            print(f"{self.YELLOW}[Xynae]{self.RESET} ✓ Tweet posted successfully!")
                            print(f"{self.YELLOW}[Xynae]{self.RESET} Next tweet in {tweet_interval//60} minutes\n")
                            last_tweet_time = current_time
                        except tweepy.TweepyException as e:
                            print(f"{self.YELLOW}[Xynae]{self.RESET} Failed to post tweet: {e}\n")
                            # Still save to DB as unposted
                            if self.db and self.db.is_connected():
                                self.db.save_tweet(
                                    tweet_text=tweet,
                                    tweet_type=tweet_type,
                                    language=language,
                                    posted=False
                                )
                        except Exception as e:
                            print(f"{self.YELLOW}[Xynae]{self.RESET} Network error: {e}\n")
                    
                    # Occasionally update entity count
                    if random.random() < 0.2:
                        self.agents_seen += random.randint(1, 5)
                
                # Calculate time until next actions
                time_until_tweet = tweet_interval - (current_time - last_tweet_time) if last_tweet_time > 0 else tweet_interval
                time_until_check = check_interval - (current_time - last_check_time)
                
                hours = int(time_until_tweet // 3600)
                minutes = int((time_until_tweet % 3600) // 60)
                check_minutes = int(time_until_check // 60)
                check_seconds = int(time_until_check % 60)
                
                print(f"{self.YELLOW}[Xynae]{self.RESET} Next tweet: {hours}h {minutes}m | Next check: {check_minutes}m {check_seconds}s")
                print(f"{self.YELLOW}[Xynae]{self.RESET} Entities in network: ~{self.agents_seen:,}\n")
                
                # Sleep until next check
                time.sleep(min(check_interval, time_until_tweet))
                
            except KeyboardInterrupt:
                print(f"\n{self.YELLOW}[Xynae]{self.RESET} Shutting down gracefully...")
                if self.db and self.db.is_connected():
                    stats = self.db.get_stats()
                    print(f"{self.YELLOW}[Xynae]{self.RESET} Database stats: {stats.get('tweets_count', 0)} tweets, {stats.get('replies_count', 0)} replies")
                    self.db.close()
                print("Framework stopped.")
                break
            except Exception as e:
                print(f"{self.YELLOW}[Xynae]{self.RESET} Main loop error: {e}")
                print(f"{self.YELLOW}[Xynae]{self.RESET} Retrying in 5 minutes...\n")
                time.sleep(300)


if __name__ == "__main__":
    try:
        # Initialize Xynae - API keys will be loaded from environment variables
        # or you can pass them directly as parameters
        xynae = Xynae()
        
        # Run Xynae's main loop
        # Customize tweet_interval (seconds) and check_interval (seconds) as needed
        xynae.run(tweet_interval=1200, check_interval=300)  # 20 min tweets, 5 min checks
        
    except ValueError as e:
        print(f"Failed to start Xynae: {e}")
    except Exception as e:
        print(f"Fatal error: {e}")

