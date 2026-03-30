import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ── Request Interceptor: Add JWT token to every request ──────────────
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ── Response Interceptor: Handle 401 (token expired) ────────────────
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// ── Auth API Endpoints ────────────────────────────────────────────────
export const authAPI = {
  register: (name: string, email: string, password: string) =>
    apiClient.post('/auth/register', { name, email, password }),

  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),
};

// ── Market Data API Endpoints ─────────────────────────────────────────
export const marketAPI = {
  getAllItems: () =>
    apiClient.get('/market/'),

  getBySymbol: (symbol: string) =>
    apiClient.get(`/market/${symbol}`),

  search: (query: string) =>
    apiClient.get('/market/search', { params: { q: query } }),
};

// ── User API Endpoints ────────────────────────────────────────────────
export const userAPI = {
  getMe: () =>
    apiClient.get('/users/me'),

  updateProfile: (data: { name?: string; email?: string }) =>
    apiClient.put('/users/me', data),
};

// ── Watchlist API Endpoints ───────────────────────────────────────────
export const watchlistAPI = {
  getWatchlist: () =>
    apiClient.get('/watchlist/'),

  addToWatchlist: (marketDataId: string) =>
    apiClient.post('/watchlist/', { market_data_id: marketDataId }),

  removeFromWatchlist: (watchlistId: string) =>
    apiClient.delete(`/watchlist/${watchlistId}`),
};

// ── Dashboard API Endpoints ───────────────────────────────────────────
export const dashboardAPI = {
  getSummary: () =>
    apiClient.get('/dashboard/summary'),
};

export default apiClient;
