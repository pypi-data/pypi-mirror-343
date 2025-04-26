[English Version](README_en.md)

# AICLI

一个基于AI的命令行助手工具。

## 生动的例子

![](./images/python-automate-aicli-ex1-zh.gif)

## 安装

### PYPI 安装

```sh
pip install aicli-agent
```

### 源码安装

1. 克隆此仓库:

```sh
git clone https://github.com/callmexss/aicli.git
cd aicli
```

2. 安装依赖:

```sh
pip install -e .
```

3. 设置环境变量:

复制`.env.example`文件为`.env`并填写必要的环境变量:
```sh
cp .env.example .env
```
然后编辑`.env`文件,填写您的API密钥和其他设置。

## 使用

安装后,您可以直接在命令行中使用`aicli`命令:

```sh
aicli 查询
```

例如:

```sh
aicli 列出当前目录的文件
aicli "帮我安装 nvm"
```

## 致谢

本项目基于 [GeneralAgent](https://github.com/CosmosShadow/GeneralAgent) 构建。
