/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import ListingPage from './pages/ListingPage';
import DetailPage from './pages/DetailPage';
import AuthPage from './pages/AuthPage';
import ChatWidget from './components/ChatWidget';
import { Page } from './types';
import { AuthProvider } from './contexts/AuthContext';

function AppContent() {
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [selectedProductId, setSelectedProductId] = useState<string>('');
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>('');
  const [selectedBrandId, setSelectedBrandId] = useState<string | null>(null);

  // Scroll to top on page change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [currentPage]);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <HomePage
            setPage={setCurrentPage}
            setProductId={setSelectedProductId}
            setCategoryId={setSelectedCategoryId}
            setBrandId={setSelectedBrandId}
          />
        );
      case 'listing':
        return (
          <ListingPage
            setPage={setCurrentPage}
            setProductId={setSelectedProductId}
            setCategoryId={setSelectedCategoryId}
            categoryId={selectedCategoryId}
            brandId={selectedBrandId}
            setBrandId={setSelectedBrandId}
          />
        );
      case 'detail':
        return <DetailPage productId={selectedProductId} categoryId={selectedCategoryId} setPage={setCurrentPage} />;
      case 'auth':
        return <AuthPage setPage={setCurrentPage} />;
      default:
        return (
          <HomePage
            setPage={setCurrentPage}
            setProductId={setSelectedProductId}
            setCategoryId={setSelectedCategoryId}
            setBrandId={setSelectedBrandId}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-[#FCF9F5] text-zinc-900 selection:bg-[#FFD194] selection:text-zinc-900">
      <Navbar currentPage={currentPage} setPage={setCurrentPage} />
      
      <main className="max-w-[1440px] mx-auto px-6 pt-28 pb-20">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage + (currentPage === 'detail' ? selectedProductId : '')}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </main>

      <Footer />
      <ChatWidget />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
