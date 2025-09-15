import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Zap, 
  Palette, 
  Video, 
  ArrowRight, 
  CheckCircle, 
  Star,
  Play,
  Users,
  TrendingUp,
  Shield
} from 'lucide-react';
import { healthCheck } from '../services/api';

const Home = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const status = await healthCheck();
        setHealthStatus(status);
      } catch (error) {
        console.error('Health check failed:', error);
        setHealthStatus({ status: 'unhealthy', error: error.message });
      } finally {
        setIsLoading(false);
      }
    };

    checkHealth();
  }, []);

  const features = [
    {
      icon: Zap,
      title: 'AI Face Swap',
      description: 'Advanced face swapping technology with real-time processing and high-quality results.',
      link: '/face-swap',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Palette,
      title: 'AR Masks',
      description: 'Apply stunning AR masks and filters with precise face tracking and realistic effects.',
      link: '/ar-mask',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Video,
      title: 'Live Streaming',
      description: 'Stream live with AI effects using Agora SDK integration for seamless broadcasting.',
      link: '/dashboard',
      color: 'from-green-500 to-teal-500'
    }
  ];

  const stats = [
    { label: 'Active Users', value: '10K+', icon: Users },
    { label: 'Face Swaps', value: '1M+', icon: Zap },
    { label: 'Success Rate', value: '99.9%', icon: TrendingUp },
    { label: 'Uptime', value: '99.9%', icon: Shield }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Content Creator',
      content: 'PLAYALTER has revolutionized my content creation process. The face swap quality is incredible!',
      rating: 5
    },
    {
      name: 'Mike Chen',
      role: 'Streamer',
      content: 'The AR masks are so fun and engaging. My audience loves the interactive features.',
      rating: 5
    },
    {
      name: 'Emma Davis',
      role: 'Social Media Manager',
      content: 'Easy to use, professional results. Perfect for our social media campaigns.',
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 text-white overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Transform Your Digital
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">
                Experience
              </span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-gray-100 max-w-3xl mx-auto">
              Unleash the power of AI with advanced face swap, AR masks, and live streaming technology. 
              Create, innovate, and captivate your audience.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/face-swap"
                className="inline-flex items-center px-8 py-4 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
              >
                <Zap className="w-5 h-5 mr-2" />
                Try Face Swap
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              <Link
                to="/ar-mask"
                className="inline-flex items-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-purple-600 transition-colors"
              >
                <Palette className="w-5 h-5 mr-2" />
                Explore AR Masks
              </Link>
            </div>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute top-0 right-0 w-1/3 h-full opacity-20">
          <div className="w-full h-full bg-gradient-to-l from-white to-transparent"></div>
        </div>
      </section>

      {/* Status Banner */}
      {!isLoading && (
        <section className="py-4 bg-gray-50 border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-center">
              {healthStatus?.status === 'healthy' ? (
                <div className="flex items-center text-green-600">
                  <CheckCircle className="w-5 h-5 mr-2" />
                  <span className="font-medium">All systems operational</span>
                  {healthStatus.integrations && (
                    <span className="text-gray-500 ml-2">
                      • Stripe: {healthStatus.integrations.stripe === 'connected' ? '✓' : '⚠️'}
                      • n8n: {healthStatus.integrations.n8n === 'connected' ? '✓' : '⚠️'}
                    </span>
                  )}
                </div>
              ) : (
                <div className="flex items-center text-yellow-600">
                  <Shield className="w-5 h-5 mr-2" />
                  <span className="font-medium">Some services may be limited</span>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful AI Features
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience the future of digital content creation with our cutting-edge AI technology
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="group relative bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
                >
                  <div className={`absolute inset-0 bg-gradient-to-r ${feature.color} opacity-0 group-hover:opacity-10 transition-opacity`}></div>
                  <div className="relative p-8">
                    <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${feature.color} text-white mb-4`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 mb-6">
                      {feature.description}
                    </p>
                    <Link
                      to={feature.link}
                      className="inline-flex items-center text-purple-600 font-semibold hover:text-purple-700 transition-colors"
                    >
                      Learn more
                      <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
                    <Icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-2">
                    {stat.value}
                  </div>
                  <div className="text-gray-600">
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600">
              Join thousands of satisfied creators and streamers
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-gray-50 rounded-xl p-6">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-700 mb-4 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold text-gray-900">
                    {testimonial.name}
                  </div>
                  <div className="text-gray-600 text-sm">
                    {testimonial.role}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your Content?
          </h2>
          <p className="text-xl mb-8 text-gray-100">
            Join thousands of creators using PLAYALTER to create amazing content with AI
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/pricing"
              className="inline-flex items-center px-8 py-4 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Play className="w-5 h-5 mr-2" />
              Get Started Now
            </Link>
            <Link
              to="/about"
              className="inline-flex items-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-purple-600 transition-colors"
            >
              Learn More
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
