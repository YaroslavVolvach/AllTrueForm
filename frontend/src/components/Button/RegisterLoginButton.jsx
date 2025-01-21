import React from 'react';
import { Link } from 'react-router-dom';

const RegisterLoginButton = () => {
  return (
    <>
      <Link to="/register" className="navbar-button">
        Registration
      </Link>
      <Link to="/login" className="navbar-button">
        Login
      </Link>
    </>
  );
};

export default RegisterLoginButton;
