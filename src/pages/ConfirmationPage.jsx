import React from 'react';
import { useSelector } from 'react-redux';
import '../styles/confirmation.css';

const ConfirmationPage = () => {
  const formData = useSelector((state) => state.form.formData);

  if (!formData) return <p className="no-data">No data submitted!</p>;

  return (
    <div className="confirmation-container">
      <h1>Confirmation</h1>
      <p>
        <strong>Full Name:</strong> {formData.fullName}
      </p>
      <p>
        <strong>Email:</strong> {formData.email}
      </p>
      <p>
        <strong>Issue Type:</strong> {formData.issueType}
      </p>
      <p>
        <strong>Tags:</strong> {formData.tags.join(', ')}
      </p>
      <h3>Steps to Reproduce:</h3>
      <ul>
        {formData.steps.map((step, index) => (
          <li key={index}>{step}</li>
        ))}
      </ul>
      <button>Submit</button>
    </div>
  );
};

export default ConfirmationPage;
