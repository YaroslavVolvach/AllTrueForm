import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SupportRequestForm from './components/Form/SupportRequestForm';
import Navbar from './components/Navbar';
import ConfirmationPage from './pages/ConfirmationPage';
import RegistrationForm from './components/Form/RegistrationForm';
import LoginForm from './components/Form/LoginForm';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<SupportRequestForm />} />
        <Route path="/confirmation" element={<ConfirmationPage />} />
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginForm />} />
      </Routes>
    </Router>
  );
};

export default App;
