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
    data?: unknown
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const options: RequestInit = {
      method,
      headers,
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
