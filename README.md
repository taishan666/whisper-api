# whisper-api

#### 介绍
使用winsper语音识别开源模型封装成openai chatgpt兼容接口

#### 软件架构
使用uvicorn、fastapi、openai-whisper等开源库实现高性能接口

更多介绍 `[https://blog.csdn.net/weixin_40986713/article/details/138712293](https://blog.csdn.net/weixin_40986713/article/details/138712293)`

#### 使用说明

1.  下载代码
2.  安装依赖 `pip install -r requirements.txt`
3.  运行代码 `python main.py`

这里的 `http://0.0.0.0:3003` 就是连接地址。

#### docker 

1. docker打包命令

`docker build -t whisper .`

2.docker命令启动

 **gpu显卡模式** 

`docker run -itd --name whisper-api -p 3003:3003--gpus all --restart=always whisper`

 **cpu模式** 
`docker run -itd --name whisper-api -p 3003:3003--restart=always whisper`

 **鉴权模式** 

```
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken --gpus all --restart=always whisper
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken --restart=always whisper
```
- 默认 ACCESS_TOKEN=`sk-tarzan`

#### 配置文件
options.json
```
{
  "model_size": "base",
  "language": "Chinese"
}
```

