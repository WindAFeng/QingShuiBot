dic = [{'help': {'name': '/help', 'param': '<页数(非必填项)>', 'content': '获取指令帮助', 'reg_name': 'help', 'param_num': [0, 1]}},
       {'main': {'name': '/main', 'param': '', 'content': '打开清风社区主页', 'reg_name': 'main', 'param_num': []}}]
dic1 = {}
for i in dic:
    for key in i:
        dic1[key] = i[key]
print(dic1)
