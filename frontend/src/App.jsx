import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Elements } from '@stripe/react-stripe-js';
import { getStripe } from './services/stripe';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import FaceSwap from './pages/FaceSwap';
import ARMask from './pages/ARMask';
import Pricing from './pages/Pricing';
import Dashboard from './pages/Dashboard';
import PaymentSuccess from './pages/PaymentSuccess';
import PaymentCancel from './pages/PaymentCancel';
import About from './pages/About';
import Contact from './pages/Contact';

function App() {
  return (
    <Elements stripe={getStripe()}>
      <Router>
        <div className="min-h-screen bg-gray-50 flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/face-swap" element={<FaceSwap />} />
              <Route path="/ar-mask" element={<ARMask />} />
              <Route path="/pricing" element={<Pricing />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/payment-success" element={<PaymentSuccess />} />
              <Route path="/payment-cancel" element={<PaymentCancel />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </Elements>
  );
}

export default App;
