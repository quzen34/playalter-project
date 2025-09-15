import { useState } from 'react';
import { createCheckoutSession as apiCreateCheckoutSession } from '../services/api';

export const useStripe = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const createCheckoutSession = async ({ priceId, successUrl, cancelUrl }) => {
    setIsLoading(true);
    setError(null);

    try {
      // For demo purposes, we'll use a mock email
      const email = 'demo@playalter.com';
      
      const response = await apiCreateCheckoutSession(
        priceId,
        email,
        successUrl,
        cancelUrl
      );

      if (response.checkout_url) {
        // Redirect to Stripe Checkout
        window.location.href = response.checkout_url;
      } else {
        throw new Error('No checkout URL received');
      }
    } catch (err) {
      setError(err.message);
      console.error('Stripe checkout error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStripeRedirect = async (sessionId) => {
    // Handle successful payment redirect
    try {
      // You could verify the session here with your backend
      console.log('Payment successful, session ID:', sessionId);
      return { success: true, sessionId };
    } catch (err) {
      console.error('Error handling Stripe redirect:', err);
      return { success: false, error: err.message };
    }
  };

  return {
    isLoading,
    error,
    createCheckoutSession,
    handleStripeRedirect,
  };
};
