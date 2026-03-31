// ---- API Response Types ----
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  errors: string[];
}

export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

// ---- Domain Types ----
export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface Portfolio {
  id: string;
  name: string;
  description: string;
  initial_capital: number;
  cash_balance: number;
  is_paper: boolean;
  created_at: string;
}

export interface Position {
  id: string;
  portfolio_id: string;
  symbol: string;
  quantity: number;
  avg_entry_price: number;
  current_price: number;
  created_at: string;
}

export interface Strategy {
  id: string;
  name: string;
  description: string;
  strategy_type: string;
  symbols: string[];
  parameters: Record<string, unknown>;
  status: "draft" | "active" | "paused" | "stopped";
  is_paper: boolean;
  created_at: string;
}

export interface Order {
  id: string;
  portfolio_id: string;
  strategy_id: string | null;
  symbol: string;
  side: "buy" | "sell";
  order_type: "market" | "limit" | "stop" | "stop_limit";
  quantity: number;
  limit_price: number | null;
  stop_price: number | null;
  filled_price: number | null;
  filled_quantity: number | null;
  status: "pending" | "submitted" | "filled" | "partially_filled" | "cancelled" | "rejected";
  broker_order_id: string | null;
  created_at: string;
}

export interface Watchlist {
  id: string;
  name: string;
  items: WatchlistItem[];
  created_at: string;
}

export interface WatchlistItem {
  id: string;
  symbol: string;
  notes: string;
  created_at: string;
}

export interface Alert {
  id: string;
  symbol: string;
  condition: "price_above" | "price_below" | "percent_change_up" | "percent_change_down";
  threshold: number;
  is_triggered: boolean;
  is_active: boolean;
  message: string;
  created_at: string;
}

export interface MarketQuote {
  symbol: string;
  price: number;
  previous_close: number;
  open: number;
  day_high: number;
  day_low: number;
  volume: number;
  market_cap: number;
  name: string;
  currency: string;
}
