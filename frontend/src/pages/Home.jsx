/**
 * MediNova AI - Landing Page
 * Premium healthcare platform landing page with hero, features, stats, and CTA
 */

import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
  Brain, CalendarDays, HeartPulse, Pill, MapPin, Shield,
  ChevronRight, Star, Activity, Stethoscope, Users, Clock,
  ArrowRight, CheckCircle, Zap, Lock, Globe, Play
} from 'lucide-react';

/* ── Animated counter hook ──────────────────────────────────────────── */
const useCounter = (target, duration = 2000, start = false) => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!start) return;
    let startTime = null;
    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      setCount(Math.floor(progress * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [start, target, duration]);
  return count;
};

/* ── Intersection Observer hook ──────────────────────────────────────── */
const useInView = (options = {}) => {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { setInView(true); observer.disconnect(); }
    }, options);
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  return [ref, inView];
};

/* ── Stat card with animated counter ─────────────────────────────────── */
const StatItem = ({ value, suffix = '', label, color }) => {
  const [ref, inView] = useInView({ threshold: 0.3 });
  const count = useCounter(value, 2000, inView);
  return (
    <div ref={ref} className="text-center">
      <p className={`text-4xl lg:text-5xl font-black ${color}`}>
        {count.toLocaleString()}{suffix}
      </p>
      <p className="text-neutral-400 text-sm mt-2 font-medium">{label}</p>
    </div>
  );
};

/* ── Feature card ──────────────────────────────────────────────────────  */
const FeatureCard = ({ icon: Icon, title, description, gradient, delay = 0 }) => {
  const [ref, inView] = useInView({ threshold: 0.1 });
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`group bg-white dark:bg-neutral-800/60 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 hover:border-primary-300 dark:hover:border-primary-700 shadow-sm hover:shadow-xl transition-all duration-500 ${
        inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
    >
      <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <h3 className="text-lg font-bold text-neutral-900 dark:text-white mb-2">{title}</h3>
      <p className="text-neutral-500 dark:text-neutral-400 text-sm leading-relaxed">{description}</p>
    </div>
  );
};

/* ── Testimonial card ─────────────────────────────────────────────────── */
const TestimonialCard = ({ name, role, quote, rating, avatar }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm flex flex-col gap-4">
    <div className="flex gap-1">
      {Array.from({ length: rating }).map((_, i) => (
        <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
      ))}
    </div>
    <p className="text-neutral-600 dark:text-neutral-300 text-sm leading-relaxed italic">"{quote}"</p>
    <div className="flex items-center gap-3 mt-auto">
      <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${avatar} flex items-center justify-center text-white font-bold text-sm flex-shrink-0`}>
        {name[0]}
      </div>
      <div>
        <p className="font-semibold text-sm text-neutral-900 dark:text-white">{name}</p>
        <p className="text-xs text-neutral-400">{role}</p>
      </div>
    </div>
  </div>
);

/* ── How it works step ────────────────────────────────────────────────── */
const Step = ({ number, title, description, icon: Icon }) => (
  <div className="flex gap-4">
    <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-primary-500 text-white flex items-center justify-center font-black text-lg shadow-lg shadow-primary-500/30">
      {number}
    </div>
    <div>
      <h3 className="font-bold text-neutral-900 dark:text-white mb-1 flex items-center gap-2">
        <Icon className="w-4 h-4 text-primary-500" />
        {title}
      </h3>
      <p className="text-sm text-neutral-500 dark:text-neutral-400 leading-relaxed">{description}</p>
    </div>
  </div>
);

