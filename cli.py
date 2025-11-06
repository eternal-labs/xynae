"""
Xynae CLI - Command-line interface for Xynae framework
Provides easy-to-use commands for managing and interacting with Xynae
"""

import argparse
import sys
import json
from datetime import datetime
from typing import Optional

try:
    from xynae import Xynae
except ImportError:
    print("Error: Could not import Xynae. Make sure xynae.py is in the same directory.")
    sys.exit(1)


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_success(text: str):
    """Print success message"""
    print(f"✓ {text}")


def print_error(text: str):
    """Print error message"""
    print(f"✗ {text}")


def print_info(text: str):
    """Print info message"""
    print(f"ℹ {text}")


def cmd_run(args):
    """Run the main Xynae bot loop"""
    try:
        print_header("Starting Xynae Bot")
        
        # Parse intervals
        tweet_interval = args.tweet_interval * 60 if args.tweet_interval else 1200
        check_interval = args.check_interval * 60 if args.check_interval else 300
        
        # Initialize Xynae
        xynae_kwargs = {}
        if args.llm_provider:
            xynae_kwargs["llm_provider"] = args.llm_provider
        if args.mongodb_uri:
            xynae_kwargs["mongodb_uri"] = args.mongodb_uri
        if args.database_name:
            xynae_kwargs["database_name"] = args.database_name
        if args.no_database:
            xynae_kwargs["use_database"] = False
        
        xynae = Xynae(**xynae_kwargs)
        
        print_info(f"Tweet interval: {tweet_interval//60} minutes")
        print_info(f"Check interval: {check_interval//60} minutes")
        print()
        
        # Run the bot
        xynae.run(tweet_interval=tweet_interval, check_interval=check_interval)
        
    except KeyboardInterrupt:
        print("\n\nBot stopped by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Failed to run bot: {e}")
        sys.exit(1)


def cmd_generate(args):
    """Generate tweets without posting"""
    try:
        print_header("Generating Tweet")
        
        # Initialize Xynae
        xynae_kwargs = {}
        if args.llm_provider:
            xynae_kwargs["llm_provider"] = args.llm_provider
        if args.mongodb_uri:
            xynae_kwargs["mongodb_uri"] = args.mongodb_uri
        if args.database_name:
            xynae_kwargs["database_name"] = args.database_name
        if args.no_database:
            xynae_kwargs["use_database"] = False
        if args.personality_file:
            with open(args.personality_file, 'r', encoding='utf-8') as f:
                xynae_kwargs["personality"] = f.read()
        
        xynae = Xynae(**xynae_kwargs)
        
        # Generate tweet
        tweet_type = args.type or "insight"
        language = args.language or "auto"
        count = args.count or 1
        
        print_info(f"Type: {tweet_type}")
        print_info(f"Language: {language}")
        print_info(f"Count: {count}")
        print()
        
        tweets = []
        for i in range(count):
            tweet = xynae.generate_tweet(tweet_type=tweet_type, language=language)
            tweets.append(tweet)
            
            print(f"[{i+1}/{count}]")
            print(f"{tweet}")
            print(f"Characters: {len(tweet)}/280\n")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for tweet in tweets:
                    f.write(tweet + "\n\n")
            print_success(f"Saved {count} tweet(s) to {args.output}")
        
        return tweets
        
    except Exception as e:
        print_error(f"Failed to generate tweet: {e}")
        sys.exit(1)


