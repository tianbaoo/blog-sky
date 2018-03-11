"""分页组件示例功能"""
msg_list = [
    # id 为评论者的ID  content 为评论内容 parent_id 为父级ID None表示第一层
    {'id':1,'content':'写的不错','parent_id':None},
    {'id':2,'content':'继续加油','parent_id':None},
    {'id':3,'content':'膜拜大神','parent_id':None},
    {'id':4,'content':'写的不错？初级水平而已','parent_id':1},
    {'id':5,'content':'初级水平能达到这样子真的很厉害了','parent_id':4},
    {'id':6,'content':'加柴油，功率大','parent_id':2},
    {'id':7,'content':'表示赞同，真的很厉害','parent_id':5},
    {'id':8,'content':'大神？不存在的。。。','parent_id':3},
]
msg_list_dict = {}
for item in msg_list:
    item['child'] = []
    msg_list_dict[item['id']] = item
result = []
for item in msg_list:
    pid = item['parent_id']
    if pid:
        msg_list_dict[pid]['child'].append(item)
    else:
        result.append(item)
for i in result:
    print(i)

'''
[{'id': 1, 'content': '写的不错', 'parent_id': None, 
        'child': [{'id': 4, 'content': '写的不错？初级水平而已', 'parent_id': 1, 
        'child': [{'id': 5, 'content': '初级水平能达到这样子真的很厉害了', 'parent_id': 4, 
        'child': [{'id': 7, 'content': '表示赞同，真的很厉害', 'parent_id': 5, 'child': []}]}]}]},
    {'id': 2, 'content': '继续加油', 'parent_id': None, 
        'child': [{'id': 6, 'content': '加柴油，功率大', 'parent_id': 2, 'child': []}]},
    {'id': 3, 'content': '膜拜大神', 'parent_id': None, 
        'child': [{'id': 8, 'content': '大神？不存在的。。。', 'parent_id': 3, 'child': []}]}]
'''