/* ── Main Home component ──────────────────────────────────────────────── */
const Home = () => {
  const [heroVisible, setHeroVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setHeroVisible(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const features = [
    {
      icon: Brain,
      title: 'AI Symptom Analysis',
      description: 'Advanced multi-agent AI analyzes your symptoms and provides personalized health insights and recommendations.',
      gradient: 'from-violet-500 to-purple-600',
      delay: 0
    },
    {
      icon: CalendarDays,
      title: 'Smart Appointment Booking',
      description: 'Book consultations with verified specialists instantly. Video, in-person, or chat — your choice.',
      gradient: 'from-blue-500 to-cyan-500',
      delay: 100
    },
    {
      icon: HeartPulse,
      title: 'Personal Health Records',
      description: 'Securely store and access your complete medical history, vitals, and lab results in one place.',
      gradient: 'from-rose-500 to-pink-500',
      delay: 200
    },
    {
      icon: Pill,
      title: 'Medication Management',
      description: 'Track prescriptions, set reminders, and get drug interaction alerts to stay on top of your health.',
      gradient: 'from-emerald-500 to-teal-500',
      delay: 300
    },
    {
      icon: MapPin,
      title: 'Nearby Hospitals',
      description: 'Find hospitals, clinics, and emergency care near you with real-time availability information.',
      gradient: 'from-amber-500 to-orange-500',
      delay: 400
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'Enterprise-grade encryption and HIPAA-compliant infrastructure keeps your health data safe.',
      gradient: 'from-indigo-500 to-blue-600',
      delay: 500
    },
  ];

  const testimonials = [
    {
      name: 'Priya Sharma',
      role: 'Patient',
      quote: 'MediNova AI transformed how I manage my health. Booking appointments takes seconds, and the AI insights are incredibly accurate.',
      rating: 5,
      avatar: 'from-rose-400 to-pink-600'
    },
    {
      name: 'Dr. Rahul Mehta',
      role: 'Cardiologist',
      quote: 'As a doctor, the platform makes managing my patient queue effortless. The consultation tools are comprehensive and intuitive.',
      rating: 5,
      avatar: 'from-emerald-400 to-teal-600'
    },
    {
      name: 'Ananya Krishnan',
      role: 'Patient',
      quote: 'The medication reminders and health records feature have been life-changing for managing my chronic condition.',
      rating: 5,
      avatar: 'from-violet-400 to-purple-600'
    },
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-neutral-900 overflow-x-hidden">

      {/* ─── Navigation Bar ──────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-xl border-b border-neutral-200 dark:border-neutral-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-primary-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30">
              <span className="text-white font-black text-lg">M</span>
            </div>
            <span className="text-lg font-display font-bold text-neutral-900 dark:text-white">
              MediNova <span className="text-primary-500">AI</span>
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-600 dark:text-neutral-400">
            <a href="#features" className="hover:text-primary-500 transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-primary-500 transition-colors">How it works</a>
            <a href="#testimonials" className="hover:text-primary-500 transition-colors">Testimonials</a>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login" className="hidden sm:block text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:text-primary-500 transition-colors px-3 py-2">
              Sign In
            </Link>
            <Link to="/register" className="bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors shadow-lg shadow-primary-500/20">
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      {/* ─── Hero Section ────────────────────────────────────────────── */}
      <section className="relative pt-16 pb-24 lg:pt-24 lg:pb-32 overflow-hidden">
        {/* Background elements */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-violet-500/10 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-0 w-64 h-64 bg-cyan-500/8 rounded-full blur-3xl" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
            {/* Left copy */}
            <div className={`flex-1 text-center lg:text-left transition-all duration-700 ${heroVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              <div className="inline-flex items-center gap-2 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 text-xs font-semibold px-3 py-1.5 rounded-full mb-6 border border-primary-200 dark:border-primary-800">
                <Zap className="w-3.5 h-3.5" />
                AI-Powered Healthcare Platform
              </div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display font-black text-neutral-900 dark:text-white leading-[1.1] mb-6">
                Your Health,
                <br />
                <span className="bg-gradient-to-r from-primary-500 via-violet-500 to-cyan-500 bg-clip-text text-transparent">
                  Intelligently
                </span>{' '}
                Managed
              </h1>
              <p className="text-lg text-neutral-500 dark:text-neutral-400 mb-8 max-w-xl mx-auto lg:mx-0 leading-relaxed">
                MediNova AI connects patients, doctors, and administrators through intelligent automation — from booking appointments to analyzing health records with advanced AI agents.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center gap-2 bg-primary-500 hover:bg-primary-600 text-white font-semibold px-6 py-3.5 rounded-xl transition-all shadow-xl shadow-primary-500/30 hover:shadow-primary-500/50 hover:-translate-y-0.5"
                >
                  Start for Free <ArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center gap-2 bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 text-neutral-700 dark:text-neutral-300 font-semibold px-6 py-3.5 rounded-xl transition-all"
                >
                  Sign In <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              <div className="flex items-center gap-6 mt-8 justify-center lg:justify-start">
                <div className="flex -space-x-2">
                  {['from-rose-400 to-pink-500', 'from-blue-400 to-cyan-500', 'from-emerald-400 to-teal-500', 'from-violet-400 to-purple-500'].map((g, i) => (
                    <div key={i} className={`w-8 h-8 rounded-full bg-gradient-to-br ${g} border-2 border-white dark:border-neutral-900`} />
                  ))}
                </div>
                <div className="text-sm text-neutral-500 dark:text-neutral-400">
                  <span className="font-bold text-neutral-900 dark:text-white">50,000+</span> patients trust MediNova
                </div>
              </div>
            </div>

            {/* Right dashboard preview */}
            <div className={`flex-1 w-full max-w-lg lg:max-w-none transition-all duration-700 delay-200 ${heroVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'}`}>
              <div className="relative">
                {/* Floating cards */}
                <div className="absolute -top-4 -left-4 z-20 bg-white dark:bg-neutral-800 rounded-2xl p-3 shadow-xl border border-neutral-200 dark:border-neutral-700 animate-bounce-slow hidden sm:block">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-emerald-100 flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-neutral-800 dark:text-white">Appointment Confirmed</p>
                      <p className="text-xs text-neutral-400">Dr. Sharma · 2:00 PM</p>
                    </div>
                  </div>
                </div>

                <div className="absolute -bottom-4 -right-4 z-20 bg-white dark:bg-neutral-800 rounded-2xl p-3 shadow-xl border border-neutral-200 dark:border-neutral-700 hidden sm:block">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-rose-100 flex items-center justify-center">
                      <HeartPulse className="w-4 h-4 text-rose-600" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-neutral-800 dark:text-white">Heart Rate</p>
                      <p className="text-xs text-neutral-400">72 bpm · Normal</p>
                    </div>
                  </div>
                </div>

                {/* Main dashboard preview card */}
                <div className="bg-white dark:bg-neutral-800 rounded-3xl shadow-2xl border border-neutral-200 dark:border-neutral-700 overflow-hidden">
                  {/* Mock header */}
                  <div className="bg-gradient-to-r from-primary-600 to-cyan-500 p-5 text-white">
                    <p className="text-primary-100 text-xs mb-1">Good morning,</p>
                    <p className="font-bold text-lg">Priya Sharma 👋</p>
                    <p className="text-primary-100 text-xs mt-0.5">Here's your health summary for today.</p>
                  </div>
                  {/* Mock stats */}
                  <div className="p-4 grid grid-cols-2 gap-3">
                    {[
                      { label: 'Upcoming Appts', value: '3', color: 'bg-blue-500', icon: CalendarDays },
                      { label: 'Medications', value: '5', color: 'bg-violet-500', icon: Pill },
                      { label: 'Health Records', value: '12', color: 'bg-emerald-500', icon: Activity },
                      { label: 'Notifications', value: '2', color: 'bg-amber-500', icon: Brain },
                    ].map(item => (
                      <div key={item.label} className="bg-neutral-50 dark:bg-neutral-700/50 rounded-xl p-3 flex items-center gap-3">
                        <div className={`w-8 h-8 ${item.color} rounded-lg flex items-center justify-center`}>
                          <item.icon className="w-4 h-4 text-white" />
                        </div>
                        <div>
                          <p className="font-bold text-neutral-900 dark:text-white text-sm">{item.value}</p>
                          <p className="text-xs text-neutral-400">{item.label}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  {/* Mock appointment */}
                  <div className="px-4 pb-4">
                    <div className="bg-neutral-50 dark:bg-neutral-700/50 rounded-xl p-3 flex items-center gap-3">
                      <div className="w-10 h-10 bg-primary-100 rounded-xl flex flex-col items-center justify-center flex-shrink-0">
                        <span className="text-xs font-bold text-primary-700">Jul</span>
                        <span className="text-sm font-black text-primary-600">22</span>
                      </div>
                      <div className="flex-grow">
                        <p className="font-semibold text-sm text-neutral-900 dark:text-white">Dr. Rahul Mehta</p>
                        <p className="text-xs text-neutral-400">Cardiologist · 3:00 PM · Video</p>
                      </div>
                      <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-lg font-medium">Confirmed</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Stats section ────────────────────────────────────────────── */}
      <section className="py-16 bg-neutral-950 dark:bg-neutral-950">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <StatItem value={50000} suffix="+" label="Patients Served" color="text-primary-400" />
            <StatItem value={1200} suffix="+" label="Verified Doctors" color="text-violet-400" />
            <StatItem value={98} suffix="%" label="Satisfaction Rate" color="text-emerald-400" />
            <StatItem value={24} suffix="/7" label="AI Support" color="text-amber-400" />
          </div>
        </div>
      </section>

      {/* ─── Features section ─────────────────────────────────────────── */}
      <section id="features" className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <div className="inline-flex items-center gap-2 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 text-xs font-semibold px-3 py-1.5 rounded-full mb-4 border border-primary-200 dark:border-primary-800">
              Platform Features
            </div>
            <h2 className="text-3xl lg:text-4xl font-display font-black text-neutral-900 dark:text-white mb-4">
              Everything you need for <br className="hidden sm:block" />
              <span className="text-primary-500">smarter healthcare</span>
            </h2>
            <p className="text-neutral-500 dark:text-neutral-400 max-w-xl mx-auto">
              MediNova AI brings together cutting-edge technology and compassionate care in a single unified platform.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((f) => (
              <FeatureCard key={f.title} {...f} />
            ))}
          </div>
        </div>
      </section>

      {/* ─── How it works ─────────────────────────────────────────────── */}
      <section id="how-it-works" className="py-20 lg:py-28 bg-white dark:bg-neutral-900">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-violet-50 dark:bg-violet-900/20 text-violet-600 dark:text-violet-400 text-xs font-semibold px-3 py-1.5 rounded-full mb-6 border border-violet-200 dark:border-violet-800">
                How It Works
              </div>
              <h2 className="text-3xl lg:text-4xl font-display font-black text-neutral-900 dark:text-white mb-8">
                Get started in <span className="text-violet-500">3 simple steps</span>
              </h2>
              <div className="space-y-8">
                <Step
                  number="1"
                  title="Create Your Account"
                  description="Register as a patient or doctor in minutes. Our AI-guided onboarding captures your health profile for personalized recommendations."
                  icon={Users}
                />
                <Step
                  number="2"
                  title="Connect with Specialists"
                  description="Browse verified doctors by specialization, location, and availability. Book video or in-person consultations instantly."
                  icon={Stethoscope}
                />
                <Step
                  number="3"
                  title="Manage Your Health"
                  description="Track medications, store records, get AI-powered insights, and monitor your health journey from a single dashboard."
                  icon={Activity}
                />
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 to-violet-500/20 rounded-3xl blur-2xl" />
              <div className="relative bg-white dark:bg-neutral-800 rounded-3xl p-8 border border-neutral-200 dark:border-neutral-700 shadow-2xl">
                <div className="space-y-4">
                  {[
                    { label: 'Account Setup', time: '2 min', done: true, color: 'bg-emerald-500' },
                    { label: 'Profile Verification', time: '5 min', done: true, color: 'bg-emerald-500' },
                    { label: 'Find a Doctor', time: 'Instant', done: true, color: 'bg-emerald-500' },
                    { label: 'Book Appointment', time: '1 click', done: false, color: 'bg-primary-500' },
                    { label: 'AI Health Insights', time: 'Always on', done: false, color: 'bg-violet-500' },
                  ].map(step => (
                    <div key={step.label} className="flex items-center gap-4 p-3 rounded-xl bg-neutral-50 dark:bg-neutral-700/50">
                      <div className={`w-3 h-3 rounded-full ${step.color} flex-shrink-0 ${!step.done ? 'ring-2 ring-offset-2 ring-primary-300 dark:ring-primary-700' : ''}`} />
                      <span className="flex-grow text-sm font-medium text-neutral-700 dark:text-neutral-300">{step.label}</span>
                      <span className="text-xs text-neutral-400 bg-neutral-200 dark:bg-neutral-600 px-2 py-0.5 rounded-md">{step.time}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-6 p-4 bg-gradient-to-r from-primary-50 to-violet-50 dark:from-primary-900/20 dark:to-violet-900/20 rounded-xl border border-primary-100 dark:border-primary-800">
                  <p className="text-sm font-semibold text-primary-700 dark:text-primary-300 flex items-center gap-2">
                    <Zap className="w-4 h-4" /> Average setup time: under 10 minutes
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Testimonials ─────────────────────────────────────────────── */}
      <section id="testimonials" className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <h2 className="text-3xl lg:text-4xl font-display font-black text-neutral-900 dark:text-white mb-4">
              Loved by <span className="text-primary-500">patients & doctors</span>
            </h2>
            <p className="text-neutral-500 dark:text-neutral-400">Real experiences from our community</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map(t => <TestimonialCard key={t.name} {...t} />)}
          </div>
        </div>
      </section>

      {/* ─── CTA section ──────────────────────────────────────────────── */}
      <section className="py-20 lg:py-28 bg-gradient-to-br from-primary-600 via-primary-500 to-violet-600 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full -translate-y-32 translate-x-32 blur-xl" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-white/5 rounded-full translate-y-16 -translate-x-16 blur-xl" />
        </div>
        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-5xl font-display font-black text-white mb-6">
            Start your health journey today
          </h2>
          <p className="text-primary-100 text-lg mb-8 max-w-xl mx-auto">
            Join over 50,000 patients and 1,200 doctors already using MediNova AI for smarter healthcare.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="inline-flex items-center justify-center gap-2 bg-white text-primary-600 font-bold px-8 py-4 rounded-xl hover:bg-primary-50 transition-all shadow-xl hover:-translate-y-0.5"
            >
              Create Free Account <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center justify-center gap-2 bg-white/20 text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/30 transition-all border border-white/30"
            >
              Sign In
            </Link>
          </div>
          <div className="flex items-center justify-center gap-6 mt-8 text-primary-100 text-sm">
            <span className="flex items-center gap-1.5"><CheckCircle className="w-4 h-4" /> No credit card required</span>
            <span className="flex items-center gap-1.5"><Lock className="w-4 h-4" /> HIPAA compliant</span>
            <span className="flex items-center gap-1.5"><Globe className="w-4 h-4" /> Available 24/7</span>
          </div>
        </div>
      </section>

      {/* ─── Footer ───────────────────────────────────────────────────── */}
      <footer className="bg-neutral-950 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 bg-primary-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-black text-base">M</span>
              </div>
              <span className="text-base font-display font-bold text-white">
                MediNova <span className="text-primary-400">AI</span>
              </span>
            </div>
            <p className="text-neutral-500 text-sm">
              © 2026 MediNova AI. All rights reserved. Built with ❤️ for better healthcare.
            </p>
            <div className="flex items-center gap-6 text-sm text-neutral-500">
              <a href="#" className="hover:text-neutral-300 transition-colors">Privacy</a>
              <a href="#" className="hover:text-neutral-300 transition-colors">Terms</a>
              <a href="#" className="hover:text-neutral-300 transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>

      {/* Slow bounce animation style */}
      <style>{`
        @keyframes bounce-slow {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-8px); }
        }
        .animate-bounce-slow {
          animation: bounce-slow 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};

export default Home;
