

# QueryTools -  1.0

### 郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担。



```

```





```text
任务流程:
    1.读取文本中的ip/domain
        domain -> 查询备案
        ip -> 判断是国内还是国外ip
        国内ip: 查询ip下的域名 -> 查询域名备案(seo等)
        国外ip: 查询ip下的域名 -> 查询域名seo权重
        
```



###运行

```text
命令行运行: cmd 
cd queryTools

默认queryTools中的text.txt (但是text.txt需要放数据进去)
python start.py 

指定txt
python start.py -f D:\XXX\CC\hello.txt
```





### 存储：json 


### 使用注意事项：如果本地开启了科学,那么可能你会得到一大串红色的东西,因为我没写带本地代理（lan)
