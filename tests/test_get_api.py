import unittest
__import__("sys").path.append("../src")
import weatherquery as wq

class TestAdd(unittest.TestCase):
    def test_get_api_type(self):
        self.assertEqual(isinstance(wq.getapi("101010100"),dict), True)

if __name__=='__main__':
    unittest.main()