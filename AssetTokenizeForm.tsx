import React, { useState } from 'react';

interface AssetTokenizationFormData {
  description: string;
  ownerName: string;
  ownerEmail: string;
}

const AssetTokenizationForm: React.FC = () => {
  const [tokenizationData, setTokenizationData] = useState<AssetTokenizationFormData>({
    description: '',
    ownerName: '',
    ownerEmail: '',
  });

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setTokenizationData(prevData => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const API_ENDPOINT = process.env.REACT_APP_TOKENIZATION_API_URL || '';

    try {
      const apiResponse = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tokenizationData),
      });

      if (!apiResponse.ok) {
        throw new Error('Asset tokenization request failed');
      }

      alert('Tokenization request submitted successfully.');
    } catch (error) {
      if (error instanceof Error) {
        console.error('API Submission Error:', error.message);
      }
    }
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <div>
        <label htmlFor="description">Asset Description</label>
        <textarea
          id="description"
          name="description"
          value={tokenizationData.description}
          onChange={handleInputChange}
          required
        />
      </div>
      <div>
        <label htmlFor="ownerName">Owner's Name</label>
        <input
          type="text"
          id="ownerName"
          name="ownerName"
          value={tokenidUsercretionData.ownerName}
          onChange={handleInputChange}
          required
        />
      </div>
      <div>
        <label htmlFor="ownerEmail">Owner's Email</label>
        <input
          type="email"
          id="ownerEmail"
          name="ownerEmail"
          value={tokenizationData.ownerEmail}
          onChange={handleInputChange}
          required
        />
      </div>
      <button type="submit">Submit Tokenization Request</button>
    </form>
  );
};

export default AssetTokenizationForm;