/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useState } from 'react';
import { Star, ShieldCheck, Truck, RotateCcw, Heart, Share2, ChevronLeft, ChevronRight, ChevronDown, ChevronUp, Maximize2, MessageSquare } from 'lucide-react';
import { PRODUCTS } from '../data';
import { Page } from '../types';
import ProductCard from '../components/ProductCard';

import { apiClient, ProductVariant } from '../api/client';

interface DetailPageProps {
  productId: string;
  categoryId: string;
  setPage: (page: Page) => void;
}

export default function DetailPage({ productId, categoryId, setPage }: DetailPageProps) {
  // const product = PRODUCTS.find((p) => p.id === productId) || PRODUCTS[0];
  const [showAllSpecs, setShowAllSpecs] =
  useState(false);

  const [selectedSpecGroup, setSelectedSpecGroup] =
  useState(0);

  const [variants, setVariants] =
  useState<ProductVariant[]>([]);

  const [selectedVariant, setSelectedVariant] =
    useState<ProductVariant | null>(
      null
    );

  const [
    userSelectedVariant,
    setUserSelectedVariant,
  ] = useState(false);

  const [
    previewVariantImage,
    setPreviewVariantImage,
  ] = useState<string | null>(
    null
  );

  const [
    isDescriptionExpanded,
    setIsDescriptionExpanded,
  ] = useState(false);

  const [product, setProduct] =
    useState<any>(null);

  const [
    selectedImageIndex,
    setSelectedImageIndex,
  ] = useState(0);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    if (
      showAllSpecs &&
      product?.spec_groups?.length
    ) {
      setSelectedSpecGroup(0);
    }
  }, [showAllSpecs, product]);

  /* -----------------------------
    Product Images
  ----------------------------- */
  const productImages =
    product?.image_urls
      ?.filter(
        (url: string) =>
          url &&
          /\.(jpg|jpeg|png|webp)$/i.test(
            url
          )
      ) ?? [];
  /* -----------------------------
    Current Image
  ----------------------------- */
  const currentImage =
    previewVariantImage ||
    productImages[
      selectedImageIndex
    ] ||
    product?.primary_image_url ||
    '';


  const [relatedProducts, setRelatedProducts] =
    useState<any[]>([]);

  const [
    loadingRelatedProducts,
    setLoadingRelatedProducts,
  ] = useState(false);

  const [
    currentRelatedIndex,
    setCurrentRelatedIndex,
  ] = useState(0);

  const handleNextRelatedProducts =
    () => {
      if (
        relatedProducts.length <= 5
      )
        return;

      setCurrentRelatedIndex(
        (prev) =>
          prev + 1 >
          relatedProducts.length - 5
            ? 0
            : prev + 1
      );
    };

  const handlePrevRelatedProducts =
    () => {
      if (
        relatedProducts.length <= 5
      )
        return;

      setCurrentRelatedIndex(
        (prev) =>
          prev === 0
            ? relatedProducts.length - 5
            : prev - 1
      );
    };

  const visibleRelatedProducts =
    relatedProducts.slice(
      currentRelatedIndex,
      currentRelatedIndex + 5
    );
  
  useEffect(() => {
    if (
      !userSelectedVariant ||
      !selectedVariant
    ) {
      return;
    }

    const variantImage =
      selectedVariant
        .primary_image_url ||
      selectedVariant.image_urls?.[0];

    if (!variantImage) return;

    setSelectedImageIndex(0);
  }, [
    selectedVariant,
    userSelectedVariant,
  ]);

  /* -----------------------------
    Image Navigation
  ----------------------------- */
  const handlePrevImage = () => {
    if (productImages.length === 0)
      return;

    setSelectedImageIndex(
      (prev) =>
        prev === 0
          ? productImages.length - 1
          : prev - 1
    );
  };

  const handleNextImage = () => {
    if (productImages.length === 0)
      return;

    setSelectedImageIndex(
      (prev) =>
        prev ===
        productImages.length - 1
          ? 0
          : prev + 1
    );
  };

  /* -----------------------------
    Static Specs
  ----------------------------- */
  const fullSpecs = [
    {
      label: 'Màn hình',
      value:
        '6.1 inch, LTPO Super Retina XDR OLED, 120Hz',
    },
    {
      label: 'Chipset',
      value:
        'Apple A17 Pro (3 nm)',
    },
    {
      label: 'CPU',
      value:
        'Hexa-core (2x3.78 GHz + 4x2.11 GHz)',
    },
    {
      label: 'GPU',
      value:
        'Apple GPU (6-core graphics)',
    },
    {
      label: 'Camera sau',
      value:
        '48MP (Chính) + 12MP (Tele) + 12MP (Ultra wide)',
    },
    {
      label: 'Camera trước',
      value:
        '12MP, f/1.9, 23mm (wide)',
    },
    {
      label: 'RAM',
      value: '8GB',
    },
    {
      label: 'Pin',
      value:
        'Li-Ion 3274 mAh, Sạc 50% trong 30p',
    },
    {
      label:
        'Hệ điều hành',
      value: 'iOS 17',
    },
    {
      label:
        'Khối lượng',
      value:
        '187 g (6.60 oz)',
    },
    {
      label: 'SIM',
      value:
        'Nano-SIM và eSIM',
    },
    {
      label:
        'Cổng sạc',
      value:
        'USB Type-C 3.0',
    },
    {
      label:
        'Kháng nước',
      value:
        'IP68 (độ sâu 6m trong 30p)',
    },
  ];

  const displayedSpecs =
    showAllSpecs
      ? fullSpecs
      : fullSpecs.slice(0, 10);

  useEffect(() => {
      const loadRelatedProducts =
        async () => {
          if (
            !product?.category_id
          ) {
            setRelatedProducts([]);
            return;
          }
  
          try {
            setLoadingRelatedProducts(
              true
            );
  
            const response =
              await apiClient.productList({
                category_id:
                  product.category_id,
                page: 1,
                limit: 20,
              });
  
            const list =
              Array.isArray(response)
                ? response
                : response?.data ?? [];
  
            const mappedProducts =
              list
                // remove current product
                .filter(
                  (item: any) =>
                    item.id !==
                    product.id
                )
                .map((item: any) => ({
                  id: item.id,
                  name:
                    item.name ||
                    'Product',
                  price:
                    item.price ??
                    item.base_price ??
                    0,
                  originalPrice:
                    item.base_price &&
                    item.base_price >
                      (item.price ??
                        0)
                      ? item.base_price
                      : undefined,
                  image:
                    item.primary_image_url ||
                    '',
                  category:
                    item.category_name ||
                    '',
                  brand:
                    item.brand_name ||
                    '',
                  rating: 4,
                  reviewsCount: 10,
                  description:
                    item.description ??
                    '',
                }));
  
            setRelatedProducts(
              mappedProducts
            );
          } catch (error) {
            console.error(
              'Failed to load related products:',
              error
            );
  
            setRelatedProducts([]);
          } finally {
            setLoadingRelatedProducts(
              false
            );
          }
        };
  
      loadRelatedProducts();
    }, [
      product?.id,
      product?.category_id,
    ]);

  /* -----------------------------
    Reviews Mock Data
  ----------------------------- */
  const reviews = [
    {
      id: 1,
      user: 'Hoàng Anh',
      rating: 5,
      date: '2 ngày trước',
      comment:
        'Máy rất mượt, camera chụp đêm xuất sắc. Rất hài lòng với dịch vụ của WiseTech.',
      replies: [
        {
          id: 101,
          user:
            'Admin WiseTech',
          date:
            '1 ngày trước',
          comment:
            'Cảm ơn bạn đã tin tưởng ủng hộ WiseTech ạ!',
        },
      ],
    },
    {
      id: 2,
      user:
        'Minh Tuấn',
      rating: 4,
      date:
        '1 tuần trước',
      comment:
        'Hiệu năng tốt nhưng pin dùng bình thường.',
      replies: [],
    },
  ];

  /* -----------------------------
    Load Product Detail
  ----------------------------- */
  useEffect(() => {
    if (
      !productId ||
      !categoryId
    ) {
      return;
    }

    const loadProduct =
      async () => {
        try {
          setLoading(true);
          setError(null);

          const response =
            await apiClient.productDetail(
              categoryId,
              productId
            );

          console.log(
            'Product detail:',
            response
          );

          setProduct(response);
        } catch (err) {
          console.error(
            'Failed to load product detail:',
            err
          );

          setError(
            'Không thể tải chi tiết sản phẩm.'
          );
        } finally {
          setLoading(false);
        }
      };

    loadProduct();
  }, [productId, categoryId]);

  /* -----------------------------
    Reset Image
  ----------------------------- */
  useEffect(() => {
    if (!product?.id) return;

    const fetchVariants = async () => {
      try {
        const res =
          await apiClient.productVariantList(
            product.id
          );

        setVariants(res.data || []);

        setSelectedVariant(
          res.data?.[0] || null
        );
      } catch (error) {
        console.error(
          'Failed to load variants:',
          error
        );
      }
    };

    fetchVariants();
  }, [product?.id]);

  /* -----------------------------
    Loading / Error
  ----------------------------- */
  if (loading) {
    return (
      <div className="flex justify-center py-20">
        Đang tải sản phẩm...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center py-20 text-red-500">
        {error}
      </div>
    );
  }

  if (!product) {
    return (
      <div className="flex justify-center py-20">
        Đang tải sản phẩm...
      </div>
    );
  }



  /* -----------------------------
    Safe Product Data
  ----------------------------- */
  const displayProduct = {
    ...product,
    rating:
      product.rating ??
      4.5,

    reviewsCount:
      product.reviewsCount ??
      0,

    originalPrice:
      product.price_max &&
      product.price_max >
        product.price_min
        ? product.price_max
        : null,
  };

  return (
    <>   
    
    <div className="space-y-16">
      {/* Spec Popup Modal */}
      {showAllSpecs && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          
          {/* Overlay */}
          <div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() =>
              setShowAllSpecs(false)
            }
          />

          {/* Modal */}
          <div className="relative z-10 bg-white w-full max-w-6xl max-h-[88vh] rounded-[32px] shadow-2xl overflow-hidden flex flex-col">
            
            {/* Header */}
            <div className="flex items-center justify-between px-8 py-6 border-b border-zinc-200 shrink-0">
              <h2 className="text-xl font-black uppercase tracking-widest text-zinc-900">
                Thông số kỹ thuật
              </h2>

              <button
                onClick={() =>
                  setShowAllSpecs(false)
                }
                className="w-10 h-10 rounded-full hover:bg-zinc-100 flex items-center justify-center transition"
              >
                <ChevronUp className="w-5 h-5 text-zinc-700" />
              </button>
            </div>

            {/* Spec Groups Navigation */}
            <div className="border-b border-zinc-200 px-8 py-5 bg-zinc-50">
              <div className="flex flex-wrap gap-3">
                {product?.spec_groups?.map(
                  (group: any, idx: number) => (
                    <button
                      key={group.group_id}
                      onClick={() =>
                        setSelectedSpecGroup(idx)
                      }
                      className={`
                        px-5 py-2.5 rounded-2xl
                        text-sm font-semibold
                        transition-all duration-200
                        border
                        ${
                          selectedSpecGroup === idx
                            ? 'bg-zinc-900 text-white border-zinc-900 shadow-lg shadow-zinc-900/10'
                            : 'bg-white text-zinc-600 border-zinc-200 hover:border-zinc-400 hover:bg-zinc-100'
                        }
                      `}
                    >
                      {group.group_name}
                    </button>
                  )
                )}
              </div>
            </div>

            {/* Selected Group Content */}
            <div className="overflow-y-auto p-8">
              {product?.spec_groups?.[
                selectedSpecGroup
              ] && (
                <div>
                  <h3 className="text-3xl font-bold text-zinc-900 mb-6">
                    {
                      product
                        .spec_groups[
                        selectedSpecGroup
                      ]
                        .group_name
                    }
                  </h3>

                  <div className="rounded-2xl border border-zinc-200 overflow-hidden">
                    <table className="w-full text-sm">
                      <tbody>
                        {product.spec_groups[
                          selectedSpecGroup
                        ].values?.map(
                          (
                            spec: any
                          ) => (
                            <tr
                              key={
                                spec.key
                              }
                              className="border-b border-zinc-200 last:border-0"
                            >
                              {/* Label */}
                              <td className="w-[30%] bg-zinc-50 px-6 py-5 text-zinc-700 font-medium align-top">
                                {
                                  spec.label
                                }
                              </td>

                              {/* Value */}
                              <td className="px-6 py-5 text-zinc-900 whitespace-pre-line leading-7">
                                {spec.value_text ||
                                  spec.value_number ||
                                  spec.value_boolean?.toString() ||
                                  '-'}
                              </td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs font-semibold text-zinc-400">
        <button onClick={() => setPage('home')} className="hover:text-zinc-900 uppercase tracking-wider">Home</button>
        <ChevronRight className="w-3 h-3" />
        <button onClick={() => setPage('listing')} className="hover:text-zinc-900 uppercase tracking-wider">{product.primary_category_name}</button>
        <ChevronRight className="w-3 h-3" />
        <span className="text-zinc-900 uppercase tracking-wider truncate max-w-[200px]">{product.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Left: Gallery */}
        <div className="lg:col-span-7 space-y-6">
          {/* Main Image */}
          <div className="relative aspect-[4/3] rounded-3xl bg-zinc-50 border border-zinc-100 overflow-hidden group">
            
            {/* Previous Button */}
            {productImages.length > 1 && (
              <button
                onClick={handlePrevImage}
                className="absolute left-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-white/90 backdrop-blur-sm border border-zinc-200 shadow-lg flex items-center justify-center hover:scale-105 hover:bg-white transition-all active:scale-95"
              >
                <ChevronLeft className="w-5 h-5 text-zinc-700" />
              </button>
            )}

            {/* Product Image */}
            <div className="w-full h-full flex items-center justify-center p-12">
              <img
                className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-700 mix-blend-multiply"
                src={currentImage}
                alt={product.name}
                onError={(e) => {
                  e.currentTarget.src =
                    product.primary_image_url;
                }}
              />
            </div>

            {/* Next Button */}
            {productImages.length > 1 && (
              <button
                onClick={handleNextImage}
                className="absolute right-4 top-1/2 -translate-y-1/2 z-20 w-12 h-12 rounded-full bg-white/90 backdrop-blur-sm border border-zinc-200 shadow-lg flex items-center justify-center hover:scale-105 hover:bg-white transition-all active:scale-95"
              >
                <ChevronRight className="w-5 h-5 text-zinc-700" />
              </button>
            )}

            {/* Image Counter */}
            {productImages.length > 1 && (
              <div className="absolute bottom-4 right-4 bg-zinc-900/80 text-white text-xs font-bold px-3 py-1 rounded-full backdrop-blur-sm">
                {selectedImageIndex + 1} /{" "}
                {productImages.length}
              </div>
            )}
          </div>

          {/* Thumbnail Images */}
          <div className="relative">
            {/* Prev Thumbnail Button */}
            {productImages.length > 6 && (
              <button
                onClick={() => {
                  const container = document.getElementById(
                    "thumbnail-scroll"
                  );
                  if (container) {
                    container.scrollBy({
                      left: -500,
                      behavior: "smooth",
                    });

                    // if at beginning -> go end
                    if (container.scrollLeft <= 10) {
                      container.scrollTo({
                        left: container.scrollWidth,
                        behavior: "smooth",
                      });
                    }
                  }
                }}
                className="absolute left-0 top-1/2 -translate-y-1/2 z-20 w-10 h-10 rounded-full bg-white border border-zinc-200 shadow-md flex items-center justify-center hover:scale-105"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            )}

            {/* Thumbnail Container */}
            <div
              id="thumbnail-scroll"
              className="flex gap-4 overflow-x-auto scrollbar-hide px-12 scroll-smooth"
            >
              {productImages.map(
                (image: string, index: number) => (
                  <button
                    key={index}
                    onClick={() => {
                      setSelectedImageIndex(index);

                      // back to normal gallery image
                      setPreviewVariantImage(null);
                    }}
                    className={`
                      shrink-0 w-24 h-24 rounded-2xl
                      bg-zinc-50 border
                      overflow-hidden p-2
                      transition-all duration-200
                      hover:border-zinc-900
                      hover:scale-[1.02]
                      ${
                        selectedImageIndex === index
                          ? "border-zinc-900 ring-2 ring-zinc-900/10"
                          : "border-zinc-200"
                      }
                    `}
                  >
                    <img
                      className="w-full h-full object-contain mix-blend-multiply"
                      src={image}
                      alt={`${product.name}-${index}`}
                      onError={(e) => {
                        e.currentTarget.src =
                          product.primary_image_url;
                      }}
                    />
                  </button>
                )
              )}
            </div>

            {/* Next Thumbnail Button */}
            {productImages.length > 6 && (
              <button
                onClick={() => {
                  const container = document.getElementById(
                    "thumbnail-scroll"
                  );

                  if (container) {
                    container.scrollBy({
                      left: 500,
                      behavior: "smooth",
                    });

                    // if near end -> go back first
                    const maxScroll =
                      container.scrollWidth -
                      container.clientWidth;

                    if (
                      container.scrollLeft >=
                      maxScroll - 10
                    ) {
                      container.scrollTo({
                        left: 0,
                        behavior: "smooth",
                      });
                    }
                  }
                }}
                className="absolute right-0 top-1/2 -translate-y-1/2 z-20 w-10 h-10 rounded-full bg-white border border-zinc-200 shadow-md flex items-center justify-center hover:scale-105"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Right: Info & Purchase */}
        <div className="lg:col-span-5 space-y-8">
          <div>
            <div className="flex items-center gap-4 mb-3">
              <span className="text-[#ba1a1a] font-black text-xs uppercase tracking-[0.2em]">New Arrival</span>
              <div className="flex items-center gap-1 text-[#FFD700]">
                <Star className="w-4 h-4 fill-current" />
                <span className="text-zinc-900 font-bold text-sm">{displayProduct.rating}</span>
                <span className="text-zinc-400 font-medium text-sm">({displayProduct.reviewsCount} reviews)</span>
              </div>
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">{product.name}</h1>
            <div className="flex items-end gap-3 mb-6">
              <span className="text-3xl font-black text-zinc-900">
                {!displayProduct.price_min ||
                displayProduct.price_min <= 0
                  ? 'Giá liên hệ'
                  : `${displayProduct.price_min.toLocaleString(
                      'vi-VN'
                    )}₫`}
              </span>

              {!!displayProduct.price_min &&
                displayProduct.price_min > 0 &&
                displayProduct.originalPrice && (
                  <span className="text-zinc-400 text-lg line-through pb-1">
                    {displayProduct.originalPrice.toLocaleString(
                      'vi-VN'
                    )}₫
                  </span>
                )}
            </div>
          </div>

          {/* Configuration Options */}
          <div className="space-y-6">
            <div>
              <h4 className="font-bold text-xs uppercase tracking-widest text-zinc-400 mb-3">
                Chọn màu sắc
              </h4>

              <div className="grid grid-cols-3 gap-2">
                {variants.map((variant) => {
                  const isSelected =
                    selectedVariant?.id ===
                    variant.id;

                  return (
                    <button
                      key={variant.id}
                      onClick={() => {
                        setSelectedVariant(variant);

                        setPreviewVariantImage(
                          variant.primary_image_url ||
                          variant.image_urls?.[0] ||
                          null
                        );
                      }}
                      className={`
                        relative flex items-center gap-2
                        rounded-xl border
                        p-2 h-[72px]
                        text-left transition-all
                        overflow-hidden
                        ${
                          isSelected
                            ? 'border-zinc-900 bg-zinc-50 ring-1 ring-zinc-900/10'
                            : 'border-zinc-200 hover:border-zinc-400 bg-white'
                        }
                      `}
                    >
                      {/* Product Image */}
                      <div className="w-12 h-12 shrink-0 rounded-lg bg-zinc-50 border border-zinc-100 flex items-center justify-center overflow-hidden">
                        <img
                          src={
                            variant.primary_image_url
                          }
                          alt={
                            variant.attributes
                              ?.color
                          }
                          className="w-full h-full object-contain"
                        />
                      </div>

                      {/* Info */}
                      <div className="flex flex-col min-w-0">
                        <span className="text-[11px] font-bold text-zinc-900 truncate leading-tight">
                          Màu{' '}
                          {variant.attributes
                            ?.color || ''}
                        </span>

                        <span className="text-[10px] text-zinc-500 mt-1">
                          Còn lại:{' '}
                          {
                            variant.stock_quantity
                          }
                        </span>
                      </div>

                      {/* Selected check */}
                      {isSelected && (
                        <div className="absolute top-1.5 right-1.5 w-4 h-4 rounded-full bg-zinc-900 text-white flex items-center justify-center text-[9px]">
                          ✓
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* <div>
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
            </div> */}
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

          <div
            className={`relative ${
              !isDescriptionExpanded
                ? 'max-h-[600px] overflow-hidden'
                : ''
            }`}
          >
            <div className="prose prose-zinc max-w-none">
              <div
                className="text-zinc-600 leading-8 whitespace-pre-line font-['Inter'] text-[15px]"
              >
                {product?.description ||
                  'Chưa có mô tả sản phẩm.'}
              </div>
            </div>

            {/* Gradient overlay + expand button */}
            {!isDescriptionExpanded &&
              product?.description &&
              product.description.length >
                500 && (
                <div className="absolute bottom-0 left-0 w-full h-40 bg-gradient-to-t from-white to-transparent flex items-end justify-center pb-4">
                  <button
                    onClick={() =>
                      setIsDescriptionExpanded(
                        true
                      )
                    }
                    className="px-6 py-2 bg-white border border-zinc-200 rounded-full font-bold text-sm shadow-lg hover:bg-zinc-50 flex items-center gap-2 transition"
                  >
                    Xem thêm
                    <ChevronDown className="w-4 h-4" />
                  </button>
                </div>
              )}

            {/* Collapse button */}
            {isDescriptionExpanded &&
              product?.description &&
              product.description.length >
                500 && (
                <div className="flex justify-center mt-6">
                  <button
                    onClick={() =>
                      setIsDescriptionExpanded(
                        false
                      )
                    }
                    className="px-6 py-2 bg-white border border-zinc-200 rounded-full font-bold text-sm hover:bg-zinc-50 flex items-center gap-2 transition"
                  >
                    Thu gọn
                    <ChevronUp className="w-4 h-4" />
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

            {/* Preview Specs */}
            <div className="space-y-4">
              {product?.spec_groups
                ?.slice(0, 2)
                .flatMap(
                  (
                    group: any
                  ) => group.values
                )
                .slice(0, 8)
                .map(
                  (
                    spec: any,
                    idx: number
                  ) => (
                    <div
                      key={idx}
                      className="flex justify-between items-start py-3 border-b border-zinc-200 last:border-0"
                    >
                      <span className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider">
                        {spec.label}
                      </span>

                      <span className="text-sm font-medium text-zinc-900 text-right max-w-[220px] line-clamp-2">
                        {spec.value_text ||
                          spec.value_number ||
                          '-'}
                      </span>
                    </div>
                  )
                )}
            </div>

            {/* Button */}
            <button
              onClick={() =>
                setShowAllSpecs(true)
              }
              className="w-full mt-8 py-3 bg-white border border-zinc-200 rounded-xl font-bold text-xs uppercase tracking-widest text-zinc-900 hover:bg-zinc-100 transition-all flex items-center justify-center gap-2"
            >
              Xem thông số chi tiết
              <Maximize2 className="w-3 h-3" />
            </button>
          </div>
        </aside>
      </div>

      {/* Reviews Section - Instagram Style & Centered */}
      <section className="pt-20 border-t border-zinc-100 flex flex-col items-center">
        <div className="w-full max-w-2xl px-4 lg:px-0">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-black uppercase tracking-tighter text-zinc-900 flex items-center gap-3">
              Reviews <span className="text-zinc-300">({displayProduct.reviewsCount})</span>
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
        <h2 className="text-2xl font-black uppercase tracking-tighter text-zinc-900 mb-10">
          Sản phẩm cùng danh mục
        </h2>

        <div className="relative">
          {/* Left Arrow */}
          <button
            onClick={
              handlePrevRelatedProducts
            }
            className="absolute left-[-20px] top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white border border-zinc-200 shadow-lg flex items-center justify-center hover:bg-zinc-900 hover:text-white transition-all"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          {/* Products */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {loadingRelatedProducts ? (
              <div className="col-span-full text-center py-10 text-zinc-400">
                Loading products...
              </div>
            ) : (
              visibleRelatedProducts.map(
                (p) => (
                  <ProductCard
                    key={p.id}
                    product={p}
                    onClick={(id) => {
                      window.scrollTo({
                        top: 0,
                        behavior: 'smooth',
                      });

                      setPage(
                        'detail'
                      );
                    }}
                  />
                )
              )
            )}
          </div>

          {/* Right Arrow */}
          <button
            onClick={
              handleNextRelatedProducts
            }
            className="absolute right-[-20px] top-1/2 -translate-y-1/2 z-10 w-12 h-12 rounded-full bg-white border border-zinc-200 shadow-lg flex items-center justify-center hover:bg-zinc-900 hover:text-white transition-all"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </section>
    </div>
    </>
  );
}
