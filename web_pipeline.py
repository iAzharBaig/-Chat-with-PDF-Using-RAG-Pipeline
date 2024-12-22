from typing import List, Dict, Any
from crawler import crawl_and_scrape
from embedding import convert_to_embeddings
from vector_database import store_embeddings, similarity_search
from query_handler import generate_response

class WebPipeline:
    def ingest_data(self, urls: List[str]) -> None:
        if not urls:
            raise ValueError("No URLs provided")
            
        try:
            for url in urls:
                text = crawl_and_scrape(url)
                if text:
                    # Better chunking strategy with minimum length
                    chunks = [chunk.strip() for chunk in text.split('.') if len(chunk.strip()) > 10]
                    embeddings = convert_to_embeddings(chunks)
                    store_embeddings(chunks, embeddings)
                else:
                    print(f"Warning: No content retrieved from {url}")
        except Exception as e:
            raise Exception(f"Error in data ingestion: {str(e)}")

    def handle_query(self, query: str) -> str:
        try:
            relevant_chunks = similarity_search(query)
            return generate_response(query, relevant_chunks)
        except Exception as e:
            raise Exception(f"Error in query handling: {str(e)}")

if __name__ == "__main__":
    pipeline = WebPipeline()
    urls = ["https://example.com"]
    try:
        pipeline.ingest_data(urls)
        user_query = input("Enter your query: ")
        response = pipeline.handle_query(user_query)
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")
