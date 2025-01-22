import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: {
    fullName: localStorage.getItem('fullName') || null,
    email: localStorage.getItem('email') || null,
  },
  token: localStorage.getItem('token') || null,
  isLoading: false,
  isError: false,
  errorMessage: '',
};

const saveToLocalStorage = (key, value) => {
  localStorage.setItem(key, value);
};

const removeFromLocalStorage = (key) => {
  localStorage.removeItem(key);
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => {
      state.isLoading = true;
      state.isError = false;
      state.errorMessage = '';
    },
    loginSuccess: (state, action) => {
      const { token, fullName, email } = action.payload;

      state.isLoading = false;
      state.token = token;
      state.user.fullName = fullName;
      state.user.email = email;

      saveToLocalStorage('token', token);
      saveToLocalStorage('fullName', fullName);
      saveToLocalStorage('email', email);
    },
    loginFailure: (state, action) => {
      state.isLoading = false;
      state.isError = true;
      state.errorMessage = action.payload;
    },
    logout: (state) => {
      state.user.fullName = null;
      state.user.email = null;
      state.token = null;
      state.isLoading = false;
      state.isError = false;
      state.errorMessage = '';

      removeFromLocalStorage('token');
      removeFromLocalStorage('fullName');
      removeFromLocalStorage('email');
    },
    setToken: (state, action) => {
      state.token = action.payload;
      saveToLocalStorage('token', action.payload);
    },
    removeToken: (state) => {
      state.token = null;
      removeFromLocalStorage('token');
    },
  },
});

export const {
  loginStart,
  loginSuccess,
  loginFailure,
  logout,
  setToken,
  removeToken,
} = authSlice.actions;

export default authSlice.reducer;
