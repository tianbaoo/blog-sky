class PageInfo(object):
    """
    分页组件
    """
    def __init__(self,current_page,all_count,per_page,base_url,show_page=11):
        """
        :param current_page: 当前页
        :param all_count: 数据库总行数
        :param per_page: 每页显示函数
        :return:
        """
        try:
            self.current_page = int(current_page)  #把URL中获取到的当前页转换为数字
        except Exception as e: # 转换出错则跳转到第一页
            self.current_page = 1
        self.per_page = per_page # 每页显示的条数

        a,b = divmod(all_count,per_page) # 总条数除以每页条数获得一共有多少页
        if b: # 如果有余数则证明剩下的不够每页显示的数目但是需要加一页
            a = a +1
        self.all_pager = a   # all_pager 表示总页数
        self.show_page = show_page  # show_page 数据很多时显示11页
        self.base_url = base_url    # 传入要跳转的URL地址
    def start(self):  # 取文章数据的时候
        return (self.current_page-1) * self.per_page  # 当前页减一乘以每页显示的条数  第几条

    def end(self):
        return self.current_page * self.per_page     # 当前页乘以每页显示的条数        到第几条

    def pager(self):
        page_list = []
        # half是用来显示前五页和后五页的一个数
        half = int((self.show_page-1)/2)   # 显示的页码减一除以二

        # 如果数据总页数 < 11
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager + 1
        # 如果数据总页数 > 11
        else:
            # 如果当前页 <=5,永远显示1,11
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_pager:   #当前页加五后大于总页码的时候
                    begin = self.all_pager - self.show_page + 1 # 起始页为最后一页往前倒11页
                    stop = self.all_pager + 1                   # 最后一页
                else:
                    begin = self.current_page - half          # 当前页往前倒5页
                    stop = self.current_page + half + 1       # 当前页往后倒5页

        if self.current_page <= 1:  # 当前页小于等于1时,上一页不能点
            prev = "<li><a href='#'>上一页</a></li>"
        else: # 当前页大于1时,上一页能点
            prev = "<li><a href='%s?page=%s'>上一页</a></li>" %(self.base_url,self.current_page-1,)
        page_list.append(prev)  # 把标签放入列表中

        for i in range(begin,stop):
            if i == self.current_page: # 当前页等于i时证明当前页被选中加上active属性
                temp = "<li class='active'><a  href='%s?page=%s'>%s</a></li>" %(self.base_url,i,i,)
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" %(self.base_url,i,i,)
            page_list.append(temp) # 把标签放入列表中

        if self.current_page >= self.all_pager:  # 当前页大于等于最后一页时,下一页不能点
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='%s?page=%s'>下一页</a></li>" %(self.base_url,self.current_page+1,)
        page_list.append(nex) # 把标签放入列表中

        return ''.join(page_list) # 返回一个拼接的字符串