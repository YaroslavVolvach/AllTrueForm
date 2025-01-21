import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: null,
  token: localStorage.getItem('token') || null,
  isLoading: false,
  isError: false,
  errorMessage: '',
};

const saveTokenToLocalStorage = (token) => {
  localStorage.setItem('token', token);
};

const removeTokenFromLocalStorage = () => {
  localStorage.removeItem('token');
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    registerStart: (state) => {
      state.isLoading = true;
      state.isError = false;
      state.errorMessage = '';
    },
    registerSuccess: (state, action) => {
      state.isLoading = false;
      state.user = action.payload.user;
      state.token = action.payload.token;
      saveTokenToLocalStorage(state.token);
    },
    registerFailure: (state, action) => {
      state.isLoading = false;
      state.isError = true;
      state.errorMessage = action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isLoading = false;
      state.isError = false;
      state.errorMessage = '';
      removeTokenFromLocalStorage();
    },
    setToken: (state, action) => {
      state.token = action.payload;
      saveTokenToLocalStorage(action.payload);
    },
    removeToken: (state) => {
      state.token = null;
      removeTokenFromLocalStorage();
    },
  },
});

export const {
  registerStart,
  registerSuccess,
  registerFailure,
  logout,
  setToken,
  removeToken,
} = authSlice.actions;

export default authSlice.reducer;