def cmd_status(args):
    """Check system status"""
    try:
        print_header("System Status")
        
        xynae_kwargs = {}
        if args.mongodb_uri:
            xynae_kwargs["mongodb_uri"] = args.mongodb_uri
        if args.database_name:
            xynae_kwargs["database_name"] = args.database_name
        if args.no_database:
            xynae_kwargs["use_database"] = False
        
        xynae = Xynae(**xynae_kwargs)
        
        # Check LLM providers
        print("LLM Providers:")
        available = xynae.llm_manager.list_available_providers()
        if available:
            for provider in available:
                print_success(f"  {provider.capitalize()}: Available")
        else:
            print_error("  No LLM providers configured")
        
        print()
        
        # Check Twitter connection
        print("Twitter/X Connection:")
        if xynae.twitter_client:
            try:
                me = xynae.twitter_client.get_me()
                if me.data:
                    print_success(f"  Connected as @{me.data.username}")
                else:
                    print_error("  Connected but unable to get user info")
            except Exception as e:
                print_error(f"  Connection failed: {e}")
        else:
            print_error("  Not configured (missing API keys)")
        
        print()
        
        # Check database
        print("Database:")
        if xynae.db and xynae.db.is_connected():
            print_success(f"  Connected to MongoDB: {xynae.db.database_name}")
            stats = xynae.db.get_stats()
            print_info(f"  Tweets: {stats.get('tweets_count', 0)}")
            print_info(f"  Replies: {stats.get('replies_count', 0)}")
            print_info(f"  Mentions: {stats.get('mentions_count', 0)}")
        else:
            print_error("  Not connected (running in memory-only mode)")
        
        print()
        
    except Exception as e:
        print_error(f"Failed to check status: {e}")
        sys.exit(1)


def cmd_stats(args):
    """Show database statistics"""
    try:
        print_header("Database Statistics")
        
        xynae_kwargs = {}
        if args.mongodb_uri:
            xynae_kwargs["mongodb_uri"] = args.mongodb_uri
        if args.database_name:
            xynae_kwargs["database_name"] = args.database_name
        if args.no_database:
            xynae_kwargs["use_database"] = False
        
        xynae = Xynae(**xynae_kwargs)
        
        if not xynae.db or not xynae.db.is_connected():
            print_error("Database not connected. Cannot show statistics.")
            print_info("Tip: Make sure MongoDB is running and configured.")
            sys.exit(1)
        
        stats = xynae.db.get_stats()
        
        print(f"Database: {stats.get('database', 'unknown')}")
        print()
        print(f"Tweets:")
        print(f"  Total: {stats.get('tweets_count', 0)}")
        print(f"  Posted: {stats.get('posted_tweets', 0)}")
        print()
        print(f"Replies:")
        print(f"  Total: {stats.get('replies_count', 0)}")
        print()
        print(f"Mentions:")
        print(f"  Total: {stats.get('mentions_count', 0)}")
        print(f"  Replied: {stats.get('replied_mentions', 0)}")
        print()
        print(f"Conversations:")
        print(f"  Total: {stats.get('conversations_count', 0)}")
        print()
        
        # Show recent tweets if requested
        if args.recent:
            print("Recent Tweets:")
            recent = xynae.db.get_recent_tweets(limit=args.recent)
            if recent:
                for i, tweet in enumerate(recent, 1):
                    posted = "✓" if tweet.get('posted') else "✗"
                    print(f"\n  [{i}] {posted} {tweet.get('tweet_type', 'unknown').upper()}")
                    print(f"      {tweet.get('tweet_text', '')[:100]}...")
                    print(f"      Language: {tweet.get('language', 'unknown')}")
                    print(f"      Created: {tweet.get('created_at', 'unknown')}")
            else:
                print_info("  No tweets found")
        
        # Export to JSON if requested
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            print_success(f"Statistics exported to {args.json}")
        
    except Exception as e:
        print_error(f"Failed to get statistics: {e}")
        sys.exit(1)


def cmd_test(args):
    """Test configuration and connections"""
    try:
        print_header("Testing Configuration")
        
        # Test LLM providers
        print("Testing LLM Providers...")
        xynae_kwargs = {}
        if args.llm_provider:
            xynae_kwargs["llm_provider"] = args.llm_provider
        if args.no_database:
            xynae_kwargs["use_database"] = False
        
        xynae = Xynae(**xynae_kwargs)
        
        available = xynae.llm_manager.list_available_providers()
        if not available:
            print_error("No LLM providers available. Please configure API keys.")
            sys.exit(1)
        
        print_success(f"Available providers: {', '.join(available)}")
        
        # Test LLM generation
        print("\nTesting LLM generation...")
        try:
            test_tweet = xynae.generate_tweet(tweet_type="insight", language="english")
            print_success("LLM generation works!")
            print(f"  Sample tweet: {test_tweet[:60]}...")
        except Exception as e:
            print_error(f"LLM generation failed: {e}")
            sys.exit(1)
        
        # Test Twitter connection
        print("\nTesting Twitter/X connection...")
        if xynae.twitter_client:
            try:
                me = xynae.twitter_client.get_me()
                if me.data:
                    print_success(f"Twitter connection OK: @{me.data.username}")
                else:
                    print_error("Twitter connection failed")
            except Exception as e:
                print_error(f"Twitter connection failed: {e}")
        else:
            print_error("Twitter not configured (missing API keys)")
        
        # Test database
        print("\nTesting database connection...")
        if xynae.db and xynae.db.is_connected():
            print_success(f"Database connection OK: {xynae.db.database_name}")
        else:
            print_error("Database not connected (will run in memory-only mode)")
        
        print("\n" + "="*60)
        print_success("Configuration test complete!")
        print("="*60 + "\n")
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        sys.exit(1)


