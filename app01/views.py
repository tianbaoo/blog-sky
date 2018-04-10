#!/usr/bin/env python
#_*_coding:utf-8_*_

from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from app01 import forms
from django.db.models import F
from django.db import transaction
from django.core.exceptions import NON_FIELD_ERRORS
import os,json
from django.db.models import Count
from utils.Pager import PageInfo
from django.views.decorators.cache import cache_page

def layout(request,**kwargs):
    return render(request,'layout.html')
#装饰器
def check_login(func):
    """
    用来验证用户是否已登录登录的装饰器
    :param func: 
    :return: 
    """
    def wrapper(request,*args,**kwargs):
        try:
            if request.session.get('user_info'):
                nickname = request.session.get('user_info').get('nickname')
                user_id = request.session.get('user_info').get('user_id')
                if models.UserInfo.objects.filter(nid=user_id):
                    return func(request,*args,**kwargs)
                else:
                    return redirect('index.html')
            else:
                return redirect('index.html')
        except Exception as e:
            return HttpResponse(e) # 抛出错误信息
    return wrapper

# 网站首页
@cache_page(60 * 15)
def index(request,*args,**kwargs):
    """
    网站首页
    :param request: 
    :param args: 
    :param kwargs: 
    :return: 
    """
    if request.method == 'GET':
        try:
            nickname = request.session.get('user_info').get('nickname')   # 去session里拿到用户昵称
            user = models.UserInfo.objects.filter(nickname=nickname).first() # 去数据库里拿到用户对象
        except Exception as e:  # 当在数据库里拿不到用户对象时,让user等于一个字符串
            user = ''
        type_id =int(kwargs.get('type_id')) if kwargs.get('type_id') else None  # 获取url中的大分类ID
        conditions = {}
        if type_id:
            try:
                nickname = request.session.get('user_info').get('nickname')
                user = models.UserInfo.objects.filter(nickname=nickname).first()
            except Exception as e:
                user = ''
            conditions['article_type_id'] = type_id  # article_type_id字符串 必须是Article表中的字段
        # 获取Article中所有的数据按发布时间排列
        article_list = models.Article.objects.filter(**conditions).order_by('-create_time')
        # -up_count 从大到小排序 down_count 从小到大排序 [:6] 取前6条数据 按赞数排列
        recommend_list = models.Article.objects.all().order_by('-up_count','down_count','nid')[:6]
        new_list = models.Article.objects.all().order_by('-create_time')[:6]
        type_choices_list = models.Article.type_choices  # type_choices_list 是获取网站的大分类

        ##########################分页功能#############################
        all_count = article_list.count()   # 获取数据库中指定对象的总条数
        # request.GET.get('page'):从URL中获取当前页 all_count:总条数 2:每页显示2条 '/' 是跳转网址 数据很多时显示11页
        page_info = PageInfo(request.GET.get('page'), all_count, 5, '/', 11)
        user_list = article_list[page_info.start():page_info.end()]  # 每页显示的数据 由上面那个2的位置参数决定

        return render(request,'index.html',
                      {'type_choices_list':type_choices_list, # 文章大分类列表
                       'article_list':article_list,            # 所有文章
                       'type_id':type_id,                       # URL中的大分类文章ID
                       'user':user,                              # 当前登录用户
                       'recommend_list':recommend_list,         # 推荐阅读列表
                       'new_list':new_list,                      # 推荐阅读列表
                       'user_list': user_list,                   # 筛选过后的每页显示的数据
                       'page_info': page_info})                  # 页码对象
    else:
        pass

