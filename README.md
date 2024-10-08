# whisper-api

#### 介绍
使用winsper语音识别开源模型封装成openai chatgpt兼容接口

#### 软件架构
使用uvicorn、fastapi、openai-whisper等开源库实现高性能接口

更多介绍 [https://blog.csdn.net/weixin_40986713/article/details/138712293](https://blog.csdn.net/weixin_40986713/article/details/138712293)

#### 使用说明

1.  下载代码
2.  安装 ffmpeg [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html#build-windows)
3.  安装依赖 项目根目录下执行命令 `pip install -r requirements.txt`
4.  运行代码 项目根目录下执行命令 `python main.py`

这里的 `http://0.0.0.0:3003` 就是连接地址。

- 首次启动会下载模型，如果下载失败，请手动下载模型，放在项目根目录下，并修改 `main.py` 里的 `model_size` 参数。

#### docker 

1. docker打包命令

```
docker build -t whisper .
```


2.docker命令启动

 **gpu显卡模式** 

```
docker run -itd --name whisper-api -p 3003:3003 --gpus all --restart=always whisper
```
- 默认 ACCESS_TOKEN=sk-tarzan

 **cpu模式** 

```
docker run -itd --name whisper-api -p 3003:3003 --restart=always whisper
```
- 默认 ACCESS_TOKEN=sk-tarzan

 **鉴权模式** 

```
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken --gpus all --restart=always whisper
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken --restart=always whisper
```
- yourtoken 修改你设置的鉴权token,接口调用header 里传 `Authorization:Bearer sk-tarzan`

 **参数模式** 

```
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken MODEL_SIZE=base MODEL_SIZE=base LANGUAGE=Chinese --gpus all --restart=always whisper
docker run -itd --name whisper-api -p 3003:3003-e ACCESS_TOKEN=yourtoken MODEL_SIZE=base MODEL_SIZE=base LANGUAGE=Chinese  --restart=always whisper
```
- ACCESS_TOKEN 默认是`sk-tarzan`,修改你设置的鉴权token,接口调用header 里传 `Authorization:Bearer sk-tarzan`
- MODEL_SIZE模型类型，默认是small,可选模型Available models: ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large']
- LANGUAGE语言类型，默认根据用户语言自动选择，可选语言Available languages: ['auto','Chinese','English','French','German','Italian','Korean','Polish','Portuguese','Russian','Spanish','Japanese']
- LANGUAGE=auto 时会再第一次调用模型时候，下载tiny模型，使用tiny模式来判断用户的语言
- 因为whisper模型训练时，没有区分中文简体和繁体，代码里对输出中文做了格式化处理，默认中文设置为简体中文
## 可用型号和语言

您可能还需要安装 [`rust`](http://rust-lang.org)，以防 [tiktoken](https://github.com/openai/tiktoken) 没有为您的平台提供预编译的轮子。如果在上述 `pip install` 命令过程中遇到安装错误，请按照 [入门页面](https://www.rust-lang.org/learn/get-started) 的指引来安装 Rust 开发环境。此外，您可能需要配置 `PATH` 环境变量，例如 `export PATH="$HOME/.cargo/bin:$PATH"`。如果安装过程中出现 `No module named 'setuptools_rust'` 错误，您需要安装 `setuptools_rust`，可以通过运行类似命令来完成。

|  尺寸| 参数大小| 纯英文型号 | 多语言模型 | 所需显存 | 相对速度 |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |     不适用       |      `large`       |    ~10 GB     |       1x       |


针对仅英文应用的`.en`模型往往表现更佳，尤其是对于`tiny.en`和`base.en`模型。我们观察到，对于`small.en`和`medium.en`模型，这种差异变得不那么明显。

Whisper的表现因语言而异，幅度很大。下图展示了使用WER（词错误率）或CER（字符错误率，以斜体显示）在Common Voice 15和Fleurs数据集上评估的`large-v3`和`large-v2`模型按语言划分的性能分解。其他模型和数据集对应的更多WER/CER指标，以及用于翻译评估的BLEU（双语评估替代）分数，可以在[论文](https://arxiv.org/abs/2212.04356)的附录D.1、D.2和D.4中找到。
 **docker日志查看**
```
docker logs -f [容器id或容器名称]
```

## 可识别语言细分

- Dutch: 荷兰语
- Spanish: 西班牙语
- Korean: 韩语
- Italian: 意大利语
- German: 德语
- Thai: 泰语
- Russian: 俄语
- Portuguese: 葡萄牙语
- Polish: 波兰语
- Indonesian: 印度尼西亚语
- Mandarin (TW): 普通话（台湾）
- Swedish: 瑞典语
- Czech: 捷克语
- English: 英语
- Japanese: 日语
- French: 法语
- Romanian: 罗马尼亚语
- Cantonese (CN): 粤语（中国大陆）
- Turkish: 土耳其语
- Mandarin (CN): 普通话（中国大陆）
- Catalan: 加泰罗尼亚语
- Hungarian: 匈牙利语
- Ukrainian: 乌克兰语
- Greek: 希腊语
- Bulgarian: 保加利亚语
- Arabic: 阿拉伯语
- Serbian: 塞尔维亚语
- Macedonian: 马其顿语
- Cantonese (HK): 粤语（香港）
- Latvian: 拉脱维亚语
- Slovenian: 斯洛文尼亚语
- Hindi: 印地语
- Galician: 加利西亚语
- Danish: 丹麦语
- Urdu: 乌尔都语
- Slovak: 斯洛伐克语
- Hebrew: 希伯来语
- Finnish: 芬兰语
- Azerbaijani: 阿塞拜疆语
- Lithuanian: 立陶宛语
- Estonian: 爱沙尼亚语
- Nynorsk: 新挪威语
- Welsh: 威尔士语
- Punjabi: 旁遮普语
- Afrikaans: 南非荷兰语
- Persian: 波斯语
- Basque: 巴斯克语
- Vietnamese: 越南语
- Bengali: 孟加拉语
- Nepali: 尼泊尔语
- Marathi: 马拉地语
- Belarusian: 白俄罗斯语
- Kazakh: 哈萨克语
- Armenian: 亚美尼亚语
- Swahili: 斯瓦希里语
- Tamil: 泰米尔语
- Albanian: 阿尔巴尼亚语
