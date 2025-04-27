# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP  
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("Article Extractor")

@mcp.tool()
def extract_article(url: str) -> dict:
    """从指定URL提取文章正文"""

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 尝试多种常见文章容器选择器
        article = (soup.find('div', id='detail-content') or
                  soup.find('div', class_='article-content') or
                  soup.find('div', class_='article-body') or
                  soup.find('div', class_='content'))

        if not article:
            return {"error": "无法提取文章正文"}

         # 提取纯文本并去除多余空白
        text = article.get_text(' ', strip=True)
        # 去除可能存在的视频描述等无关内容
        return {
            "url": url,
            "content": '\n'.join(line for line in text.split('\n') 
                           if line.strip())
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
