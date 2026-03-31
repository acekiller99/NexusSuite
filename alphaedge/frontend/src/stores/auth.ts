import { create } from "zustand";
import { authApi } from "@/services/api";

interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email: string, password: string) => {
    const response = await authApi.login({ username: email, password });
    const { access_token, refresh_token } = response.data.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const meResponse = await authApi.me();
    set({ user: meResponse.data.data, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ user: null, isAuthenticated: false });
  },

  fetchMe: async () => {
    try {
      const response = await authApi.me();
      set({ user: response.data.data, isAuthenticated: true });
    } catch {
      set({ user: null, isAuthenticated: false });
    }
  },
}));
