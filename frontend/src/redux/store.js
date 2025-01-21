import { configureStore } from '@reduxjs/toolkit';
import formReducer from './slices/formSlice';
import authReducer from './slices/authSlice';
const store = configureStore({
  reducer: {
    form: formReducer,
    auth: authReducer,
  },
});

export default store;
