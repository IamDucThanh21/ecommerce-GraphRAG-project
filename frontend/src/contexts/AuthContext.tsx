/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiClient } from '../api/client';

export interface User {
  id: string;
  username: string;
  email?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signUp: (username: string, email: string, password: string, firstName?: string, lastName?: string, phone?: string) => Promise<void>;
  logOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in on mount
  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('auth_token');

    if (userId && username && token && apiClient.isAuthenticated()) {
      setUser({ id: userId, username });
    }
    setIsLoading(false);
  }, []);

  const signIn = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.signIn({ username, password });
      setUser({
        id: response.data.user_id,
        username: response.data.username,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const signUp = async (
    username: string,
    email: string,
    password: string,
    firstName?: string,
    lastName?: string,
    phone?: string
  ) => {
    setIsLoading(true);
    try {
      const response = await apiClient.signUp({
        username,
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        phone,
      });
      setUser({
        id: response.data.user_id,
        username: response.data.username,
        email: response.data.email,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const logOut = async () => {
    setIsLoading(true);
    try {
      await apiClient.logOut();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        signIn,
        signUp,
        logOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
