/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Globe, Mail } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full py-12 px-6 border-t border-zinc-200 bg-zinc-50 font-['Inter']">
      <div className="max-w-[1440px] mx-auto flex flex-col md:flex-row justify-between items-start gap-12">
        <div className="max-w-sm">
          <h2 className="text-xl font-bold text-zinc-900 mb-4 tracking-tighter">WiseTech</h2>
          <p className="text-zinc-500 text-sm leading-relaxed mb-6">
            Precision engineered for the digital age. Your destination for high-end technology and premium lifestyle electronics.
          </p>
          <div className="flex gap-4">
            <button className="w-10 h-10 rounded-full bg-zinc-200 flex items-center justify-center hover:bg-[#FFD194] transition-all">
              <Globe className="w-5 h-5 text-zinc-600" />
            </button>
            <button className="w-10 h-10 rounded-full bg-zinc-200 flex items-center justify-center hover:bg-[#FFD194] transition-all">
              <Mail className="w-5 h-5 text-zinc-600" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-12 flex-1">
          <div className="flex flex-col gap-4">
            <h4 className="font-bold text-sm uppercase tracking-wider text-zinc-900">Về chúng tôi</h4>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Giới thiệu WiseTech</a>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Tuyển dụng</a>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Hệ thống cửa hàng</a>
          </div>
          <div className="flex flex-col gap-4">
            <h4 className="font-bold text-sm uppercase tracking-wider text-zinc-900">Hỗ trợ khách hàng</h4>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Chính sách bảo hành</a>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Đổi trả & Hoàn tiền</a>
            <a className="text-zinc-500 hover:underline decoration-[#FFD194] decoration-2 underline-offset-4 text-sm" href="#">Phương thức thanh toán</a>
          </div>
          <div className="flex flex-col gap-4">
            <h4 className="font-bold text-sm uppercase tracking-wider text-zinc-900">Liên hệ</h4>
            <p className="text-zinc-500 text-sm">Hotline: <span className="font-bold text-zinc-900">1800 6601</span></p>
            <p className="text-zinc-500 text-sm">Email: <span className="font-bold text-zinc-900">support@wisetech.vn</span></p>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-zinc-200 text-center">
        <p className="text-zinc-400 text-xs">© 2024 WiseTech. Precision engineered for the digital age.</p>
      </div>
    </footer>
  );
}
