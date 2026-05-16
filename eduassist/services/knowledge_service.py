"""Knowledge base service for Q&A functionality."""

from typing import Dict, Tuple, List


class KnowledgeService:
    """Service for querying the knowledge base."""
    
    SUBJECT_KEY_MAPPING = {
        "Python Programming": "python_programming",
        "Data Structures": "data_structures",
        "Database Management Systems": "dbms",
        "Operating Systems": "operating_systems",
        "Machine Learning": "machine_learning",
        "Computer Networks": "computer_networks",
        "C Programming": "c_programming",
    }
    
    def __init__(self, knowledge_base: Dict):
        self.knowledge_base = knowledge_base
    
    def find_answer(self, question: str, subject_key: str = "python_programming") -> Tuple[str, str]:
        """
        Find an answer for a given question.
        
        Args:
            question: The user's question
            subject_key: The subject to search in
            
        Returns:
            Tuple of (answer, match_type)
        """
        question_lower = question.lower()
        
        if "general" in self.knowledge_base:
            for topic, data in self.knowledge_base["general"].items():
                keywords = data.get("keywords", [])
                for keyword in keywords:
                    if keyword.lower() in question_lower:
                        return data.get("answer", ""), "general"
        
        subject_kb = self.knowledge_base.get(subject_key, {})
        best_match = None
        max_matches = 0
        
        for topic, data in subject_kb.items():
            keywords = data.get("keywords", [])
            match_count = sum(1 for keyword in keywords if keyword.lower() in question_lower)
            if match_count > max_matches:
                max_matches = match_count
                best_match = data
        
        if best_match and max_matches > 0:
            return best_match.get("answer", ""), "subject"
        
        return "", "not_found"
    
    @classmethod
    def get_subject_key(cls, subject_name: str) -> str:
        """Convert subject name to subject key."""
        return cls.SUBJECT_KEY_MAPPING.get(subject_name, "python_programming")
    
    @staticmethod
    def generate_practice_questions(subject: str, topic: str) -> List[str]:
        """Generate practice questions for a given subject and topic."""
        questions = {
            "python_programming": {
                "default": [
                    "What is the difference between a list and a tuple in Python?",
                    "Explain the concept of list comprehension with an example.",
                    "What are decorators in Python and how do they work?",
                    "Write a program to check if a number is prime.",
                    "Explain the difference between shallow copy and deep copy."
                ],
                "loops": [
                    "What is the difference between for and while loops?",
                    "How do you use break and continue statements?",
                    "Write a program to print Fibonacci series using loops.",
                    "Explain nested loops with an example.",
                    "What is an infinite loop and how to avoid it?"
                ],
                "oop": [
                    "What are the four pillars of OOP?",
                    "Explain inheritance with an example.",
                    "What is polymorphism in Python?",
                    "Difference between class variables and instance variables?",
                    "What is method overriding?"
                ]
            },
            "data_structures": {
                "default": [
                    "What is the difference between an array and a linked list?",
                    "Explain the time complexity of different sorting algorithms.",
                    "What is a binary search tree?",
                    "How does a hash table work?",
                    "Explain the difference between BFS and DFS."
                ]
            },
            "dbms": {
                "default": [
                    "What is normalization and why is it important?",
                    "Explain ACID properties in database transactions.",
                    "What is the difference between SQL and NoSQL databases?",
                    "What are indexes and how do they improve performance?",
                    "Explain different types of joins in SQL."
                ]
            }
        }
        
        subject_questions = questions.get(subject, {"default": ["Practice questions for this subject coming soon!"]})
        topic_questions = subject_questions.get(topic, subject_questions.get("default", []))
        return topic_questions
