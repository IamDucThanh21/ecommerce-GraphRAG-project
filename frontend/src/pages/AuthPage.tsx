/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Mail, Lock, User, Github, Chrome, ArrowRight, Loader } from 'lucide-react';
import { Page } from '../types';
import { useAuth } from '../contexts/AuthContext';

interface AuthPageProps {
  setPage: (page: Page) => void;
}

export default function AuthPage({ setPage }: AuthPageProps) {
  const [isLogin, setIsLogin] = useState(true);
  const { signIn, signUp, isLoading } = useAuth();
  const [error, setError] = useState<string>('');
  
  // Login form state
  const [loginData, setLoginData] = useState({
    username: '',
    password: '',
  });

  // Signup form state
  const [signupData, setSignupData] = useState({
    username: '',
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    phone: '',
  });

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await signIn(loginData.username, loginData.password);
      setPage('home');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed. Please try again.');
      console.error('Login error:', err);
    }
  };

  const handleSignupSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await signUp(
        signupData.username,
        signupData.email,
        signupData.password,
        signupData.firstName,
        signupData.lastName,
        signupData.phone
      );
      setPage('home');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign up failed. Please try again.');
      console.error('Signup error:', err);
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center font-['Inter']">
      <div className="w-full max-w-md p-8 bg-white rounded-3xl shadow-xl border border-zinc-100">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-black text-zinc-900 tracking-tighter mb-2">
            {isLogin ? 'Chào mừng trở lại' : 'Tạo tài khoản mới'}
          </h1>
          <p className="text-zinc-500 text-sm">
            {isLogin ? 'Đăng nhập vào WiseTech để tiếp tục' : 'Bắt đầu trải nghiệm công nghệ đỉnh cao'}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* <div className="space-y-4">
          <button className="w-full h-12 flex items-center justify-center gap-3 border border-zinc-200 rounded-xl hover:bg-zinc-50 transition-all font-bold text-sm text-zinc-700">
            <Chrome className="w-5 h-5" /> Đăng nhập với Google
          </button>
          <button className="w-full h-12 flex items-center justify-center gap-3 border border-zinc-200 rounded-xl hover:bg-zinc-50 transition-all font-bold text-sm text-zinc-700">
            <Github className="w-5 h-5" /> Đăng nhập với Github
          </button>
        </div> */}

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-zinc-100"></div>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white px-4 text-zinc-400 font-bold tracking-widest">Hoặc sử dụng Email</span>
          </div>
        </div>

        <form className="space-y-4" onSubmit={isLogin ? handleLoginSubmit : handleSignupSubmit}>
          {!isLogin && (
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
              <input 
                className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
                placeholder="Họ và tên"
                type="text"
                value={signupData.firstName}
                onChange={(e) => setSignupData({ ...signupData, firstName: e.target.value })}
              />
            </div>
          )}
          {!isLogin && (
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
              <input 
                className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
                placeholder="Username"
                type="text"
                required
                value={signupData.username}
                onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
              />
            </div>
          )}
          {!isLogin && (
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
              <input 
                className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
                placeholder="Địa chỉ Email"
                type="email"
                required
                value={signupData.email}
                onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
              />
            </div>
          )}
          {isLogin && (
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
              <input 
                className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
                placeholder="Username hoặc Email"
                type="text"
                required
                value={loginData.username}
                onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
              />
            </div>
          )}
          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
            <input 
              className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
              placeholder="Mật khẩu"
              type="password"
              required
              value={isLogin ? loginData.password : signupData.password}
              onChange={(e) => 
                isLogin 
                  ? setLoginData({ ...loginData, password: e.target.value })
                  : setSignupData({ ...signupData, password: e.target.value })
              }
            />
          </div>

          {isLogin && (
            <div className="flex justify-end">
              <button className="text-xs font-bold text-zinc-400 hover:text-zinc-900 transition-all">Quên mật khẩu?</button>
            </div>
          )}

          <button 
            type="submit"
            disabled={isLoading}
            className="w-full h-12 bg-zinc-900 text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-zinc-800 transition-all active:scale-95 mt-6 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                {isLogin ? 'Đang đăng nhập...' : 'Đang đăng ký...'}
              </>
            ) : (
              <>
                {isLogin ? 'Đăng nhập' : 'Đăng ký'} <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-sm text-zinc-500">
            {isLogin ? 'Bạn chưa có tài khoản?' : 'Bạn đã có tài khoản?'} {' '}
            <button 
              onClick={() => setIsLogin(!isLogin)}
              className="font-bold text-zinc-900 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4"
            >
              {isLogin ? 'Đăng ký ngay' : 'Đăng nhập ngay'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
