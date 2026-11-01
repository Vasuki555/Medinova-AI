/**
 * Footer Component
 * Global footer
 */

import { APP_NAME, APP_VERSION } from '@/utils/constants';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-neutral-900 text-neutral-300 py-12 mt-auto">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">M</span>
              </div>
              <span className="text-xl font-display font-bold text-white">
                {APP_NAME}
              </span>
            </div>
            <p className="text-neutral-400 max-w-md">
              Multi-Agent Healthcare Intelligence Platform powered by AI.
              Making healthcare accessible, intelligent, and efficient.
            </p>
            <p className="text-sm text-neutral-500 mt-4">
              Version {APP_VERSION}
            </p>
          </div>

          {/* Links - Will be expanded in future modules */}
          <div>
            <h3 className="text-white font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-primary-400 transition-colors">
                  Features
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary-400 transition-colors">
                  Pricing
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-primary-400 transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary-400 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-neutral-800 mt-8 pt-8 text-center">
          <p className="text-neutral-500 text-sm">
            © {currentYear} {APP_NAME}. Final Year Engineering Project.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
