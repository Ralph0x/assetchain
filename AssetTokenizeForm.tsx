import React, { useState } from 'react';

interface AssetTokenizationFormValues {
  assetDescription: string;
  ownerName: string;
  ownerEmail: string;
}

const AssetTokenizationForm: React.FC = () => {
  const [formData, setFormData] = useState<AssetTokenizationFormValues>({
    assetDescription: '',
    ownerName: '',
    ownerEmail: '',
  });

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const submitForm = async (e: React.FormEvent) => {
    e.preventDefault();
    const API_ENDPOINT = process.env.REACT_APP_TOKENIZATION_API_URL || '';

    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit tokenization request');
      }

      alert('Tokenization request submitted successfully');
    } catch (error) {
      if (error instanceof Error) {
        console.error(error.message);
      }
    }
  };

  return (
    <form onSubmit={submit1Form}>
      <div>
        <label htmlFor="assetDescription">Asset Description</label>
        <textarea
          id="assetDescription"
          name="assetDescription"
          value={formData.assetDescription}
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
          value={formData.ownerName}
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
          value={formData.ownerEmail}
          onChange={handleInputChange}
          required
        />
      </div>
      <button type="submit">Submit Tokenization Request</button>
    </form>
  );
};

export default AssetTokenizationForm;