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
    const attemptWalletConnectionOnLoad = async () => {
      if (window.ethereum && ethereum.isMetaMask) {
        try {
          await ethereum.request({ method: 'eth_accounts' });
          setWalletState((prev) => ({ ...prev, isConnected: true }));
        } catch (error) {
          console.error('Error connecting to MetaMask:', error);
        }
      }
    };

    attemptWalletConnectionOnLoad();
  }, []);

  const initiateWalletConnection = async (): Promise<void> => {
    if (window.ethereum) {
      try {
        await ethereum.request({ method: 'eth_requestAccounts' });
        setWalletState((prev) => ({ ...prev, isConnected: true }));
      } catch (error) {
        console.error('Could not connect to wallet:', error);
      }
    } else {
      console.log('Please install MetaMask!');
    }
  };

  const executeAssetTokenization = async (assetDetails: any) => {
    if (!walletState.isConnected) {
      console.log('Wallet not connected!');
      return;
    }

    setWalletState((prev) => ({ ...prev, transactionStatus: 'pending' }));

    try {
      const provider = new ethers.providers.Web1Provider((window as any).ethereum);
      const signer = provider.getSigner();
      const transaction = await signer.sendTransaction({ 
        // Details about the transaction would go here
      });

      await transaction.wait();
      setWalletState((prev) => ({ ...prev, transactionStatus: 'success' }));
    } catch (error) {
      console.error('Transaction failed:', error);
      setWalletState((prev) => ({ ...prev, transactionStatus: 'error' }));
    }
  };

  return (
    <div>
      {!walletState.isConnected ? (
        <button onClick={initiateWalletConnection}>Connect Wallet</button>
      ) : (
        <>
          <Dashboard userState={walletState} />
          <AssetTokenizeForm onAssetTokenization={executeAssetTokenization} />
        </>
      )}
    </div>
  );
};

export default App;