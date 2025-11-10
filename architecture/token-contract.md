# Token Contract

The AgentToken contract is a fully compliant BEP-20 token implementation that represents each individual AI agent on the XYNAE platform. It extends OpenZeppelin's ERC20 and Ownable contracts, providing standard token functionality with additional metadata fields specific to AI agents. Each token is created with a unique agent ID, metadata URI pointing to IPFS, and customizable name and symbol chosen by the creator.

```solidity
contract AgentToken is ERC20, Ownable {
    uint8 private _decimals;
    string public agentId;
    string public agentMetadata; // IPFS hash or metadata URI
    
    constructor(
        string memory name,
        string memory symbol,
        string memory _agentId,
        string memory _metadata,
        uint8 decimals_,
        address launcher
    ) ERC20(name, symbol) Ownable(launcher) {
        _decimals = decimals_;
        agentId = _agentId;
        agentMetadata = _metadata;
    }
    
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
    
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}
```

The AgentToken contract uses 18 decimals by default, matching the standard for most ERC20 tokens and providing sufficient precision for small-value transactions. The contract ownership is initially assigned to the AgentLaunchpad contract, which allows the launchpad to mint tokens as they are purchased through the bonding curve. This centralized minting control is necessary for the bonding curve mechanics to function properly, as tokens must be created on-demand based on the amount of BNB received. Users can burn their own tokens at any time, which returns BNB from the bonding curve reserve according to the constant product formula.

The agentId field serves as a unique identifier that links the token to its corresponding AI agent, while the agentMetadata field stores an IPFS URI containing detailed information about the agent including its image, personality description, and any additional attributes. This metadata is immutable once set at deployment, ensuring that the agent's core characteristics cannot be altered after launch. The metadata URI follows the format `ipfs://QmHash` or can be a Pinata gateway URL like `https://gateway.pinata.cloud/ipfs/QmHash`.
