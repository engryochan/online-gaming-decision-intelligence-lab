import subprocess, unittest
from 驗證與提交 import 逐步執行

class 發布阻斷測試(unittest.TestCase):
    def 檢查阻斷(self,失敗項):
        經過=[]
        def 執行器(命令,**kwargs):
            self.assertTrue(kwargs['check']);經過.append(命令[0])
            if 命令[0]==失敗項:raise subprocess.CalledProcessError(1,命令)
        with self.assertRaises(subprocess.CalledProcessError):逐步執行([['驗證'],['提交'],['推送']],執行器)
        return 經過
    def test_驗證失敗禁止提交推送(self):self.assertEqual(self.檢查阻斷('驗證'),['驗證'])
    def test_提交失敗禁止推送(self):self.assertEqual(self.檢查阻斷('提交'),['驗證','提交'])
if __name__=='__main__':unittest.main()
