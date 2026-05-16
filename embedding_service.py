"""
Embedding Service for JNTU EduAssist AI
Uses ChromaDB with built-in DefaultEmbeddingFunction for semantic search.
"""

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import json
import os
from typing import List, Dict, Tuple, Optional


class EmbeddingService:
    """Service for managing embeddings and semantic search using ChromaDB."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the embedding service with ChromaDB.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.embedding_fn = DefaultEmbeddingFunction()
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine", "description": "JNTU EduAssist knowledge base embeddings"}
        )
    
    def load_knowledge_base(self, kb_path: str = "knowledge_base.json") -> Dict:
        """Load knowledge base from JSON file.
        
        Args:
            kb_path: Path to knowledge base JSON file
            
        Returns:
            Dictionary containing knowledge base data
        """
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file not found: {kb_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in knowledge base: {kb_path}")
            return {}
    
    def populate_from_knowledge_base(self, kb_path: str = "knowledge_base.json") -> int:
        """Populate ChromaDB with content from knowledge base.
        
        Args:
            kb_path: Path to knowledge base JSON file
            
        Returns:
            Number of documents added
        """
        knowledge_base = self.load_knowledge_base(kb_path)
        if not knowledge_base:
            return 0
        
        documents = []
        metadatas = []
        ids = []
        
        for subject_key, topics in knowledge_base.items():
            if not isinstance(topics, dict):
                continue
                
            for topic_key, topic_data in topics.items():
                if not isinstance(topic_data, dict):
                    continue
                    
                answer = topic_data.get("answer", "")
                keywords = topic_data.get("keywords", [])
                
                if not answer:
                    continue
                
                keywords_text = ", ".join(keywords) if keywords else ""
                document_text = f"Topic: {topic_key.replace('_', ' ').title()}\nKeywords: {keywords_text}\n\n{answer}"
                
                doc_id = f"{subject_key}_{topic_key}"
                
                documents.append(document_text)
                metadatas.append({
                    "subject": subject_key,
                    "topic": topic_key,
                    "keywords": keywords_text,
                    "answer": answer
                })
                ids.append(doc_id)
        
        if documents:
            existing_ids = set(self.collection.get()["ids"])
            new_docs = []
            new_metas = []
            new_ids = []
            
            for doc, meta, doc_id in zip(documents, metadatas, ids):
                if doc_id not in existing_ids:
                    new_docs.append(doc)
                    new_metas.append(meta)
                    new_ids.append(doc_id)
            
            if new_docs:
                self.collection.add(
                    documents=new_docs,
                    metadatas=new_metas,
                    ids=new_ids
                )
                return len(new_docs)
        
        return 0
    
    def search(self, query: str, n_results: int = 3, subject_filter: Optional[str] = None) -> List[Dict]:
        """Search for relevant content using semantic similarity.
        
        Args:
            query: User's question or search query
            n_results: Number of results to return
            subject_filter: Optional subject to filter results
            
        Returns:
            List of matching documents with metadata and scores
        """
        where_filter = None
        if subject_filter:
            where_filter = {"subject": subject_filter}
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            print(f"Search error: {e}")
            return []
        
        if not results or not results.get("ids") or not results["ids"][0]:
            return []
        
        formatted_results = []
        for i, doc_id in enumerate(results["ids"][0]):
            distance = results["distances"][0][i] if results.get("distances") else 2.0
            similarity = 1.0 - (distance / 2.0)
            result = {
                "id": doc_id,
                "document": results["documents"][0][i] if results.get("documents") else "",
                "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                "distance": distance,
                "similarity": similarity
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def get_best_answer(self, query: str, subject_filter: Optional[str] = None, 
                        similarity_threshold: float = 0.5) -> Tuple[str, str, float]:
        """Get the best matching answer for a query.
        
        Args:
            query: User's question
            subject_filter: Optional subject to filter results
            similarity_threshold: Minimum similarity score to consider a match
            
        Returns:
            Tuple of (answer, match_type, similarity_score)
        """
        results = self.search(query, n_results=1, subject_filter=subject_filter)
        
        if not results:
            return "", "not_found", 0.0
        
        best_result = results[0]
        similarity = best_result.get("similarity", 0.0)
        
        if similarity < similarity_threshold:
            return "", "not_found", similarity
        
        answer = best_result.get("metadata", {}).get("answer", "")
        subject = best_result.get("metadata", {}).get("subject", "")
        
        match_type = "general" if subject == "general" else "subject"
        
        return answer, match_type, similarity
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"error": str(e)}
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection(name="knowledge_base")
            self.collection = self.client.get_or_create_collection(
                name="knowledge_base",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine", "description": "JNTU EduAssist knowledge base embeddings"}
            )
        except Exception as e:
            print(f"Error clearing collection: {e}")


_embedding_service: Optional[EmbeddingService] = None

def get_embedding_service() -> EmbeddingService:
    """Get or create a singleton embedding service instance.
    
    Returns:
        EmbeddingService instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
        docs_added = _embedding_service.populate_from_knowledge_base()
        if docs_added > 0:
            print(f"Added {docs_added} documents to ChromaDB")
    return _embedding_service


def initialize_embeddings() -> Dict:
    """Initialize embeddings and return status.
    
    Returns:
        Dictionary with initialization status
    """
    service = get_embedding_service()
    stats = service.get_collection_stats()
    return {
        "status": "initialized",
        "stats": stats
    }


if __name__ == "__main__":
    print("Initializing Embedding Service...")
    service = EmbeddingService()
    
    service.clear_collection()
    
    docs_added = service.populate_from_knowledge_base()
    print(f"Added {docs_added} documents to ChromaDB")
    
    stats = service.get_collection_stats()
    print(f"Collection stats: {stats}")
    
    print("\nTesting search...")
    test_queries = [
        "How do I use loops in Python?",
        "What is object oriented programming?",
        "Explain file handling",
        "hello, can you help me?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        answer, match_type, similarity = service.get_best_answer(query)
        print(f"Match type: {match_type}, Similarity: {similarity:.2f}")
        if answer:
            print(f"Answer preview: {answer[:100]}...")
