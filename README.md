# Flux Schnell Server

基于[Flux Schnell](https://huggingface.co/spaces/black-forest-labs/flux-1-schnell)模型的MCP图像生成服务器。

## 功能特点

- 提供基于MCP协议的图像生成API
- 支持自定义图片尺寸（宽度和高度）
- 支持设置随机种子以复现特定生成结果
- 支持异步流式响应
- 提供HTTP接口调用Hugging Face的模型服务

## 安装要求

- Python >= 3.10
- 依赖包：
  - httpx >= 0.28.1
  - mcp[cli] >= 1.3.0

## 使用方法
### 开发环境设置

1. 创建并激活 Python 虚拟环境
```bash
uv venv && source .venv/bin/activate  # Unix/macOS
# 或
.venv\Scripts\activate  # Windows
```

2. 安装开发依赖
```bash
uv sync  # 以可编辑模式安装项目
```

### 调试方法

1. 启用调试
```bash
mcp dev main.py
或者
npx -y @modelcontextprotocol/inspector uv run main.py
```

2. 调用图像生成工具：
```python
# 示例代码
async def test_main():
    img_url = await image_generation(
        prompt="your prompt here",
        image_width=512,  # 可选，默认512
        image_height=512, # 可选，默认512
        seed=3           # 可选，默认3
    )
    print(img_url)
```

## API参数说明

- `prompt` (str): 图像生成提示词
- `image_width` (int, optional): 生成图片宽度，默认512
- `image_height` (int, optional): 生成图片高度，默认512
- `seed` (int, optional): 随机种子，默认3

## 示例

### 春天的生机

![春天的生机](https://black-forest-labs-flux-1-schnell.hf.space/file=/tmp/gradio/45d6489d73142fa77851d8985bb1010572433d6a/image.webp)

> 春天来了，大地苏醒，万物复苏。花儿竞相开放，嫩绿的叶子在微风中轻轻摇曳。空气中弥漫着泥土的芬芳和花儿的香气。小鸟在枝头欢快地歌唱，蝴蝶在花丛中翩翩起舞。阳光洒在大地上，温暖而明亮。春天的生机勃勃，让人心旷神怡。

这个示例展示了使用服务生成的图片效果。您可以在demo目录中找到完整的网页展示代码。

生成的图片URL可以直接用于：
1. 网页图片展示
2. 社交媒体分享
3. 应用程序界面