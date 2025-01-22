import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { FiX } from 'react-icons/fi';
import '../styles/confirmation.css';

const ConfirmationPage = () => {
  const token = useSelector((state) => state.auth.token);
  const id = useSelector((state) => state.auth.user.id);
  const [supportRequests, setSupportRequests] = useState([]);
  const [error, setError] = useState('');
  const [sortCriteria, setSortCriteria] = useState('id_desc');

  useEffect(() => {
    if (!id) {
      setError('User ID not found. Please log in.');
      return;
    }

    const fetchSupportRequests = async () => {
      try {
        const response = await axios.post(
          `http://localhost:8000/v1/confirmation/my-confirmations`,
          { user_id: id, token },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setSupportRequests(response.data);
      } catch (err) {
        setError('Failed to fetch support requests. Please try again later.');
      }
    };

    fetchSupportRequests();
  }, [token, id]);

  const handleSortChange = (event) => {
    setSortCriteria(event.target.value);
  };

  const handleDelete = async (confirmationId) => {
    try {
      await axios.delete(
        `http://localhost:8000/v1/confirmation/confirmation_delete`,
        {
          data: { confirmation_id: confirmationId, token },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setSupportRequests((prevRequests) =>
        prevRequests.filter((request) => request.id !== confirmationId)
      );
    } catch (err) {
      console.error('Failed to delete confirmation:', err);
      setError('Failed to delete the confirmation. Please try again later.');
    }
  };

  const sortRequests = (requests, criteria) => {
    switch (criteria) {
      case 'id_asc':
        return [...requests].sort((a, b) => a.id - b.id);
      case 'id_desc':
        return [...requests].sort((a, b) => b.id - a.id);
      default:
        return requests;
    }
  };

  if (!id)
    return (
      <p className="error">Please log in to view your support requests.</p>
    );

  if (error) return <p className="error">{error}</p>;

  if (supportRequests.length === 0)
    return <p className="no-data">No support requests found for this user.</p>;

  const sortedRequests = sortRequests(supportRequests, sortCriteria);

  return (
    <div className="confirmation-container">
      <h1>Your Support Requests</h1>
      <div className="sort-container">
        <label htmlFor="sort">Sort by:</label>
        <select id="sort" value={sortCriteria} onChange={handleSortChange}>
          <option value="id_desc">Newest First</option>
          <option value="id_asc">Oldest First</option>
        </select>
      </div>
      <div className="card-list">
        {sortedRequests.map((request) => (
          <div key={request.id} className="card">
            <div className="card-header">
              <h3>Support Request ID: {request.id}</h3>
              <FiX
                className="delete-icon"
                onClick={() => handleDelete(request.id)}
              />
            </div>
            <p>
              <strong>Full Name:</strong> {request.full_name}
            </p>
            <p>
              <strong>Email:</strong> {request.email}
            </p>
            <p>
              <strong>Issue Type:</strong> {request.issue_type}
            </p>
            <p>
              <strong>Tags:</strong>{' '}
              {request.tagNames && request.tagNames.length > 0
                ? request.tagNames.join(', ')
                : 'N/A'}
            </p>
            <h4>Steps to Reproduce:</h4>
            <ul>
              {request.steps && request.steps.length > 0 ? (
                request.steps.map((step, index) => <li key={index}>{step}</li>)
              ) : (
                <li>No steps provided.</li>
              )}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConfirmationPage;
