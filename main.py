import json
from mcp.server.fastmcp import FastMCP
import httpx

server = FastMCP("flux-schnell-server")

@server.tool()
async def image_generation(prompt: str, image_width: int = 512, image_height: int = 512, seed: int = 3):
    """
    Generate an image from a prompt.
    Args:
        prompt (str): 生成图片的提示词
        image_size (int, optional): 生成图片的大小. Defaults to 512.
    Returns:
        str: 生成的图片的base64编码
    """
    async with httpx.AsyncClient() as client:
        try:
            # 创建图片生成请求
            # data: [提示词, seed种子, 是否使用随机种子, 图片宽, 图片高, 步长]
            response = await client.post(
                "https://black-forest-labs-flux-1-schnell.hf.space/call/infer",
                json={"data": [prompt, 0, True, image_width, image_height, seed]},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            response_data = response.json()

            event_id = response_data.get("event_id")
            if not event_id:
                return "Failed to generate image: No event_id received."

            # 构造流式获取图片的URL
            url = f"https://black-forest-labs-flux-1-schnell.hf.space/call/infer/{event_id}"
            full_response = ""

            # 获取图片数据
            async with client.stream("GET", url) as stream_response:
                stream_response.raise_for_status()
                async for chunk in stream_response.aiter_text():
                    full_response += chunk

            # 解析最终图片URL
            data_parts = full_response.split("data: ")
            if len(data_parts) < 2:
                return "Failed to parse image response."

            image_data = json.loads(data_parts[-1])
            return image_data[0]["url"]

        except httpx.HTTPStatusError as e:
            return f"HTTP error occurred: {e.response.status_code} {e.response.text}"
        except json.JSONDecodeError:
            return "Failed to decode JSON response."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
def main():
    server.run(transport="stdio")

async def test_main():
    img_url = await image_generation("a cat")
    print(img_url)

if __name__ == "__main__":
    main()
    # import asyncio
    # asyncio.run(test_main())
