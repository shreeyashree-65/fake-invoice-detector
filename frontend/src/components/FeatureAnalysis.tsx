import React from 'react';
import { Grid, Paper, Typography, Box, Chip } from '@mui/material';
import { PredictionResult } from '../types/types';

interface FeatureAnalysisProps {
  result: PredictionResult;
}

const FeatureAnalysis: React.FC<FeatureAnalysisProps> = ({ result }) => {
  const getFeatureInsights = () => {
    const insights = [
      {
        name: 'Model Confidence',
        value: result.confidence,
        description: 'Overall confidence in the prediction',
        risk_level: result.confidence >= 90 ? 'low' : result.confidence >= 70 ? 'medium' : 'high'
      },
      {
        name: 'Risk Factors Count',
        value: Object.keys(result.risk_factors).length,
        description: 'Number of suspicious patterns detected',
        risk_level: Object.keys(result.risk_factors).length === 0 ? 'low' : Object.keys(result.risk_factors).length <= 2 ? 'medium' : 'high'
      },
      {
        name: 'Fraud Classification',
        value: result.is_fake ? 100 : 0,
        description: result.is_fake ? 'Classified as fraudulent' : 'Classified as genuine',
        risk_level: result.is_fake ? 'high' : 'low'
      },
      {
        name: 'Model Used',
        value: result.model_used === 'ensemble' ? 100 : 80,
        description: `Prediction made using ${result.model_used} model`,
        risk_level: 'low'
      }
    ];
    
    return insights;
  };

  const getRiskColor = (risk_level: string) => {
    switch (risk_level) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      default: return 'success';
    }
  };

  const insights = getFeatureInsights();

  return (
    <Box>
      <Grid container spacing={2}>
        {insights.map((insight, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">
                  {insight.name}
                </Typography>
                <Chip
                  label={insight.risk_level.toUpperCase()}
                  color={getRiskColor(insight.risk_level) as any}
                  size="small"
                />
              </Box>
              
              <Typography variant="h4" color={getRiskColor(insight.risk_level)} gutterBottom>
                {insight.name === 'Model Confidence' 
                  ? `${insight.value.toFixed(1)}%` 
                  : insight.name === 'Risk Factors Count'
                  ? insight.value
                  : insight.name === 'Fraud Classification'
                  ? (result.is_fake ? 'FAKE' : 'GENUINE')
                  : insight.value
                }
              </Typography>
              
              <Typography variant="body2" color="text.secondary">
                {insight.description}
              </Typography>
            </Paper>
          </Grid>
        ))}
        
        {/* Risk Factors Details */}
        {Object.keys(result.risk_factors).length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Detailed Risk Analysis
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(result.risk_factors).map(([key, value], index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Box p={2} bgcolor="error.light" borderRadius={1}>
                      <Typography variant="subtitle2" color="error.dark">
                        {key.replace(/_/g, ' ').toUpperCase()}
                      </Typography>
                      <Typography variant="body2" color="error.dark">
                        {value}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default FeatureAnalysis;
