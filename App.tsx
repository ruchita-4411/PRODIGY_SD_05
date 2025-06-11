import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Snackbar,
  FormControlLabel,
  Switch,
} from '@mui/material';
import axios from 'axios';

interface Product {
  name: string;
  price: string;
  rating: string;
  reviews: string;
  url: string;
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [pages, setPages] = useState(1);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [testMode, setTestMode] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim() && !testMode) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // First check if the backend is running
      await axios.get(`${API_BASE_URL}/api/health`);
      
      const response = await axios.post(`${API_BASE_URL}/api/scrape`, {
        query: searchQuery,
        pages: pages,
        test_mode: testMode,
      });

      setProducts(response.data.products);
      setSuccess(`Successfully scraped ${response.data.count} products!`);
    } catch (err: any) {
      if (err.code === 'ERR_NETWORK') {
        setError('Cannot connect to the backend server. Please make sure the backend is running on http://localhost:8000');
      } else {
        setError(err.response?.data?.detail || 'An error occurred while scraping');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Amazon Product Scraper
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
            <TextField
              fullWidth
              label="Search Query"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter product to search..."
              disabled={testMode}
            />
            <TextField
              type="number"
              label="Pages"
              value={pages}
              onChange={(e) => setPages(Number(e.target.value))}
              inputProps={{ min: 1, max: 5 }}
              sx={{ width: '120px' }}
              disabled={testMode}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              sx={{ minWidth: '120px' }}
            >
              {loading ? <CircularProgress size={24} /> : 'Search'}
            </Button>
          </Box>
          <FormControlLabel
            control={
              <Switch
                checked={testMode}
                onChange={(e) => setTestMode(e.target.checked)}
                color="primary"
              />
            }
            label="Test Mode (Use Sample Products)"
          />
        </Paper>

        {products.length > 0 && (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Product Name</TableCell>
                  <TableCell>Price</TableCell>
                  <TableCell>Rating</TableCell>
                  <TableCell>Reviews</TableCell>
                  <TableCell>URL</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {products.map((product, index) => (
                  <TableRow key={index}>
                    <TableCell>{product.name}</TableCell>
                    <TableCell>${product.price}</TableCell>
                    <TableCell>{product.rating}</TableCell>
                    <TableCell>{product.reviews}</TableCell>
                    <TableCell>
                      <a href={product.url} target="_blank" rel="noopener noreferrer">
                        View on Amazon
                      </a>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={() => setError('')}
        >
          <Alert severity="error" onClose={() => setError('')}>
            {error}
          </Alert>
        </Snackbar>

        <Snackbar
          open={!!success}
          autoHideDuration={6000}
          onClose={() => setSuccess('')}
        >
          <Alert severity="success" onClose={() => setSuccess('')}>
            {success}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default App; 