#登录函数
def login(request):
    """
    登录函数
    :param request: 
    :return: 
    """
    if request.method == 'GET':
        # GET 请求过来的时候,Form组件在页面生成相应的input框,传入request参数获取session中的图片验证码值
        obj = forms.LoginForm(request)
        return render(request, 'login.html', {'obj': obj})
    else:
        obj = forms.LoginForm(request,request.POST)
        if obj.is_valid():  # 如果验证成功(验证码已过校验在Form中)
            user = request.POST.get('user')
            passwd = request.POST.get('passwd')
            obj = forms.LoginForm(request)
            res = models.UserInfo.objects.filter(username=user,password=passwd).first()  # 去数据库里查询用户是否存在
            if not res: # 用户不存在则返回相应的错误提示
                msg = '用户名或密码错误,请检查你输入的信息是否正确'
                return render(request, 'login.html', {'msg': msg,'obj': obj})
            else: # 存在则把用户相关信息写入session中在跳转到首页
                request.session['user_info'] = {'user_id': res.nid, 'username': res.username,'nickname': res.nickname}
                return redirect('/')
        else:
            return render(request, 'login.html', {'obj': obj})

#注销
def logout(request):
    try:
        if request.session.get('user_info'):  # 注销用户时,清除一下session即可
            request.session.clear()  # 相当于删除cookie 相当于设置了超时时间过期了
            return redirect('/')
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/')

#注册
def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    try:
        if request.method == "GET":
            obj = forms.RegisterForm(request) # GET 请求过来的时候Form在页面生成相应的输入框
            return render(request,'register.html',{'obj':obj})
        else: # request.FILES 有文件上传的时候需要加这个
            obj = forms.RegisterForm(request,request.POST,request.FILES)
            if obj.is_valid():    # 验证成功后将用户信息写入数据库
                username = request.POST.get('username')
                nickname = request.POST.get('nickname')
                email = request.POST.get('email')
                passwd = request.POST.get('passwd')
                avatar = request.FILES.get('avatar')
                file_path = os.path.join('static/imgs', avatar.name)
                file_path2 = file_path.replace('\\','/')
                with open(file_path2, 'wb') as f:
                    for chunk in avatar.chunks():  # 写入图片文件需要.chunks()
                        f.write(chunk)
                with transaction.atomic():  # 事物,原子性操作
                    obj = models.UserInfo.objects.create(username=username,nickname=nickname,email=email,password=passwd,avatar=file_path2)
                    models.Blog.objects.create(title=nickname,theme='warm',user_id=obj.nid,site=username)

                return redirect('/')
            else:
                return render(request,'register.html',{'obj':obj})
    except Exception as e:
        return HttpResponse(str(e))

def check_code(request):
    from io import BytesIO
    from utils.random_check_code import rd_check_code  # 引入封装的rd_check_code生成图片

    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    data = stream.getvalue()
    request.session['code'] = code  # 把验证码的信息写入数据
    return HttpResponse(data)

def home(request,site):
    """
    访问博客主页 http://127.0.0.1/simayi/
    :param request: 
    :return: 
    """
    # 拿到开通了博客的某用户
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 获取分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    # 获取标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 获取时间
    create_time_list = models.Article.objects.filter(blog=blog).extra(select={"ctime":'strftime("%%Y-%%m",create_time)'}).values('ctime').annotate(c=Count('nid'))

    # 博主的所有文章
    article_list = models.Article.objects.filter(blog=blog).all()

    ##########################分页功能#############################
    all_count = article_list.count()  # 获取数据库中指定对象的总条数
    # request.GET.get('page'):从URL中获取当前页 all_count:总条数 10:每页显示10条
    base_url = '/%s/'%(blog.user.username)   # 获取跳转的url
    page_info = PageInfo(request.GET.get('page'), all_count, 2, base_url, 11)
    user_list = article_list[page_info.start():page_info.end()]  # 每页显示的数据

    return render(request,'home.html',{
        'blog':blog,
        'category_list':category_list,
        'tag_list':tag_list,
        'create_time_list':create_time_list,
        'article_list':article_list,
        'user_list': user_list, 'page_info': page_info
    })

