# Bonding Curve Trading

Trading on the bonding curve happens through the buyTokens and sellTokens functions, which users access through the marketplace interface. When buying tokens, users specify the amount of BNB they want to spend. The frontend calculates an estimate of tokens they'll receive by calling the contract's calculatePurchaseReturn view function, which simulates the bonding curve calculation without executing a transaction. This estimate is displayed to the user before they confirm the purchase.

```typescript
const handleBuy = async (tokenAddress: string, bnbAmount: string) => {
  try {
    const { ethers } = await import('ethers')
    const provider = new ethers.BrowserProvider(window.ethereum)
    const signer = await provider.getSigner()
    
    const contract = new ethers.Contract(LAUNCHPAD_ADDRESS, LAUNCHPAD_ABI, signer)
    
    // Get estimated tokens
    const bnbValue = ethers.parseEther(bnbAmount)
    const estimatedTokens = await contract.calculatePurchaseReturn(tokenAddress, bnbValue)
    
    // Execute buy
    const tx = await contract.buyTokens(tokenAddress, { value: bnbValue })
    await tx.wait()
    
    // Refresh token data
    await fetchTokenData(tokenAddress)
  } catch (error) {
    console.error('Buy failed:', error)
  }
}
```

Selling tokens requires user approval for the launchpad contract to spend their tokens. The ERC20 approve function must be called first, allowing the launchpad to transfer the specified amount of tokens from the user's wallet to the contract for burning. Once approval is granted, the sellTokens function is called with the token address and amount to sell. The contract calculates the BNB return, updates the bonding curve state, burns the tokens, and transfers BNB to the seller.
