#!/usr/bin/env python
#_*_coding:utf-8_*_

from django.forms import Form,fields,widgets
from django.core.exceptions import ValidationError
from app01 import models

class LoginForm(Form):
    """
    验证用户登录的Form组件
    """
    # required=True 要求非空 'placeholder': u'用户名' 提示用户
    user = fields.CharField(min_length=2, max_length=32, required=True,
                                error_messages={
                                    'min_length': '用户名太短',
                                    'max_length': '用户名太长',
                                    'required': '用户名不能为空'
                                },
                                widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'用户名'})
                                )

    passwd = fields.CharField(min_length=6, max_length=64, required=True,
                              error_messages={
                                  'min_length': '密码太短',
                                  'max_length': '密码太长',
                                  'required': '密码不能为空'
                              },
                              widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'密码'})
                              )
    code = fields.CharField(required=True,
                            error_messages={
                                'required': '验证码不能为空'
                            },
                            widget=widgets.TextInput(attrs={'class': 'form-control'})
                            )
    def __init__(self,request,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)
        self.request = request

    def clean_code(self):       # clean 加 下划线 加 字段名 进行对code的验证
        # 获取我们输入的验证码值 我们的各种输入的数据都存在self.cleaned_data['字段名']里
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')  # 去session的获取验证码的值,进行对比验证
        if input_code.upper() == session_code.upper():
            return input_code                            # 返回我们的输入值
        else:
            self.add_error('code', ValidationError('验证码错误'))  # 把错误加到errors中

class RegisterForm(Form):
    """
        验证用户注册的Form组件
    """
    username = fields.CharField(min_length=2,max_length=8,required=True,
                              error_messages={
                                  'min_length':'用户名太短',
                                    'max_length':'用户名太长',
                                    'required':'用户名不能为空'
                                },
        widget = widgets.TextInput(attrs={'class':'form-control','placeholder': u'用户名'})
    )
    nickname = fields.CharField(min_length=2,max_length=8,required=True,
                              error_messages={
                                  'min_length':'昵称太短',
                                    'max_length':'昵称太长',
                                    'required':'昵称不能为空'
                                },
        widget=widgets.TextInput(attrs={'class': 'form-control','placeholder': u'昵称'})
    )
    email = fields.EmailField(required=True,
                             error_messages={
                                 'required': u'邮箱不能为空',
                                 'invalid': u'邮箱格式错误'
                             },
        widget=widgets.EmailInput(attrs={'class': 'form-control','placeholder': u'电子邮箱'})
    )
    passwd = fields.CharField(min_length=6,max_length=64,required=True,
                              error_messages={
                                  'min_length':'密码太短',
                                    'max_length':'密码太长',
                                    'required':'密码不能为空'
                                },
        widget=widgets.PasswordInput(attrs={'class': 'form-control','placeholder': u'密码'})
    )
    passwd2 = fields.CharField(required=True,
                            error_messages={
                                    'required':'密码不能为空'
                                },
        widget=widgets.PasswordInput(attrs={'class': 'form-control','placeholder': u'确认密码'})
    )
    avatar = fields.FileField(
        widget = widgets.FileInput(attrs={'id':"imgSelect",'class':"f1",'title':u'上传头像'})
    )
    code = fields.CharField(required=True,
                            error_messages={
                                    'required':'验证码不能为空'
                                },
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self,request,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.request = request

    def clean_code(self):       # clean 加 下划线 加 字段名 进行对code的验证
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        else:
            self.add_error('code', ValidationError('验证码错误'))

    def clean(self):   # clean方法是Form组件一定会执行的
        p1 = self.cleaned_data.get('passwd')
        p2 = self.cleaned_data.get('passwd2')
        if p1 == p2 :
            return None
        self.add_error('passwd2',ValidationError('密码不一致'))

class AddArticleForm(Form):
    article_title = fields.CharField(widget=widgets.TextInput(attrs={'class': "article_title"}),
                                     error_messages={
                                         'required': '文章标题不能为空'
                                        })
    article_summary = fields.CharField(widget=widgets.Textarea(attrs={'class': "article_summary"}),
                                     error_messages={
                                         'required': '文章简介不能为空'
                                        })
    content = fields.CharField(widget=widgets.Textarea(attrs={'id': 't1'}))
    article_type_list = fields.ChoiceField(widget=widgets.RadioSelect(attrs={'class': "article_type_id"}))
    category_list = fields.ChoiceField(widget=widgets.RadioSelect(attrs={'class': "category_id"}))
    tag_list = fields.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple(attrs={'class': "tag_id"}))

    def __init__(self,blog_id, *args, **kwargs):
        super(AddArticleForm, self).__init__(*args, **kwargs)
        self.blog_id = blog_id
        self.fields['article_type_list'].widget.choices = models.Article.type_choices
        self.fields['category_list'].widget.choices = models.Category.objects.filter(blog=self.blog_id).values_list('nid','title')
        self.fields['tag_list'].widget.choices = models.Tag.objects.filter(blog_id=self.blog_id).values_list('nid','title')

    def clean_content(self):
        content = self.cleaned_data['content'] # Form组件帮验证 防止xss攻击
        from utils.xss import xss
        return xss(content)