

# QueryTools - 春节版

**郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，<u>任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担</u>** 。

<p align="center"><a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a><a href="https://github.com/z-bool/QueryTools"><img  src="https://goreportcard.com/badge/github.com/projectdiscovery/httpx"></a></p>

<p align="center"><a href="#install">依赖安装</a> · <a href="#tall">使用说明</a> · <a href="#notice">注意事项</a> · <a href="#communicate">技术交流</a></p>

<div id="install"></div>

### 依赖安装

```bash
pip install -r requirements.txt # 正常这句就OK，成功安装所有依赖，但是会有fake-useragent报错的
pip install ./lib/fake-useragent-1.1.1.tar.gz # fake-useragent报错安装不上的用安装包安装
```

如果在使用安装包安装还有问题的话可以在群里提问或私聊。

<div id= "tall"></div>

### 使用说明

作为一个安全的行内人士，大家在交CNVD时肯定都被资产的<u>域名、ICP、权重、资产</u>等需要手工收集而困扰，所以站在爱偷懒的开发者的角度，选择自动化一站式搜哈。但是在结果处理上是选择JSON格式(由于在项目设计之初没想到用excel后面就懒得改了)，JSON格式在常规使用上也对我们其实并无影响，无论写对接读取处理的系统还是直接放在**火狐浏览器(默认)** |**Chrome(装插件)** 格式化后都轻松可读，对开发者和安全大佬们都很友好。

```text
# 由于是py脚本所以不限制系统
python start.py                   # 使用默认文件text.txt
python start.py -f domains.txt    # 自定义文件domains.txt
```

测试结果会在终端打印以及输出一份`data.json` 在当前目录下。

![image-20230118190512036](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230118190512036.png)

这是为了限制速度导致接口在多线程下被迅速封禁的，如果本地就全局了变化的代理的可以开放线程锁，位置在`tools/task.py` 中的该位置：

![image-20230118190801082](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230118190801082.png)

这里还设置了一个延时1-3秒，嫌速度慢的可以自己删。



设计之初是为了区分域名和IP，后期修复。临时解决方案:'全局替换为","{全局替换为{,"}全局替换为}。

<div id="notice"></div>

### 注意事项

- 本项目是通过多个ICP接口批量查询得到，目前没有设置代理，可能会存在IP拒绝连接。虽然为了缓解这一情况QueryTools通过多个接口轮询以及失败后重新入队的方式来解决，但是如果数据量多大的话建议还是分割处理。
- JSON处理结果可能会因为中间的异常导出部分出错，可以用文本全局替换的方式处理。
- 爬取的时候不要挂代理，把Clash这些记得都关掉再启动，几千条数据一个IP就OK，不然你会收获一大堆报错。
- 使用前先将data.json文件删除

<div id="communicate"></div>

### 技术交流

<img src="https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230116172606976.png" alt="交流群" style="zoom: 80%;" align="left" /><img src="https://cdn.jsdelivr.net/gh/z-bool/images@master/img/qrcode_for_gh_c90beef1e2e7_258.jpg" alt="阿呆攻防公众号" style="zoom:100%;" />![image-20230116173105809](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230116173105809.png)



微信群有过期时间限制，如果有技术交流、BUG解决、环境安装问题都可以于公众号/QQ群获取微信群信息。
