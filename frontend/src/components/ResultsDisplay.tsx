import React from 'react';
import {
  Box,
  Typography,
  Alert,
  Chip,
  LinearProgress,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Warning,
  Info,
  Security,
  Assessment,
} from '@mui/icons-material';
import { PredictionResult } from '../types/types';

interface ResultsDisplayProps {
  result: PredictionResult | null;
  loading: boolean;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result, loading }) => {
  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" py={4}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Analyzing Invoice...
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Running ML algorithms to detect fraud patterns
        </Typography>
      </Box>
    );
  }

  if (!result) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" py={4}>
        <Security sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h6" color="text.secondary">
          No Analysis Yet
        </Typography>
        <Typography variant="body2" color="text.secondary" textAlign="center">
          Upload an invoice to see fraud detection results
        </Typography>
      </Box>
    );
  }

  const getResultColor = (isFake: boolean) => {
    return isFake ? 'error' : 'success';
  };

  const getResultIcon = (isFake: boolean) => {
    return isFake ? <Error /> : <CheckCircle />;
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'success';
    if (confidence >= 70) return 'warning';
    return 'error';
  };

  const getRiskFactorIcon = (riskType: string) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      vendor_name: <Warning color="warning" />,
      amount: <Error color="error" />,
      tax_calculation: <Info color="info" />,
      description: <Assessment color="warning" />,
      date: <Warning color="warning" />,
      invoice_id: <Error color="error" />,
    };
    return iconMap[riskType] || <Warning color="warning" />;
  };

  return (
    <Box>
      {/* Main Result */}
      <Alert
        severity={result.is_fake ? 'error' : 'success'}
        icon={getResultIcon(result.is_fake)}
        sx={{ mb: 3 }}
      >
        <Typography variant="h6">
          {result.is_fake ? '🚨 FAKE Invoice Detected' : '✅ Invoice Appears Genuine'}
        </Typography>
        <Typography variant="body2">
          {result.is_fake
            ? 'This invoice shows suspicious patterns indicating potential fraud'
            : 'This invoice passes all authenticity checks'}
        </Typography>
      </Alert>

      {/* Confidence Score */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6">Confidence Score</Typography>
            <Chip
              label={`${result.confidence.toFixed(1)}%`}
              color={getConfidenceColor(result.confidence)}
              variant="filled"
            />
          </Box>
          <LinearProgress
            variant="determinate"
            value={result.confidence}
            color={getConfidenceColor(result.confidence)}
            sx={{ height: 10, borderRadius: 5 }}
          />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Model used: {result.model_used}
          </Typography>
        </CardContent>
      </Card>

      {/* Risk Factors */}
      {Object.keys(result.risk_factors).length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              🔍 Risk Factors Detected
            </Typography>
            <List dense>
              {Object.entries(result.risk_factors).map(([key, value], index) => (
                <React.Fragment key={key}>
                  <ListItem>
                    <ListItemIcon>
                      {getRiskFactorIcon(key)}
                    </ListItemIcon>
                    <ListItemText
                      primary={key.replace(/_/g, ' ').toUpperCase()}
                      secondary={value}
                    />
                  </ListItem>
                  {index < Object.entries(result.risk_factors).length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

      {/* No Risk Factors */}
      {Object.keys(result.risk_factors).length === 0 && !result.is_fake && (
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center">
              <CheckCircle color="success" sx={{ mr: 1 }} />
              <Typography variant="h6">
                No Risk Factors Detected
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              All invoice patterns appear legitimate and consistent with genuine invoices.
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default ResultsDisplay;
