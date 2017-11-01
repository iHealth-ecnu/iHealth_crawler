## iHealth_crawler
iHealth 项目的内容爬虫

### 特性

### 安装依赖
* requests
* pymongo
* lxml

### MongoDB 配置
1. 开启 MongoDB 权限认证：**在配置文件中加入 auth = true**

2. 创建管理员用户（如果你是第一次使用 MongoDB）  
```
use admin
db.createUser({user:"admin",pwd:"admin123",roles:["userAdminAnyDatabase"]})
```
管理员用户用来创建其他数据库和用户

3. 使用管理员账户远程登录
```
C:\Users\cs>mongo [your_ip]:27017
> use admin
switched to db admin
> db.auth('admin','admin123')
1
```

4. 创建 iHealth 数据库，以及操作该数据库的用户
```
use iHealth         // 创建数据库，并作为认证数据库
db.createUser({
    user:'admin',   // 用户名
    pwd:'admin123', // 用户密码
    roles:[{role:'readWrite',db:'iHealth'}]     // 为该用户赋予数据库的读写权限
})
```

5. 使用该用户远程登录 iHealth 数据库
```
C:\Users\cs>mongo [your_ip]:27017
> use iHealth
switched to db iHealth
> db.auth('admin','admin123')
1
> db.getCollectionNames()
[ ]
```
数据库刚刚创建，所以没有数据


### 启动说明
1. 安装环境：Python 环境和依赖 + MongoDB 配置

2. 配置 common.py 中的数据库信息
```
# 数据库配置
mongo_dbname = 'iHealth'
mongo_host = 'your_ip'          # mongodb 主机地址
mongo_port = 27017              # mongodb 主机端口
mongo_user = 'your_user'        # mongodb 登陆用户
mongo_pwd  = 'your_password'    # mongodb 用户密码
```

3. 运行
    * Windows :  
    ```
    python iHealth_crawler.py
    ```  
    * Linux :  
    ```
    sh server.sh start
    ```


### 注意
* 脚本功能：
    * server.sh：启动/停止/重启/查看状态/查看日志 heatbox 服务，用法：  
    ```
    Usages: sh server.sh [start|stop|restart|status|log]
    ```

### 参考资料
* Python爬虫利器三之Xpath语法与lxml库的用法  
http://cuiqingcai.com/2621.html