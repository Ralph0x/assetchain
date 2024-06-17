import React, { useState, useEffect } from 'react';
import AssetTokenizeForm from './AssetTokenizeForm';
import Dashboard from './Dashboard';
import { ethers } from 'ethers';

function App() {
  const [walletConnected, setWalletConnected] = useState(false);
  const [transactionStatus, setTransactionStatus] = useState({});

  useEffect(() => {
    connectWallet();
  }, []);

  const connectWallet = async () => {
    try {
      if (window.ethereum) {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        setWalletConnected(true);
      } else {
        alert('Please install MetaMask!');
      }
    } catch (error) {
      console.error('Error connecting to wallet:', error);
    }
  };

  const updateTransactionStatus = (status) => {
    setTransactionStatus(status);
  };

  return (
    <div className="App">
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