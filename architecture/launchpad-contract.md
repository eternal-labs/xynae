# Launchpad Contract

The AgentLaunchpad contract is the heart of the XYNAE platform, orchestrating token launches, managing bonding curves, and facilitating all trading operations. It implements a constant product bonding curve similar to Uniswap's automated market maker, but designed specifically for token launches rather than liquidity pools. The contract maintains mappings of all launched agents, their bonding curve parameters, and trading statistics.

```solidity
struct AgentInfo {
    address tokenAddress;
    address creator;
    string agentId;
    string name;
    string symbol;
    string metadata;
    uint256 createdAt;
    uint256 totalRaised;
    uint256 marketCap;
    bool tradingEnabled;
    bool graduated;
}

struct BondingCurve {
    uint256 virtualBNBReserve;  // Virtual BNB reserve for constant product
    uint256 virtualTokenReserve; // Virtual token reserve for constant product
    uint256 k;                  // Constant product (k = virtualBNB × virtualToken)
    uint256 realBNBReserve;     // Actual BNB collected from buys
    uint256 realTokenReserve;   // Actual tokens available for sale
    uint256 soldTokens;         // Tokens sold so far
    uint256 graduationThreshold; // BNB amount to graduate to DEX
}
```

The launchAgent function is the primary entry point for creating new tokens. It accepts parameters for the token name, symbol, agent ID, metadata URI, initial price, maximum supply, and graduation threshold. The function performs extensive validation to ensure all parameters are valid, checks that the agent ID hasn't been used before, and requires a minimum launch fee of 0.001 BNB to prevent spam. Once validation passes, it deploys a new AgentToken contract, initializes the bonding curve with calculated parameters, and stores the agent information in contract state.

```solidity
function launchAgent(
    string memory name,
    string memory symbol,
    string memory agentId,
    string memory metadata,
    uint256 initialPrice,
    uint256 maxSupply,
    uint256 graduationThreshold
) external payable nonReentrant returns (address) {
    require(msg.value >= launchFee, "Insufficient launch fee");
    require(bytes(agentId).length > 0, "Agent ID required");
    require(agentIdToToken[agentId] == address(0), "Agent ID already exists");
    require(initialPrice > 0, "Initial price must be > 0");
    require(maxSupply > 0, "Max supply must be > 0");
    require(graduationThreshold > 0, "Graduation threshold must be > 0");
    
    // Deploy new agent token
    address tokenAddress = address(new AgentToken(
        name,
        symbol,
        agentId,
        metadata,
        18,
        address(this)
    ));
    
    // Initialize bonding curve
    _initializeBondingCurve(tokenAddress, maxSupply, graduationThreshold);
    
    allAgents.push(tokenAddress);
    agentIdToToken[agentId] = tokenAddress;
    
    emit AgentLaunched(tokenAddress, msg.sender, agentId, name, symbol, block.timestamp);
    
    return tokenAddress;
}
```

The contract uses the nonReentrant modifier from OpenZeppelin's ReentrancyGuard to prevent reentrancy attacks during token purchases and sales. This is critical because the contract handles BNB transfers and could be vulnerable to reentrancy if not properly protected. The launch fee is immediately transferred to the designated fee recipient, while any additional BNB sent with the transaction is used to perform an initial token purchase, effectively giving the creator the first tokens at the initial bonding curve price.
