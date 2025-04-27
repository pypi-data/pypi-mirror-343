import unittest
from ..devwer.metrics import Metrics

class TestDevnagariWER(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize('यह एक परीक्षण है।'), 'यह एक परीक्षण है')
    
    def test_wer(self):
        reference = normalize('यह एक परीक्षण है')
        hypothesis = normalize('यह एक परिक्षण है')
        self.assertAlmostEqual(calculate_wer(reference, hypothesis), 0.25, places=2)

if __name__ == '__main__':
    unittest.main()


# from devwer import Metrics
# metrics = Metrics()

# metrics.wer("संगम","सङ्गम")
# metrics.wer('यह एक परीक्षण है।', 'यह एक परीक्षण है')
# metrics.wer("संगम","सङ्गम")

# metrics.wer_legacy('यह एक परीक्षण है।', 'यह एक परीक्षण है')

# metrics.tokenize('यह एक परीक्षण है।')
