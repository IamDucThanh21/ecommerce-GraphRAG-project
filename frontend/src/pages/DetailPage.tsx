/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useState } from 'react';
import { Star, ShieldCheck, Truck, RotateCcw, Heart, Share2, ChevronLeft, ChevronRight, ChevronDown, ChevronUp, Maximize2, MessageSquare } from 'lucide-react';
import { PRODUCTS } from '../data';
import { Page } from '../types';
import ProductCard from '../components/ProductCard';
import { ToastContainer, toast } from "react-toastify";

import { apiClient, ProductVariant, CommentDetail, ReviewSummary, ReviewTagGroup } from '../api/client';

interface DetailPageProps {
  productId: string;
  categoryId: string;
  setProductId: (id: string) => void;
  setCategoryId: (id: string) => void;
  setPage: (page: Page) => void;
}

export default function DetailPage({productId, categoryId, setPage, setProductId,  setCategoryId}: DetailPageProps) {
  const [selectedStar, setSelectedStar] = useState<number | null>(null);
  // const product = PRODUCTS.find((p) => p.id === productId) || PRODUCTS[0];
  const [showAllSpecs, setShowAllSpecs] = useState(false);

  const [selectedSpecGroup, setSelectedSpecGroup] = useState(0);

  const [variants, setVariants] = useState<ProductVariant[]>([]);

  const [selectedVariant, setSelectedVariant] = useState<ProductVariant | null>(null);

  const [reviewSummary, setReviewSummary] =
  useState<ReviewSummary | null>(null);

  const [reviewGroups, setReviewGroups] =
    useState<ReviewTagGroup[]>([]);

  const handleRelatedProductClick = (
    id: string,
    categoryId?: string
  ) => {
    setProductId(id);

    if (categoryId) {
      setCategoryId(categoryId);
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });

    setPage("detail");
  };

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
    Auth check
  ----------------------------- */

  const [isAuthenticated, setIsAuthenticated] = useState(apiClient.isAuthenticated());

  useEffect(() => {
      const checkAuth = () =>
        setIsAuthenticated(apiClient.isAuthenticated());

      checkAuth();

      window.addEventListener('auth-change', checkAuth);

      return () => {
        window.removeEventListener(
          'auth-change',
          checkAuth
        );
      };
    }, []);
    

    const handleSubmitReview = async () => {
    // Chưa đăng nhập
    if (!apiClient.isAuthenticated()) {
      toast.warning('Xin vui lòng đăng nhập');
      return;
    }

    // Chưa load product
    if (!product) {
      toast.error('Không tìm thấy thông tin sản phẩm.');
      return;
    }

    // Chưa nhập nội dung
    if (!reviewContent.trim()) {
      toast.warning('Vui lòng nhập nội dung đánh giá.');
      return;
    }

    // Chưa chọn số sao
    if (reviewStar < 1 || reviewStar > 5) {
      toast.warning('Vui lòng chọn số sao.');
      return;
    }

    try {
      // Lấy id của option tương ứng với từng group
      const tagOptionIds = Object.entries(groupRatings)
        .map(([groupId, star]) => {
          const option = tagOptions[groupId]?.find(
            (o) => o.option_sort_order === star
          );

          return option?.id;
        })
        .filter(Boolean) as string[];

      const payload = {
        resource_type: 'product',
        resource_id: product.id,
        content: reviewContent.trim(),
        star: reviewStar,
        tag_option_ids: tagOptionIds,
      };

      console.log('Create comment payload:', payload);
      
      console.log(localStorage.getItem("auth_token"));
      
      await apiClient.createComment(payload);

      toast.success('Đánh giá thành công!');

      // Reset form
      setReviewContent('');
      setReviewStar(5);

      setHoverStar(0);

      setGroupRatings({});
      setHoverGroupRatings({});

      // Reload comment list
      const [commentRes, allCommentRes, summaryRes] =
        await Promise.all([
          apiClient.commentList({
            resourceId: product.id,
            page: 1,
            limit: 25,
            star: selectedStar ?? undefined,
          }),

          apiClient.commentList({
            resourceId: product.id,
            page: 1,
            limit: 1000,
          }),

          apiClient.getCommentSummary(product.id),
        ]);

      setComments(commentRes.data ?? []);
      setAllComments(allCommentRes.data ?? []);
      setReviewSummary(summaryRes);
    } catch (error) {
      console.error(error);

      toast.error('Không thể gửi đánh giá.');
    }
  };

  /* -----------------------------
    Reviews get data
  ----------------------------- */
  const [comments, setComments] = useState<CommentDetail[]>([]);
  const [commentLoading, setCommentLoading] = useState(false);

  const [allComments, setAllComments] = useState<CommentDetail[]>([]);
  useEffect(() => {
    if (!product?.id) return;

    const loadAllComments = async () => {
      try {
        const response = await apiClient.commentList({
          resourceId: product.id,
          page: 1,
          limit: 1000,
        });

        setAllComments(response.data ?? []);
      } catch (error) {
        console.error(error);
      }
    };

    loadAllComments();
  }, [product?.id]);

  useEffect(() => {
    if (!product?.id) return;

    const loadComments = async () => {
      try {
        setCommentLoading(true);

        const response = await apiClient.commentList({
          resourceId: product.id,
          page: 1,
          limit: 25,
          star: selectedStar ?? undefined,
        });
        setComments(response.data ?? []);
      } catch (error) {
        console.error(error);
      } finally {
        setCommentLoading(false);
      }
    };

    loadComments();
  }, [product?.id, selectedStar]);

  const formatCommentDate = (date: string) => {
    return new Date(date).toLocaleDateString('vi-VN');
  };

  const avatarColors = [
    'bg-red-500',
    'bg-orange-500',
    'bg-amber-500',
    'bg-yellow-500',
    'bg-lime-500',
    'bg-green-500',
    'bg-emerald-500',
    'bg-teal-500',
    'bg-cyan-500',
    'bg-sky-500',
    'bg-blue-500',
    'bg-indigo-500',
    'bg-violet-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-rose-500',
  ];

  const getAvatarLetter = (comment: CommentDetail) => {
    return comment.name_user?.charAt(0)?.toUpperCase() || 'U';
  };

  const getAvatarColor = (name?: string | null) => {
    if (!name) {
      return 'bg-gray-500';
    }

    const hash = name
      .split('')
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);

    return avatarColors[hash % avatarColors.length];
  };

  const averageRating =
    allComments.length > 0
      ? (
          allComments.reduce((sum, c) => sum + c.star, 0) /
          allComments.length
        ).toFixed(1)
      : '0.0';


  const [reviewStar, setReviewStar] = useState<number>(5);
  const [hoverStar, setHoverStar] = useState<number>(0);  
  const [selectedTags, setSelectedTags] = useState<Record<string, string>>({});
  
  type ReviewTagOption = {
    id: string;
    group_id: string;
    option_name: string;
    option_sort_order: number; // 1 -> 5 stars
  };

  const [tagOptions, setTagOptions] = useState<Record<string, ReviewTagOption[]>  >({});
  const [groupRatings, setGroupRatings] = useState<Record<string, number>>({});

  const [hoverGroupRatings, setHoverGroupRatings] = useState<Record<string, number>>({});
  
  useEffect(() => {
    if (!reviewGroups.length) return;

    const loadTagOptions = async () => {
      try {
        const responses = await Promise.all(
          reviewGroups.map((group) =>
            apiClient.reviewTagOptionList(
              group.id
            )
          )
        );

        const optionMap: Record<
          string,
          ReviewTagOption[]
        > = {};

        reviewGroups.forEach(
          (group, index) => {
            optionMap[group.id] =
              responses[index].data.sort(
                (a, b) =>
                  a.option_sort_order -
                  b.option_sort_order
              );
          }
        );

        setTagOptions(optionMap);

        console.log(
          'tag options loaded',
          optionMap
        );
      } catch (error) {
        console.error(error);
      }
    };

    loadTagOptions();
  }, [reviewGroups]);
  const getGroupOptionText = (
    groupId: string,
    star: number
  ) => {
    const options = tagOptions[groupId] ?? [];
    console.log(
      'groupId=',
      groupId,
      'star=',
      star,
      'options=',
      options
    );

    return (
      options.find(
        (o) => o.option_sort_order === star
      )?.option_name ?? ''
    );
  };

  const [reviewContent, setReviewContent] = useState('');

  const getSelectedOptionIds = () => {
    return Object.entries(groupRatings)
      .map(([groupId, star]) => {
        const option = tagOptions[groupId]?.find(
          (o) => o.option_sort_order === star
        );

        return option?.id;
      })
      .filter(Boolean) as string[];
  };
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

          // console.log(
          //   'Product detail:',
          //   response
          // );

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

  useEffect(() => {
    if (!product?.id || !product?.category_id) return;

    const loadReviewMeta = async () => {
      try {
        const [groupsResult, summaryResult] =
          await Promise.allSettled([
            apiClient.getReviewTagGroups(product.category_id),
            apiClient.getCommentSummary(product.id),
          ]);

        if (groupsResult.status === "fulfilled") {
          setReviewGroups(groupsResult.value.data ?? []);
        }

        if (summaryResult.status === "fulfilled") {
          setReviewSummary(summaryResult.value);
        } else {
          setReviewSummary({
            average_star: 0,
            num_comments: 0,
            groups: [],
          });
        }
      } catch (error) {
        console.error(error);
      }
    };

    loadReviewMeta();
  }, [product?.id, product?.category_id]);

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

      {/* Reviews Section */}
      <section className="mt-16">
        <div className="bg-stone-50 rounded-3xl p-6 lg:p-10 border border-stone-200">

          <h2 className="text-4xl font-bold text-stone-900 mb-8">
            Đánh giá & nhận xét
          </h2>

          {/* ================= TOP ROW ================= */}
          <div className="grid lg:grid-cols-12 gap-6 items-start">

            {/* Rating */}
            <div className="lg:col-span-2">
              <div className="flex items-end gap-2">
                <span className="text-6xl font-bold">
                  {reviewSummary?.average_star?.toFixed(1) ?? '0.0'}
                </span>

                <span className="text-3xl text-stone-400 mb-1">
                  /5
                </span>
              </div>

              <div className="flex mt-2">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Star
                    key={s}
                    className={`w-5 h-5 ${
                      s <= Math.round(reviewSummary?.average_star ?? 0)
                        ? 'fill-yellow-400 text-yellow-400'
                        : 'text-stone-300'
                    }`}
                  />
                ))}
              </div>

              <div className="mt-2 text-sm text-stone-500">
                {reviewSummary?.num_comments ?? 0} lượt đánh giá
              </div>
            </div>

            {/* Experience */}
            <div className="lg:col-span-4 border-l border-stone-200 pl-5 -ml-7">
              <h3 className="font-semibold text-stone-800 mb-3">
                Đánh giá theo trải nghiệm
              </h3>

              <div className="space-y-3">
                {reviewGroups
                  ?.sort((a, b) => a.sort_order - b.sort_order)
                  .map((group) => {
                    const summary =
                      reviewSummary?.groups?.find(
                        (g) => g._id === group.id
                      );

                    return (
                      <div
                        key={group.id}
                        className="flex items-center"
                      >
                        <div className="w-36 text-sm text-stone-700">
                          {group.name}
                        </div>

                        <div className="ml-auto flex items-center gap-3">
                          <div className="flex">
                            {[1, 2, 3, 4, 5].map((s) => (
                              <Star
                                key={s}
                                className={`w-4 h-4 ${
                                  s <= Math.round(summary?.average ?? 0)
                                    ? "fill-yellow-400 text-yellow-400"
                                    : "text-stone-300"
                                }`}
                              />
                            ))}
                          </div>

                          <span className="text-sm font-medium">
                            {(summary?.average ?? 0).toFixed(1)}/5
                          </span>

                          <span className="text-sm text-stone-400 whitespace-nowrap">
                            ({summary?.num_vote ?? 0} đánh giá)
                          </span>
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            {/* Star Distribution */}
            <div className="lg:col-span-6 border-l border-stone-200 pl-5">
              <h3 className="font-semibold text-stone-800 mb-3">
                Đánh giá theo số sao
              </h3>

              <div className="space-y-3">
                {[5, 4, 3, 2, 1].map((star) => {
                  const count = allComments.filter(
                    (c) => c.star === star
                  ).length;

                  return (
                    <div
                      key={star}
                      className="flex items-center gap-3"
                    >
                      <span className="w-10 text-sm">
                        {star} sao
                      </span>

                      <div className="flex-1 h-2 rounded-full bg-stone-200 overflow-hidden">
                        <div
                          className="h-full bg-yellow-400"
                          style={{
                            width: `${
                              allComments.length
                                ? (count / allComments.length) * 100
                                : 0
                            }%`,
                          }}
                        />
                      </div>

                      <span className="w-8 text-sm text-stone-500">
                        {count}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

          </div>

          {/* ================= BOTTOM ROW ================= */}
          <div className="grid lg:grid-cols-12 gap-8 items-start mt-4">

            {/* Write Review */}
            <div className="lg:col-span-5 border-r border-stone-200 pr-8">
              <div className="mb-8">
                <h3 className="font-bold text-xl mb-6">
                  Đánh giá chung
                </h3>

                <div className="flex justify-between">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onMouseEnter={() =>
                        setHoverStar(star)
                      }
                      onMouseLeave={() =>
                        setHoverStar(0)
                      }
                      onClick={() =>
                        setReviewStar(star)
                      }
                      className="flex flex-col items-center gap-2"
                    >
                      <Star
                        className={`w-8 h-8 ${
                          star <=
                          (hoverStar || reviewStar)
                            ? 'fill-yellow-400 text-yellow-400'
                            : 'text-stone-300'
                        }`}
                      />
                      <span className="text-sm">
                        {[
                          '',
                          'Rất tệ',
                          'Tệ',
                          'Bình thường',
                          'Tốt',
                          'Tuyệt vời',
                        ][star]}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-8">
                <h3 className="font-bold text-xl mb-6">
                  Theo trải nghiệm
                </h3>

                <div className="space-y-4">
                  {reviewGroups
                    ?.sort((a, b) => a.sort_order - b.sort_order)
                    .map((group) => {
                      const hoverValue =
                        hoverGroupRatings[group.id];

                      const currentValue =
                        hoverValue && hoverValue > 0
                          ? hoverValue
                          : groupRatings[group.id] ?? 0;

                      return (
                        <div
                          key={group.id}
                          className="
                            grid
                            grid-cols-[140px_150px_220px]
                            items-center
                            gap-4
                          "
                        >
                          {/* Group name */}
                          <div className="text-stone-700 text-lg">
                            {group.name}
                          </div>

                          {/* Stars */}
                          <div className="flex gap-1">
                            {[1, 2, 3, 4, 5].map((star) => (
                              <Star
                                key={star}
                                onMouseEnter={() =>
                                  setHoverGroupRatings((prev) => ({
                                    ...prev,
                                    [group.id]: star,
                                  }))
                                }
                                onMouseLeave={() =>
                                  setHoverGroupRatings((prev) => {
                                    const next = { ...prev };
                                    delete next[group.id];
                                    return next;
                                  })
                                }
                                onClick={() =>
                                  setGroupRatings((prev) => ({
                                    ...prev,
                                    [group.id]: star,
                                  }))
                                }
                                className={`w-5 h-5 cursor-pointer ${
                                  star <= currentValue
                                    ? 'fill-yellow-400 text-yellow-400'
                                    : 'text-stone-300'
                                }`}
                              />
                            ))}
                          </div>

                          {/* Option text */}
                          <div className="text-stone-600 text-base">
                            {getGroupOptionText(
                              group.id,
                              currentValue
                            )}
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>

              <h3 className="font-semibold text-stone-800 mb-4">
                Viết đánh giá
              </h3>

              <div className="border border-stone-200 rounded-2xl bg-white p-5">

                <textarea
                  rows={5}
                  placeholder="Xin mời chia sẻ cảm nhận về sản phẩm..."
                  className="
                    w-full
                    rounded-xl
                    border
                    border-stone-200
                    p-3
                    resize-none
                    outline-none
                  "
                  value={reviewContent}
                    onChange={(e) => setReviewContent(e.target.value)}
                />

                <button
                  onClick={handleSubmitReview}
                  className="
                    mt-4
                    w-full
                    py-3
                    rounded-xl
                    bg-red-600
                    text-white
                    font-semibold
                    hover:bg-red-700
                  "
                >
                  Gửi đánh giá
                </button>
              </div>
            </div>

            {/* Customer Reviews */}
            <div className="lg:col-span-7">

              <h3 className="font-semibold text-stone-800 mb-4">
                Nhận xét từ khách hàng
              </h3>

                <div className="flex flex-wrap gap-2 mb-4">
                    <button
                      onClick={() => setSelectedStar(null)}
                      className={`
                        px-4 py-2 rounded-full text-sm
                        ${
                          selectedStar === null
                            ? 'bg-blue-600 text-white'
                            : 'bg-stone-100 text-stone-700'
                        }
                      `}
                    >
                      Tất cả
                    </button>

                    {[5, 4, 3, 2, 1].map((star) => (
                      <button
                        key={star}
                        onClick={() => setSelectedStar(star)}
                        className={`
                          px-4 py-2 rounded-full text-sm transition
                          ${
                            selectedStar === star
                              ? 'bg-blue-600 text-white'
                              : 'bg-stone-100 text-stone-700 hover:bg-stone-200'
                          }
                        `}
                      >
                        {star} sao
                      </button>
                    ))}
                  </div>

              <div
                  className="
                    space-y-4
                    max-h-[800px]
                    overflow-y-auto
                    pr-2
                  "
                >

                  {comments.map((comment) => (
                    <div
                      key={comment.id}
                      className="
                        bg-white
                        rounded-2xl
                        border
                        border-stone-200
                        p-4
                        shadow-sm
                      "
                    >

                      {/* Header */}
                      <div className="flex justify-between items-start gap-4">

                        <div className="flex gap-3">

                          <div
                            className={`
                              w-10
                              h-10
                              rounded-full
                              text-white
                              flex
                              items-center
                              justify-center
                              font-semibold
                              ${getAvatarColor(comment.name_user)}
                            `}
                          >
                            {getAvatarLetter(comment)}
                          </div>

                          <div>
                            <div className="font-semibold text-stone-900">
                              {comment.name_user ?? 'Người dùng'}
                            </div>

                            <div className="text-xs text-stone-400">
                              {formatCommentDate(comment.created)}
                            </div>
                          </div>

                        </div>

                        <div className="flex">
                          {[1, 2, 3, 4, 5].map((s) => (
                            <Star
                              key={s}
                              className={`w-4 h-4 ${
                                s <= comment.star
                                  ? 'fill-yellow-400 text-yellow-400'
                                  : 'text-stone-300'
                              }`}
                            />
                          ))}
                        </div>

                      </div>
                      {/* Tags */}
                      {comment.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-4">
                          {comment.tags.map((tag) => (
                            <span
                              key={tag.option_id}
                              className="
                                px-2.5
                                py-1
                                rounded-md
                                bg-stone-100
                                text-xs
                                text-stone-600
                              "
                            >
                              {tag.option_name}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Content */}
                      <p className="mt-4 text-sm text-stone-700 leading-relaxed">
                        {comment.content}
                      </p>
                    </div>
                  ))}
                </div>
            </div>
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
                  // <ProductCard
                  //   key={p.id}
                  //   product={p}
                  //   onClick={(id) => {
                  //     window.scrollTo({
                  //       top: 0,
                  //       behavior: 'smooth',
                  //     });

                  //     setPage(
                  //       'detail'
                  //     );
                  //   }}
                  // />
                  <ProductCard
                    key={p.id}
                    product={p}
                    onClick={handleRelatedProductClick}
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
