// components/LogoutButton.js
import React from 'react';
import { useDispatch } from 'react-redux';
import { removeToken } from '../../redux/slices/authSlice';

const LogoutButton = () => {
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(removeToken());
    localStorage.removeItem('token');
  };

  return (
    <button className="navbar-button" onClick={handleLogout}>
      Logout
    </button>
  );
};

export default LogoutButton;
