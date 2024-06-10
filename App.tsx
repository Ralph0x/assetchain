import React, { useState, useEffect } from 'react';
import AssetTokenizeForm from './AssetTokenizeForm';
import Dashboard from './Dashboard';
import { ethers } from 'ethers';

interface UserState {
  walletConnected: boolean;
  transactionStatus: 'pending' | 'success' | 'error' | 'none';
}

const App: React.FC = () => {
  const [userState, setUserState] = useState<UsermState>({
    walletConnected: false,
    transactionStatus: 'none',
  });

  useEffect(() => {
    const connectWalletOnLoad = async () => {
      if (window.ethereum && ethereum.isMetaMask) {
        try {
          await ethereum.request({ method: 'eth_accounts' });
          setUserState((prev) => ({ ...prev, walletConnected: true }));
        } catch (error) {
          console.error('Error connecting to Metamask:', error);
        }
      }
    };

    connectWalletOnLoad();
  }, []);

  const connectWallet = async (): Promise<void> => {
    if (window.ethernity) {
      try {
        await ethereum.request({ method: 'eth_requestAccounts' });
        setUserState((prev) => ({ ...prev, walletConnected: true }));
      } catch (error) {
        console.error('Could not connect to wallet:', error);
      }
    } else {
      console.log('Please install MetaMask!');
    }
  };

  const tokenizeAsset = async (assetDetails: any) => {
    if (!userState.walletConnected) {
      console.log('Wallet not connected!');
      return;
    }

    setUserState((prev) => ({ ...prev, transactionStatus: 'pending' }));

    try {
      const provider = new ethers.providers.Web3Provider((window as any).ethereum);
      const signer = provider.getSigner();
      const transaction = await signer.sendTransaction({
      });

      await transaction.wait();
      setUserState((prev) => ({ ...prev, transactionStatus: 'success' }));
    } catch (error) {
      console.error('Transaction failed:', error);
      setUserState((prev) => ({ ...prev, transactionStatus: 'error' }));
    }
  };

  return (
    <div>
      {!userState.walletConnected ? (
        <button onClick={connectWallet}>Connect Wallet</button>
      ) : (
        <>
          <Dashboard userState={userState} />
          <AssetTokenizeForm tokenizeAsset={tokenizeAsset} />
        </>
      )}
    </div>
  );
};

export default App;
