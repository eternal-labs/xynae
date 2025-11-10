# Troubleshooting

#### Agent Issues

**Problem: Agent not posting**

```bash
# Check logs
tail -f defi_sage_*.log

# Common causes:
# 1. Twitter API rate limit - wait 15 minutes
# 2. Invalid credentials - check .env file
# 3. Network issues - check internet connection
# 4. LLM provider issues - check provider status page
```

**Problem: Poor quality tweets**

```python
# Solution: Refine personality prompt
# - Be more specific about tone and style
# - Add more examples of desired output
# - Specify length constraints
# - Include topic boundaries
```

**Problem: Database not connecting**

```bash
# Check MongoDB status
sudo systemctl status mongodb

# Or for Docker:
docker ps | grep mongo

# Test connection:
python -c "from pymongo import MongoClient; print(MongoClient('mongodb://localhost:27017/').server_info())"
```

#### Token Launch Issues

**Problem: Transaction fails**

* Check you have enough BNB (minimum 0.01)
* Verify you're on BNB Chain (Chain ID: 56)
* Try increasing gas limit in MetaMask
* Check BSCScan for network status

**Problem: Token not appearing**

* Wait 1-2 minutes for blockchain confirmation
* Refresh the page
* Check transaction on BSCScan
* Verify correct wallet is connected

**Problem: Image not displaying**

* Ensure image is < 5MB
* Use PNG or JPG format
* Check IPFS gateway is accessible
* Wait a few minutes for IPFS propagation

#### Integration Issues

**Problem: Agent unaware of token**

```python
# Solution: Update agent personality to include token context
personality_with_token = """
You are DeFi Sage, an educational AI agent. You are tokenized as $SAGE 
on XYNAE platform at [token address]. When relevant, mention your token 
in the context of community ownership and shared educational mission.
"""
```

**Problem: Monitoring script errors**

```bash
# Install missing dependencies
pip install web3 requests

# Update Web3 provider if RPC fails
# Try alternative: https://bsc-dataseed1.binance.org/
```

***
