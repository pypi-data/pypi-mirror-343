import re
import math
from collections import defaultdict, Counter
from typing import List, Optional
from pydantic import BaseModel

class Page(BaseModel):
    title: str
    url: str
    content: Optional[str] = None  # contentをオプショナルに変更

class DocumentSearchEngine:
    def __init__(self):
        """Initialize an empty search engine.

        Creates an empty search engine with no documents and an empty inverted index.
        """
        self.documents = {}
        self.inverted_index = defaultdict(list)
        self.document_lengths = {}
        self.idf = {}
        
    def set_documents(self, pages: List[Page]):
        """Set documents from a list of Page objects.
        
        Args:
            pages: List of Page objects containing title, url, and optional content.
        
        Returns:
            None
        
        Note:
            This method will not update documents if they already exist.
        """
        # Skip if documents already exist
        if len(self.documents) > 0:
            return
        
        # Store documents using URL as the document ID
        for page in pages:
            # Use title as the indexable content if no content is provided
            content = page.content if page.content is not None else ""
            self.documents[page.url] = {
                'title': page.title,
                'content': content
            }
        
        # Build the index with the new documents
        self.build_index()
    
    def preprocess_text(self, text: str) -> List[str]:
        """Clean and tokenize text into words.
        
        Args:
            text: The input text to be processed.
            
        Returns:
            List[str]: A list of tokenized words.
            
        Note:
            Words shorter than 2 characters are filtered out.
        """
        if not text:
            return []
            
        # Convert to lowercase and split on non-alphanumeric characters
        words = re.findall(r'\w+', text.lower())
        # Filter out very short words (optional)
        words = [word for word in words if len(word) > 1]
        return words
    
    def build_index(self) -> None:
        """Build the inverted index and calculate IDF values.
        
        Processes all documents to create an inverted index and calculate
        inverse document frequency (IDF) values for each term.
        
        Returns:
            None
        """
        # Count document frequency for each term
        doc_freq = defaultdict(int)
        
        # Process each document
        for doc_id, doc_data in self.documents.items():
            content = doc_data['content'] or ""  # Use empty string if content is None
            
            # Add title to indexable content to give it more weight
            indexable_text = f"{doc_data['title']} {content}"
            
            # Tokenize and count terms in the document
            terms = self.preprocess_text(indexable_text)
            term_freq = Counter(terms)
            
            # Skip documents with no terms
            if not terms:
                continue
                
            # Store document length (for normalization)
            self.document_lengths[doc_id] = math.sqrt(sum(tf * tf for tf in term_freq.values()))
            
            # Update the inverted index with term frequencies
            for term, freq in term_freq.items():
                self.inverted_index[term].append((doc_id, freq))
                doc_freq[term] += 1
        
        # Calculate IDF for each term
        num_docs = max(1, len(self.documents))  # Avoid division by zero
        self.idf = {term: math.log(num_docs / freq) for term, freq in doc_freq.items()}
    
    def search(self, query, top_k=5) -> list[tuple[str, float]]:
        """Search for documents matching the query.
        
        Args:
            query: Search query (English).
            top_k: Number of top results to return.
            
        Returns:
            list[tuple[str, float]]: List of (document_id, score) tuples.
        """
        query_terms = self.preprocess_text(query)
        
        # If no valid terms in query, return empty results
        if not query_terms:
            return []
            
        # Count query terms
        query_term_freq = Counter(query_terms)
        
        # Calculate query vector length for normalization
        query_length = math.sqrt(sum((tf * self.idf.get(term, 0)) ** 2 
                                 for term, tf in query_term_freq.items()))
        
        # Initialize scores
        scores = defaultdict(float)
        
        # Calculate TF-IDF scores using cosine similarity
        for term, query_tf in query_term_freq.items():
            if term in self.inverted_index:
                query_weight = query_tf * self.idf.get(term, 0)
                
                # For each document containing this term
                for doc_id, doc_tf in self.inverted_index[term]:
                    doc_weight = doc_tf
                    scores[doc_id] += query_weight * doc_weight
        
        # Normalize scores by document length
        for doc_id in scores:
            if query_length > 0 and self.document_lengths.get(doc_id, 0) > 0:
                scores[doc_id] = scores[doc_id] / (query_length * self.document_lengths[doc_id])
        
        # Return top k results
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return results


    def get_search_results_with_metadata(self, query, top_k=5) -> list[dict[str, str | float]]:
        """Get search results with document metadata and snippets.
        
        Args:
            query: Search query.
            top_k: Number of top results to return.
            
        Returns:
            list[dict[str, str | float]]: List of dictionaries with document metadata and snippets.
            Each dictionary contains 'url', 'title', and optionally 'content'.
        """
        search_results = self.search(query, top_k)
        results_with_metadata = []
        
        for doc_id, _ in search_results:
            content = self.documents[doc_id].get('content', '')
            result = {
                'url': doc_id,
                'title': self.documents[doc_id]['title'],
            }
            if content:
                result['content'] = content
            
            results_with_metadata.append(result)
            
        return results_with_metadata
    


# Example usage
if __name__ == "__main__":
    # Create sample Page objects, some with content and some without
    pages = [
        Page(
            title="Introduction to Python",
            url="https://example.com/python-intro",
            content="Python is a high-level programming language known for its readability and simplicity. Python supports multiple programming paradigms including procedural, object-oriented, and functional programming."
        ),
        Page(
            title="Python for Data Science",
            url="https://example.com/python-data-science",
            # This page has no content, only title
        ),
        Page(
            title="Web Development with Flask",
            url="https://example.com/flask-web-dev",
            content="Flask is a micro web framework written in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications."
        ),
        Page(
            title="JavaScript Basics",
            url="https://example.com/js-basics",
            # Another page without content
        )
    ]
    
    # Initialize search engine and set documents
    search_engine = DocumentSearchEngine()
    search_engine.set_documents(pages)
    
    # Search for documents
    query = "python programming language oppai"
    results = search_engine.get_search_results_with_metadata(query)
    print(f"Search results for '{query}':")
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        if 'content' in result:
            print(f"Content: {result['content']}")
        print()