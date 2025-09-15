import React, { useState } from 'react';
import { Check, Star, Zap, Crown, Rocket } from 'lucide-react';
import { useStripe } from '../hooks/useStripe';

const Pricing = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const { createCheckoutSession, isLoading } = useStripe();

  const plans = [
    {
      id: 'starter',
      name: 'Starter',
      description: 'Perfect for individuals getting started with AI content',
      icon: Zap,
      color: 'from-blue-500 to-cyan-500',
      monthly: { price: 9.99, priceId: 'price_starter_monthly' },
      yearly: { price: 8.33, originalPrice: 9.99, priceId: 'price_starter_yearly' },
      features: [
        '50 Face swaps per month',
        '20 AR mask applications',
        'Basic quality processing',
        'Standard support',
        'Download in HD',
        'Basic templates'
      ],
      limitations: [
        'Watermark on results',
        'Processing queue priority: Low'
      ]
    },
    {
      id: 'pro',
      name: 'Pro',
      description: 'Ideal for content creators and social media professionals',
      icon: Star,
      color: 'from-purple-500 to-pink-500',
      popular: true,
      monthly: { price: 24.99, priceId: 'price_pro_monthly' },
      yearly: { price: 20.83, originalPrice: 24.99, priceId: 'price_pro_yearly' },
      features: [
        '200 Face swaps per month',
        '100 AR mask applications',
        'High quality processing',
        'Priority support',
        'Download in 4K',
        'Premium templates',
        'No watermarks',
        'Batch processing',
        'Custom AR masks'
      ],
      limitations: []
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      description: 'For businesses and teams requiring maximum capabilities',
      icon: Crown,
      color: 'from-yellow-500 to-orange-500',
      monthly: { price: 99.99, priceId: 'price_enterprise_monthly' },
      yearly: { price: 83.33, originalPrice: 99.99, priceId: 'price_enterprise_yearly' },
      features: [
        'Unlimited face swaps',
        'Unlimited AR masks',
        'Ultra-high quality processing',
        '24/7 premium support',
        'Download in 8K',
        'All templates included',
        'No watermarks',
        'Priority processing',
        'Custom integrations',
        'API access',
        'Team management',
        'Advanced analytics'
      ],
      limitations: []
    }
  ];

  const handleSubscribe = async (plan, cycle) => {
    const priceId = cycle === 'monthly' ? plan.monthly.priceId : plan.yearly.priceId;
    
    try {
      await createCheckoutSession({
        priceId,
        successUrl: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
        cancelUrl: `${window.location.origin}/pricing`
      });
    } catch (error) {
      console.error('Subscription error:', error);
    }
  };

  const getCurrentPrice = (plan) => {
    return billingCycle === 'monthly' ? plan.monthly.price : plan.yearly.price;
  };

  const getOriginalPrice = (plan) => {
    return billingCycle === 'yearly' ? plan.yearly.originalPrice : null;
  };

  const getSavings = (plan) => {
    if (billingCycle === 'yearly') {
      const monthlyCost = plan.monthly.price * 12;
      const yearlyCost = plan.yearly.price * 12;
      return Math.round(((monthlyCost - yearlyCost) / monthlyCost) * 100);
    }
    return 0;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Unlock the full potential of AI-powered content creation with our flexible pricing plans
          </p>

          {/* Billing Toggle */}
          <div className="inline-flex items-center bg-white border border-gray-200 rounded-lg p-1 shadow-sm">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-md font-medium transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 py-2 rounded-md font-medium transition-all relative ${
                billingCycle === 'yearly'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Yearly
              <span className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                Save 17%
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {plans.map((plan) => {
            const Icon = plan.icon;
            const currentPrice = getCurrentPrice(plan);
            const originalPrice = getOriginalPrice(plan);
            const savings = getSavings(plan);

            return (
              <div
                key={plan.id}
                className={`relative bg-white rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-xl ${
                  plan.popular ? 'ring-2 ring-purple-500' : ''
                }`}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute top-0 left-0 right-0 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-center py-2 font-semibold">
                    Most Popular
                  </div>
                )}

                <div className={`p-8 ${plan.popular ? 'pt-16' : ''}`}>
                  {/* Plan Header */}
                  <div className="text-center mb-6">
                    <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${plan.color} text-white mb-4`}>
                      <Icon className="w-8 h-8" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {plan.name}
                    </h3>
                    <p className="text-gray-600">
                      {plan.description}
                    </p>
                  </div>

                  {/* Price */}
                  <div className="text-center mb-6">
                    <div className="flex items-center justify-center mb-2">
                      {originalPrice && (
                        <span className="text-lg text-gray-400 line-through mr-2">
                          ${originalPrice}
                        </span>
                      )}
                      <span className="text-4xl font-bold text-gray-900">
                        ${currentPrice}
                      </span>
                      <span className="text-gray-600 ml-2">
                        /{billingCycle === 'monthly' ? 'month' : 'month'}
                      </span>
                    </div>
                    {billingCycle === 'yearly' && (
                      <div className="text-sm text-green-600 font-medium">
                        Save {savings}% with yearly billing
                      </div>
                    )}
                  </div>

                  {/* Features */}
                  <div className="space-y-3 mb-8">
                    {plan.features.map((feature, index) => (
                      <div key={index} className="flex items-center">
                        <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                        <span className="text-gray-700">{feature}</span>
                      </div>
                    ))}
                    {plan.limitations.map((limitation, index) => (
                      <div key={index} className="flex items-center opacity-60">
                        <div className="w-5 h-5 mr-3 flex-shrink-0 flex items-center justify-center">
                          <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                        </div>
                        <span className="text-gray-600 text-sm">{limitation}</span>
                      </div>
                    ))}
                  </div>

                  {/* CTA Button */}
                  <button
                    onClick={() => handleSubscribe(plan, billingCycle)}
                    disabled={isLoading}
                    className={`w-full py-3 px-6 font-semibold rounded-lg transition-all ${
                      plan.popular
                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700'
                        : 'bg-gray-900 text-white hover:bg-gray-800'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {isLoading ? 'Processing...' : `Get Started with ${plan.name}`}
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* FAQ Section */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Frequently Asked Questions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Can I change my plan anytime?
                </h3>
                <p className="text-gray-600">
                  Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the next billing cycle.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Is there a free trial?
                </h3>
                <p className="text-gray-600">
                  We offer a 7-day free trial for all plans so you can test our features before committing.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  What payment methods do you accept?
                </h3>
                <p className="text-gray-600">
                  We accept all major credit cards, PayPal, and bank transfers for enterprise customers.
                </p>
              </div>
            </div>
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Do you offer refunds?
                </h3>
                <p className="text-gray-600">
                  Yes, we offer a 30-day money-back guarantee if you're not satisfied with our service.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Is my data secure?
                </h3>
                <p className="text-gray-600">
                  Absolutely. We use enterprise-grade encryption and never store your images longer than necessary for processing.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Need a custom plan?
                </h3>
                <p className="text-gray-600">
                  Contact our sales team for custom pricing and features tailored to your specific needs.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Enterprise CTA */}
        <div className="mt-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg overflow-hidden">
          <div className="px-8 py-12 text-center text-white">
            <Rocket className="w-12 h-12 mx-auto mb-4" />
            <h2 className="text-3xl font-bold mb-4">
              Need Something More?
            </h2>
            <p className="text-xl mb-6 text-blue-100">
              Get custom integrations, dedicated support, and enterprise-grade security
            </p>
            <button className="inline-flex items-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors">
              Contact Sales
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;
