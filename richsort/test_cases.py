"""
Test cases module for RichSort.

This module contains the standard test cases used across different UI implementations.
"""

# Standard test cases for sorting algorithms
TEST_CASES = [
    {
        "name": "🎲 Caso Aleatório",
        "array": [10, 30, 20, 40, 5],
        "description": "Array com elementos em ordem aleatória",
    },
    {
        "name": "✅ Melhor Caso",
        "array": [1, 2, 3, 4, 5],
        "description": "Array já ordenado - mínimo de trocas",
    },
    {
        "name": "❌ Pior Caso",
        "array": [50, 40, 30, 20, 10],
        "description": "Array em ordem decrescente - máximo de trocas",
    },
    {
        "name": "🔄 Caso com Duplicatas",
        "array": [3, 1, 4, 1, 5, 9, 2, 6],
        "description": "Array com elementos repetidos",
    },
]


def get_test_cases():
    """Get the standard test cases for sorting algorithms."""
    return TEST_CASES.copy()
