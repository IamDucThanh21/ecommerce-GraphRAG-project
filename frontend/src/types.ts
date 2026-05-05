/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface Product {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  category: string;
  brand: string;
  rating: number;
  reviewsCount: number;
  badges?: string[];
  specs?: { [key: string]: string };
  description?: string;
  features?: string[];
  colors?: string[];
  storageOptions?: string[];
}

export interface NewsItem {
  id: string;
  title: string;
  excerpt: string;
  date: string;
  image: string;
}

export interface AccessoryCategory {
  id: string;
  name: string;
  icon: string;
}

export type Page = 'home' | 'listing' | 'detail' | 'auth';
