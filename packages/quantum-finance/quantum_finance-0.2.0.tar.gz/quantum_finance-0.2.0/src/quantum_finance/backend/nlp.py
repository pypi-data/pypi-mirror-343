"""
NLP module for Quantum-AI Platform.

Provides NLP capabilities integrated with quantum computing components.
"""

import logging
from transformers import pipeline
from quantum_finance.backend.quantum_algorithms import run_grover, shor_factorization

class QuantumNLP:
    """
    NLP interface integrated with quantum computing components.
    """

    def __init__(self, model_name='distilbert-base-uncased-distilled-squad'):
        self.logger = logging.getLogger(__name__)
        self.nlp_model = pipeline('question-answering', model=model_name)
        self.logger.info(f"NLP model '{model_name}' initialized.")

    def answer_query(self, question, context):
        """
        Answer a query using the NLP model.

        Args:
            question (str): The question to answer.
            context (str): Contextual information for answering the question.

        Returns:
            dict: Answer and confidence score.
        """
        try:
            result = self.nlp_model(question=question, context=context)
            self.logger.debug(f"Query answered: {result}")
            return {
                'answer': result['answer'],
                'score': result['score']
            }
        except Exception as e:
            self.logger.error(f"Error answering query: {e}")
            return {
                'error': str(e)
            }

    def classify_query(self, query):
        """
        Classify the query to determine if it should trigger quantum processing.

        Returns:
            str: Classification result indicating query type ('quantum' or 'classical').
        """
        quantum_keywords = ['quantum', 'grover', 'shor', 'entanglement', 'superposition']
        if any(keyword in query.lower() for keyword in quantum_keywords):
            classification = 'quantum'
        else:
            classification = 'classical'

        self.logger.info(f"Query classified as: {classification}")
        return classification

    def process_quantum_query(self, query):
        """
        Process queries classified as quantum-related by invoking quantum algorithms.

        Args:
            query (str): The quantum-related query.

        Returns:
            dict: Result from quantum algorithm execution.
        """
        try:
            if 'grover' in query.lower():
                result = run_grover(query)
                self.logger.debug(f"Grover's algorithm result: {result}")
                return {'algorithm': 'grover', 'result': result}
            elif 'shor' in query.lower():
                result = shor_factorization(query)
                self.logger.debug(f"Shor's algorithm result: {result}")
                return {'algorithm': 'shor', 'result': result}
            else:
                self.logger.warning("Quantum query type not recognized.")
                return {'error': 'Unsupported quantum query type.'}
        except Exception as e:
            self.logger.error(f"Error processing quantum query: {e}")
            return {'error': str(e)}

    def handle_query(self, query, context=None):
        """
        Main entry point to handle NLP queries, routing to quantum or classical processing.

        Args:
            query (str): The user's query.
            context (str, optional): Contextual information for classical NLP queries.

        Returns:
            dict: Result from NLP or quantum processing.
        """
        classification = self.classify_query(query)
        if classification == 'quantum':
            return self.process_quantum_query(query)
        else:
            if context is None:
                error_msg = 'Context required for classical NLP queries.'
                self.logger.error(error_msg)
                return {'error': error_msg}
            return self.answer_query(query, context)