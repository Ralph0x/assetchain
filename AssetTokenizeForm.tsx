import React, { useState } from 'react';

interface TokenizationFormData {
  assetDescription: string;
  ownerName: string;
  ownerEmail: string;
}

const TokenizationForm: React.FC = () => {
  const [formValues, setFormValues] = useState<TokenizationFormData>({
    assetDescription: '',
    ownerName: '',
    ownerEmail: '',
  });

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setFormValues(prevValues => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const TOKENIZATION_API_URL = process.env.REACT_APP_TOKENIZATION_API_URL || '';

    try {
      const response = await fetch(TOKENIZATION_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formValues),
      });

      if (!response.ok) {
        throw new Error('Tokenization request submission failed');
      }

      alert('Tokenization request submitted successfully.');
    } catch (error) {
      if (error instanceof Error) {
        console.error('Submission Error:', error.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="assetDescription">Asset Description</label>
        <textarea
          id="assetDescription"
          name="assetDescription"
          value={formValues.assetDescription}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="ownerName">Owner's Name</label>
        <input
          type="text"
          id="ownerName"
          name="ownerName"
          value={formValues.ownerName}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="ownerEmail">Owner's Email</label>
        <input
          type="email"
          id="ownerEmail"
          name="ownerEmail"
          value={formValues.ownerEmail}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Submit Request</button>
    </form>
  );
};

export default TokenizationForm;