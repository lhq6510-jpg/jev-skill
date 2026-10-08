import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("optimizer", ROOT / "scripts" / "optimize.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SafetyTests(unittest.TestCase):
    def test_short(self):
        r=m.optimize('计算 17 + 25。');self.assertTrue(r['skip']);self.assertEqual(r['selected_text'],'计算 17 + 25。')

    def test_natural_language_no_forced_rewrite(self):
        text=(ROOT/'tests'/'tasks.txt').read_text(encoding='utf-8').split('TASK t2')[1].split('TASK t3')[0]
        self.assertEqual(m.optimize(text)['selected_text'],text)

    def test_adjacent_repeated_requirements(self):
        p='必须保留所有数据，不允许修改源文件。';candidate=m.cleanup(p+'\n\n'+p)
        self.assertEqual(candidate,p);self.assertTrue(m.verify(p+'\n\n'+p,candidate)[0])

    def test_code_verbatim(self):
        text='```python\ndef f(x):\n    return x * x - 4\n```\n'+'背景说明。'*100
        self.assertEqual(m.optimize(text,unseen=True)['selected_text'],text)

    def test_chinese_path(self):
        self.assertFalse(m.verify('必须保留 C:\\资料\\输入.json。','必须保留输入文件。')[0])

    def test_numbers_versions_units(self):
        self.assertFalse(m.verify('版本 3.12.10，超时 2500 ms。','版本 3.12，超时 2 秒。')[0])
        self.assertFalse(m.verify('版本 3.12.10。','版本 13.12.100。',{'requirements':[{'original':'版本 3.12.10。','candidate':'版本 13.12.100。','equivalent':True}]},True)[0])

    def test_negations(self):
        self.assertFalse(m.verify('不允许删除文件。\n\n禁止上传凭据。','允许删除文件。\n\n上传凭据。')[0])

    def test_order(self):
        self.assertFalse(m.verify('先备份，再修改，最后测试。','先修改，再备份，最后测试。')[0])

    def test_concise(self):
        self.assertTrue(m.optimize('排序 [3,1,2]。')['skip'])

    def test_failure_fallback(self):
        text='任务说明。'*100
        for candidate in ['',None,123]:
            r=m.optimize(text,candidate=candidate);self.assertEqual(r['selected_text'],text)

    def test_cost_and_sunk_input(self):
        p='本次工作围绕访谈材料整理展开，需要使描述简洁易读，同时呈现参与者讨论的背景。'*30
        text=p+'\n\n'+p
        sunk=m.optimize(text);self.assertTrue(sunk['skip']);self.assertLess(sunk['estimated_net_saved_tokens'],0)
        unseen=m.optimize(text,unseen=True);self.assertTrue(unseen['applied']);self.assertGreater(unseen['estimated_net_saved_tokens'],0)

    def test_semantic_inventory_incomplete(self):
        text='关于访谈材料的背景说明。'*30+'\n\n另有一项独立整理工作。'
        inventory={'requirements':[{'original':'另有一项独立整理工作。','candidate':'整理。','equivalent':True}]}
        self.assertFalse(m.verify(text,'整理。',inventory,True)[0])


if __name__=='__main__':unittest.main()
