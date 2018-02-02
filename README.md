# pkulaw-spider

### 基于bs3的spider, 用于从 "北大法宝" 网站上抓取所需数据.

### 使用

* 环境要求

    * Python 2.7 <br>

    * 所需依赖

        * MySQLdb // MySQL数据库操作库
        * BeautifulSoup // 对象化dom树, [Doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#)
        * requests //  发送网络请求, [Doc](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)

* 使用

    * 执行sql文件配置数据库

    * 修改 ```config.py``` 中数据库配置

    * 执行命令

        ```
        python main.py
        ```