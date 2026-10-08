"""Score actual paired Agent outputs; never fabricates model Usage."""
import json
import sys
from pathlib import Path

EXPECTED={
 't1':42,'t2':['需求评审','修复登录错误','回归测试','发布'],
 't3':['status','message','request_id'],'t4':5,
 't5':{'input':'C:\\资料\\登录错误\\输入.json','output':'C:\\资料\\登录错误\\结果.json'},
 't6':{'python_version':'3.12.10','node_version':'24.19.0','timeout_ms':2500,'retries':2},
 't7':['修复登录'],'t8':['backup','inspect','fix','test','release','report'],
 't9':[1,2,3],'t10':{'safe':True,'action':'保留原文'}}

def evaluate(path):
    text=Path(path).read_text(encoding='utf-8-sig').strip()
    if text.startswith('```'):text='\n'.join(text.splitlines()[1:-1])
    try:result=json.loads(text)
    except Exception:return {'quality_passed':0,'cases':10,'parse_failed':True}
    # "执行回归测试" and "回归测试" name the same requested step; do not penalize wording.
    normalized=dict(result)
    if isinstance(normalized.get('t2'),list):normalized['t2']=['回归测试' if x=='执行回归测试' else x for x in normalized['t2']]
    scores={k:normalized.get(k)==v for k,v in EXPECTED.items()}
    return {'quality_passed':sum(scores.values()),'cases':10,'case_results':scores,
            'constraint_failure_case_rate':1-sum(scores.values())/10,
            'scope':'Exact acceptance-output checks; not a general semantic-quality guarantee'}

if __name__=='__main__':print(json.dumps(evaluate(sys.argv[1]),ensure_ascii=False,indent=2))
