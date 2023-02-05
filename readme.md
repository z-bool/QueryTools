

# QueryTools - 重构版

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

作为一个安全的行内人士，大家在交CNVD时肯定都被资产的<u>域名、ICP、权重、资产</u>等需要手工收集而困扰，所以站在爱偷懒的开发者的角度，选择自动化一站式搜哈。重构版使用csv的导出方式让结果更直观可读。

```text
# 由于是py脚本所以不限制系统
python start.py                   # 使用默认文件text.txt
python start.py -f domains.txt    # 自定义文件domains.txt
```

测试结果会在终端打印以及输出一份`result.csv` 在当前目录下。

![image-20230205122621572](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230205122621572.png)

![image-20230205122727443](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230205122727443.png)

![image-20230205122738752](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230205122738752.png)

![image-20230205122749648](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230205122749648.png)

<div id="notice"></div>

### 注意事项

- 已经完全重构了，没啥注意事项，里面Request Error都做过重新入队处理，不必担心，这次把速度降下来了，大家耐心多等等。

<div id="communicate"></div>

### 技术交流

<img src="https://cdn.jsdelivr.net/gh/z-bool/images@master/img/qrcode_for_gh_c90beef1e2e7_258.jpg" alt="阿呆攻防公众号" style="zoom:100%;" />![image-20230116173105809](https://cdn.jsdelivr.net/gh/z-bool/images@master/img/image-20230116173105809.png)



微信群有过期时间限制，如果有技术交流、BUG解决、环境安装问题都可以于公众号/QQ群获取微信群信息。
