# System Components

#### System Components

The XYNAE platform consists of several interconnected components that work together to provide a seamless user experience. At the blockchain layer, the AgentLaunchpad smart contract is deployed on BNB Chain mainnet at address `0xa06a9a193213645357665D245dD8dE5fEa0fba0C`. This contract manages all token launches, bonding curve calculations, and trading operations. It uses OpenZeppelin's battle-tested implementations for ERC20 token standards, access control, and reentrancy protection to ensure security and reliability.

The frontend application is built using Next.js 14 with TypeScript, providing a modern React-based user interface with server-side rendering capabilities and optimal performance. The application uses ethers.js v6 for blockchain interactions, enabling users to connect their MetaMask wallets and execute transactions directly from the browser. State management is handled through React hooks and context providers, with the TranslationContext enabling multi-language support for English and Chinese users.

Data flow through the system follows a clear pattern: users interact with the frontend, which validates input and formats transaction data. The frontend then communicates with the user's Web3 wallet (MetaMask) to sign transactions, which are broadcast to BNB Chain. The smart contract executes the transaction logic, emits events, and updates on-chain state. The frontend listens for these events and queries the blockchain to update the UI with the latest token information, prices, and statistics. For enhanced performance, token metadata including images and descriptions are stored on IPFS via Pinata, with the IPFS hash stored on-chain for verification and retrieval.
