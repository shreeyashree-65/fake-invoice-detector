import axios from 'axios';
import { InvoiceData, PredictionResult, ApiResponse } from '../types/types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async healthCheck(): Promise<any> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('API health check failed');
    }
  },

  // Main prediction endpoint
  async predictInvoice(invoiceData: InvoiceData): Promise<ApiResponse> {
    try {
      const response = await api.post<PredictionResult>('/predict', invoiceData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Prediction failed',
      };
    }
  },

  // Random Forest prediction
  async predictRandomForest(invoiceData: InvoiceData): Promise<ApiResponse> {
    try {
      const response = await api.post<PredictionResult>('/predict/random_forest', invoiceData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Random Forest prediction failed',
      };
    }
  },

  // XGBoost prediction
  async predictXGBoost(invoiceData: InvoiceData): Promise<ApiResponse> {
    try {
      const response = await api.post<PredictionResult>('/predict/xgboost', invoiceData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'XGBoost prediction failed',
      };
    }
  },

  // Get feature names
  async getFeatureNames(): Promise<string[]> {
    try {
      const response = await api.get('/features');
      return response.data.features;
    } catch (error) {
      throw new Error('Failed to get feature names');
    }
  },
};

export default apiService;
