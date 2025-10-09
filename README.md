Polymarket Copy Trading Bot
Introduction
This project is a Polymarket Copy Trading Bot that allows users to automatically copy trades from a selected trader on Polymarket.

Features
Automated Trading: Automatically copy trades from a selected trader.
Real-time Monitoring: Continuously monitor the selected trader's activity.
Customizable Settings: Configure trading parameters and risk management.
Installation
Install latest version of Node.js and npm
Navigate to the project directory:
cd polymarket_copy_trading_bot
Create .env file:
touch .env
Configure env variables:
USER_ADDRESS = 'Selected account wallet address to copy'

PROXY_WALLET = 'Your Polymarket account address'
PRIVATE_KEY = 'My wallet private key'

CLOB_HTTP_URL = 'https://clob.polymarket.com/'
CLOB_WS_URL = 'wss://ws-subscriptions-clob.polymarket.com/ws'

FETCH_INTERVAL = 1      // default is 1 second
TOO_OLD_TIMESTAMP = 1   // default is 1 hour
RETRY_LIMIT = 3         // default is 3 times

MONGO_URI = 'mongodb+srv://polymarket_copytrading_bot:V5ufvi9ra1dsOA9M@cluster0.j1flc.mongodb.net/polymarket_copytrading'

RPC_URL = 'https://polygon-mainnet.infura.io/v3/90ee27dc8b934739ba9a55a075229744'

USDC_CONTRACT_ADDRESS = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
Install the required dependencies:
npm install
Build the project:
npm run build
Run BOT:
npm run start
Contributing
Contributions are welcome! Please open an issue or submit a pull request. And if you are interested in this project, please consider giving it a star✨.