def filter(request,site,key,val):
    blog = models.Blog.objects.filter(site=site).first()
    # 获取分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))
    # 获取标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count('id'))
    # 获取时间
    create_time_list = models.Article.objects.filter(blog=blog).extra(
        select={"ctime": 'strftime("%%Y-%%m",create_time)'}).values('ctime').annotate(c=Count('nid'))

    if key == 'category':
        try:
            article_list = models.Article.objects.filter(blog=blog,category_id=val)
        except Exception as e:
            article_list = models.Article.objects.filter(blog=blog)
    elif key == 'tag':
        article_list = models.Article.objects.filter(blog=blog,tags__nid=val)
        # print(article_list)
    else:
        article_list = models.Article.objects.filter(blog=blog).extra(where=['strftime("%%Y-%%m",create_time)=%s',],params=[val,])

    ##########################分页功能#############################
    all_count = article_list.count()  # 获取数据库中指定对象的总条数
    # request.GET.get('page'):从URL中获取当前页 all_count:总条数 10:每页显示10条
    base_url = '/%s/%s/%s/' % (blog.user.username,key,val)  # 获取跳转的url
    page_info = PageInfo(request.GET.get('page'), all_count, 2, base_url, 11)
    user_list = article_list[page_info.start():page_info.end()]  # 每页显示的数据

    return render(request,'filter.html',{
        'blog':blog,
        'category_list':category_list,
        'tag_list':tag_list,
        'create_time_list':create_time_list,
        'article_list':article_list,
        'user_list': user_list, 'page_info': page_info
    })

def article(request,site,nid):
    if request.method == 'POST':
        try:
            request.session['user_info'].get('user_id')
        except Exception as e:
            return redirect('/')

        current_user_id = request.POST.get('user_id')
        article_id = nid
        content = request.POST.get('commented')
        models.Comment.objects.create(user_id=int(current_user_id),article_id=article_id,content=content)
        models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)
        return redirect('/%s/%s.html'%(site,nid))
    else:
        blog = models.Blog.objects.filter(site=site).first()
        if not blog:
            return redirect('/')

        # 获取分类
        category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
            ct=Count('nid'))

        # 获取标签
        tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
            ct=Count('id'))

        # 获取时间
        create_time_list = models.Article.objects.filter(blog=blog).extra(
            select={"ctime": 'strftime("%%Y-%%m",create_time)'}).values('ctime').annotate(c=Count('nid'))

        # 博主的所有文章
        article = models.Article.objects.filter(blog=blog,nid=nid).first()
        article_id = nid
        msg_list = models.Comment.objects.filter(article_id=int(article_id)).all().values('user_id','content','reply_id')
        if msg_list:
            msg_list_dict = {}
            for item in msg_list:
                item['nickname'] = models.UserInfo.objects.filter(nid=item['user_id']).values_list('nickname')[0]
                item['child'] = []
                msg_list_dict[item['user_id']] = item
            result = []
            for item in msg_list:
                pid = item['reply_id']
                if pid:
                    msg_list_dict[pid]['child'].append(item)
                else:
                    result.append(item)
        else:
            result = []

        from utils.comment import comment_tree
        comment_str = comment_tree(result)
        try:
            current_user_id = request.session['user_info'].get('user_id')  # userinfo 里的ID
        except Exception as e:
            current_user_id = ''

        return render(request, 'article.html', {
            'blog': blog,
            'category_list': category_list,
            'tag_list': tag_list,
            'create_time_list': create_time_list,
            'article': article,
            'comment_str': comment_str,
            'current_user_id':current_user_id
        })

def updown(request):
    response = {'status': '200', 'msg': ''}
    # 200 代表赞  201 代表踩  202 代表发生异常  203 代表已赞或已踩
    try:
        user_id = request.session.get('user_info').get('user_id')  # 去session拿已登录用户的ID
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))
        obj = models.UpDown.objects.filter(user_id=user_id, article_id=article_id).first()
        if obj:
            # 已经赞或踩过
            up_down = obj.up
            response['status'] = '203'
            if val == up_down:
                if val == 1:
                    response['msg'] = '你已赞过一次,不能再赞第二次'
                else:
                    response['msg'] = '你已踩过一次,请手下留情'
            else:
                if val == 1 and up_down == 0 :
                    response['msg'] = '你已踩过一次,现在又想赞别人,内心愧疚啦？'
                else:
                    response['msg'] = '你已赞过一次,现在又踩别人,这样做不太合适吧'

            return HttpResponse(json.dumps(response))
        else:
            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count') + 1)
                    response['status'] = '200'
                else:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count') + 1)
                    response['status'] = '201'
    except Exception as e:
        response['status'] = '202'
        response['msg'] = '你还没有登录,请登录后再进行该操作'

    return HttpResponse(json.dumps(response))

