/**
 * Header Component
 * Global navigation header
 */

import { Link } from 'react-router-dom';
import { APP_NAME } from '@/utils/constants';

const Header = () => {
  return (
    <header className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">M</span>
            </div>
            <span className="text-xl font-display font-bold text-neutral-900">
              {APP_NAME}
            </span>
          </Link>

          {/* Navigation - Will be expanded in future modules */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className="text-neutral-600 hover:text-primary-500 transition-colors font-medium"
            >
              Home
            </Link>
          </nav>

          {/* Right side buttons - Will be expanded in future modules */}
          <div className="flex items-center space-x-4">
            <button className="btn-secondary py-2 px-4 text-sm">
              Sign In
            </button>
            <button className="btn-primary py-2 px-4 text-sm">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
