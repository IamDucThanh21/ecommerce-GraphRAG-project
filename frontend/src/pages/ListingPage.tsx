/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useState, useCallback } from 'react';
import { Filter, ChevronDown, LayoutGrid, List } from 'lucide-react';
import { PRODUCTS } from '../data';
import ProductCard from '../components/ProductCard';
import { apiClient, Brand } from '../api/client';
import { Page, Product} from '../types';

interface BackendProductListResponse {
  data?: unknown[];
  pagination?: unknown;
}

interface ListingPageProps {
  setPage: (page: Page) => void;
  setProductId: (id: string) => void;
  categoryId: string;
  brandId: string | null;
  setBrandId: (id: string | null) => void;
}

export default function ListingPage({ setPage, setProductId, categoryId, brandId, setBrandId }: ListingPageProps) {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loadingBrands, setLoadingBrands] = useState(false);  
  // const [brandId, setBrandId] = useState<string | null>(null);

  const [products, setProducts] = useState<Product[]>([]);
  const [visibleCount, setVisibleCount] = useState(25);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const [sortBy, setSortBy] = useState<string>('');

  const PRICE_FILTERS = [
    {
      label: 'Dưới 2 triệu',
      min: 0,
      max: 2000000,
    },
    {
      label: 'Từ 2 - 4 triệu',
      min: 2000000,
      max: 4000000,
    },
    {
      label: 'Từ 4 - 7 triệu',
      min: 4000000,
      max: 7000000,
    },
    {
      label: 'Từ 7 - 13 triệu',
      min: 7000000,
      max: 13000000,
    },
    {
      label: 'Trên 13 triệu',
      min: 13000000,
      max: null,
    },
  ];

  const [priceFilter, setPriceFilter] = useState<{
    min?: number;
    max?: number;
  } | null>(null);

  const handleProductClick = (id: string) => {
    setProductId(id);
    setPage('detail');
  };

  const handleBrandClick = (id: string) => {
    if (brandId === id) {
      setBrandId(null);
      return;
    }

    setBrandId(id);
  };

  const fetchProducts = useCallback(
  async (
    pageNumber: number,
    append: boolean = false
  ) => {
    try {
      const response =
        await apiClient.productList({
          category_id: categoryId,
          brand_id:
            brandId ?? undefined,
          page: pageNumber,
          limit: 25,
          sort: sortBy || undefined,
          price_min:
            priceFilter?.min,
          price_max:
            priceFilter?.max,
        });

      const list = Array.isArray(
        response
      )
        ? response
        : (response as BackendProductListResponse)
            ?.data ??
          (response as any)?.items ??
          (response as any)
            ?.objects ??
          [];

      const mappedProducts: Product[] =
        (list as any[])
          .map((item) => ({
            id: item.id,

            name:
              item.name ||
              'Sản phẩm',

            // priority:
            // sale_price -> price -> base_price
            price:
              item.sale_price ??
              item.price ??
              item.base_price ??
              0,

            originalPrice:
              item.base_price &&
              item.base_price >
                (item.sale_price ??
                  item.price ??
                  0)
                ? item.base_price
                : undefined,

            image:
              item.primary_image_url ||
              item.image ||
              null,

            category:
              item.category_name ||
              '',

            brand:
              item.brand_name || '',

            rating: 4,

            reviewsCount: 10,

            badges: item.tag
              ? [item.tag]
              : item.category_name
              ? [item.category_name]
              : undefined,

            description:
              item.description ??
              '',
          }))
          .sort((a, b) => {
            const priceA =
              a.price || 0;

            const priceB =
              b.price || 0;

            // always move zero-price products to bottom
            if (
              priceA === 0 &&
              priceB !== 0
            ) {
              return 1;
            }

            if (
              priceB === 0 &&
              priceA !== 0
            ) {
              return -1;
            }

            // keep backend order
            return 0;
          });

      if (append) {
        setProducts((prev) => [
          ...prev,
          ...mappedProducts,
        ]);
      } else {
        setProducts(mappedProducts);
      }

      setHasMore(
        mappedProducts.length === 25
      );
    } catch (err) {
      console.error(
        'Error loading products:',
        err
      );

      setError(
        'Không thể tải sản phẩm.'
      );

      if (!append) {
        setProducts([]);
      }
    }
  },
  [
    categoryId,
    brandId,
    sortBy,
    priceFilter,
  ]
);

  useEffect(() => {
    const loadBrands = async () => {
      if (!categoryId) {
        setBrands([]);
        return;
      }

      try {
        setLoadingBrands(true);

        const response = await apiClient.categoryBrandList(
          categoryId
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
  }, [categoryId]);

  useEffect(() => {
    if (!categoryId) {
      setProducts([]);
      setError(null);
      setLoading(false);
      setVisibleCount(25);
      return;
    }

    setLoading(true);
    setError(null);
    setVisibleCount(25);
    setCurrentPage(1);
    setHasMore(true);

    fetchProducts(1, false).finally(() => {
      setLoading(false);
    });
  }, [categoryId, brandId, sortBy, fetchProducts]);

  const handleLoadMore = useCallback(() => {
    if (loadingMore || !hasMore) return;

    setLoadingMore(true);
    const nextPage = page + 1;

    fetchProducts(nextPage, true)
      .then(() => {
        setCurrentPage(nextPage);
      })
      .finally(() => {
        setLoadingMore(false);
      });
  }, [fetchProducts, hasMore, loadingMore, page]);

  const allProducts = categoryId ? products : PRODUCTS;
  const displayProducts = categoryId ? allProducts : allProducts.slice(0, visibleCount);
  const productCount = allProducts.length;

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
                {PRICE_FILTERS.map((price) => (
                  <label
                    key={price.label}
                    className="flex items-center gap-2 cursor-pointer group"
                  >
                    <input
                      type="radio"
                      name="price"
                      checked={
                        priceFilter?.min === price.min &&
                        priceFilter?.max === price.max
                      }
                      onChange={() =>
                        setPriceFilter({
                          min: price.min,
                          max: price.max ?? undefined,
                        })
                      }
                      className="w-4 h-4 rounded-full border-zinc-200 text-[#ba1a1a] focus:ring-[#FFD194]"
                    />

                    <span className="text-sm text-zinc-600 group-hover:text-zinc-900">
                      {price.label}
                    </span>
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
        {/* Brand Header */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xs font-black uppercase tracking-[0.4em] text-zinc-300">
              Brand
            </h2>

            <div className="h-[1px] flex-1 bg-zinc-100 ml-8"></div>
          </div>

          {loadingBrands ? (
            <div className="flex gap-4 overflow-x-auto pb-4">
              {Array.from({ length: 7 }).map((_, idx) => (
                <div
                  key={idx}
                  className="min-w-[140px] h-[110px] rounded-[2rem] border border-zinc-100 bg-white animate-pulse"
                />
              ))}
            </div>
          ) : brands.length > 0 ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4">
              {brands.map((brand) => (
                <button
                  key={brand.id}
                  onClick={() => handleBrandClick(brand.id)}
                  className={`
                    flex items-center justify-center
                    h-[60px]
                    px-4
                    bg-white
                    rounded-[2rem]
                    border
                    transition-all
                    group
                    hover:-translate-y-1
                    ${
                      brandId === brand.id
                        ? 'border-zinc-900 shadow-xl ring-2 ring-zinc-900/10'
                        : 'border-zinc-100 shadow-[0_10px_40px_-20px_rgba(0,0,0,0.05)] hover:border-zinc-900 hover:shadow-2xl'
                    }
                  `}
                >
                  <div className="h-10 flex items-center justify-center">
                    {brand.logo_url ? (
                      <img
                        src={brand.logo_url}
                        alt={brand.name}
                        className="
                          max-h-8
                          object-contain
                          opacity-90
                          group-hover:opacity-100
                          transition-all
                          duration-300
                        "
                      />
                    ) : (
                      <div className="w-10 h-10 rounded-full bg-zinc-100" />
                    )}
                  </div>
                </button>
              ))}
            </div>
          ) : null}
        </div>

        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
          <div>
            <h1 className="text-4xl font-black tracking-tighter text-zinc-900 mb-1 font-['Inter'] uppercase">Điện thoại</h1>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 bg-[#FFD194] rounded-full"></div>
              <p className="text-zinc-400 text-xs font-black uppercase tracking-[0.2em]">
                {productCount} PREMIUM ITEMS
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4 w-full md:w-auto">
            <div>
              <span className="
                text-xs
                font-black
                uppercase
                tracking-[0.2em]
                text-zinc-500
              ">
                Sắp xếp theo
              </span>
            </div>
            <div className="relative group/sort">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setSortBy('price.asc')}
                  className={`
                    flex items-center gap-2
                    px-6 py-3
                    rounded-2xl
                    border
                    bg-white
                    text-sm
                    font-semibold
                    transition-all
                    ${
                      sortBy === 'price.desc'
                        ? 'border-zinc-900 text-zinc-900 shadow-lg'
                        : 'border-zinc-200 text-zinc-600 hover:border-zinc-900'
                    }
                  `}
                >
                  <ChevronDown className="w-4 h-4 rotate-180" />
                  Giá Thấp - Cao
                </button>

                <button
                  onClick={() => setSortBy('price.desc')}
                  className={`
                    flex items-center gap-2
                    px-6 py-3
                    rounded-2xl
                    border
                    bg-white
                    text-sm
                    font-semibold
                    transition-all
                    ${
                      sortBy === 'price.desc'
                        ? 'border-zinc-900 text-zinc-900 shadow-lg'
                        : 'border-zinc-200 text-zinc-600 hover:border-zinc-900'
                    }
                  `}
                >
                  <ChevronDown className="w-4 h-4" />
                  Giá Cao - Thấp
                </button>
              </div>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="rounded-2xl border border-zinc-200 bg-white p-8 text-center text-zinc-600">
            Đang tải sản phẩm...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-8 text-center text-red-700">
            {error}
          </div>
        ) : categoryId && allProducts.length === 0 ? (
          <div className="rounded-2xl border border-zinc-200 bg-white p-8 text-center text-zinc-600">
            Không có sản phẩm cho danh mục smartphone.
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {displayProducts.map((product) => (
              <ProductCard 
                key={product.id} 
                product={product} 
                onClick={handleProductClick} 
              />
            ))}
          </div>
        )}
        
        {categoryId && hasMore && !loading && (
          <div className="mt-12 flex justify-center">
            <button
              onClick={handleLoadMore}
              className="px-8 py-3 bg-white border-2 border-zinc-900 text-zinc-900 rounded-xl font-bold hover:bg-zinc-900 hover:text-white transition-all"
            >
              {loadingMore ? 'Đang tải thêm...' : 'Xem thêm 25 sản phẩm'}
            </button>
          </div>
        )}

        {!categoryId && displayProducts.length < allProducts.length && !loading && (
          <div className="mt-12 flex justify-center">
            <button
              onClick={() => setVisibleCount((prev) => prev + 25)}
              className="px-8 py-3 bg-white border-2 border-zinc-900 text-zinc-900 rounded-xl font-bold hover:bg-zinc-900 hover:text-white transition-all"
            >
              Xem thêm 25 sản phẩm
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
