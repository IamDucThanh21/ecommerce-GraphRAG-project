/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { Search, ShoppingCart, User, Menu, LogOut } from 'lucide-react';
import { Page } from '../types';
import logoImage from '../assets/images/w.png';
import { useAuth } from '../contexts/AuthContext';
import { apiClient, ProductVariant } from '../api/client';

// console.log('Navbar loaded');

interface NavbarProps {
  currentPage: Page;
  setPage: (page: Page) => void;
  setCategoryId: (id: string) => void;
  setSearchText: (text: string) => void;
}

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
}

export default function Navbar({ currentPage, setPage, setCategoryId, setSearchText }: NavbarProps) {
  const { user, isAuthenticated, logOut } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');

  const [categories, setCategories] =
    useState<Category[]>([]);

  const [loadingCategories, setLoadingCategories] =
    useState(false);
  
  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoadingCategories(true);

        const response = await apiClient.categoryList();
        const list = response.data ?? [];
        setCategories(list);
      } catch (error) {
        console.error('Failed to load categories:', error);
      } finally {
        setLoadingCategories(false);
      }
    };

    loadCategories();
  }, []);

  const handleLogout = async () => {
    await logOut();

    setShowUserMenu(false);
    setPage('home');
  };
  const navItems = [
    { label: 'Shop', id: 'home' },
    { label: 'Products', id: 'listing' },
    { label: 'Deals', id: 'listing' },
  ];

  const handleSearch = async () => {
    if (!searchKeyword.trim()) 
      {
        return;
      }

    setCategoryId('');
    setSearchText(searchKeyword.trim());
    setPage('listing');
  };

  return (
    <header className="fixed top-0 w-full z-50 border-b border-zinc-900/5 bg-[#FCF9F5]/80 backdrop-blur-xl transition-all h-20">
      <div className="max-w-[1440px] mx-auto flex justify-between items-center px-6 h-full gap-8">
        <button 
          onClick={() => setPage('home')}
          className="flex items-center gap-2 group transition-transform active:scale-95 shrink-0"
        >
          <img src={logoImage} alt="WiseTech Logo" className="w-12 h-12 rounded-lg" />
          <span className="text-2xl font-black tracking-tighter text-zinc-900">WiseTech</span>
        </button>
        
        <nav className="hidden lg:flex items-center gap-6 shrink-0 h-full">
          <div className="relative group/nav h-full flex items-center">
            <button
              onClick={() => setPage('home')}
              className={`font-semibold transition-colors font-['Inter'] text-sm uppercase tracking-wider flex items-center gap-1 ${
                currentPage === 'home' ? 'text-zinc-900' : 'text-zinc-500 hover:text-zinc-800'
              }`}
            >
              Categories
            </button>
            <div className="absolute top-full left-0 bg-white shadow-xl border border-zinc-100 rounded-xl py-4 min-w-[200px] opacity-0 translate-y-2 pointer-events-none group-hover/nav:opacity-100 group-hover/nav:translate-y-0 group-hover/nav:pointer-events-auto transition-all duration-200">
              {loadingCategories ? (
                <div className="px-6 py-2 text-sm text-zinc-400">
                  Loading...
                </div>
              ) : (
                categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => {
                      setSearchText('');
                      setCategoryId(category.id);

                      setPage('listing');
                    }}
                    className="w-full text-left px-6 py-2 text-sm text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50 transition-colors capitalize"
                  >
                    {category.name}
                  </button>
                ))
              )}
            </div>
            {currentPage === 'home' && <div className="absolute bottom-0 left-0 w-full h-1 bg-[#FFD194]"></div>}
          </div>
        </nav>

        <div className="flex-1 max-w-2xl relative group hidden md:block">
          <input
            value={searchKeyword}
            onChange={(e) =>
              setSearchKeyword(
                e.target.value
              )
            }
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSearch();
              }
            }}
            className="w-full h-11 px-5 rounded-xl border border-zinc-900/5 bg-white/50 focus:ring-4 focus:ring-[#FFD194]/30 focus:border-zinc-900/10 outline-none transition-all font-sans text-sm"
            placeholder="Search for premium tech..."
            type="text"
          />
          <button
            onClick={handleSearch}
            className="absolute right-4 top-1/2 -translate-y-1/2"
          >
            <Search className="text-zinc-400 hover:text-zinc-700 w-5 h-5" />
          </button>
        </div>

        <div className="flex items-center gap-2 md:gap-4 shrink-0">
          <button className="w-11 h-11 flex items-center justify-center rounded-lg hover:bg-zinc-900/5 active:scale-95 transition-all outline-none relative">
            <ShoppingCart className="w-6 h-6 text-zinc-800" />
            <span className="absolute top-2 right-2 w-4 h-4 bg-[#ba1a1a] text-white text-[10px] flex items-center justify-center rounded-full font-bold">3</span>
          </button>
          
          <div className="relative group/user">
            {isAuthenticated ? (
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="w-11 h-11 flex items-center justify-center rounded-lg hover:bg-zinc-900/5 active:scale-95 transition-all outline-none bg-zinc-900 text-white"
                title={user?.username}
              >
                <span className="text-sm font-bold">{user?.username?.[0]?.toUpperCase()}</span>
              </button>
            ) : (
              <button 
                onClick={() => setPage('auth')}
                className="w-11 h-11 flex items-center justify-center rounded-lg hover:bg-zinc-900/5 active:scale-95 transition-all outline-none"
              >
                <User className="w-6 h-6 text-zinc-800" />
              </button>
            )}

            {isAuthenticated && showUserMenu && (
              <div className="absolute top-full right-0 mt-2 bg-white shadow-xl border border-zinc-100 rounded-xl py-2 min-w-[200px] z-50">
                <div className="px-4 py-3 border-b border-zinc-100">
                  <p className="text-sm font-semibold text-zinc-900">{user?.username}</p>
                  {user?.email && <p className="text-xs text-zinc-500 mt-1">{user.email}</p>}
                </div>
                <button
                  onClick={() => {
                    setShowUserMenu(false);
                    setPage('home');
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-50 transition-colors"
                >
                  Profile
                </button>
                <button
                  onClick={() => {
                    setShowUserMenu(false);
                    setPage('home');
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-50 transition-colors"
                >
                  Orders
                </button>
                <div className="border-t border-zinc-100 mt-2 pt-2">
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>

          <button className="lg:hidden w-11 h-11 flex items-center justify-center rounded-lg hover:bg-zinc-900/5 active:scale-95 transition-all outline-none">
            <Menu className="w-6 h-6 text-zinc-800" />
          </button>
        </div>
      </div>
    </header>
  );
}