def comments(request,nid):

    response = {'status':True,'msg':None,'data':None}
    try:
        # 数据库查询到的真实数据
        article_id = nid
        msg_list = models.Comment.objects.filter(article_id=int(article_id)).all().values('user_id','content','reply_id')
        if msg_list:
            msg_list_dict = {}          # 新建一个字典
            for item in msg_list:      # 遍历查到的数据
                item['nickname'] = models.UserInfo.objects.filter(nid=item['user_id']).values_list('nickname')[0]
                item['child'] = []     # 给每个数据变成类似 {'id': 1, 'content': '写的不错', 'parent_id': None,'child' = []},
                msg_list_dict[item['user_id']] = item # msg_list_dict={1:{'id': 1, 'content': '写的不错', 'parent_id': None,'child' = []}}
            result = []                 # 新建一个列表
            for item in msg_list:      # 遍历查到的数据
                pid = item['reply_id']     # 拿到每个数据的parent_id
                if pid:  # 如果parent_id存在,则证明是子评论有父级
                    # 根据parent_id 先查到它的父级，然后把自己加进父级的child列表中
                    msg_list_dict[pid]['child'].append(item)
                else:
                    result.append(item)
        else:
            result = []

        response['data'] = result
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)
    return HttpResponse(json.dumps(response))

def management(request,**kwargs):
    try:
        if request.method == 'GET':
            blog = models.Blog.objects.filter(user_id=kwargs.get('user_id')).first()
            # 大分类
            type_choices = models.Article.type_choices
            # 用户自定义分类
            category_list = models.Category.objects.filter(blog_id=blog.nid)
            # 用户自定义标签
            tag_list = models.Tag.objects.filter(blog_id=blog.nid)

            conditions = {}
            for k,v in kwargs.items():
                if k == 'user_id':
                    continue
                kwargs[k] = int(v)
                if v != '0': # 传过来的kwargs中的值为字符串类型
                    conditions[k] = v

            conditions['blog_id'] = blog.nid
            # 拿到当前登录用户的所有文章
            article_list = models.Article.objects.filter(**conditions)

            user = models.UserInfo.objects.filter(nid=kwargs.get('user_id')).first()

            all_count = article_list.count()  # 获取数据库中指定对象的总条数
            # request.GET.get('page'):从URL中获取当前页 all_count:总条数 10:每页显示10条
            base_url = '/management/%s-%s-%s-%s' % (blog.nid,kwargs.get('article_type_id'),kwargs.get('category_id'),kwargs.get('tags__nid'))
            page_info = PageInfo(request.GET.get('page'), all_count, 2, base_url, 11)
            user_list = article_list[page_info.start():page_info.end()]  # 每页显示的数据

            return render(request,'layout_home.html',  # management.html
                          {'user':user,
                           'blog':blog,
                           'type_choices':type_choices,
                           'category_list':category_list,
                           'tag_list':tag_list,
                           'kwargs':kwargs,
                           'article_list':article_list,
                           'page_info':page_info,
                           'user_list':user_list,
                           })
        else:
            return HttpResponse('123')
    except Exception as e:
        return HttpResponse(str(e))

