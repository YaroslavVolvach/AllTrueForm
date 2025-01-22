import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import {
  loginStart,
  loginSuccess,
  loginFailure,
} from '../../redux/slices/authSlice';
import { useNavigate } from 'react-router-dom';
import '../../styles/login.css';

const LoginForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [loginError, setLoginError] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    dispatch(loginStart());
    try {
      const response = await axios.post(
        'http://localhost:8000/v1/users/login',
        data
      );

      const { access_token, user } = response.data;
      dispatch(
        loginSuccess({
          token: access_token,
          fullName: user.fullName,
          email: user.email,
        })
      );

      navigate('/');
    } catch (error) {
      setLoginError('Invalid email or password');
      dispatch(loginFailure('Invalid email or password'));
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="form">
        <div className="form-field">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            {...register('email', { required: 'Email is required' })}
          />
          {errors.email && (
            <span className="error">{errors.email.message}</span>
          )}
        </div>
        <div className="form-field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            {...register('password', { required: 'Password is required' })}
          />
          {errors.password && (
            <span className="error">{errors.password.message}</span>
          )}
        </div>
        {loginError && <p className="error">{loginError}</p>}
        <button type="submit" className="submit-btn">
          Login
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
