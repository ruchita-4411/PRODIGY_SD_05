# Amazon Product Scraper

A full-stack web application that scrapes product information from Amazon and displays it in a beautiful UI. The application includes both frontend and backend components.

## Features

- Search for products on Amazon
- Extract product names, prices, ratings, and reviews
- Save data to CSV format
- Modern Material-UI interface
- Real-time search results
- Error handling and loading states

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup

### Backend Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python main.py
```

The backend server will run on http://localhost:8000

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter a product search query in the search box
3. Select the number of pages to scrape (1-5)
4. Click the "Search" button
5. View the results in the table below
6. Click on product links to view them on Amazon

## Notes

- The scraper includes delays between requests to be respectful to Amazon's servers
- The application uses a custom User-Agent to avoid being blocked
- Results are automatically saved to a CSV file in the backend directory

## Technologies Used

- Backend:
  - FastAPI
  - BeautifulSoup4
  - Requests
  - Pandas

- Frontend:
  - React
  - TypeScript
  - Material-UI
  - Axios 