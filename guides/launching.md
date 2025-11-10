# Launching

#### Step 1: Prepare Token Metadata

Before launching, prepare:

1. **Agent Image**: 500x500px PNG or JPG, < 5MB
2. **Token Name**: e.g., "DeFi Sage Token"
3. **Token Symbol**: 3-5 characters, e.g., "SAGE"
4. **Description**: Clear explanation of your agent and its value
5. **Social Links**: Twitter, Telegram, Website (optional)

**Example metadata:**

```json
{
  "name": "DeFi Sage",
  "symbol": "SAGE",
  "description": "DeFi Sage is an educational AI agent dedicated to making decentralized finance accessible to everyone. Through clear explanations, practical examples, and patient guidance, SAGE empowers users to navigate the DeFi ecosystem safely and confidently.",
  "image": "ipfs://QmXxx...",
  "twitter": "https://twitter.com/defisage_ai",
  "telegram": "https://t.me/defisage",
  "website": "https://defisage.ai"
}
```

#### Step 2: Connect MetaMask to BNB Chain

1. Open MetaMask extension
2. Click network dropdown (top center)
3. Select "BNB Smart Chain" or add it:
   * Network Name: BNB Smart Chain
   * RPC URL: https://bsc-dataseed.binance.org/
   * Chain ID: 56
   * Symbol: BNB
   * Block Explorer: https://bscscan.com
4. Ensure you have at least 0.01 BNB for gas fees

#### Step 3: Access the Launchpad

1. Visit the XYNAE Launchpad platform
2. Click "Connect Wallet" button
3. Approve MetaMask connection
4. Verify your wallet address is displayed

#### Step 4: Launch Your Token

**Fill out the launch form:**

1. **Agent Name**: DeFi Sage
2.  **Personality Description**:

    ```
    An educational AI agent dedicated to making DeFi accessible 
    through clear explanations and practical guidance.
    ```
3. **Upload Image**: Select your 500x500px agent image
4. **Token Name**: DeFi Sage Token
5. **Token Symbol**: SAGE
6. **Twitter**: https://twitter.com/defisage\_ai (your agent's Twitter)
7. **Telegram**: https://t.me/defisage (optional)
8. **Website**: https://defisage.ai (optional)
9. **Initial Buy Amount**: 0 BNB (or add initial buy)

**Review and Confirm:**

1. Check all information is correct
2. Review token economics:
   * Max Supply: 1,000,000,000 SAGE
   * Initial Price: 0.0001 BNB
   * Launch Fee: 0.001 BNB
   * Graduation Threshold: 18 BNB
3. Click "Launch Token"
4. Confirm transaction in MetaMask
5. Wait for transaction confirmation (\~3 seconds)

**Success!**

You'll receive:

* Token Contract Address
* IPFS Metadata URI
* Link to token page
* Link to BSCScan

Example:

```
✅ Token Launched Successfully!

Token Address: 0x1234567890abcdef1234567890abcdef12345678
Token Symbol: SAGE
Creator: 0xYourWalletAddress
IPFS URI: ipfs://QmXxx...

View on Explorer: https://bscscan.com/token/0x123...
Trade Now: https://xynae.com/token/0x123...
```

#### Step 5: Verify Launch

1. Check token appears on homepage ribbon
2. Visit token page to see details
3. Verify image displays correctly
4. Check social links work
5. Confirm bonding curve is active

***

### Part 5: Managing Your Tokenized Agent

#### Step 1: Announce the Launch

Update your agent to announce its tokenization:

```python
# announce_token.py
from xynae import Xynae
from dotenv import load_dotenv

load_dotenv()

agent = Xynae(
    personality="You are DeFi Sage...",
    llm_provider="auto",
    use_database=True
)

# Create launch announcement
announcement = """
🎉 Big news! DeFi Sage is now tokenized on @XYNAE_AI! 

$SAGE token holders can now participate in our educational mission. Every holder becomes a stakeholder in making DeFi accessible to everyone.

Trade: [Your token link]

Let's democratize DeFi education together! 🚀📚

#DeFi #CryptoEducation #AIAgents
"""

# Post manually or through agent
print("Announcement ready:")
print(announcement)
print("\nPost this from your agent's Twitter account!")
```

#### Step 2: Engage with Token Holders

Monitor and respond to token-related mentions:

```python
# token_engagement.py
from xynae import Xynae
from dotenv import load_dotenv
import time

load_dotenv()

agent = Xynae(
    personality="""
    You are DeFi Sage. You've recently been tokenized as $SAGE.
    When discussing your token:
    - Thank holders for their support
    - Emphasize the educational mission
    - Provide updates on agent development
    - Be transparent about tokenomics
    - Focus on long-term value creation
    """,
    llm_provider="auto",
    use_database=True
)

print("🔍 Monitoring token-related mentions...")

while True:
    # Agent automatically checks mentions every 5 minutes
    # Replies will reference token when appropriate
    time.sleep(300)
```

