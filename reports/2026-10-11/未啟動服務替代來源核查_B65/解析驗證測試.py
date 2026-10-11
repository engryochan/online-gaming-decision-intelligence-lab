import struct,unittest
from 栅格標籤解析 import 解析
class 解析測試(unittest.TestCase):
    def test_大小端序與兩種目錄格式(self):
        for e in ['<','>']:
            for big in [False,True]:
                with self.subTest(端序=e,大檔=big):
                    marker=b'II' if e=='<' else b'MM'
                    if big:
                        header=marker+struct.pack(e+'HHHQ',43,8,0,16);data=header+struct.pack(e+'Q',2)
                        for tag,v in [(256,31),(257,27)]:data+=struct.pack(e+'HHQ',tag,4,1)+struct.pack(e+'I',v)+b'\0'*4
                        data+=b'\0'*8
                    else:
                        header=marker+struct.pack(e+'HI',42,8);data=header+struct.pack(e+'H',2)
                        for tag,v in [(256,31),(257,27)]:data+=struct.pack(e+'HHII',tag,4,1,v)
                        data+=b'\0'*4
                    def 讀(o,n):
                        b=data[o:o+n];self.assertEqual(len(b),n);return b
                    r=解析(讀);self.assertEqual((r['像元列數'],r['像元行數']),(31,27))
    def test_拒絕偽格式(self):
        with self.assertRaises(AssertionError):解析(lambda o,n:b'XX'+b'\0'*14)
    def test_拒絕過量標籤(self):
        data=b'II'+struct.pack('<HIH',42,8,1025)+b'\0'*10
        with self.assertRaises(AssertionError):解析(lambda o,n:data[o:o+n])
    def test_拒絕截斷目錄(self):
        data=b'II'+struct.pack('<HIH',42,8,2)+b'\0'*10
        def 讀(o,n):
            b=data[o:o+n]
            if len(b)!=n:raise EOFError('來源範圍不足')
            return b
        with self.assertRaises(EOFError):解析(讀)
if __name__=='__main__':unittest.main()