def add_article(request,**kwargs):
    try:
        if request.method == 'GET':

            blog_id = kwargs.get('blog_id')
            blog = models.Blog.objects.filter(nid=blog_id).first()
            obj = forms.AddArticleForm(blog_id)

            return render(request,'layout_add_article.html',{'obj':obj,'blog':blog})   # add_article.html
        else:
            blog_id = kwargs.get('blog_id')
            blog = models.Blog.objects.filter(nid=blog_id).first()
            obj = forms.AddArticleForm(blog_id,request.POST, request.FILES)

            if obj:

                article_title = request.POST.get('article_title') # 文章标题
                article_summary = request.POST.get('article_summary') # 文章简介
                content = request.POST.get('content') # 文章内容
                article_type_list = request.POST.get('article_type_list') # 网站分类id
                category_list = request.POST.get('category_list') # 个人分类id
                tag_list = request.POST.getlist('tag_list') # 个人标签id列表

                with transaction.atomic(): # 事物 原子性操作
                    article_new = models.Article.objects.create(title=article_title,summary=article_summary,blog_id=blog_id,
                                                  category_id=category_list,article_type_id=article_type_list)
                    if tag_list: # 如果标签列表中有值
                        for row in tag_list:
                            # print(row)
                            # print(type(row))
                            models.Article2Tag.objects.create(article_id=article_new.nid,tag_id=int(row))
                    models.ArticleDetail.objects.create(article_id=article_new.nid,content=content)
                return redirect('/')
            else:
                return render(request,'layout_add_article.html',{'obj':obj,'blog':blog})  # add_article.html
    except Exception as e:
        return HttpResponse(str(e))

def upload_img(request):
    """
    KindEditor富文本编辑框中有图片时,上传到指定路径并返回路径进行预览
    :param request: 
    :return: 
    """
    import os
    upload_type = request.GET.get('dir')
    file_obj = request.FILES.get('imgFile')
    file_path = os.path.join('static/imgs',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '错误了...'
    }
    import json
    return HttpResponse(json.dumps(dic))

# ##################分类的增删改查#####################

def layout_category(request,user_id):
    if request.method == 'GET':
        result = models.Category.objects.filter(blog__user__nid=user_id).all()
        user = models.UserInfo.objects.filter(nid=user_id).first()
        return render(request,'layout_category.html',{'result':result,'user':user})
    else:
        pass

def edit_category(request):
    user_id = request.session['user_info'].get('user_id')
    if request.method == 'GET':
        category_id = request.GET.get('nid')
        old_category_name = models.Category.objects.filter(blog__user__nid=user_id,nid=category_id).first()
        return render(request,'edit_category.html',{'old_category_name':old_category_name,'category_id':category_id})
    else:
        new_category_name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        models.Category.objects.filter(blog__user__nid=int(user_id),nid=int(category_id)).update(title=new_category_name)
        return redirect('/layout_category/%s.html'%user_id)

def add_category(request):
    user_id = request.session['user_info'].get('user_id')
    if request.method == 'GET':
        return render(request,'add_category.html')
    else:
        blog_id = models.Blog.objects.filter(user_id=user_id).values('nid')[0]['nid']
        new_category_name = request.POST.get('name')
        print(new_category_name)
        print(blog_id)
        models.Category.objects.create(blog_id=int(blog_id),title=new_category_name)
        return redirect('/layout_category/%s.html'%user_id)

# ##################标签的增删改查#####################

def layout_tag(request,user_id):
    if request.method == 'GET':
        result = models.Tag.objects.filter(blog__user__nid=user_id).all()
        user = models.UserInfo.objects.filter(nid=user_id).first()
        return render(request,'layout_tag.html',{'result':result,'user':user})
    else:
        pass

def edit_tag(request):
    user_id = request.session['user_info'].get('user_id')
    if request.method == 'GET':
        tag_id = request.GET.get('nid')
        old_tag_name = models.Tag.objects.filter(blog__user__nid=user_id,nid=tag_id).first()
        return render(request,'edit_tag.html',{'old_tag_name':old_tag_name,'tag_id':tag_id})
    else:
        new_tag_name = request.POST.get('name')
        tag_id = request.POST.get('tag_id')
        print(new_tag_name)
        print(tag_id)
        models.Tag.objects.filter(blog__user__nid=int(user_id),nid=int(tag_id)).update(title=new_tag_name)
        return redirect('/layout_tag/%s.html'%user_id)

def add_tag(request):
    user_id = request.session['user_info'].get('user_id')
    if request.method == 'GET':
        return render(request,'add_tag.html')
    else:
        blog_id = models.Blog.objects.filter(user_id=user_id).values('nid')[0]['nid']
        new_tag_name = request.POST.get('name')
        models.Tag.objects.create(blog_id=int(blog_id),title=new_tag_name)
        return redirect('/layout_tag/%s.html'%user_id)






