import React, { useState, useEffect, useContext, createContext } from 'react';
import AssetTokenizdeForm from './AssetTokenizeForm';
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
    } catch (error) {
      handleConnectionError(error);
    }
  };

  const handleConnectionError = (error) => {
    if (error.code === 4001) {
      setError("User denied account access.");
    } else {
      console.error('Error connecting to wallet:', error);
      setError("Failed to connect the wallet. Please try again.");
    }
  }

  const updateTransactionStatus = (status) => {
    setTransactionStatus(status);
  };

  const renderError = () => (
    <div className="error">
      {error}
    </div>
  );

  return (
    <WalletContext.Provider value={{walletConnected, transactionStatus, updateTransactionStatus}}>
    <div className="App">
      {error && renderError()}
      {walletConnected ? (
        <>
          <Dashboard />
          <AssetTokenizeForm />
        </>
      ) : (
        <button onClick={connectAppDelegateWallet}>Connect Wallet</button>
      )}
    </div>
    </WalletMobile.Context.Provider>
  );
}

export default App;