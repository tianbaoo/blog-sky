# 博客园笔记
[个人学习笔记](http://www.cnblogs.com/guotianbao/)  
# 博客
线上地址：[博客天地](http://207.246.124.116/)  请挂梯子访问,否则速度会很慢，服务器位于纽约新泽西。
# 开发环境
Python==3.6.1  
beautifulsoup4==4.6.0  
Django==1.10.6  
lxml==4.1.1  
Pillow==4.2.1  
# Windows7下安装运行  
把blog-sky文件下载下来  
1. 打开cmd窗口输入：pip install virtualenv 创建虚拟环境（前提是你已经安装好pip）  
2. 桌面新建一个名为Test的文件夹,进入该文件夹Shift+鼠标右键打开cmd输入：virtualenv testenv  
3. Test的文件夹内生成了testenv文件夹，进入testenv文件夹的Scripts文件夹中，Shift+鼠标右键打开cmd输入：activate激活虚拟环境  
4. 把下载的blog-sky文件夹拖入Scripts文件夹中，在cmd中进入blog-sky文件夹：cd blog-sky  
5. requirements.txt所在blog-sky文件夹内，在cmd输入：pip install -r requirements.txt 回车    
6. 安装完所有的环境依赖后，在cmd中再输入：python manage.py runserver  
7. 不要关闭cmd窗口，去浏览器打开：127.0.0.1:8000 看看是否可以访问。  
# 功能
1. 写博客 （kindeditor-4.1.10 编译器）
2. Form组件验证用户登录和注册
3. 用户头像上传和预览
4. 登陆后后台可添加个人分类、标签
5. 登陆后可点赞、踩、评论他人博客
6. 进入个人后台可组合搜索个人文章
7. 登录和注册时动态生成图片验证码
8. 分页功能
9. 对用户发的文章和评论内容进行xss攻击检查，过滤关键词、script标签
# 预览
首页
![image](https://raw.githubusercontent.com/tianbaoo/blog-sky/master/readme_add_pic/index.png)
注册
![image](https://raw.githubusercontent.com/tianbaoo/blog-sky/master/readme_add_pic/register.png)
后台
![image](https://raw.githubusercontent.com/tianbaoo/blog-sky/master/readme_add_pic/home.png)
标签管理
![image](https://raw.githubusercontent.com/tianbaoo/blog-sky/master/readme_add_pic/tag.png)





