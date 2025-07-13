import React, { useState } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  AppBar,
  Toolbar
} from '@mui/material';
import { Security, Assessment, CloudUpload } from '@mui/icons-material';
import InvoiceUpload from './components/InvoiceUpload';
import ResultsDisplay from './components/ResultsDisplay';
import FeatureAnalysis from './components/FeatureAnalysis';
import { PredictionResult } from './types/types';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handlePrediction = (result: PredictionResult) => {
    setPredictionResult(result);
    setLoading(false);
  };

  const handleLoadingChange = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <Security sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Fake Invoice Detector
          </Typography>
          <Assessment sx={{ mr: 1 }} />
          <Typography variant="body2">
            AI-Powered Detection
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box textAlign="center" mb={4}>
          <Typography variant="h4" gutterBottom>
            🔍 AI-Powered Invoice Authentication
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Upload an invoice to detect fraudulent patterns using machine learning
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* Upload Section */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Box display="flex" alignItems="center" mb={2}>
                <CloudUpload sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Upload Invoice</Typography>
              </Box>
              <InvoiceUpload 
                onPrediction={handlePrediction}
                onLoadingChange={handleLoadingChange}
                loading={loading}
              />
            </Paper>
          </Grid>

          {/* Results Section */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Box display="flex" alignItems="center" mb={2}>
                <Assessment sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Analysis Results</Typography>
              </Box>
              <ResultsDisplay result={predictionResult} loading={loading} />
            </Paper>
          </Grid>

          {/* Feature Analysis Section */}
          {predictionResult && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  📊 Detailed Feature Analysis
                </Typography>
                <FeatureAnalysis result={predictionResult} />
              </Paper>
            </Grid>
          )}
        </Grid>

        {/* Footer */}
        <Box mt={6} py={3} textAlign="center">
          <Typography variant="body2" color="text.secondary">
            Built with React, TypeScript, FastAPI, and Machine Learning
          </Typography>
          <Typography variant="body2" color="text.secondary">
            XGBoost • Random Forest • Feature Engineering
          </Typography>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
