/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Filter, ChevronDown, LayoutGrid, List } from 'lucide-react';
import { PRODUCTS } from '../data';
import ProductCard from '../components/ProductCard';
import { Page } from '../types';

interface ListingPageProps {
  setPage: (page: Page) => void;
  setProductId: (id: string) => void;
}

export default function ListingPage({ setPage, setProductId }: ListingPageProps) {
  const handleProductClick = (id: string) => {
    setProductId(id);
    setPage('detail');
  };

  return (
    <div className="flex flex-col lg:flex-row gap-8">
      {/* Sidebar - Filter */}
      <aside className="w-full lg:w-64 space-y-8 h-fit lg:sticky lg:top-24">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-zinc-900" />
            <h3 className="font-bold uppercase tracking-wider text-sm">Filters</h3>
          </div>
          <div className="space-y-6">
            <div>
              <h4 className="font-bold text-xs uppercase text-zinc-400 mb-3 tracking-widest">Mức giá</h4>
              <div className="space-y-2">
                {['Dưới 2 triệu', 'Từ 2 - 4 triệu', 'Từ 4 - 7 triệu', 'Từ 7 - 13 triệu', 'Trên 13 triệu'].map((price) => (
                  <label key={price} className="flex items-center gap-2 cursor-pointer group">
                    <input type="radio" name="price" className="w-4 h-4 rounded-full border-zinc-200 text-[#ba1a1a] focus:ring-[#FFD194]" />
                    <span className="text-sm text-zinc-600 group-hover:text-zinc-900">{price}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-bold text-xs uppercase text-zinc-400 mb-3 tracking-widest">Tính năng đặc biệt</h4>
              <div className="space-y-2">
                {[
                  'Hỗ trợ 5G', 'Sạc siêu nhanh', 'Kháng nước, kháng bụi', 'Pin trâu trên 5000mAh'
                ].map((feature) => (
                  <label key={feature} className="flex items-center gap-2 cursor-pointer group">
                    <input type="checkbox" className="w-4 h-4 rounded border-zinc-200 text-[#ba1a1a] focus:ring-[#FFD194]" />
                    <span className="text-sm text-zinc-600 group-hover:text-zinc-900">{feature}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1">
        {/* High Density Brand Header */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xs font-black uppercase tracking-[0.4em] text-zinc-300">Shop by Brand</h2>
            <div className="h-[1px] flex-1 bg-zinc-100 ml-8"></div>
          </div>
          <div className="flex gap-4 overflow-x-auto pb-6 scrollbar-hide">
            {[
              { name: 'Apple', logo: 'https://cdn-icons-png.flaticon.com/512/882/882704.png' },
              { name: 'Samsung', logo: 'https://cdn-icons-png.flaticon.com/512/5969/5969116.png' },
              { name: 'Xiaomi', logo: 'https://cdn-icons-png.flaticon.com/512/5969/5969134.png' },
              { name: 'Oppo', logo: 'https://cdn-icons-png.flaticon.com/512/882/882745.png' },
              { name: 'Realme', logo: 'https://cdn-icons-png.flaticon.com/512/5969/5969106.png' },
              { name: 'Vivo', logo: 'https://cdn-icons-png.flaticon.com/512/882/882760.png' },
              { name: 'Nokia', logo: 'https://cdn-icons-png.flaticon.com/512/882/882741.png' },
            ].map((brand, idx) => (
              <button 
                key={idx}
                className="flex flex-col items-center gap-4 min-w-[130px] p-6 bg-white rounded-[2rem] border border-zinc-100 shadow-[0_10px_40px_-20px_rgba(0,0,0,0.05)] hover:border-zinc-900 hover:shadow-2xl hover:-translate-y-2 transition-all group shrink-0 active:scale-95"
              >
                <div className="w-10 h-10 flex items-center justify-center grayscale opacity-30 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500">
                  <img src={brand.logo} alt={brand.name} className="w-full h-full object-contain" />
                </div>
                <span className="text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 group-hover:text-zinc-900 transition-colors">{brand.name}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
          <div>
            <h1 className="text-4xl font-black tracking-tighter text-zinc-900 mb-1 font-['Inter'] uppercase">Điện thoại</h1>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-[#FFD194] rounded-full"></div>
              <p className="text-zinc-400 text-xs font-black uppercase tracking-[0.2em]">{PRODUCTS.length} PREMIUM ITEMS</p>
            </div>
          </div>
          <div className="flex items-center gap-4 w-full md:w-auto">
            <div className="flex border-2 rounded-2xl overflow-hidden border-zinc-900 bg-white shadow-xl shadow-zinc-900/5 transition-transform active:scale-95">
              <button className="p-3 bg-zinc-900 text-white"><LayoutGrid className="w-4 h-4" /></button>
              <button className="p-3 text-zinc-400 hover:text-zinc-900"><List className="w-4 h-4" /></button>
            </div>
            <div className="relative group/sort">
              <button className="flex items-center gap-4 px-6 py-3 bg-white border-2 border-zinc-100 rounded-2xl text-xs font-black uppercase tracking-widest hover:border-zinc-900 transition-all flex-1 md:flex-none">
                Sort By <ChevronDown className="w-4 h-4 text-zinc-400 group-hover:text-zinc-900 transition-colors" />
              </button>
              <div className="absolute top-full right-0 mt-3 bg-white shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border border-zinc-100 rounded-2xl py-3 min-w-[260px] opacity-0 translate-y-4 pointer-events-none group-hover/sort:opacity-100 group-hover/sort:translate-y-0 group-hover/sort:pointer-events-auto transition-all z-[60] overflow-hidden">
                {['Bán chạy nhất', 'Giá từ thấp đến cao', 'Giá từ cao đến thấp', 'Mới nhất'].map((opt) => (
                  <button key={opt} className="w-full text-left px-8 py-4 text-[10px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-zinc-900 hover:bg-zinc-50 transition-colors border-b border-zinc-50 last:border-0 flex items-center justify-between group/opt">
                    {opt}
                    <div className="w-1.5 h-1.5 bg-[#FFD194] rounded-full opacity-0 group-hover/opt:opacity-100 transition-opacity"></div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6">
          {PRODUCTS.map((product) => (
            <ProductCard 
              key={product.id} 
              product={product} 
              onClick={handleProductClick} 
            />
          ))}
        </div>
        
        <div className="mt-12 flex justify-center">
          <button className="px-8 py-3 bg-white border-2 border-zinc-900 text-zinc-900 rounded-xl font-bold hover:bg-zinc-900 hover:text-white transition-all">
            Xem thêm 24 sản phẩm
          </button>
        </div>
      </main>
    </div>
  );
}
