/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Mail, Lock, User, Github, Chrome, ArrowRight } from 'lucide-react';
import { Page } from '../types';

interface AuthPageProps {
  setPage: (page: Page) => void;
}

export default function AuthPage({ setPage }: AuthPageProps) {
  const [isLogin, setIsLogin] = useState(true);

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

        <div className="space-y-4">
          <button className="w-full h-12 flex items-center justify-center gap-3 border border-zinc-200 rounded-xl hover:bg-zinc-50 transition-all font-bold text-sm text-zinc-700">
            <Chrome className="w-5 h-5" /> Đăng nhập với Google
          </button>
          <button className="w-full h-12 flex items-center justify-center gap-3 border border-zinc-200 rounded-xl hover:bg-zinc-50 transition-all font-bold text-sm text-zinc-700">
            <Github className="w-5 h-5" /> Đăng nhập với Github
          </button>
        </div>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-zinc-100"></div>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white px-4 text-zinc-400 font-bold tracking-widest">Hoặc sử dụng Email</span>
          </div>
        </div>

        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          {!isLogin && (
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
              <input 
                className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
                placeholder="Họ và tên"
                type="text"
              />
            </div>
          )}
          <div className="relative">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
            <input 
              className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
              placeholder="Địa chỉ Email"
              type="email"
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" />
            <input 
              className="w-full h-12 pl-12 pr-4 rounded-xl border border-zinc-200 focus:border-zinc-900 focus:ring-1 focus:ring-zinc-900 outline-none transition-all text-sm"
              placeholder="Mật khẩu"
              type="password"
            />
          </div>

          {isLogin && (
            <div className="flex justify-end">
              <button className="text-xs font-bold text-zinc-400 hover:text-zinc-900 transition-all">Quên mật khẩu?</button>
            </div>
          )}

          <button 
            className="w-full h-12 bg-zinc-900 text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-zinc-800 transition-all active:scale-95 mt-6"
            onClick={() => setPage('home')}
          >
            {isLogin ? 'Đăng nhập' : 'Đăng ký'} <ArrowRight className="w-4 h-4" />
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
