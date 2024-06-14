import React, { useState, useEffect } from 'react';
import AssetTokenizeForm from './AssetTokenizeForm';
import Dashboard from './Dashboard';
import { ethers } from 'ethers';

interface UserWalletState {
  isConnected: boolean;
  transactionStatus: 'pending' | 'success' | 'error' | 'none';
}

const App: React.FC = () => {
  const [walletState, setWalletState] = useState<UserWalletState>({
    isConnected: false,
    transactionStatus: 'none',
  });

  useEffect(() => {
    const connectWalletOnLoad = async () => {
      if (window.ethereum && ethereum.isMetaMask) {
        try {
          await ethereum.request({ method: 'eth_accounts' });
          setWalletState((prevState) => ({ ...prevState, isConnected: true }));
        } catch (error) {
          console.error('Error connecting to MetaMask:', error);
        }
      }
    };

    connectWalletOnLoad();
  }, []);

  const connectWallet = async (): Promise<void> => {
    if (window.ethereum) {
      try {
        await ethereum.request({ method: 'eth_requestAccounts' });
        setWalletState((prevState) => ({ ...prevState, isConnected: true }));
      } catch (error) {
        console.error('Could not connect to wallet:', error);
      }
    } else {
      console.log('Please install MetaMask!');
    }
  };

  const tokenizeAsset = async (assetDetails: any) => {
    if (!walletState.isConnected) {
      console.log('Wallet not connected!');
      return;
    }

    setWalletState((prevState) => ({ ...prevState, transactionStatus: 'pending' }));

    try {
      const provider = new ethers.providers.Web3Provider((window as any).ethereum);
      const signer = provider.getSigner();
      const transaction = await signer.sendTransaction({ 
      });

      await transaction.wait();
      setWalletState((prevState) => ({ ...prevState, transactionStatus: 'success' }));
    } catch (error) {
      console.error('Transaction failed:', error);
      setWalletState((prevState) => ({ ...prevState, transactionStatus: 'error' }));
    }
  };

  return (
    <div>
      {!walletState.isConnected ? (
        <button onClick={connectWallet}>Connect Wallet</button>
      ) : (
        <>
          <Dashboard userState={walletState} />
          <AssetTokenizeForm onAssetTokenization={tokenizeAsset} />
        </>
      )}
    </div>
  );
};

export default App;