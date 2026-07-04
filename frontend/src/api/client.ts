/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface SignInRequest {
  username: string;
  password: string;
}

export interface SignInResponse {
  status: string;
  message: string;
  data: {
    user_id: string;
    username: string;
    access_token: string;
    token_type: string;
    expires_in: number;
    session_id: string;
  };
}

export interface SignUpRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export interface SignUpResponse {
  status: string;
  message: string;
  data: {
    user_id: string;
    username: string;
    email: string;
    access_token: string;
    token_type: string;
    expires_in: number;
  };
}

interface SignOutResponse {
  data: {
    'user-logout-response': {
      user_id: string;
      session_id: string;
      logged_out_at: string;
    };
  };
  status: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
}


export interface CategoryListResponse {
  status?: string;
  message?: string;
  data?: Category[];
  pagination?: {
    limit: number;
    offset: number;
    page: number;
    total: number;
    pages: number;
  };
}

export interface Brand {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
  logo_url?: string | null;
  category_name?: string;
}

export interface CategoryBrandListResponse {
  status?: string;
  message?: string;
  data?: Brand[];
  pagination?: {
    limit: number;
    offset: number;
    page: number;
    total: number;
    pages: number;
  };
}

export interface ProductListRequest {
  category_id: string;
  brand_id?: string;
  page?: number;
  limit?: number;
  sort?: string;
  price_min?: number;
  price_max?: number;
}

export interface ProductListResponse {
  status?: string;
  message?: string;
  data?: unknown[];
  pagination?: unknown;
}

export interface ProductDetailSpecValue {
  key: string;
  label: string;
  value_text: string | null;
  value_number: number | null;
  value_boolean: boolean | null;
  value_unit: string | null;
  is_filterable: boolean;
  sort_order: number;
}

export interface ProductDetailSpecGroup {
  group_id: string;
  group_name: string;
  sort_order: number;
  values: ProductDetailSpecValue[];
}

export interface ProductDetailResponse {
  id: string;
  created: string;
  updated: string | null;
  name: string;
  description: string;
  slug: string;
  status: string;

  brand_id: string;
  brand_name: string;
  brand_slug: string;
  brand_logo_url: string | null;

  category_id: string;
  primary_category_name: string;

  primary_image_url: string | null;
  image_urls: string[];

  variant_count: number;
  price_min: number;
  price_max: number;
  total_stock: number;

  spec_groups: ProductDetailSpecGroup[];
}

export interface ProductVariant {
  id: string;
  created: string;
  updated: string | null;

  product_id: string;
  product_name: string;
  product_slug: string;
  product_status: string;

  sku: string;

  price: number;
  base_price: number;

  stock_quantity: number;
  status: string;
  tag: string | null;

  attributes: {
    color?: string;
    [key: string]: unknown;
  };

  primary_image_url: string | null;
  image_urls: string[];

  specs: Record<string, unknown> | null;
}

export interface ProductVariantListResponse {
  data: ProductVariant[];
  pagination: {
    limit: number;
    offset: number;
    page: number;
    total: number;
    pages: number;
  };
}

export interface SearchProductResponse {
  data: ProductVariant[];
  pagination: {
    limit: number;
    offset: number;
    page: number;
    total: number;
    pages: number;
  };
}

export interface CreateConversationRequest {
  title: string;
}

export interface CreateConversationResponse {
  data: {
    'conversation-service-response': {
      user_id: string;
      title: string;
      status: string;
      version: number;
      _id: string;
      _created: string;
      _updated: string;
      _creator: string;
      _etag: string;
    };
  };
  status: string;
}

// Comment data
export interface CommentTag {
  option_id: string;
  option_name: string;
  group_id: string;
  group_name: string;
}

export interface CommentDetail {
  id: string;
  created: string;
  updated: string | null;
  resource_type: string;
  resource_id: string;
  user_id: string | null;
  name_user: string;
  parent_id: string | null;
  depth: number;
  content: string;
  star: number;
  reply_count: number;
  reaction_count: number;
  reaction_summary: Record<string, number>;
  tags: CommentTag[];
}

export interface CommentListResponse {
  data: CommentDetail[];
}

export interface CommentListResponse {
  data: CommentDetail[];
}

export interface SendMessageRequest {
  content: string;
}

export interface SendMessageResponse {
  data: {
    'message-service-response': {
      user_message: {
        conversation_id: string;
        sequence_number: number;
        role: string;
        content: string;
        _id: string;
      };

      bot_message: {
        conversation_id: string;
        sequence_number: number;
        role: string;
        content: string;
        _id: string;
      };

      product_ids?: string[];
    };
  };
  status: string;
}

export interface ReviewSummaryGroup {
  _id: string;
  group_name: string;
  num_vote: number;
  average: number;
}

