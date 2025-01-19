import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SupportRequestForm from './components/Form/SupportRequestForm';
import Navbar from './components/Navbar';
import ConfirmationPage from './pages/ConfirmationPage';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<SupportRequestForm />} />
        <Route path="/confirmation" element={<ConfirmationPage />} />
      </Routes>
    </Router>
  );
};

export default App;
