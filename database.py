"""
MongoDB Database Integration for Xynae
Stores tweets, replies, mentions, and conversation history
"""

import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError


class XynaeDatabase:
    """MongoDB database wrapper for Xynae"""
    
    def __init__(self, connection_string: str = None, database_name: str = "xynae"):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string (defaults to env var or localhost)
            database_name: Name of the database to use
        """
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", 
            os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")
        )
        self.database_name = database_name
        self.client = None
        self.db = None
        self.connected = False
        
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.connected = True
            print(f"[Database] Connected to MongoDB: {self.database_name}")
        except (ConnectionFailure, ConfigurationError, Exception) as e:
            print(f"[Database] MongoDB connection failed: {e}")
            print(f"[Database] Running in memory-only mode (no persistence)")
            self.connected = False
            self.client = None
            self.db = None
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connected
    
    def save_tweet(self, tweet_text: str, tweet_type: str, language: str, 
                   posted: bool = False, tweet_id: str = None) -> str:
        """
        Save a generated tweet
        
        Returns:
            Document ID
        """
        if not self.connected:
            return None
        
        document = {
            "tweet_text": tweet_text,
            "tweet_type": tweet_type,
            "language": language,
            "posted": posted,
            "tweet_id": tweet_id,
            "created_at": datetime.utcnow(),
            "character_count": len(tweet_text)
        }
        
        result = self.db.tweets.insert_one(document)
        return str(result.inserted_id)
    
    def save_reply(self, original_tweet_id: str, original_text: str, 
                   username: str, reply_text: str, reply_tweet_id: str = None) -> str:
        """
        Save a reply to a mention
        
        Returns:
            Document ID
        """
        if not self.connected:
            return None
        
        document = {
            "original_tweet_id": original_tweet_id,
            "original_text": original_text,
            "username": username,
            "reply_text": reply_text,
            "reply_tweet_id": reply_tweet_id,
            "created_at": datetime.utcnow()
        }
        
        result = self.db.replies.insert_one(document)
        return str(result.inserted_id)
    
    def save_mention(self, tweet_id: str, text: str, username: str, 
                     author_id: str, replied: bool = False) -> str:
        """
        Save a mention received
        
        Returns:
            Document ID
        """
        if not self.connected:
            return None
        
        document = {
            "tweet_id": tweet_id,
            "text": text,
            "username": username,
            "author_id": author_id,
            "replied": replied,
            "created_at": datetime.utcnow()
        }
        
        result = self.db.mentions.insert_one(document)
        return str(result.inserted_id)
    
    def mark_mention_replied(self, tweet_id: str):
        """Mark a mention as replied"""
        if not self.connected:
            return
        
        self.db.mentions.update_one(
            {"tweet_id": tweet_id},
            {"$set": {"replied": True, "replied_at": datetime.utcnow()}}
        )
    
    def is_tweet_replied(self, tweet_id: str) -> bool:
        """Check if a tweet has already been replied to"""
        if not self.connected:
            return False
        
        mention = self.db.mentions.find_one({"tweet_id": tweet_id, "replied": True})
        return mention is not None
    
    def save_conversation(self, content_type: str, content: str, metadata: Dict = None):
        """Save conversation history"""
        if not self.connected:
            return None
        
        document = {
            "content_type": content_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow()
        }
        
        result = self.db.conversations.insert_one(document)
        return str(result.inserted_id)
    
    def get_recent_tweets(self, limit: int = 10) -> List[Dict]:
        """Get recent tweets"""
        if not self.connected:
            return []
        
        return list(self.db.tweets.find().sort("created_at", -1).limit(limit))
    
    def get_recent_replies(self, limit: int = 10) -> List[Dict]:
        """Get recent replies"""
        if not self.connected:
            return []
        
        return list(self.db.replies.find().sort("created_at", -1).limit(limit))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.connected:
            return {"connected": False}
        
        return {
            "connected": True,
            "database": self.database_name,
            "tweets_count": self.db.tweets.count_documents({}),
            "replies_count": self.db.replies.count_documents({}),
            "mentions_count": self.db.mentions.count_documents({}),
            "conversations_count": self.db.conversations.count_documents({}),
            "posted_tweets": self.db.tweets.count_documents({"posted": True}),
            "replied_mentions": self.db.mentions.count_documents({"replied": True})
        }
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False

