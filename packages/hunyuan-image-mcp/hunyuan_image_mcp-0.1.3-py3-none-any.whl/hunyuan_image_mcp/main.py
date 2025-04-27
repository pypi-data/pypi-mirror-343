from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import os
import logging
import httpx
from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Dict

from hunyuan_image_mcp.exceptions import *

# Initialize FastMCP server
mcp = FastMCP(
    "hunyuan-image-mcp",
    host="0.0.0.0",
    port=os.getenv("PORT", 8000)
)

apiKey = os.getenv("API_KEY")


headers = {
    "X-Source": "web",
    "Content-Type": "application/json",
    "Authorization": apiKey
}


@mcp.tool()
async def hunyuanText2Image(imageUrl: str, prompt: str) -> dict:
    """
    通过文字描述生成图片，或者根据要求修改图片
    
    Args:
        imageUrl: 需要修改的图片url地址
        prompt: 用于生成图片或者修改图片的提示词
    """
    
    hunyuanText2ImageUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"hunyuanText2Image",
            "arguments": {
                "image_url": imageUrl,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用混元文本转图像")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(hunyuanText2ImageUrl, headers=headers, json=payload, timeout=timeout)
        response_json = response.json()
        if "error" in response_json:
            error_data = response_json["error"]
            return TextContent(
                type="text",
                text=str(error_data)
            )
        
        return TextContent(
            type="text",
            text=response_json["result"]["content"][0]["text"]
        )
    except YuanqiAPIError as e:
        return TextContent(
            type="text",
            text=f"调用工具失败: {str(e)}"
        )


def run_mcp():
    print("starting")
    mcp.run()

if __name__ == '__main__':
    print("starting main")
    logging.info("开始运行腾讯混元生图")
    run_mcp()
