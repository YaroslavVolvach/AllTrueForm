import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { removeToken } from '../redux/slices/authSlice';
import '../styles/navbar.css';

const Navbar = () => {
  const token = useSelector((state) => state.auth.token);
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(removeToken());
    localStorage.removeItem('token');
  };

  return (
    <nav className="navbar">
      <h1 className="navbar-title">All True</h1>
      <div className="navbar-buttons">
        {!token ? (
          <>
            <Link to="/register" className="navbar-button">
              Registration
            </Link>
            <Link to="/login" className="navbar-button">
              Login
            </Link>
          </>
        ) : (
          <>
            <Link to="/confirmations" className="navbar-button">
              Confirmations
            </Link>
            <button className="navbar-button" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
