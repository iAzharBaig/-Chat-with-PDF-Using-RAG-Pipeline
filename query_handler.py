from typing import List

class QueryHandler:
    def generate_response(self, query: str, relevant_chunks: List[str]) -> str:
        try:
            if not relevant_chunks:
                return "No relevant information found."
            
            # Simple response generation by combining most relevant chunk with query
            most_relevant = relevant_chunks[0]
            return f"Based on the query '{query}', here is the most relevant information: {most_relevant}"
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

# Initialize global instance
query_handler = QueryHandler()

def generate_response(query: str, relevant_chunks: List[str]) -> str:
    return query_handler.generate_response(query, relevant_chunks)