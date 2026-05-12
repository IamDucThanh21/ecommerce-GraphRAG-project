/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useState } from 'react';
import {
  ChevronRight,
  ChevronLeft,
  Smartphone,
  Laptop,
  Tablet,
  Watch,
  Bolt,
  Camera,
  BatteryFull,
  LayoutGrid
} from 'lucide-react';
import { PRODUCTS, ACCESSORIES, NEWS } from '../data';
import ProductCard from '../components/ProductCard';
import { Page, Product } from '../types';
import { apiClient, Category, Brand } from '../api/client';

interface HomePageProps {
  setPage: (page: Page) => void;
  setProductId: (id: string) => void;
  setCategoryId: (id: string) => void;
  setBrandId: (id: string | null) => void;
}

const SMARTPHONE_CATEGORY_ID = '5e883863-9808-4319-acb7-078e6206798d';

export default function HomePage({ setPage, setProductId, setCategoryId, setBrandId }: HomePageProps) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loadingCategories, setLoadingCategories] = useState(false);
  const [activeCategoryId, setActiveCategoryId] = useState<string | null>(null);

  const [brands, setBrands] = useState<Brand[]>([]);
  const [loadingBrands, setLoadingBrands] = useState(false);  

  const [activeBrandId, setActiveBrandId] = useState<string | null>(null);

  const [products, setProducts] = useState<Product[]>([]);
  const [loadingProducts, setLoadingProducts] = useState(false);

  const [currentProductIndex, setCurrentProductIndex] = useState(0);

  const capitalize = (value: string) =>
    value.charAt(0).toUpperCase() + value.slice(1);

  const handleProductClick = (id: string) => {
    setProductId(id);
    setPage('detail');
  };

  const handleSmartphoneQuery = () => {
    setCategoryId(SMARTPHONE_CATEGORY_ID);
    setPage('listing');
  };

  const handleHomepageCategoryClick = (
    category: Category
  ) => {
    setActiveCategoryId(category.id);

    // reset selected brand
    setActiveBrandId(null);
  };
  
  const handleBrandClick = (brand: Brand) => {
    setActiveBrandId(brand.id);
  };

  const handleNextProducts = () => {
    if (products.length <= 5) return;

    setCurrentProductIndex((prev) =>
      prev + 1 > products.length - 5
        ? 0
        : prev + 1
    );
  };

  const handlePrevProducts = () => {
    if (products.length <= 5) return;

    setCurrentProductIndex((prev) =>
      prev === 0
        ? products.length - 5
        : prev - 1
    );
  };

  const visibleProducts = products.slice(
    currentProductIndex,
    currentProductIndex + 5
  );

  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoadingCategories(true);

        const response = await apiClient.categoryList();

        const list = response.data ?? [];

        setCategories(list);

        // default active tab
        if (list.length > 0) {
          setActiveCategoryId(list[0].id);
        }
      } catch (error) {
        console.error('Failed to load categories:', error);
      } finally {
        setLoadingCategories(false);
      }
    };

    loadCategories();
  }, []);

  useEffect(() => {
    const loadBrands = async () => {
      if (!activeCategoryId) {
        setBrands([]);
        return;
      }

      try {
        setLoadingBrands(true);

        const response = await apiClient.categoryBrandList(
          activeCategoryId
        );

        setBrands(response.data ?? []);
      } catch (error) {
        console.error('Failed to load brands:', error);
        setBrands([]);
      } finally {
        setLoadingBrands(false);
      }
    };

    loadBrands();
  }, [activeCategoryId]);

  useEffect(() => {
    const loadProducts = async () => {
      if (!activeCategoryId) {
        setProducts([]);
        return;
      }

      try {
        setLoadingProducts(true);

        const response = await apiClient.productList({
          category_id: activeCategoryId,
          brand_id: activeBrandId ?? undefined,
          page: 1,
          limit: 10,
        });

        const list = Array.isArray(response)
          ? response
          : response?.data ?? [];

        const mappedProducts: Product[] = list.map(
          (item: any) => ({
            id: item.id,
            name: item.name || 'Product',
            price:
              item.price ??
              item.base_price ??
              0,
            originalPrice:
              item.base_price &&
              item.base_price >
                (item.price ?? 0)
                ? item.base_price
                : undefined,
            image:
              item.primary_image_url ||
              item.image ||
              '',
            category:
              item.category_name || '',
            brand:
              item.brand_name || '',
            rating: 4,
            reviewsCount: 10,
            badges: item.tag
              ? [item.tag]
              : undefined,
            description:
              item.description ?? '',
          })
        );

        setProducts(mappedProducts);
      } catch (error) {
        console.error(
          'Failed to load products:',
          error
        );

        setProducts([]);
      } finally {
        setLoadingProducts(false);
      }
    };

    loadProducts();
  }, [activeCategoryId, activeBrandId]);

  return (
    <div className="space-y-12">
      {/* Top Section: Category Sidebar + Hero + Mini Ad */}
      <div className="grid grid-cols-12 gap-gutter">
        {/* Category Sidebar */}
        <aside className="hidden lg:block col-span-3 bg-white rounded-2xl border border-zinc-100 shadow-sm overflow-hidden h-[480px]">
          <div className="bg-zinc-900 text-white px-6 py-4 flex items-center gap-2">
            <LayoutGrid className="w-5 h-5" />
            <span className="font-bold uppercase tracking-widest text-xs">Categories</span>
          </div>
          <nav className="p-2 space-y-1 overflow-y-auto h-[calc(100%-56px)]">
            {[
              { icon: <Smartphone className="w-5 h-5" />, label: 'Smartphone' },
              { icon: <Laptop className="w-5 h-5" />, label: 'Laptop' },
              { icon: <Tablet className="w-5 h-5" />, label: 'Tablet' },
              { icon: <Watch className="w-5 h-5" />, label: 'Smartwatch' },
              { icon: <Bolt className="w-5 h-5" />, label: 'Components' },
              { icon: <Camera className="w-5 h-5" />, label: 'Camera' },
              { icon: <BatteryFull className="w-5 h-5" />, label: 'Accessories' },
            ].map((item, idx) => (
              <button 
                key={idx}
                onClick={() => item.label === 'Smartphone' ? handleSmartphoneQuery() : setPage('listing')}
                className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 group transition-all"
              >
                <div className="flex items-center gap-3">
                  <span className="text-zinc-400 group-hover:text-zinc-900 transition-colors">{item.icon}</span>
                  <span className="text-sm font-semibold text-zinc-600 group-hover:text-zinc-900">{item.label}</span>
                </div>
                <ChevronRight className="w-4 h-4 text-zinc-300 group-hover:text-zinc-900 transition-colors" />
              </button>
            ))}
          </nav>
        </aside>

        {/* Hero Banner Area */}
        <section className="col-span-12 lg:col-span-9 space-y-gutter">
          <div className="rounded-2xl overflow-hidden shadow-xl relative h-[480px]">
            <img 
              className="w-full h-full object-cover" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBJ_FixJsOPrDcyxDFaPx5c1X1vzc3fs3Xqnkel7vVOU5Zmh9uQffWodE4y5jvj9fVtsXPc-KD9k_ONQJvivtmo0nbwQSN9bwS7XGMG91QEz_8zHIbvu6RMkTFmwaov9Fh5rbtbzrt9jvkzRnhEVtQ2jf0UAVDsGJSEhOx7nsDY_pOaLmmu2_1fUryj5u7ge5bOZ2xZpnQ9rw4fBC6fpltdANwxkqxyV3MBkcVE7vl4NUwoxxMA_SEJ46dXkkY_3JVylePkzq-UPMs"
              alt="Hero"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-zinc-900/60 to-transparent flex items-center px-12">
              <div className="max-w-md text-white">
                <span className="text-xs font-black uppercase tracking-[0.3em] mb-4 block text-[#FFD194]">Pre-order Now</span>
                <h1 className="font-bold text-5xl mb-6 leading-tight tracking-tight">iPhone 15 Pro<br/>Titanium.</h1>
                <p className="text-lg mb-8 opacity-90 font-['Inter'] leading-relaxed">Experience the next generation of power and elegance. Engineered with aerospace-grade titanium.</p>
                <div className="flex gap-4">
                  <button 
                    onClick={handleSmartphoneQuery}
                    className="bg-[#FFD194] text-zinc-900 px-8 py-4 rounded-xl font-bold hover:scale-105 active:scale-95 transition-all outline-none shadow-lg shadow-[#FFD194]/20"
                  >
                    Xem smartphone
                  </button>
                </div>
              </div>
            </div>
            {/* Pagination dots simulation */}
            <div className="absolute bottom-6 left-12 flex gap-2">
              <div className="w-8 h-1 bg-[#FFD194] rounded-full"></div>
              <div className="w-2 h-1 bg-white/50 rounded-full"></div>
              <div className="w-2 h-1 bg-white/50 rounded-full"></div>
            </div>
          </div>
        </section>
      </div>

      {/* Mini Promotions Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { title: 'iPad Pro', text: 'Trade-in and save', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBI6EemfcmCKeepSNWm-J52tj-kLHHeMWcJTRY-RgtCeV78-qVZ7DKVui4wnRbazJsrRYtwaHHdiQD99xjsaPkHyfQVkJDDe5cJOzLyYHbSqekX-RiLX4eFNn4gMKUnP7YcuAAauGnRjvakBatQIHXqPgmBEPmLCNSAFeoVSXeQK_nObanvmKyWAOboYgEiErMPymtG9RKDXeh6KRTzmW8zBpQENct089sW6sh_y5H9cllwYIaE7d6LKjf9prYP5mnhn7LDJmvTxmw' },
          { title: 'Audio Sale', text: 'Up to 30% Off', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAHTVjf4VXkdNmTEVpHJ7S70yro9bKM8m2SJIfJtJ852owVRWIX4Ehk-ThOc0xs6QdimyzdrHrh7NCUhDNC1QZh9Q2vFFlo16M_ZUxR2ZYx20y6AWJmwoiTTQB2Clvv6jp59xmgAW7cEJH_HIB269sJPBe2tyDMWamRbW3c-fU8N6-hitzUSsqByzi4vcHzro6XxO3A9Kvio6d_BO51bWsvza0-XBmVGRZoSlP7tB2uiMiH2dXhJrCHhJnzU-TB1BJyk8FqXZ66aak' },
          { title: 'Gadget Hub', text: 'New Arrivals', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA1pkop_MMT0x01VsTcwrp4hOQVHrd1lpU3ccp9Nc5EBmLqgnx3LKRkFJHVM9ewCCT67F6N-mTBzY_HTwu8_ZA84Q4VtOsDKkhHPuCD-XRt2psGBiMWDBFi2OjEJcZgT5VWEbf9T6d0oOBxFoF7sE_vCN59EoWGIfRgCkH308OGBmT5DA9cPKmTIiGdN3BioIgwkk_XUlMegEACMpjkJW-oGe5esjWwQPTSRDsz_dkG-6WKjROIrqqLZlQtkGqBw2XKJy5gPAMO_OY' }
        ].map((promo, idx) => (
          <div key={idx} className="bg-zinc-100 rounded-2xl p-4 flex items-center gap-4 hover:shadow-md transition-shadow group cursor-pointer">
            <div className="w-20 h-20 bg-white rounded-xl overflow-hidden shrink-0">
              <img className="w-full h-full object-cover group-hover:scale-110 transition-transform" src={promo.img} alt={promo.title} />
            </div>
            <div>
              <h4 className="font-bold text-zinc-900">{promo.title}</h4>
              <p className="text-xs text-zinc-500 font-semibold uppercase tracking-wider">{promo.text}</p>
            </div>
          </div>
        ))}
      </section>

      {/* Tabs / Filter Row */}
      <section>
        <div className="flex items-center justify-between mb-8 border-b border-zinc-200">
            <div className="flex gap-8">
              {loadingCategories ? (
                <div className="pb-4 text-sm text-zinc-400">
                  Loading...
                </div>
              ) : (
                categories.map((category) => {
                  const isActive = activeCategoryId === category.id;

                  return (
                    <button
                      key={category.id}
                      onClick={() => handleHomepageCategoryClick(category)}
                      className={`pb-4 font-bold text-sm uppercase tracking-[0.2em] transition-all ${
                        isActive
                          ? 'text-zinc-900 border-b-2 border-zinc-900'
                          : 'text-zinc-400 hover:text-zinc-600'
                      }`}
                    >
                      {category.name}
                    </button>
                  );
                })
              )}
            </div>
          <button 
            onClick={() => {
              if (activeCategoryId) {
                setCategoryId(activeCategoryId);
              }

              setBrandId(activeBrandId);

              setPage('listing');
            }}
            className="pb-4 text-xs font-bold text-zinc-400 hover:text-zinc-900 transition-all uppercase tracking-widest"
          >
            Show all
          </button>
        </div>

        {/* Feature Icons */}
        <div className="flex gap-4 mb-8 overflow-x-auto pb-2 scrollbar-hide">
          {[
            { icon: <Smartphone className="w-6 h-6" />, label: 'Tất cả' },
            { icon: <Bolt className="w-6 h-6" />, label: 'Gaming' },
            { icon: <Camera className="w-6 h-6" />, label: 'Chụp ảnh' },
            { icon: <BatteryFull className="w-6 h-6" />, label: 'Pin trâu' },
          ].map((item, idx) => (
            <button 
              key={idx}
              className="flex flex-col items-center min-w-[100px] p-4 bg-white rounded-2xl border border-zinc-100 shadow-sm hover:border-[#FFD194] transition-all"
            >
              <div className="text-zinc-700 mb-2">{item.icon}</div>
              <span className="text-xs font-bold">{item.label}</span>
            </button>
          ))}
        </div>

        {/* Brand Pills */}
        <div className="flex gap-3 mb-8 flex-wrap">
          {loadingBrands ? (
            <div className="text-sm text-zinc-400">
              Loading brands...
            </div>
          ) : (
            brands.map((brand) => (
              <button
                key={brand.id}
                onClick={() => handleBrandClick(brand)}
                className={`px-6 py-2 rounded-full border transition-all text-sm font-medium ${
                  activeBrandId === brand.id
                    ? 'border-zinc-900 bg-zinc-900 text-white'
                    : 'border-zinc-200 bg-white text-zinc-700 hover:border-zinc-900 hover:text-zinc-900'
                }`}
              >
                {capitalize(brand.name)}
              </button>
            ))
          )}
        </div>

        {/* Product Carousel */}
        <div className="relative">
          {/* Left Arrow */}
          <button
            onClick={handlePrevProducts}
            className="absolute left-[-20px] top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white border border-zinc-200 shadow-lg flex items-center justify-center hover:bg-zinc-900 hover:text-white transition-all"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          {/* Products */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {loadingProducts ? (
              <div className="col-span-full text-center py-10 text-zinc-400">
                Loading products...
              </div>
            ) : (
              visibleProducts.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onClick={handleProductClick}
                />
              ))
            )}
          </div>

          {/* Right Arrow */}
          <button
            onClick={handleNextProducts}
            className="absolute right-[-20px] top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white border border-zinc-200 shadow-lg flex items-center justify-center hover:bg-zinc-900 hover:text-white transition-all"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </section>

      {/* Accessories Section */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="font-bold text-2xl text-zinc-900 tracking-tight">SẮM THÊM PHỤ KIỆN CHẤT LƯỢNG</h2>
          <button className="text-zinc-500 text-sm font-medium hover:text-zinc-900 transition-all flex items-center gap-1">
            Xem tất cả <ChevronRight className="w-4 h-4" />
          </button>
        </div>
        <div className="bg-white rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.03)] border border-zinc-100 overflow-hidden">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6">
            {ACCESSORIES.map((acc, idx) => (
              <div 
                key={acc.id}
                className={`p-6 flex items-center gap-4 hover:bg-zinc-50 transition-colors group cursor-pointer ${
                  idx % 6 !== 5 ? 'border-r' : ''
                } ${idx < 6 ? 'border-b' : ''}`}
              >
                <div className="w-6 h-6 text-zinc-400 group-hover:text-zinc-900">
                  <Watch className="w-6 h-6" /> {/* Placeholder icon mapping would go here */}
                </div>
                <span className="text-sm font-semibold text-zinc-700">{acc.name}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* News Section */}
      <section className="pb-12">
        <h2 className="font-bold text-2xl text-zinc-900 tracking-tight mb-8">TIN TỨC</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {NEWS.map((item) => (
            <a key={item.id} className="group block" href="#">
              <div className="aspect-[16/10] rounded-xl overflow-hidden mb-3">
                <img className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src={item.image} alt={item.title} />
              </div>
              <p className="text-xs text-zinc-400 mb-1">{item.date}</p>
              <h3 className="font-bold text-sm text-zinc-900 leading-snug group-hover:text-zinc-600 transition-colors line-clamp-2">
                {item.title}
              </h3>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
