export interface InvoiceData {
  invoice_id: string;
  vendor_name: string;
  amount: number;
  tax_amount: number;
  tax_rate: number;
  description: string;
  date: string;
}

export interface PredictionResult {
  is_fake: boolean;
  confidence: number;
  model_used: string;
  risk_factors: { [key: string]: string };
}

export interface ApiResponse {
  success: boolean;
  data?: PredictionResult;
  error?: string;
}

export interface FeatureAnalysis {
  feature_name: string;
  value: number;
  risk_level: 'low' | 'medium' | 'high';
  description: string;
}
