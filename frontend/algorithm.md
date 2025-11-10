# Algorithm

#### Mathematical Foundation

The bonding curve algorithm is based on the constant product formula: `x * y = k`, where x represents the BNB reserve, y represents the token reserve, and k is a constant. This formula ensures that the product of the two reserves remains constant, which naturally creates a price discovery mechanism. As BNB is added to the curve (buying tokens), the BNB reserve increases, which means the token reserve must decrease to maintain the constant product. This decrease in token supply relative to BNB supply increases the price per token.

The initial values for the bonding curve are carefully calculated to provide favorable launch conditions. The virtual BNB reserve is set to approximately 7.2% of the graduation threshold (about 1.3 BNB for an 18 BNB threshold), while the virtual token reserve equals 50% of the maximum supply. These values create an initial price point that allows for significant price appreciation without making early purchases prohibitively expensive. The constant k is calculated as `(virtualBNB * virtualToken) / 1e18`, with the division by 1e18 necessary to handle Solidity's integer arithmetic precision.

#### Price Calculation

Token prices are calculated dynamically based on the current state of the bonding curve reserves. The current price is determined by dividing the virtual BNB reserve by the virtual token reserve: `price = virtualBNBReserve / virtualTokenReserve`. This gives the price of one token in terms of BNB. As tokens are purchased, the virtual BNB reserve increases and the virtual token reserve decreases, causing the price to rise. Conversely, when tokens are sold, the reserves change in the opposite direction, causing the price to fall.

```solidity
function getCurrentPrice(address tokenAddress) public view returns (uint256) {
    BondingCurve memory curve = bondingCurves[tokenAddress];
    if (curve.virtualTokenReserve == 0) return 0;
    return (curve.virtualBNBReserve * 1e18) / curve.virtualTokenReserve;
}
```

The price calculation multiplies the virtual BNB reserve by 1e18 before division to maintain precision. Without this multiplication, integer division in Solidity would truncate decimals, potentially returning zero for small values. The result is a price in wei per token (with 18 decimals), which can be converted to a more readable format in the frontend by dividing by 1e18.

#### Purchase Mechanics

When a user purchases tokens, the contract must determine how many tokens they receive for their BNB input. This calculation uses the constant product formula rearranged to solve for token output: `tokens_out = virtualTokenReserve - (k / (virtualBNBReserve + bnb_in))`. The logic first calculates what the new virtual BNB reserve would be after adding the user's BNB, then calculates what the new virtual token reserve must be to maintain the constant k, and finally determines the difference between old and new token reserves as the amount to give the user.

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

The calculation includes safety checks to prevent mathematical errors. If the constant k is zero (curve not initialized), it returns zero tokens. If the calculated tokens out would be negative (which would underflow in unsigned integer arithmetic), it returns zero. Most importantly, it ensures that the tokens requested don't exceed the real token reserve, which would be impossible to fulfill. This prevents the bonding curve from promising more tokens than are actually available for distribution.

#### Sale Mechanics

Selling tokens works inversely to buying. The contract calculates how much BNB to return using the formula: `bnb_out = virtualBNBReserve - (k / (virtualTokenReserve + tokens_in))`. The logic determines the new virtual token reserve after adding the user's tokens back, calculates the corresponding new virtual BNB reserve, and returns the difference as BNB to the seller.

```solidity
function calculateSaleReturn(address tokenAddress, uint256 tokenAmount) public view returns (uint256) {
    BondingCurve memory curve = bondingCurves[tokenAddress];
    
    if (curve.k == 0 || tokenAmount > curve.soldTokens) return 0;
    
    // Calculate new virtual token reserve after sell
    uint256 newVirtualTokens = curve.virtualTokenReserve + tokenAmount;
    
    // Calculate new virtual BNB reserve using k
    uint256 newVirtualBNB = (curve.k * 1e18) / newVirtualTokens;
    
    // BNB out = old virtual BNB - new virtual BNB
    if (curve.virtualBNBReserve <= newVirtualBNB) return 0;
    
    uint256 bnbOut = curve.virtualBNBReserve - newVirtualBNB;
    
    // Can't return more BNB than what's in the reserve
    if (bnbOut > curve.realBNBReserve) {
        bnbOut = curve.realBNBReserve;
    }
    
    return bnbOut;
}
```

The sale calculation includes additional validation: users cannot sell more tokens than have been sold in total (prevents manipulating the curve with tokens minted outside the bonding curve system), and the BNB return cannot exceed the real BNB reserve (prevents insolvency). The returned BNB amount has the 1% trading fee deducted before being sent to the seller, with the fee going to the platform's fee recipient address.
