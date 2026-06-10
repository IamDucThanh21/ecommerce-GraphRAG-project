/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Star, Heart } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  key?: string | number;
  product: Product;
  onClick: (id: string, categoryId?: string) => void;
}

export default function ProductCard({ product, onClick }: ProductCardProps) {
  return (
    <div 
      className="bg-white rounded-2xl p-4 shadow-[0_10px_30px_-15px_rgba(51,51,51,0.04)] relative group hover:-translate-y-1 transition-all duration-300 border border-transparent hover:border-zinc-100 cursor-pointer"
      onClick={() => onClick(product.id, product.categoryId)}
    >
      <div className="absolute top-2 left-2 flex flex-col gap-1 z-10">
        {product.badges?.map((badge, idx) => (
          <span 
            key={idx}
            className={`text-[10px] px-2 py-1 rounded font-bold uppercase ${
              badge.includes('-') ? 'bg-[#ba1a1a] text-white' : 'bg-blue-600 text-white'
            }`}
          >
            {badge}
          </span>
        ))}
      </div>
      
      <div className="aspect-square bg-zinc-50 rounded-xl overflow-hidden mb-4 p-4 relative">
        <img 
          className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-500 mix-blend-multiply" 
          src={product.image || null} 
          alt={product.name}
          onError={(e) => {
            e.currentTarget.src =
              '/placeholder-product.png';
          }}
        />
        <button className="absolute top-2 right-2 p-2 rounded-full bg-white/80 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity">
          <Heart className="w-4 h-4 text-zinc-400 hover:text-[#ba1a1a]" />
        </button>
      </div>

      <h3 className="font-bold text-sm mb-2 line-clamp-2 h-10 text-zinc-900 group-hover:text-zinc-600">
        {product.name}
      </h3>
      
      <div className="flex items-center gap-1 mb-2">
        <div className="flex text-[#FFD700]">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className={`w-3 h-3 ${i < Math.floor(product.rating) ? 'fill-current' : 'text-zinc-200'}`} />
          ))}
        </div>
        <span className="text-xs text-zinc-400">({product.reviewsCount})</span>
      </div>

      <div className="mb-4">
        <span className="text-[#ba1a1a] font-bold text-lg">
          {product.price.toLocaleString('vi-VN')}₫
        </span>
        {product.originalPrice && (
          <span className="text-zinc-400 text-xs line-through ml-2">
            {product.originalPrice.toLocaleString('vi-VN')}₫
          </span>
        )}
      </div>

      <button className="w-full py-2 bg-zinc-50 text-zinc-900 rounded-lg font-bold text-xs hover:bg-[#FFD194] transition-colors">
        Mua ngay
      </button>
    </div>
  );
}
