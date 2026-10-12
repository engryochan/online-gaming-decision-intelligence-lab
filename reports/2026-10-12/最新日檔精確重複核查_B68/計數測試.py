import unittest
from 全量核查 import 計數
class 測試(unittest.TestCase):
    def test_精確重複與同鍵差異(self):
        r=計數([['a','t','1'],['a','t','1'],['a','t','2'],['b','t','1']], [0,1])
        self.assertEqual(r['精確重複額外行'],1)
        self.assertEqual(r['完整欄值唯一數'],3)
        self.assertEqual(r['同鍵不同完整欄值組'],1)
        self.assertEqual(r['最大同鍵資料行'],3)
    def test_不自動標準化(self):
        r=計數([['a','t','1'],['a','t','1.0'],['a','t',' 1']], [0,1])
        self.assertEqual(r['精確重複額外行'],0)
        self.assertEqual(r['同鍵不同完整欄值組'],1)
if __name__=='__main__':unittest.main()