export interface ReviewSummary {
  id: string;
  resource_type: string;
  num_comments: number;
  average_star: number;
  groups: ReviewSummaryGroup[];
}

export interface ReviewTagGroup {
  id: string;
  name: string;
  sort_order: number;
  category_id: string;
}

export interface ReviewTagOption {
  id: string;
  group_id: string;
  option_name: string;
  option_sort_order: number;
  group_name: string;
  group_sort_order: number;
  category_id: string;
}

export interface ReviewTagOptionListResponse {
  data: ReviewTagOption[];
  pagination: {
    limit: number;
    offset: number;
    page: number;
    total: number;
    pages: number;
  };
}

export interface CreateCommentRequest {
  resource_type: string;
  resource_id: string;
  content: string;
  star: number;
  tag_option_ids: string[];
}

export interface CreateCommentResponse {
  data: {
    "comment-service-response": {
      _id: string;
      resource_type: string;
      resource_id: string;
      user_id: string;
      depth: number;
      content: string;
      star: number;
    };
  };
  status: string;
}

const encodeQuery = (queryObject: Record<string, unknown>) =>
  encodeURIComponent(JSON.stringify(queryObject));

class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.loadToken();
  }

  private loadToken(): void {
    this.token = localStorage.getItem('auth_token');
  }

  private saveToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
    window.dispatchEvent(new Event('auth-change'));
  }

  public getToken(): string | null {
    return this.token;
  }

  public clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');

    window.dispatchEvent(new Event('auth-change'));
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: unknown,
    skipAuth = false
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const headers: Record<string, string> = {
      Accept: 'application/json',
    };

    // Only add content-type when sending body
    if (data !== undefined) {
      headers['Content-Type'] = 'application/json';
    }

    // Always get latest token from localStorage
    // Avoid stale this.token issue
    const token = localStorage.getItem('auth_token');

    if (!skipAuth && token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const options: RequestInit = {
      method,
      headers,
    };

    // Add body if exists
    if (data !== undefined) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);

      // Handle non-JSON error safely
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}`;

        try {
          const errorData = await response.json();
          errorMessage =
            errorData?.message ||
            errorData?.detail ||
            errorMessage;
        } catch {
          // ignore json parsing error
        }

        throw new Error(errorMessage);
      }

      // Handle empty response body
      const contentType =
        response.headers.get('content-type');

      if (
        contentType &&
        contentType.includes('application/json')
      ) {
        return await response.json();
      }

      return {} as T;
    } catch (error) {
      console.error(
        'API request failed:',
        error
      );
      throw error;
    }
  }

  public async signIn(
  credentials: SignInRequest
  ): Promise<SignInResponse> {

    const response = await this.request<SignInResponse>(
        'POST',
        '/ecom-client:sign-in/user/:new',
        credentials
      );

    const signInData = response.data['user-signin-response'];
    if (signInData?.access_token) {
      this.saveToken(
        signInData.access_token
      );
      localStorage.setItem('user_id', signInData.user_id);
      localStorage.setItem('username', signInData.username );
    }
    return response;
  }

  public async signUp(data: SignUpRequest): Promise<SignUpResponse> {
    const response = await this.request<SignUpResponse>(
      'POST',
      '/ecom-client:sign-up/user/:new',
      data
    );

    const signUpData = response.data['user-signup-response'];

    if (signUpData?.access_token) {
      this.saveToken(signUpData.access_token);
      localStorage.setItem('user_id', signUpData.user_id);
      localStorage.setItem('username', signUpData.username);
    }

    return response;
  }

  public async signOut(): Promise<SignOutResponse> {
    try {
      const response = await this.request<SignOutResponse>(
        'POST',
        '/ecom-client:sign-out/user_session/:new',
        {}
      );

      this.clearToken();

      return response;
    } catch (error) {
      console.error('Sign out failed:', error);

      // still clear local auth even if backend fails
      this.clearToken();

      throw error;
    }
  }

  // public isAuthenticated(): boolean {
  //   return !!this.token;
  // }
  public isAuthenticated(): boolean {
    return !!localStorage.getItem(
      'auth_token'
    );
  }

  public async categoryList(): Promise<CategoryListResponse> {
    return this.request<CategoryListResponse>(
      'GET',
      '/ecom-product.category-list/',
      undefined,
      true
    );
  }

  public async productList(
    params: ProductListRequest
  ): Promise<ProductListResponse | unknown[]> {

    const {
      category_id,
      brand_id,
      page = 1,
      limit = 25,
      sort,
      price_min,
      price_max,
    } = params;

    const queryObject: Record<string, unknown> = {};

    if (brand_id) {
        queryObject['brand_id.eq'] = brand_id;
    }

    if (price_min !== undefined) {
        queryObject['price.gte'] = price_min;
    }

    if (price_max !== undefined) {
        queryObject['price.lte'] = price_max;
    }

    const queryString =
      Object.keys(queryObject).length > 0
        ? `&query=${encodeURIComponent(
            JSON.stringify(queryObject)
          )}`
        : '';
    
    const sortString =
      sort && sort.trim() !== ''
        ? `&sort=${encodeURIComponent(sort)}`
        : '';

    return this.request<ProductListResponse>(
      'GET',
      `/ecom-product.product-list/category_id=${encodeURIComponent(
        category_id
      )}/?limit=${limit}&page=${page}${sortString}${queryString}`,
      undefined,
      true
    );
  }

  public async productListSearch(params: {
    text: string;
    page?: number;
    limit?: number;
  }): Promise<SearchProductResponse> {const searchParams = new URLSearchParams();

    searchParams.append('text', params.text);
    searchParams.append('page', String(params.page ?? 1) );
    searchParams.append('limit', String(params.limit ?? 25));
    return this.request<SearchProductResponse>(
      'GET',
      `/ecom-product.product-list-search/?${searchParams.toString()}`
    );
  }

  public async categoryBrandList(
    categoryId: string,
    page: number = 1,
    limit: number = 25
  ): Promise<CategoryBrandListResponse> {
    return this.request<CategoryBrandListResponse>(
      'GET',
      `/ecom-product.category-brand-list/category_id=${encodeURIComponent(
        categoryId
      )}/?page=${page}&limit=${limit}`,
      undefined,
      true
    );
  }

  public async productDetail(
    categoryId: string,
    productId: string
  ): Promise<ProductDetailResponse> {
    return this.request<ProductDetailResponse>(
      'GET',
      `/ecom-product.product-detail/category_id=${encodeURIComponent(
        categoryId
      )}/${encodeURIComponent(productId)}`,
      undefined,
      true
    );
  }

  public async productVariantList(
    productId: string,
    page: number = 1,
    limit: number = 25
  ): Promise<ProductVariantListResponse> {
    return this.request<ProductVariantListResponse>(
      'GET',
      `/ecom-product.product-variant-list/product_id%3D${encodeURIComponent(
        productId
      )}/?limit=${limit}&page=${page}`,
      undefined,
      true
    );
  }
  public async createConversation(
    data: CreateConversationRequest = {title: '',}
  ): Promise<CreateConversationResponse> {
    const response = 
      await this.request<CreateConversationResponse>(
        'POST',
        '/ecom-message:create-conversation/conversation/:new',
        data
      );
    return response;
  }
  public async sendMessage(
    conversationId: string, data: SendMessageRequest): Promise<SendMessageResponse> {
    const response =
      await this.request<SendMessageResponse>(
        'POST',
        `/ecom-message:send-message/conversation/${conversationId}`,
        data
      );

    return response;
  }

  public async commentList(params: {
    resourceId: string;
    page?: number;
    limit?: number;
    star?: number;
  }): Promise<CommentListResponse> {
    const filter = encodeURIComponent(
      `resource_type=product:resource_id=${params.resourceId}`
    );

    const searchParams = new URLSearchParams();

    searchParams.append(
      'page',
      String(params.page ?? 1)
    );

    searchParams.append(
      'limit',
      String(params.limit ?? 25)
    );

    if (params.star) {
      searchParams.append(
        'query',
        JSON.stringify({
          star: params.star,
        })
      );
    }

    return this.request<CommentListResponse>(
      'GET',
      `/ecom-discuss.comment-detail/${filter}/?${searchParams.toString()}`
    );
  }

  public async getCommentSummary(
    productId: string
  ): Promise<ReviewSummary> {
    return this.request(
      'GET',
      `/ecom-discuss.comment-summary/${productId}`
    );
  }
  
  public async getReviewTagGroups(
    categoryId: string
  ): Promise<{ data: ReviewTagGroup[] }> {
    const filter = encodeURIComponent(
      `category_id=${categoryId}`
    );

    return this.request(
      'GET',
      `/ecom-discuss.review-tag-group/${filter}/?limit=25&page=1`
    );
  }

  public async reviewTagOptionList(
    groupId: string,
    page: number = 1,
    limit: number = 25
  ): Promise<ReviewTagOptionListResponse> {
    return this.request<ReviewTagOptionListResponse>(
      'GET',
      `/ecom-discuss.review-tag-option-list/group_id=${encodeURIComponent(
        groupId
      )}/?page=${page}&limit=${limit}`,
      undefined,
      true
    );
  }

  public async createComment(
    payload: CreateCommentRequest
  ): Promise<CreateCommentResponse> {
    return this.request<CreateCommentResponse>(
      "POST",
      "/ecom-discuss:create-comment/comment/:new",
      payload
    );
  }
}

export const apiClient = new ApiClient(API_BASE_URL);