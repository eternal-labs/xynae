# Launching

Launching a token on XYNAE involves a multi-step process that combines frontend validation, metadata preparation, blockchain interaction, and post-launch data storage. The process begins when a user completes the launch form and clicks the "Launch Token" button. The frontend first validates that all required fields are filled, the wallet is connected, and an image has been uploaded. If validation passes, it proceeds to prepare the metadata JSON.

The metadata JSON contains comprehensive information about the agent: its name, personality description, image IPFS hash, social media links, and creation timestamp. This JSON is stringified and uploaded to IPFS via Pinata, returning a metadata URI that will be stored on-chain. The application then constructs the transaction parameters, calculating the total amount of BNB to send (launch fee + optional initial buy amount) and preparing the function call data.

```typescript
const handleLaunch = async () => {
  if (!walletAddress) {
    setError('Please connect your wallet first')
    return
  }

  if (!formData.agentName || !formData.tokenName || !formData.tokenSymbol || !coinImage) {
    setError('Please fill in all required fields and upload an image')
    return
  }

  setLaunching(true)
  setError('')

  try {
    const { ethers } = await import('ethers')
    const provider = new ethers.BrowserProvider(window.ethereum)
    const signer = await provider.getSigner()
    
    // Upload metadata to IPFS
    const metadata = JSON.stringify({
      name: formData.agentName,
      description: formData.personality || `${formData.agentName} AI Agent Token`,
      image: coinImageHash,
      external_url: formData.website || '',
      attributes: [
        { trait_type: 'Personality', value: formData.personality || 'Not specified' },
        { trait_type: 'Creator', value: walletAddress },
        { trait_type: 'Launch Date', value: new Date().toISOString() }
      ]
    })
    
    const metadataResponse = await fetch('https://api.pinata.cloud/pinning/pinJSONToIPFS', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${PINATA_JWT}`
      },
      body: JSON.stringify({ pinataContent: JSON.parse(metadata) })
    })
    
    const { IpfsHash } = await metadataResponse.json()
    const metadataURI = `ipfs://${IpfsHash}`
    
    // Interact with contract
    const contract = new ethers.Contract(LAUNCHPAD_ADDRESS, LAUNCHPAD_ABI, signer)
    
    const launchFee = ethers.parseEther('0.001')
    const initialBuy = ethers.parseEther(formData.initialBuyBNB || '0')
    const totalValue = launchFee + initialBuy
    
    const tx = await contract.launchAgent(
      formData.tokenName,
      formData.tokenSymbol,
      `agent_${Date.now()}`,
      metadataURI,
      ethers.parseEther('0.0001'),
      ethers.parseEther('1000000000'),
      ethers.parseEther('18'),
      { value: totalValue }
    )
    
    await tx.wait()
    
    setSuccess(true)
  } catch (error: any) {
    setError(error.message || 'Failed to launch token')
  }
  
  setLaunching(false)
}
```
