# Tokenomics

#### Fixed Parameters

All tokens launched on XYNAE share the same economic parameters to ensure consistency and fairness across the platform. The max supply is fixed at 1 billion tokens (1,000,000,000), with 500 million tokens available through the bonding curve and the remaining 500 million reserved for post-graduation liquidity on PancakeSwap. The initial price is set at 0.0001 BNB per token, providing an accessible entry point while still valuing the creator's work appropriately.

The graduation threshold of 18 BNB represents approximately $10,000-15,000 USD at typical BNB prices, a significant milestone that indicates serious community backing. Upon graduation, the accumulated BNB in the bonding curve reserve would be paired with the remaining token supply to create a liquidity pool on PancakeSwap. This automatic DEX listing eliminates the need for creators to manually provide liquidity or execute complicated DeFi operations.

#### Fee Structure

The platform implements a two-tier fee structure: a flat launch fee of 0.001 BNB ($2-3 USD) paid when creating a token, and a percentage-based trading fee of 1% applied to all buy and sell transactions. The launch fee is deliberately low to encourage experimentation and make the platform accessible to creators without significant capital. This fee covers gas costs for contract deployment and provides minimal revenue to sustain platform operations.

```solidity
uint256 public launchFee = 0.001 ether;
uint256 public tradingFeeBps = 100; // 1% = 100 basis points
uint256 public constant MAX_FEE_BPS = 500; // Max 5% cap

function updateLaunchFee(uint256 newFee) external onlyOwner {
    require(newFee <= 1 ether, "Fee too high");
    launchFee = newFee;
}

function updateTradingFee(uint256 newFeeBps) external onlyOwner {
    require(newFeeBps <= MAX_FEE_BPS, "Fee too high");
    tradingFeeBps = newFeeBps;
}
```

The trading fee is calculated as basis points (hundredths of a percent) to allow fine-grained fee adjustments. The 1% fee is competitive with most decentralized exchanges while providing revenue to support platform development and maintenance. The contract includes safety mechanisms: fees have maximum caps (1 BNB for launch fee, 5% for trading fee) and can only be updated by the contract owner, preventing arbitrary fee increases that could harm users.

#### Value Capture

The bonding curve mechanism inherently captures value for early supporters and rewards long-term holders. As more users buy tokens, the price increases along the curve, meaning early buyers acquire tokens at lower prices than later buyers. This creates an incentive to discover and support promising agents early, while also providing natural resistance to pump-and-dump schemes since selling tokens decreases the price, potentially below the purchase price.

Market cap is calculated as the total supply of sold tokens multiplied by the current price: `marketCap = soldTokens * getCurrentPrice(tokenAddress)`. This metric increases as the bonding curve progresses, providing a clear indicator of the agent's total valuation. The market cap milestone of 18 BNB triggers graduation, at which point the token transitions from bonding curve trading to traditional DEX liquidity pool trading with different dynamics.
