import { loadStripe } from '@stripe/stripe-js';
import httpService from './http.js';

// Initialize Stripe with environment-based publishable key
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_placeholder');

export const getStripe = () => stripePromise;

export const redirectToCheckout = async (sessionId) => {
  const stripe = await getStripe();
  const { error } = await stripe.redirectToCheckout({ sessionId });
  
  if (error) {
    throw new Error(error.message);
  }
};

export const createPaymentIntent = async (amount, currency = 'usd', metadata = {}) => {
  try {
    // Use the centralized HTTP service for API calls
    return await httpService.createCheckoutSession({
      amount,
      currency,
      metadata,
      success_url: `${import.meta.env.VITE_FRONTEND_URL || 'https://www.playalter.com'}/payment-success`,
      cancel_url: `${import.meta.env.VITE_FRONTEND_URL || 'https://www.playalter.com'}/payment-cancel`,
    });
  } catch (error) {
    console.error('Payment intent creation failed:', error);
    throw error;
  }
};

export default {
  getStripe,
  redirectToCheckout,
  createPaymentIntent,
};
