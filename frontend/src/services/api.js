import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const predictionService = {
  // Make a churn prediction
  predict: async (customerData) => {
    try {
      const response = await api.post('/predict', customerData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Prediction failed' };
    }
  },

  // Get dashboard statistics
  getDashboard: async () => {
    try {
      const response = await api.get('/dashboard');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to load dashboard' };
    }
  },

  // Get prediction history
  getHistory: async (page = 1, limit = 20) => {
    try {
      const response = await api.get('/history', {
        params: { page, limit },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to load history' };
    }
  },

  // Health check
  health: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Server unavailable' };
    }
  },
};

export default api;
