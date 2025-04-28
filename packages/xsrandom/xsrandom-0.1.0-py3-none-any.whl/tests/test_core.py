"""
Тесты для модуля xsrandom.core.
"""

import unittest
import xsrandom
import random

class TestCore(unittest.TestCase):
    """Тесты для основных функций генерации случайных чисел."""
    
    def test_seed(self):
        """Тест функции seed."""
        xsrandom.seed(12345)
        seq1 = [xsrandom.random() for _ in range(10)]
        
        xsrandom.seed(12345)
        seq2 = [xsrandom.random() for _ in range(10)]
        
        self.assertEqual(seq1, seq2)
    
    def test_random(self):
        """Тест функции random."""
        for _ in range(100):
            val = xsrandom.random()
            self.assertTrue(0 <= val < 1)
    
    def test_randint(self):
        """Тест функции randint."""
        a, b = 10, 20
        for _ in range(100):
            val = xsrandom.randint(a, b)
            self.assertTrue(a <= val <= b)
            self.assertTrue(isinstance(val, int))
    
    def test_uniform(self):
        """Тест функции uniform."""
        a, b = 10.5, 20.5
        for _ in range(100):
            val = xsrandom.uniform(a, b)
            self.assertTrue(a <= val < b)
    
    def test_choice(self):
        """Тест функции choice."""
        seq = [1, 2, 3, 4, 5]
        for _ in range(100):
            val = xsrandom.choice(seq)
            self.assertTrue(val in seq)
    
    def test_choices(self):
        """Тест функции choices."""
        seq = [1, 2, 3, 4, 5]
        k = 3
        result = xsrandom.choices(seq, k=k)
        self.assertEqual(len(result), k)
        for val in result:
            self.assertTrue(val in seq)
        
        weights = [0, 0, 1, 0, 0]  
        result = xsrandom.choices(seq, weights=weights, k=10)
        self.assertTrue(all(val == 3 for val in result))
    
    def test_sample(self):
        """Тест функции sample."""
        seq = [1, 2, 3, 4, 5]
        k = 3
        result = xsrandom.sample(seq, k)
        self.assertEqual(len(result), k)
        self.assertEqual(len(set(result)), k) 
        for val in result:
            self.assertTrue(val in seq)
    
    def test_shuffle(self):
        """Тест функции shuffle."""
        original = list(range(100))
        shuffled = original.copy()
        xsrandom.shuffle(shuffled)
        
        self.assertEqual(set(original), set(shuffled))
        
        self.assertNotEqual(original, shuffled)
    
    def test_randbytes(self):
        """Тест функции randbytes."""
        n = 10
        result = xsrandom.randbytes(n)
        self.assertEqual(len(result), n)
        self.assertTrue(isinstance(result, bytes))
    
    def test_getstate_setstate(self):
        """Тест функций getstate и setstate."""
        xsrandom.seed(12345)
        state = xsrandom.getstate()
        seq1 = [xsrandom.random() for _ in range(10)]
        
        xsrandom.setstate(state)
        seq2 = [xsrandom.random() for _ in range(10)]
        
        self.assertEqual(seq1, seq2)
    
    def test_bit_generator(self):
        """Тест функции bit_generator."""
        width = 8
        for _ in range(100):
            val = xsrandom.bit_generator(width)
            self.assertTrue(0 <= val < (1 << width))
    
    def test_randrange(self):
        """Тест функции randrange."""
        start, stop, step = 10, 20, 2
        expected_values = list(range(start, stop, step))
        
        for _ in range(100):
            val = xsrandom.randrange(start, stop, step)
            self.assertTrue(val in expected_values)


if __name__ == "__main__":
    unittest.main() 