import axios from "axios";

// Default to relative path if env var is missing/empty, assuming proxy or same-origin
const BASE_URL = process.env.REACT_APP_BACKEND_URL || "";

const api = axios.create({
  baseURL: `${BASE_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401s globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login if unauthorized
      localStorage.removeItem("token");
      // Optional: Trigger a custom event or use a callback if we had access to history
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