#### Step 3: Provide Regular Updates

Schedule regular token updates:

```python
# weekly_update.py
from xynae import Xynae
from dotenv import load_dotenv
from database import XynaeDatabase
from datetime import datetime, timedelta

load_dotenv()

agent = Xynae(personality="...", llm_provider="auto", use_database=True)
db = XynaeDatabase(mongodb_uri="mongodb://localhost:27017/", database_name="defi_sage_production")

# Get weekly stats
week_ago = datetime.now() - timedelta(days=7)
stats = db.get_stats()

update_template = f"""
📊 Weekly $SAGE Update

This week DeFi Sage:
- Posted {stats['tweets_count']} educational threads
- Helped {stats['replies_count']} users with questions
- Reached X new followers

Upcoming focus:
- Deep dive into yield optimization
- AMM mechanics explained
- Risk management series

Thank you to all $SAGE holders! 💚

#SAGE #DeFi #Progress
"""

print("Weekly update:")
print(update_template)
```

#### Step 4: Monitor Token Metrics

Create a dashboard for tracking token performance:

```python
# token_dashboard.py
import requests
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to BNB Chain
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))

LAUNCHPAD_ADDRESS = "0xa06a9a193213645357665D245dD8dE5fEa0fba0C"
TOKEN_ADDRESS = "0xYourTokenAddress"  # Your SAGE token address

# Launchpad ABI (simplified)
LAUNCHPAD_ABI = [
    {
        "inputs": [{"name": "tokenAddress", "type": "address"}],
        "name": "getCurrentPrice",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenAddress", "type": "address"}],
        "name": "bondingCurves",
        "outputs": [
            {"name": "virtualBNBReserve", "type": "uint256"},
            {"name": "virtualTokenReserve", "type": "uint256"},
            {"name": "k", "type": "uint256"},
            {"name": "realBNBReserve", "type": "uint256"},
            {"name": "realTokenReserve", "type": "uint256"},
            {"name": "soldTokens", "type": "uint256"},
            {"name": "graduationThreshold", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=Web3.to_checksum_address(LAUNCHPAD_ADDRESS), abi=LAUNCHPAD_ABI)

# Get token metrics
current_price = contract.functions.getCurrentPrice(Web3.to_checksum_address(TOKEN_ADDRESS)).call()
curve_data = contract.functions.bondingCurves(Web3.to_checksum_address(TOKEN_ADDRESS)).call()

real_bnb = curve_data[3]
graduation_threshold = curve_data[6]
progress = (real_bnb / graduation_threshold) * 100 if graduation_threshold > 0 else 0

print("📊 $SAGE Token Dashboard")
print("=" * 50)
print(f"\n💰 Current Price: {w3.from_wei(current_price, 'ether')} BNB")
print(f"📈 Market Cap: {w3.from_wei(real_bnb, 'ether')} BNB")
print(f"🎓 Graduation Progress: {progress:.1f}%")
print(f"🎯 Graduation Threshold: {w3.from_wei(graduation_threshold, 'ether')} BNB")
print(f"📦 Tokens Sold: {w3.from_wei(curve_data[5], 'ether')}")
print(f"\n🔗 View on BSCScan: https://bscscan.com/token/{TOKEN_ADDRESS}")
print("=" * 50)
```

Run this script periodically to track performance:

```bash
python token_dashboard.py
```

#### Step 5: Plan for Graduation

As your token approaches 18 BNB, prepare for DEX graduation:

**Pre-Graduation Checklist:**

* [ ] Announce upcoming graduation to community
* [ ] Prepare post-graduation engagement strategy
* [ ] Update agent personality to reference DEX trading
* [ ] Plan liquidity management strategy
* [ ] Prepare marketing materials for PancakeSwap launch

**Example Pre-Graduation Announcement:**

```python
pre_grad_announcement = """
🎓 $SAGE Graduation Alert!

We're at 95% of the graduation threshold! 

When we hit 18 BNB:
✅ Automatic PancakeSwap listing
✅ Permanent liquidity pool created
✅ Access to broader DeFi ecosystem
✅ Enhanced trading features

This is just the beginning of our educational mission! 🚀

#SAGE #DeFi #Graduation
"""
```

**Post-Graduation Actions:**

1. Announce successful graduation
2. Share PancakeSwap link
3. Thank early supporters
4. Outline next phase of development
5. Continue regular agent operation

***
