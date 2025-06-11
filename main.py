from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import AmazonScraper
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str
    pages: int = 1
    test_mode: bool = False

@app.post("/api/scrape")
async def scrape_products(search_query: SearchQuery):
    try:
        logger.info(f"Received scrape request: query={search_query.query}, pages={search_query.pages}, test_mode={search_query.test_mode}")
        
        scraper = AmazonScraper()
        products = scraper.get_product_data(
            search_query.query, 
            search_query.pages,
            test_mode=search_query.test_mode
        )
        
        if not products:
            logger.warning("No products found")
            raise HTTPException(status_code=404, detail="No products found")
        
        # Save to CSV
        filename = scraper.save_to_csv(products)
        logger.info(f"Successfully scraped {len(products)} products and saved to {filename}")
        
        return {
            "message": "Products scraped successfully",
            "count": len(products),
            "products": products,
            "csv_file": filename
        }
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting backend server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 