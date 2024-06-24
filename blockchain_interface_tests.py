import React, { useState, useEffect, createContext } from 'react';
import AssetTokenizeForm from './AssetTokenizeForm';
import Dashboard from './Dashboard';

const WalletContext = createContext();

function App() {
  const [walletConnected, setWalletConnected] = useState(false);
  const [transactionStatus, setTransactionStatus] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    connectWallet();
  }, []);

  const connectWallet = async () => {
    try {
      if (!window.ethereum) {
        throw new Error('Please install MetaMask!');
      }
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      setWalletConnected(true);
      logToConsole('Wallet connection successful.');
    } catch (error) {
      handleConnectionError(error);
    }
  };

  const handleConnectionError = (error) => {
    logToConsole('Error connecting to wallet: ' + error.message);
    if (error.code === 4001) {
      setError("User denied account access.");
    } else {
      console.error('Error connecting to wallet:', error);
      setError("Failed to connect the wallet. Please try again.");
    }
  }

  const updateTransactionStatus = (status) => {
    setTransactionStatus(status);
    logToConsole('Transaction status updated.');
  };

  const renderError = () => (
    <div className="error">
      {error}
    </div>
  );

  // New function to log messages to the console
  const logToConsole = (message) => {
    console.log(message);
  };

  return (
    <WalletContext.Provider value={{walletConnected, transactionStatus, updateTransactionID: updateTransactionStatus}}>
    <div className="App">
      {error && renderError()}
      {walletConnected ? (
        <>
          <Dashboard />
          <AssetTokenize1Form />
        </>
      ) : (
        <button onClick={connectWallet}>Connect Wallet</button> 
      )}
    </div>
    </WalletContext.Provider>
  );
}

export default App;