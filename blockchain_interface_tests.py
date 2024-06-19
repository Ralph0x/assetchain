import React, { useState, useEffect } from 'react';
import AssetTokenizeForm from './AssetTokenizeForm';
import Dashboard from './Dashboard';

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
    } catch (error) {
      if (error.code === 4001) {
        setError("User denied account access.");
      } else {
        console.error('Error connecting to wallet:', error);
        setError("Failed to connect the wallet. Please try again.");
      }
    }
  };

  const updateTransactionStatus = (status) => {
    setTransactionStatus(status);
  };

  const renderError = () => (
    <div className="error">
      {error}
    </div>
  );

  return (
    <div className="App">
      {error && renderError()}
      {walletConnected ? (
        <>
          <Dashboard transactionStatus={transactionStatus} />
          <AssetTokenizeForm onTransactionUpdate={updateTransactionStatus} />
        </>
      ) : (
        <button onClick={connectWallet}>Connect Wallet</button>
      )}
    </div>
  );
}

export default App;