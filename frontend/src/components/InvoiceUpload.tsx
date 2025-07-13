import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Grid,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  OutlinedInput,
  InputAdornment,
} from '@mui/material';
import { Upload, AttachMoney, Receipt, CalendarToday } from '@mui/icons-material';
import { InvoiceData, PredictionResult } from '../types/types';
import { apiService } from '../services/api';

interface InvoiceUploadProps {
  onPrediction: (result: PredictionResult) => void;
  onLoadingChange: (loading: boolean) => void;
  loading: boolean;
}

const InvoiceUpload: React.FC<InvoiceUploadProps> = ({
  onPrediction,
  onLoadingChange,
  loading,
}) => {
  const [formData, setFormData] = useState<InvoiceData>({
    invoice_id: '',
    vendor_name: '',
    amount: 0,
    tax_amount: 0,
    tax_rate: 0.18,
    description: '',
    date: new Date().toISOString().split('T')[0],
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleInputChange = (field: keyof InvoiceData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: field === 'amount' || field === 'tax_amount' || field === 'tax_rate' 
        ? parseFloat(value) || 0 
        : value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    onLoadingChange(true);

    try {
      const response = await apiService.predictInvoice(formData);
      
      if (response.success && response.data) {
        onPrediction(response.data);
        setSuccess('Invoice analyzed successfully!');
      } else {
        setError(response.error || 'Failed to analyze invoice');
      }
    } catch (err) {
      setError('Failed to connect to the API');
    } finally {
      onLoadingChange(false);
    }
  };

  const handleSampleData = () => {
    const sampleInvoices = [
      {
        invoice_id: 'INV-1234',
        vendor_name: 'Microsoft Corporation',
        amount: 1500.00,
        tax_amount: 270.00,
        tax_rate: 0.18,
        description: 'Software licensing and support services',
        date: '2024-01-15',
      },
      {
        invoice_id: 'XYZABC123',
        vendor_name: 'Microsft Corp',
        amount: 10000.00,
        tax_amount: 1800.00,
        tax_rate: 0.18,
        description: 'Miscellaneous services and products',
        date: '2024-01-20',
      },
    ];

    const randomSample = sampleInvoices[Math.floor(Math.random() * sampleInvoices.length)];
    setFormData(randomSample);
  };

  return (
    <Box component=\"form\" onSubmit={handleSubmit}>
      {error && (
        <Alert severity=\"error\" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity=\"success\" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label=\"Invoice ID\"
            value={formData.invoice_id}
            onChange={handleInputChange('invoice_id')}
            required
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position=\"start\">
                  <Receipt />
                </InputAdornment>
              ),
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label=\"Vendor Name\"
            value={formData.vendor_name}
            onChange={handleInputChange('vendor_name')}
            required
            disabled={loading}
          />
        </Grid>

        <Grid item xs={12} sm={4}>
          <FormControl fullWidth>
            <InputLabel>Amount</InputLabel>
            <OutlinedInput
              label=\"Amount\"
              type=\"number\"
              value={formData.amount}
              onChange={handleInputChange('amount')}
              required
              disabled={loading}
              startAdornment={
                <InputAdornment position=\"start\">
                  <AttachMoney />
                </InputAdornment>
              }
            />
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={4}>
          <FormControl fullWidth>
            <InputLabel>Tax Amount</InputLabel>
            <OutlinedInput
              label=\"Tax Amount\"
              type=\"number\"
              value={formData.tax_amount}
              onChange={handleInputChange('tax_amount')}
              required
              disabled={loading}
              startAdornment={
                <InputAdornment position=\"start\">
                  <AttachMoney />
                </InputAdornment>
              }
            />
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label=\"Tax Rate\"
            type=\"number\"
            value={formData.tax_rate}
            onChange={handleInputChange('tax_rate')}
            required
            disabled={loading}
            inputProps={{ step: 0.01, min: 0, max: 1 }}
          />
        </Grid>

        <Grid item xs={12} sm={8}>
          <TextField
            fullWidth
            label=\"Description\"
            value={formData.description}
            onChange={handleInputChange('description')}
            required
            disabled={loading}
            multiline
            rows={2}
          />
        </Grid>

        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label=\"Date\"
            type=\"date\"
            value={formData.date}
            onChange={handleInputChange('date')}
            required
            disabled={loading}
            InputProps={{
              startAdornment: (
                <InputAdornment position=\"start\">
                  <CalendarToday />
                </InputAdornment>
              ),
            }}
          />
        </Grid>

        <Grid item xs={12}>
          <Box display=\"flex\" gap={2}>
            <Button
              type=\"submit\"
              variant=\"contained\"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <Upload />}
              sx={{ flexGrow: 1 }}
            >
              {loading ? 'Analyzing...' : 'Analyze Invoice'}
            </Button>
            
            <Button
              type=\"button\"
              variant=\"outlined\"
              onClick={handleSampleData}
              disabled={loading}
            >
              Sample Data
            </Button>
          </Box>
        </Grid>
      </Grid>

      <Box mt={2}>
        <Typography variant=\"body2\" color=\"text.secondary\">
          💡 Click \"Sample Data\" to load example invoices for testing
        </Typography>
      </Box>
    </Box>
  );
};

export default InvoiceUpload;
