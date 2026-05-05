/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Star, ShieldCheck, Truck, RotateCcw, Heart, Share2, ChevronRight, ChevronDown, ChevronUp, Maximize2, MessageSquare } from 'lucide-react';
import { PRODUCTS } from '../data';
import { Page } from '../types';
import ProductCard from '../components/ProductCard';

interface DetailPageProps {
  productId: string;
  setPage: (page: Page) => void;
}

export default function DetailPage({ productId, setPage }: DetailPageProps) {
  const product = PRODUCTS.find((p) => p.id === productId) || PRODUCTS[0];
  const [showAllSpecs, setShowAllSpecs] = useState(false);
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);

  const fullSpecs = [
    { label: 'Màn hình', value: '6.1 inch, LTPO Super Retina XDR OLED, 120Hz' },
    { label: 'Chipset', value: 'Apple A17 Pro (3 nm)' },
    { label: 'CPU', value: 'Hexa-core (2x3.78 GHz + 4x2.11 GHz)' },
    { label: 'GPU', value: 'Apple GPU (6-core graphics)' },
    { label: 'Camera sau', value: '48MP (Chính) + 12MP (Tele) + 12MP (Ultra wide)' },
    { label: 'Camera trước', value: '12MP, f/1.9, 23mm (wide)' },
    { label: 'RAM', value: '8GB' },
    { label: 'Pin', value: 'Li-Ion 3274 mAh, Sạc 50% trong 30p' },
    { label: 'Hệ điều hành', value: 'iOS 17' },
    { label: 'Khối lượng', value: '187 g (6.60 oz)' },
    { label: 'SIM', value: 'Nano-SIM và eSIM' },
    { label: 'Cổng sạc', value: 'USB Type-C 3.0' },
    { label: 'Kháng nước', value: 'IP68 (độ sâu 6m trong 30p)' }
  ];

  const displayedSpecs = showAllSpecs ? fullSpecs : fullSpecs.slice(0, 10);

  const reviews = [
    { 
      id: 1, 
      user: 'Hoàng Anh', 
      rating: 5, 
      date: '2 ngày trước', 
      comment: 'Máy rất mượt, camera chụp đêm xuất sắc. Rất hài lòng với dịch vụ của WiseTech.',
      replies: [
        { id: 101, user: 'Admin WiseTech', date: '1 ngày trước', comment: 'Cảm ơn bạn đã tin tưởng ủng hộ WiseTech ạ! Chúc bạn có trải nghiệm tuyệt vời với iPhone 15 Pro.' }
      ]
    },
    { 
      id: 2, 
      user: 'Minh Tuấn', 
      rating: 4, 
      date: '1 tuần trước', 
      comment: 'Hiệu năng tốt nhưng pin dùng bình thường. Thiết kế titan nhẹ hơn hẳn các đời trước.',
      replies: []
    }
  ];

  return (
    <div className="space-y-16">
      {/* Spec Popup Modal */}
      {showAllSpecs && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-zinc-900/60 backdrop-blur-sm" onClick={() => setShowAllSpecs(false)}></div>
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden relative z-10 flex flex-col">
            <div className="p-8 border-b border-zinc-100 flex justify-between items-center">
              <h2 className="text-xl font-black uppercase tracking-widest text-zinc-900">Chi tiết thông số kỹ thuật</h2>
              <button 
                onClick={() => setShowAllSpecs(false)}
                className="w-10 h-10 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-500 hover:text-zinc-900 transition-colors"
              >
                <ChevronDown className="w-6 h-6 rotate-180" />
              </button>
            </div>
            <div className="p-8 overflow-y-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                {fullSpecs.map((spec, idx) => (
                  <div key={idx} className="flex flex-col gap-1 pb-4 border-b border-zinc-50 group hover:border-zinc-900 transition-colors">
                    <span className="text-[10px] font-black text-zinc-400 uppercase tracking-widest">{spec.label}</span>
                    <span className="text-sm font-bold text-zinc-900">{spec.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      {/* Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs font-semibold text-zinc-400">
        <button onClick={() => setPage('home')} className="hover:text-zinc-900 uppercase tracking-wider">Home</button>
        <ChevronRight className="w-3 h-3" />
        <button onClick={() => setPage('listing')} className="hover:text-zinc-900 uppercase tracking-wider">{product.category}</button>
        <ChevronRight className="w-3 h-3" />
        <span className="text-zinc-900 uppercase tracking-wider truncate max-w-[200px]">{product.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Left: Gallery */}
        <div className="lg:col-span-7 space-y-6">
          <div className="aspect-[4/3] rounded-3xl bg-zinc-50 border border-zinc-100 flex items-center justify-center p-12 overflow-hidden group">
            <img 
              className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-700 mix-blend-multiply" 
              src={product.image} 
              alt={product.name} 
            />
          </div>
          <div className="grid grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className={`aspect-square rounded-2xl bg-zinc-50 border cursor-pointer hover:border-[#FFD194] transition-all flex items-center justify-center overflow-hidden p-2 ${i === 0 ? 'border-zinc-900' : 'border-zinc-100'}`}>
                <img className="w-full h-full object-contain mix-blend-multiply" src={product.image} alt={product.name} />
              </div>
            ))}
          </div>
        </div>

        {/* Right: Info & Purchase */}
        <div className="lg:col-span-5 space-y-8">
          <div>
            <div className="flex items-center gap-4 mb-3">
              <span className="text-[#ba1a1a] font-black text-xs uppercase tracking-[0.2em]">New Arrival</span>
              <div className="flex items-center gap-1 text-[#FFD700]">
                <Star className="w-4 h-4 fill-current" />
                <span className="text-zinc-900 font-bold text-sm">{product.rating}</span>
                <span className="text-zinc-400 font-medium text-sm">({product.reviewsCount} reviews)</span>
              </div>
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">{product.name}</h1>
            <div className="flex items-end gap-3 mb-6">
              <span className="text-3xl font-black text-zinc-900">{product.price.toLocaleString('vi-VN')}₫</span>
              {product.originalPrice && (
                <span className="text-zinc-400 text-lg line-through pb-1">{product.originalPrice.toLocaleString('vi-VN')}₫</span>
              )}
            </div>
          </div>

          {/* Configuration Options */}
          <div className="space-y-6">
            <div>
              <h4 className="font-bold text-xs uppercase tracking-widest text-zinc-400 mb-3">Chọn màu sắc</h4>
              <div className="flex gap-3">
                {['#444748', '#dcdad6', '#fdd093', '#2b3031'].map((color, idx) => (
                  <button 
                    key={idx}
                    style={{ backgroundColor: color }}
                    className={`w-10 h-10 rounded-full border-2 transition-all ${idx === 0 ? 'border-zinc-900 ring-2 ring-zinc-900/10 ring-offset-2' : 'border-transparent'}`}
                  />
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-bold text-xs uppercase tracking-widest text-zinc-400 mb-3">Dung lượng</h4>
              <div className="flex gap-3">
                {['128GB', '256GB', '512GB', '1TB'].map((storage, idx) => (
                  <button 
                    key={idx}
                    className={`px-4 py-2 border-2 rounded-xl text-sm font-bold transition-all ${idx === 0 ? 'border-zinc-900 bg-zinc-900 text-white' : 'border-zinc-100 hover:border-zinc-900'}`}
                  >
                    {storage}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex gap-4 pt-4">
            <button className="flex-1 h-14 bg-zinc-900 text-white rounded-xl font-bold text-base hover:bg-zinc-800 transition-all active:scale-95 shadow-xl shadow-zinc-900/10">
              Thêm vào giỏ hàng
            </button>
            <button className="w-14 h-14 border-2 border-zinc-200 flex items-center justify-center rounded-xl hover:bg-zinc-50 transition-all text-zinc-600">
              <Heart className="w-6 h-6" />
            </button>
            <button className="w-14 h-14 border-2 border-zinc-200 flex items-center justify-center rounded-xl hover:bg-zinc-50 transition-all text-zinc-600">
              <Share2 className="w-6 h-6" />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4 pt-8 border-t border-zinc-100">
            {[
              { icon: <Truck className="w-5 h-5 text-zinc-400" />, text: 'Giao hàng miễn phí' },
              { icon: <ShieldCheck className="w-5 h-5 text-zinc-400" />, text: 'Bảo hành 12 tháng' },
            ].map((feature, idx) => (
              <div key={idx} className="flex items-center gap-3">
                {feature.icon}
                <span className="text-xs font-bold text-zinc-700">{feature.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Description & Specs Side-by-Side Area */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 pt-8">
        {/* Description Section */}
        <section className="lg:col-span-7 space-y-6">
          <h2 className="text-xl font-black uppercase tracking-widest text-zinc-900 mb-6 flex items-center gap-3">
            Mô tả sản phẩm
          </h2>
          <div className={`relative ${!isDescriptionExpanded ? 'max-h-[600px] overflow-hidden' : ''}`}>
            <div className="prose prose-zinc max-w-none text-zinc-600 leading-relaxed space-y-6 font-['Inter']">
              <p>
                {product.description || 'iPhone 15 Pro là chiếc iPhone đầu tiên sở hữu thiết kế cấp độ hàng không vũ trụ, sử dụng cùng loại hợp kim được dùng cho tàu vũ trụ thực hiện các sứ mệnh lên Sao Hỏa.'}
              </p>
              <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCHr9oP0v_V2K_o-W_O-D8F_d-yW6h-D-9-5-B-1-W-9-5-B-1-W-9-5-B-k-7-8-9" alt="Design" className="w-full rounded-3xl" />
              <p>
                Titan có tỷ lệ sức bền trên trọng lượng tốt nhất trong số các loại kim loại, tạo nên những mẫu máy Pro nhẹ nhất từ trước đến nay của chúng tôi. Bạn sẽ nhận ra sự khác biệt ngay khi cầm máy lên.
              </p>
              <h3 className="text-xl font-bold text-zinc-900 mt-8">Chip A17 Pro. Bước tiến khổng lồ về hiệu năng.</h3>
              <p>
                Đây là con chip hoàn toàn mới, mang lại khả năng đồ họa tốt nhất từ trước đến nay trên iPhone. Trải nghiệm chơi game di động sẽ chân thực và sống động hơn bao giờ hết, với môi trường chi tiết và các nhân vật thực tế hơn.
              </p>
            </div>
            {!isDescriptionExpanded && (
              <div className="absolute bottom-0 left-0 w-full h-40 bg-gradient-to-t from-white to-transparent flex items-end justify-center pb-4">
                <button 
                  onClick={() => setIsDescriptionExpanded(true)}
                  className="px-6 py-2 bg-white border border-zinc-200 rounded-full font-bold text-sm shadow-lg hover:bg-zinc-50 flex items-center gap-2"
                >
                  Xem thêm <ChevronDown className="w-4 h-4" />
                </button>
              </div>
            )}
            {isDescriptionExpanded && (
              <div className="flex justify-center mt-6">
                <button 
                  onClick={() => setIsDescriptionExpanded(false)}
                  className="px-6 py-2 bg-white border border-zinc-200 rounded-full font-bold text-sm hover:bg-zinc-50 flex items-center gap-2"
                >
                  Thu gọn <ChevronUp className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Specs Table Section */}
        <aside className="lg:col-span-5">
          <div className="bg-zinc-50 rounded-3xl p-8 sticky top-24 border border-zinc-100">
            <h2 className="text-lg font-black uppercase tracking-widest text-zinc-900 mb-8 pb-4 border-b border-zinc-200">
              Thông số kỹ thuật
            </h2>
            <div className="space-y-4">
              {fullSpecs.slice(0, 10).map((spec, idx) => (
                <div key={idx} className="flex justify-between items-center py-3 border-b border-zinc-200 last:border-0 group">
                  <span className="text-[10px] font-black text-zinc-400 uppercase tracking-widest">{spec.label}</span>
                  <span className="text-xs font-bold text-zinc-900 text-right max-w-[200px]">{spec.value}</span>
                </div>
              ))}
            </div>
            <button 
              onClick={() => setShowAllSpecs(true)}
              className="w-full mt-8 py-3 bg-white border border-zinc-200 rounded-xl font-bold text-xs uppercase tracking-widest text-zinc-900 hover:bg-zinc-100 transition-all flex items-center justify-center gap-2"
            >
              Xem thông số chi tiết <Maximize2 className="w-3 h-3" />
            </button>
          </div>
        </aside>
      </div>

      {/* Reviews Section - Instagram Style & Centered */}
      <section className="pt-20 border-t border-zinc-100 flex flex-col items-center">
        <div className="w-full max-w-2xl px-4 lg:px-0">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-black uppercase tracking-tighter text-zinc-900 flex items-center gap-3">
              Reviews <span className="text-zinc-300">({product.reviewsCount})</span>
            </h2>
          </div>

          {/* New Comment Input Area */}
          <div className="mb-12 p-6 bg-white border-2 border-zinc-100 rounded-[2rem] flex flex-col gap-4 shadow-xl shadow-zinc-900/5 group focus-within:border-zinc-900 transition-all">
            <div className="flex gap-4 items-center mb-2">
              <div className="w-8 h-8 rounded-full bg-zinc-100 flex items-center justify-center font-bold text-zinc-400 text-xs uppercase">You</div>
              <span className="text-xs font-black uppercase tracking-widest text-zinc-400">Share your thoughts...</span>
            </div>
            <textarea 
              className="w-full bg-transparent border-none outline-none text-sm font-medium text-zinc-800 placeholder:text-zinc-300 resize-none h-24"
              placeholder="What do you think about this product?"
            />
            <div className="flex justify-between items-center pt-2 border-t border-zinc-50">
              <div className="flex gap-2">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 text-zinc-200 hover:text-yellow-400 cursor-pointer transition-colors" />
                ))}
              </div>
              <button className="px-6 py-2 bg-zinc-900 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-zinc-800 transition-all active:scale-95">
                Post Comment
              </button>
            </div>
          </div>

          <div className="space-y-12">
            {reviews.map((rev) => (
            <div key={rev.id} className="space-y-4">
              {/* Instagram Style Comment Header */}
              <div className="flex gap-4 group">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-yellow-400 to-red-500 p-[2px] shrink-0">
                  <div className="w-full h-full rounded-full bg-white p-[2px]">
                    <div className="w-full h-full rounded-full bg-zinc-200 flex items-center justify-center font-bold text-zinc-600 text-sm overflow-hidden">
                      {rev.user.charAt(0)}
                    </div>
                  </div>
                </div>
                <div className="flex-1 pt-1">
                  <div className="flex flex-wrap items-baseline gap-2 mb-1">
                    <span className="font-bold text-zinc-900 text-sm hover:underline cursor-pointer">
                      {rev.user.toLowerCase().replace(' ', '_')}
                    </span>
                    <p className="text-sm text-zinc-700 leading-snug">
                      {rev.comment}
                    </p>
                  </div>
                  <div className="flex items-center gap-4 text-[11px] font-bold text-zinc-400 uppercase tracking-wider">
                    <span>{rev.date}</span>
                    <button className="hover:text-zinc-900 transition-colors">Reply</button>
                    <div className="flex gap-1 text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className={`w-2.5 h-2.5 ${i < rev.rating ? 'fill-current' : 'text-zinc-200'}`} />
                      ))}
                    </div>
                  </div>
                </div>
                <button className="pt-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Heart className="w-3 h-3 text-zinc-300 hover:text-red-500" />
                </button>
              </div>

              {/* Replies Section */}
              {rev.replies.length > 0 && (
                <div className="pl-14 pt-2">
                  <button className="flex items-center gap-3 text-[11px] font-bold text-zinc-400 hover:text-zinc-900 transition-colors uppercase tracking-widest mb-4">
                    <div className="w-6 h-[1px] bg-zinc-200"></div>
                    View {rev.replies.length} reply
                  </button>
                  <div className="space-y-4">
                    {rev.replies.map((reply) => (
                      <div key={reply.id} className="flex gap-3 group">
                        <div className="w-6 h-6 rounded-full bg-zinc-900 flex items-center justify-center font-black text-white text-[8px] shrink-0">
                          W
                        </div>
                        <div className="flex-1">
                          <div className="flex flex-wrap items-baseline gap-2 mb-1">
                            <span className="font-bold text-zinc-900 text-xs">
                              {reply.user.toLowerCase().replace(' ', '_')}
                            </span>
                            <p className="text-xs text-zinc-500 leading-snug">
                              {reply.comment}
                            </p>
                          </div>
                          <div className="flex items-center gap-3 text-[9px] font-bold text-zinc-400 uppercase tracking-wider">
                            <span>{reply.date}</span>
                            <button className="hover:text-zinc-900 transition-colors">Reply</button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>

      {/* Related Products */}
      <section className="pb-20">
        <h2 className="text-2xl font-black uppercase tracking-tighter text-zinc-900 mb-10">Bạn có thể cũng sẽ thích</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {PRODUCTS.filter(p => p.id !== product.id).slice(0, 5).map((p) => (
            <ProductCard 
              key={p.id} 
              product={p} 
              onClick={(id) => {
                setPage('detail');
                // Scroll handle by App.tsx
              }} 
            />
          ))}
        </div>
      </section>
    </div>
  );
}
