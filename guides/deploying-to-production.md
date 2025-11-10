# Deploying to Production

#### Step 1: Prepare for 24/7 Operation

Create a production-ready script with error handling and logging:

```python
# production_agent.py
from xynae import Xynae
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'defi_sage_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

AGENT_PERSONALITY = """
[Your refined personality prompt]
"""

def main():
    logger.info("🚀 Starting DeFi Sage in production mode")
    
    try:
        # Initialize agent
        agent = Xynae(
            personality=AGENT_PERSONALITY,
            llm_provider="auto",
            mongodb_uri=os.getenv("MONGODB_URI"),
            database_name="defi_sage_production",
            use_database=True
        )
        
        logger.info("✅ Agent initialized successfully")
        logger.info(f"📊 Database: {agent.db.is_connected()}")
        logger.info(f"🤖 LLM Providers: {agent.llm_manager.list_available_providers()}")
        
        # Run agent
        logger.info("🎯 Starting autonomous operation")
        agent.run(tweet_interval=1200, check_interval=300)
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down gracefully")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

#### Step 2: Set Up Process Management

**Option A: Using systemd (Linux)**

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/defi-sage.service
```

Add configuration:

```ini
[Unit]
Description=DeFi Sage AI Agent
After=network.target mongodb.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/xynae
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 production_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable defi-sage
sudo systemctl start defi-sage
sudo systemctl status defi-sage
```

**Option B: Using PM2 (Cross-platform)**

```bash
# Install PM2
npm install -g pm2

# Start agent with PM2
pm2 start production_agent.py --name defi-sage --interpreter python3

# Configure auto-restart on boot
pm2 startup
pm2 save

# Monitor agent
pm2 logs defi-sage
pm2 monit
```

**Option C: Using Docker**

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "production_agent.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  defi-sage:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - TWITTER_API_KEY=${TWITTER_API_KEY}
      - TWITTER_API_SECRET=${TWITTER_API_SECRET}
      - TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN}
      - TWITTER_ACCESS_SECRET=${TWITTER_ACCESS_SECRET}
      - MONGODB_URI=mongodb://mongodb:27017/
    depends_on:
      - mongodb
    restart: unless-stopped

  mongodb:
    image: mongo:latest
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
```

Deploy:

```bash
docker-compose up -d
docker-compose logs -f defi-sage
```

#### Step 3: Set Up Monitoring and Alerts

Create a health check script:

```python
# healthcheck.py
from database import XynaeDatabase
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

load_dotenv()

db = XynaeDatabase(
    mongodb_uri=os.getenv("MONGODB_URI"),
    database_name="defi_sage_production"
)

# Check database connection
if not db.is_connected():
    print("❌ Database not connected")
    sys.exit(1)

# Check recent activity (last 30 minutes)
recent_tweets = db.get_recent_tweets(limit=100)
recent_time = datetime.now() - timedelta(minutes=30)

recent_activity = [
    t for t in recent_tweets 
    if datetime.fromisoformat(t.get('timestamp', '1970-01-01')) > recent_time
]

if len(recent_activity) == 0:
    print("⚠️ No recent activity in last 30 minutes")
    sys.exit(1)

print("✅ Health check passed")
sys.exit(0)
```

Set up cron job for monitoring:

```bash
# Edit crontab
crontab -e

# Add health check every 30 minutes
*/30 * * * * /usr/bin/python3 /path/to/healthcheck.py || echo "DeFi Sage health check failed!" | mail -s "Alert: DeFi Sage Down" your@email.com
```

***
