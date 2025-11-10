# Bonding Curve Implementation

The bonding curve implementation uses a constant product formula derived from automated market maker (AMM) theory. Unlike traditional AMMs that require both assets to be deposited upfront, the XYNAE bonding curve starts with a virtual BNB reserve and a real token reserve. The virtual reserves are used to calculate prices, while the real reserves track actual holdings. This design allows tokens to launch with initial liquidity without requiring the creator to lock up capital.

```solidity
function _initializeBondingCurve(
    address tokenAddress, 
    uint256 maxSupply, 
    uint256 graduationThreshold
) internal {
    uint256 tokensForCurve = maxSupply / 2; // 50% of supply on bonding curve
    uint256 virtualBNB = (graduationThreshold * 13) / 180; // ~1.3 BNB for 18 BNB graduation
    uint256 virtualTokens = tokensForCurve;
    uint256 k = virtualBNB * virtualTokens / 1e18; // Constant product
    
    bondingCurves[tokenAddress] = BondingCurve({
        virtualBNBReserve: virtualBNB,
        virtualTokenReserve: virtualTokens,
        k: k,
        realBNBReserve: 0,
        realTokenReserve: tokensForCurve,
        soldTokens: 0,
        graduationThreshold: graduationThreshold
    });
}
```

The virtual BNB reserve is set to approximately 7.2% of the graduation threshold, which for the default 18 BNB threshold equals about 1.3 BNB. This creates an initial price point that allows for significant price appreciation as tokens are purchased. The virtual token reserve equals 50% of the maximum supply, meaning only half of all tokens will ever be sold through the bonding curve. The constant product k is calculated as the product of virtual BNB and virtual tokens divided by 1e18 to maintain precision in Solidity's integer arithmetic.

When users purchase tokens, the buyTokens function calculates the amount of tokens they receive using the constant product formula. The formula ensures that as more BNB is added to the reserve, the price per token increases, creating an automatic price discovery mechanism. A 1% trading fee is deducted from each transaction and sent to the fee recipient, providing revenue for platform operations while keeping fees minimal to encourage trading activity.

```solidity
function calculatePurchaseReturn(address tokenAddress, uint256 bnbAmount) public view returns (uint256) {
    BondingCurve memory curve = bondingCurves[tokenAddress];
    
    if (curve.k == 0) return 0;
    
    // Calculate new virtual BNB reserve after buy
    uint256 newVirtualBNB = curve.virtualBNBReserve + bnbAmount;
    
    // Calculate new virtual token reserve using k
    uint256 newVirtualTokens = (curve.k * 1e18) / newVirtualBNB;
    
    // Tokens out = old virtual tokens - new virtual tokens
    if (curve.virtualTokenReserve <= newVirtualTokens) return 0;
    
    uint256 tokensOut = curve.virtualTokenReserve - newVirtualTokens;
    
    // Can't sell more than what's available
    if (tokensOut > curve.realTokenReserve) {
        tokensOut = curve.realTokenReserve;
    }
    
    return tokensOut;
}
```

The sell mechanism works in reverse: when users sell tokens back to the bonding curve, they receive BNB based on the current price. The constant product formula ensures that selling tokens decreases the price, creating a two-way market. The contract burns the sold tokens, permanently removing them from circulation, which maintains the integrity of the bonding curve calculations. Selling is only possible if there is sufficient BNB in the real reserve to pay out, preventing liquidity crises.
