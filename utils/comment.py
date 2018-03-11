#!/usr/bin/env python
#_*_coding:utf-8_*_

def comment_tree(comment_list):
    """
    显示多级评论插件
    :param result: [ {id,:child:[xxx]},{}]
    :return:如下格式
    <div class='comment'>
        <div class='content'>%s</div>
            <div class='comment'>
                <div class='content'>%s</div>
            </div>
        <div class='content'>%s</div>
        <div class='content'>%s</div>
    </div>
    comment_list
    [{'id': 1, 'content': '写的不错', 'parent_id': None, 
        'child': [{'id': 4, 'content': '写的不错？初级水平而已', 'parent_id': 1, 
        'child': [{'id': 5, 'content': '初级水平能达到这样子真的很厉害了', 'parent_id': 4, 
        'child': [{'id': 7, 'content': '表示赞同，真的很厉害', 'parent_id': 5, 'child': []}]}]}]},
    {'id': 2, 'content': '继续加油', 'parent_id': None, 
        'child': [{'id': 6, 'content': '加柴油，功率大', 'parent_id': 2, 'child': []}]},
    {'id': 3, 'content': '膜拜大神', 'parent_id': None, 
        'child': [{'id': 8, 'content': '大神？不存在的。。。', 'parent_id': 3, 'child': []}]}]

    """
    comment_str = "<div class='comment'>"
    for row in comment_list:
        tpl = "<div class='content'>%s</div>" %(row['content'])
        comment_str += tpl
        if row['child']:
            child_str = comment_tree(row['child'])
            comment_str += child_str
    comment_str += "</div>"

    return comment_str