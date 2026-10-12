import unittest
from 全量差異核查 import 計數,差異模式
class 測試(unittest.TestCase):
    def setUp(self):差異模式.clear()
    def test_重複不混入差異(self):
        r=計數([['a','t','1','x'],['a','t','1','x'],['b','t','1','x'],['b','t','2','x']], [0,1])
        self.assertEqual(r['精確重複額外行'],1)
        self.assertEqual(dict(差異模式),{(2,):1})
    def test_多欄原字串差異(self):
        r=計數([['a','t','1','x'],['a','t','1.0',' x']], [0,1])
        self.assertEqual(r['同鍵不同完整欄值組'],1)
        self.assertEqual(dict(差異模式),{(2,3):1})
    def test_不同鍵不混成差異(self):
        r=計數([['a','t','1'],['b','t','2']], [0,1])
        self.assertEqual(r['同鍵不同完整欄值組'],0)
        self.assertEqual(dict(差異模式),{})
if __name__=='__main__':unittest.main()
