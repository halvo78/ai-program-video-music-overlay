'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Check,
  X,
  Zap,
  Crown,
  Building2,
  Sparkles,
  Video,
  Music,
  Globe,
  Palette,
  Bot,
  BarChart3,
  Shield,
  Headphones,
  ArrowRight,
  Star,
} from 'lucide-react';

const pricingTiers = [
  {
    id: 'free',
    name: 'Free',
    description: 'Perfect for trying out Taj Chat',
    priceMonthly: 0,
    priceYearly: 0,
    icon: Sparkles,
    color: 'from-gray-500 to-gray-600',
    features: [
      { name: '5 videos per month', included: true },
      { name: '720p export quality', included: true },
      { name: 'Basic AI features', included: true },
      { name: 'Taj Chat watermark', included: true },
      { name: '1 social platform', included: true },
      { name: 'Virality Score', included: false },
      { name: 'URL to Video', included: false },
      { name: 'AI B-Roll', included: false },
      { name: 'Brand Kit', included: false },
      { name: 'AI Avatars', included: false },
    ],
    cta: 'Get Started Free',
    popular: false,
  },
  {
    id: 'creator',
    name: 'Creator',
    description: 'For content creators ready to grow',
    priceMonthly: 19,
    priceYearly: 159,
    icon: Zap,
    color: 'from-blue-500 to-cyan-500',
    features: [
      { name: '30 videos per month', included: true },
      { name: '1080p export quality', included: true },
      { name: 'All AI features', included: true },
      { name: 'No watermark', included: true },
      { name: '3 social platforms', included: true },
      { name: 'Virality Score', included: true },
      { name: 'URL to Video', included: true },
      { name: 'AI B-Roll', included: false },
      { name: 'Brand Kit', included: false },
      { name: 'AI Avatars', included: false },
    ],
    cta: 'Start Creating',
    popular: true,
  },
  {
    id: 'professional',
    name: 'Professional',
    description: 'For serious creators and businesses',
    priceMonthly: 49,
    priceYearly: 399,
    icon: Crown,
    color: 'from-purple-500 to-pink-500',
    features: [
      { name: '100 videos per month', included: true },
      { name: '4K export quality', included: true },
      { name: 'All AI features', included: true },
      { name: 'No watermark', included: true },
      { name: 'All 6 social platforms', included: true },
      { name: 'Virality Score', included: true },
      { name: 'URL to Video', included: true },
      { name: 'AI B-Roll', included: true },
      { name: 'Brand Kit', included: true },
      { name: 'AI Avatars', included: false },
    ],
    cta: 'Go Professional',
    popular: false,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'For teams and agencies',
    priceMonthly: 199,
    priceYearly: 1599,
    icon: Building2,
    color: 'from-amber-500 to-orange-500',
    features: [
      { name: 'Unlimited videos', included: true },
      { name: '4K export quality', included: true },
      { name: 'All AI features', included: true },
      { name: 'White-label option', included: true },
      { name: 'All 6 social platforms', included: true },
      { name: 'Virality Score', included: true },
      { name: 'URL to Video', included: true },
      { name: 'AI B-Roll', included: true },
      { name: 'Brand Kit', included: true },
      { name: 'AI Avatars', included: true },
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

const allFeatures = [
  {
    category: 'Video Creation',
    icon: Video,
    features: [
      { name: 'AI Video Generation', free: true, creator: true, professional: true, enterprise: true },
      { name: 'AI Music Generation', free: true, creator: true, professional: true, enterprise: true },
      { name: 'Auto Captions', free: true, creator: true, professional: true, enterprise: true },
      { name: 'URL to Video', free: false, creator: true, professional: true, enterprise: true },
      { name: 'AI B-Roll Generation', free: false, creator: false, professional: true, enterprise: true },
      { name: 'AI Storyboard', free: false, creator: true, professional: true, enterprise: true },
    ],
  },
  {
    category: 'AI Features',
    icon: Bot,
    features: [
      { name: 'Virality Score', free: false, creator: true, professional: true, enterprise: true },
      { name: 'Filler Word Removal', free: false, creator: true, professional: true, enterprise: true },
      { name: 'Smart Cut (Silence Removal)', free: false, creator: true, professional: true, enterprise: true },
      { name: 'Keyword Highlighting', free: false, creator: true, professional: true, enterprise: true },
      { name: 'AI Avatars', free: false, creator: false, professional: false, enterprise: true },
      { name: 'Video Translation', free: false, creator: false, professional: true, enterprise: true },
    ],
  },
  {
    category: 'Branding',
    icon: Palette,
    features: [
      { name: 'No Watermark', free: false, creator: true, professional: true, enterprise: true },
      { name: 'Brand Kit', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Custom Intro/Outro', free: false, creator: false, professional: true, enterprise: true },
      { name: 'White-label', free: false, creator: false, professional: false, enterprise: true },
    ],
  },
  {
    category: 'Publishing',
    icon: Globe,
    features: [
      { name: 'TikTok', free: true, creator: true, professional: true, enterprise: true },
      { name: 'Instagram Reels', free: false, creator: true, professional: true, enterprise: true },
      { name: 'YouTube Shorts', free: false, creator: true, professional: true, enterprise: true },
      { name: 'Twitter/X', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Facebook', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Threads', free: false, creator: false, professional: true, enterprise: true },
    ],
  },
  {
    category: 'Analytics',
    icon: BarChart3,
    features: [
      { name: 'Basic Analytics', free: true, creator: true, professional: true, enterprise: true },
      { name: 'Advanced Analytics', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Competitor Benchmarking', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Custom Reports', free: false, creator: false, professional: false, enterprise: true },
    ],
  },
  {
    category: 'Support',
    icon: Headphones,
    features: [
      { name: 'Email Support', free: true, creator: true, professional: true, enterprise: true },
      { name: 'Priority Support', free: false, creator: false, professional: true, enterprise: true },
      { name: 'Dedicated Account Manager', free: false, creator: false, professional: false, enterprise: true },
      { name: 'SLA Guarantee', free: false, creator: false, professional: false, enterprise: true },
    ],
  },
];

export default function PricingPage() {
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly');

  const handleSubscribe = async (tierId: string) => {
    // In production, this would call the Stripe checkout API
    console.log(`Subscribing to ${tierId} (${billingPeriod})`);
    
    // Redirect to Stripe checkout
    // const response = await fetch('/api/checkout', {
    //   method: 'POST',
    //   body: JSON.stringify({ tierId, billingPeriod }),
    // });
    // const { url } = await response.json();
    // window.location.href = url;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950">
      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-6">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white via-purple-200 to-white bg-clip-text text-transparent">
                Simple, Transparent Pricing
              </span>
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8">
              Choose the plan that fits your creative needs. All plans include our core AI features.
              Upgrade or downgrade anytime.
            </p>

            {/* Billing Toggle */}
            <div className="flex items-center justify-center gap-4 mb-12">
              <span className={`text-sm ${billingPeriod === 'monthly' ? 'text-white' : 'text-gray-500'}`}>
                Monthly
              </span>
              <button
                onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'yearly' : 'monthly')}
                className="relative w-16 h-8 bg-gray-800 rounded-full p-1 transition-colors"
              >
                <motion.div
                  className="w-6 h-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                  animate={{ x: billingPeriod === 'yearly' ? 32 : 0 }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              </button>
              <span className={`text-sm ${billingPeriod === 'yearly' ? 'text-white' : 'text-gray-500'}`}>
                Yearly
                <span className="ml-2 px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded-full">
                  Save 30%
                </span>
              </span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="relative px-6 pb-20">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pricingTiers.map((tier, index) => {
              const Icon = tier.icon;
              const price = billingPeriod === 'yearly' 
                ? Math.round(tier.priceYearly / 12) 
                : tier.priceMonthly;
              
              return (
                <motion.div
                  key={tier.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`relative rounded-2xl ${
                    tier.popular 
                      ? 'bg-gradient-to-b from-purple-500/20 to-pink-500/20 border-2 border-purple-500/50' 
                      : 'bg-gray-900/50 border border-white/10'
                  } p-6 flex flex-col`}
                >
                  {tier.popular && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                      <span className="px-4 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-medium rounded-full flex items-center gap-1">
                        <Star className="w-4 h-4" />
                        Most Popular
                      </span>
                    </div>
                  )}

                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${tier.color} flex items-center justify-center mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  <h3 className="text-xl font-bold text-white mb-1">{tier.name}</h3>
                  <p className="text-sm text-gray-400 mb-4">{tier.description}</p>

                  <div className="mb-6">
                    <span className="text-4xl font-bold text-white">${price}</span>
                    <span className="text-gray-400">/month</span>
                    {billingPeriod === 'yearly' && tier.priceMonthly > 0 && (
                      <div className="text-sm text-gray-500 mt-1">
                        ${tier.priceYearly} billed yearly
                      </div>
                    )}
                  </div>

                  <ul className="space-y-3 mb-6 flex-1">
                    {tier.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2">
                        {feature.included ? (
                          <Check className="w-5 h-5 text-green-400 flex-shrink-0" />
                        ) : (
                          <X className="w-5 h-5 text-gray-600 flex-shrink-0" />
                        )}
                        <span className={feature.included ? 'text-gray-300' : 'text-gray-600'}>
                          {feature.name}
                        </span>
                      </li>
                    ))}
                  </ul>

                  <button
                    onClick={() => handleSubscribe(tier.id)}
                    className={`w-full py-3 px-4 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
                      tier.popular
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg hover:shadow-purple-500/25'
                        : 'bg-white/10 text-white hover:bg-white/20'
                    }`}
                  >
                    {tier.cta}
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="px-6 py-20 bg-gray-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Compare All Features</h2>
            <p className="text-gray-400">See exactly what's included in each plan</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-4 px-4 text-gray-400 font-medium">Features</th>
                  <th className="text-center py-4 px-4 text-gray-400 font-medium">Free</th>
                  <th className="text-center py-4 px-4 text-purple-400 font-medium">Creator</th>
                  <th className="text-center py-4 px-4 text-gray-400 font-medium">Professional</th>
                  <th className="text-center py-4 px-4 text-gray-400 font-medium">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {allFeatures.map((category) => (
                  <>
                    <tr key={category.category} className="bg-gray-800/30">
                      <td colSpan={5} className="py-3 px-4">
                        <div className="flex items-center gap-2 text-white font-medium">
                          <category.icon className="w-5 h-5" />
                          {category.category}
                        </div>
                      </td>
                    </tr>
                    {category.features.map((feature, i) => (
                      <tr key={`${category.category}-${i}`} className="border-b border-white/5">
                        <td className="py-3 px-4 text-gray-400">{feature.name}</td>
                        <td className="text-center py-3 px-4">
                          {feature.free ? (
                            <Check className="w-5 h-5 text-green-400 mx-auto" />
                          ) : (
                            <X className="w-5 h-5 text-gray-600 mx-auto" />
                          )}
                        </td>
                        <td className="text-center py-3 px-4 bg-purple-500/5">
                          {feature.creator ? (
                            <Check className="w-5 h-5 text-green-400 mx-auto" />
                          ) : (
                            <X className="w-5 h-5 text-gray-600 mx-auto" />
                          )}
                        </td>
                        <td className="text-center py-3 px-4">
                          {feature.professional ? (
                            <Check className="w-5 h-5 text-green-400 mx-auto" />
                          ) : (
                            <X className="w-5 h-5 text-gray-600 mx-auto" />
                          )}
                        </td>
                        <td className="text-center py-3 px-4">
                          {feature.enterprise ? (
                            <Check className="w-5 h-5 text-green-400 mx-auto" />
                          ) : (
                            <X className="w-5 h-5 text-gray-600 mx-auto" />
                          )}
                        </td>
                      </tr>
                    ))}
                  </>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="px-6 py-20">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Frequently Asked Questions</h2>
          </div>

          <div className="space-y-4">
            {[
              {
                q: 'Can I change my plan later?',
                a: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate any charges.',
              },
              {
                q: 'What payment methods do you accept?',
                a: 'We accept all major credit cards (Visa, Mastercard, American Express) and PayPal through our secure Stripe payment system.',
              },
              {
                q: 'Is there a free trial?',
                a: 'Our Free plan is essentially a permanent free trial. You can create up to 5 videos per month with basic features to test the platform.',
              },
              {
                q: 'What happens to my videos if I downgrade?',
                a: 'Your existing videos are never deleted. However, you may lose access to premium features like 4K export until you upgrade again.',
              },
              {
                q: 'Do you offer refunds?',
                a: 'Yes, we offer a 14-day money-back guarantee. If you\'re not satisfied, contact us for a full refund.',
              },
            ].map((faq, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-gray-900/50 border border-white/10 rounded-xl p-6"
              >
                <h3 className="text-lg font-medium text-white mb-2">{faq.q}</h3>
                <p className="text-gray-400">{faq.a}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-3xl p-12"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Create Viral Videos?
            </h2>
            <p className="text-xl text-gray-400 mb-8">
              Join thousands of creators using Taj Chat to grow their audience.
            </p>
            <button
              onClick={() => handleSubscribe('creator')}
              className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-purple-500/25 transition-all flex items-center gap-2 mx-auto"
            >
              Start Your Free Trial
              <ArrowRight className="w-5 h-5" />
            </button>
          </motion.div>
        </div>
      </section>
    </div>
  );
}

