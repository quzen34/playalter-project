import { loadStripe } from '@stripe/stripe-js';

// Initialize Stripe (you'll need to set your publishable key)
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
  // This would typically be done on the backend
  // This is just a placeholder for the frontend structure
  console.log('Creating payment intent:', { amount, currency, metadata });
};

export default {
  getStripe,
  redirectToCheckout,
  createPaymentIntent,
};