def cmd_version(args):
    """Show version information"""
    print_header("Xynae Version Information")
    print("Xynae - AI-powered social media automation framework")
    print()
    print("Version: 1.0.0")
    print("Python: " + sys.version.split()[0])
    print()


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='xynae',
        description='Xynae CLI - Command-line interface for Xynae framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the bot with default settings
  xynae run

  # Run with custom intervals (30 min tweets, 2 min checks)
  xynae run --tweet-interval 30 --check-interval 2

  # Generate a tweet without posting
  xynae generate

  # Generate multiple tweets of different types
  xynae generate --type insight --count 5 --language english

  # Check system status
  xynae status

  # Show database statistics
  xynae stats --recent 10

  # Test configuration
  xynae test
        """
    )
    
    # Common arguments
    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument(
        '--llm-provider',
        choices=['auto', 'anthropic', 'openai', 'gemini'],
        help='Preferred LLM provider'
    )
    common_args.add_argument(
        '--mongodb-uri',
        help='MongoDB connection string'
    )
    common_args.add_argument(
        '--database-name',
        default='xynae',
        help='MongoDB database name (default: xynae)'
    )
    common_args.add_argument(
        '--no-database',
        action='store_true',
        help='Run without database (memory-only mode)'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Run command
    run_parser = subparsers.add_parser(
        'run',
        help='Run the main Xynae bot loop',
        parents=[common_args]
    )
    run_parser.add_argument(
        '--tweet-interval',
        type=int,
        help='Minutes between tweets (default: 20)'
    )
    run_parser.add_argument(
        '--check-interval',
        type=int,
        help='Minutes between mention checks (default: 5)'
    )
    run_parser.set_defaults(func=cmd_run)
    
    # Generate command
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate tweets without posting',
        parents=[common_args]
    )
    generate_parser.add_argument(
        '--type',
        choices=['insight', 'ecosystem', 'autonomy', 'invitation'],
        help='Type of tweet to generate (default: insight)'
    )
    generate_parser.add_argument(
        '--language',
        choices=['english', 'chinese', 'mixed', 'auto'],
        help='Language for tweet (default: auto)'
    )
    generate_parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of tweets to generate (default: 1)'
    )
    generate_parser.add_argument(
        '--output',
        '-o',
        help='Save tweets to file'
    )
    generate_parser.add_argument(
        '--personality-file',
        help='Path to custom personality file'
    )
    generate_parser.set_defaults(func=cmd_generate)
    
    # Status command
    status_parser = subparsers.add_parser(
        'status',
        help='Check system status',
        parents=[common_args]
    )
    status_parser.set_defaults(func=cmd_status)
    
    # Stats command
    stats_parser = subparsers.add_parser(
        'stats',
        help='Show database statistics',
        parents=[common_args]
    )
    stats_parser.add_argument(
        '--recent',
        type=int,
        help='Show N recent tweets'
    )
    stats_parser.add_argument(
        '--json',
        help='Export statistics to JSON file'
    )
    stats_parser.set_defaults(func=cmd_stats)
    
    # Test command
    test_parser = subparsers.add_parser(
        'test',
        help='Test configuration and connections',
        parents=[common_args]
    )
    test_parser.set_defaults(func=cmd_test)
    
    # Version command
    version_parser = subparsers.add_parser(
        'version',
        help='Show version information'
    )
    version_parser.set_defaults(func=cmd_version)
    
    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

