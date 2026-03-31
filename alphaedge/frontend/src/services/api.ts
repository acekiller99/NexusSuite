import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ---- Auth ----
export const authApi = {
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post("/auth/register", data),
  login: (data: { username: string; password: string }) =>
    api.post("/auth/login", data, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }),
  me: () => api.get("/auth/me"),
};

// ---- Portfolios ----
export const portfolioApi = {
  list: () => api.get("/portfolios"),
  create: (data: { name: string; initial_capital: string; is_paper: boolean }) =>
    api.post("/portfolios", data),
  get: (id: string) => api.get(`/portfolios/${id}`),
  positions: (id: string) => api.get(`/portfolios/${id}/positions`),
};

// ---- Strategies ----
export const strategyApi = {
  list: () => api.get("/strategies"),
  create: (data: Record<string, unknown>) => api.post("/strategies", data),
  get: (id: string) => api.get(`/strategies/${id}`),
  update: (id: string, data: Record<string, unknown>) => api.patch(`/strategies/${id}`, data),
};

// ---- Orders ----
export const orderApi = {
  list: (portfolioId?: string) =>
    api.get("/orders", { params: portfolioId ? { portfolio_id: portfolioId } : {} }),
  create: (data: Record<string, unknown>) => api.post("/orders", data),
  get: (id: string) => api.get(`/orders/${id}`),
};

// ---- Watchlists ----
export const watchlistApi = {
  list: () => api.get("/watchlists"),
  create: (data: { name: string }) => api.post("/watchlists", data),
  addItem: (watchlistId: string, data: { symbol: string; notes?: string }) =>
    api.post(`/watchlists/${watchlistId}/items`, data),
  removeItem: (watchlistId: string, itemId: string) =>
    api.delete(`/watchlists/${watchlistId}/items/${itemId}`),
};

// ---- Alerts ----
export const alertApi = {
  list: () => api.get("/alerts"),
  create: (data: Record<string, unknown>) => api.post("/alerts", data),
  update: (id: string, data: Record<string, unknown>) => api.patch(`/alerts/${id}`, data),
  delete: (id: string) => api.delete(`/alerts/${id}`),
};

// ---- Market Data ----
export const marketApi = {
  quote: (symbol: string) => api.get(`/market/quote/${symbol}`),
  history: (symbol: string, period?: string, interval?: string) =>
    api.get(`/market/history/${symbol}`, { params: { period, interval } }),
  search: (q: string) => api.get("/market/search", { params: { q } }),
};
