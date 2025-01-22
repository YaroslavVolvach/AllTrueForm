import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: {
    id: localStorage.getItem('user_id') || null,
    full_name: localStorage.getItem('full_name') || null,
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
      const { token, id, full_name, email } = action.payload;

      state.isLoading = false;
      state.token = token;
      state.user.id = id;
      state.user.full_name = full_name;
      state.user.email = email;

      saveToLocalStorage('token', token);
      saveToLocalStorage('user_id', id);
      saveToLocalStorage('full_name', full_name);
      saveToLocalStorage('email', email);
    },
    loginFailure: (state, action) => {
      state.isLoading = false;
      state.isError = true;
      state.errorMessage = action.payload;
    },
    logout: (state) => {
      state.user.id = null;
      state.user.full_name = null;
      state.user.email = null;
      state.token = null;
      state.isLoading = false;
      state.isError = false;
      state.errorMessage = '';

      removeFromLocalStorage('token');
      removeFromLocalStorage('user_id');
      removeFromLocalStorage('full_name');
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
