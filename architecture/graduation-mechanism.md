# Graduation Mechanism

The sell mechanism works in reverse: when users sell tokens back to the bonding curve, they receive BNB based on the current price. The constant product formula ensures that selling tokens decreases the price, creating a two-way market. The contract burns the sold tokens, permanently removing them from circulation, which maintains the integrity of the bonding curve calculations. Selling is only possible if there is sufficient BNB in the real reserve to pay out, preventing liquidity crises.

#### Graduation Mechanism

When a token's bonding curve accumulates BNB equal to or exceeding the graduation threshold (default 18 BNB), the token automatically "graduates" to decentralized exchange trading. The graduation process marks the agent as graduated in the AgentInfo struct, prevents further bonding curve trading, and emits an AgentGraduated event. In production deployments, graduation would automatically add liquidity to PancakeSwap, lock the LP tokens, and renounce contract ownership to ensure decentralization.

```solidity
function _graduateToDEX(address tokenAddress) internal {
    AgentInfo storage agent = agents[tokenAddress];
    BondingCurve storage curve = bondingCurves[tokenAddress];
    
    agent.graduated = true;
    agent.tradingEnabled = true;
    
    emit AgentGraduated(tokenAddress, agent.marketCap, block.timestamp);
    
    // Note: In production, this would:
    // 1. Add liquidity to PancakeSwap
    // 2. Lock LP tokens
    // 3. Renounce ownership
}
```
