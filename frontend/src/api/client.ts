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
  }

  public getToken(): string | null {
    return this.token;
  }

  public clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
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

    if (data) {
      headers['Content-Type'] = 'application/json';
    }

    if (!skipAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const options: RequestInit = {
      method,
      headers: Object.keys(headers).length > 0 ? headers : undefined,
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  public async signIn(credentials: SignInRequest): Promise<SignInResponse> {
    const response = await this.request<SignInResponse>(
      'POST',
      '/ecom-client/sign-in',
      credentials
    );

    if (response.data.access_token) {
      this.saveToken(response.data.access_token);
      localStorage.setItem('user_id', response.data.user_id);
      localStorage.setItem('username', response.data.username);
    }

    return response;
  }

  public async signUp(data: SignUpRequest): Promise<SignUpResponse> {
    const response = await this.request<SignUpResponse>(
      'POST',
      '/ecom-client/sign-up',
      data
    );

    if (response.data.access_token) {
      this.saveToken(response.data.access_token);
      localStorage.setItem('user_id', response.data.user_id);
      localStorage.setItem('username', response.data.username);
    }

    return response;
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
      queryObject.brand_id = brand_id;
    }

    if (price_min !== undefined) {
      queryObject.price_gte = price_min;
    }

    if (price_max !== undefined) {
      queryObject.price_lte = price_max;
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

  public async logOut(): Promise<void> {
    const userId = localStorage.getItem('user_id');
    if (userId) {
      try {
        await this.request('POST', '/ecom-client/log-out', { user_id: userId });
      } catch (error) {
        console.error('Logout request failed:', error);
      }
    }
    this.clearToken();
  }

  public isAuthenticated(): boolean {
    return !!this.token;
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

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