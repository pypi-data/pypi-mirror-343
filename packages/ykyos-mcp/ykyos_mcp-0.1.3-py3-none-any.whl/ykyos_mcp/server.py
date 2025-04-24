"""
MCP Server for URL Processing
.
METhis script implements a Model Context Protocol (MCP) server with three tools:
1. fetch_markdown: Takes a URL and returns its content as markdown using the Firecrawl API
2. extract_images: Takes markdown content and extracts all image URLs
3. download_images: Takes a list of image URLs and downloads them to a specified directory
"""

import os
import re
import asyncio
import aiohttp
import ssl
import aiofiles
from urllib.parse import urlparse, urljoin

# 简化实现，不依赖外部mcp包
class Context:
    """简化的Context类，用于进度报告"""
    def __init__(self):
        pass
        
    def info(self, message):
        print(f"INFO: {message}")
        
    def error(self, message):
        print(f"ERROR: {message}")

class FastMCP:
    """简化的FastMCP类，用于工具注册"""
    def __init__(self, name):
        self.name = name
        self.tools = {}
        
    def tool(self):
        """工具装饰器"""
        def decorator(func):
            self.tools[func.__name__] = func
            return func
        return decorator
        
    def run(self):
        """启动服务器"""
        print(f"Starting {self.name} server...")
        # 实际应用中这里应该启动服务器

# Get download path from environment variable
DOWNLOAD_BASE_PATH = os.environ.get('DOWNLOAD_BASE_PATH', './downloads')

# Initialize the MCP server
mcp = FastMCP("URL Processor and Image Extractor")

@mcp.tool()
async def fetch_markdown(url: str, ctx: Context = None) -> str:
    """
    Fetches content from a URL using Firecrawl API.
    
    Args:
        url: The original URL to fetch content from
        ctx: MCP context for progress reporting
        
    Returns:
        str: The raw content from the URL
    """
    if ctx:
        ctx.info(f"Fetching content from {url} using Firecrawl")
    
    # Firecrawl API endpoint and headers
    api_url = "https://api.firecrawl.dev/v1/scrape"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}"
    }
    payload = {
        "url": url,
        "pageOptions": {
            "includeHtml": False
        }
    }
    try:
        # 创建SSL上下文，设置为不验证证书
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 使用自定义SSL上下文创建客户端会话
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            if ctx:
                ctx.info(f"Connecting to Firecrawl API with custom SSL settings")
            async with session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get('data', {}).get('content', '')
                    if ctx:
                        ctx.info(f"Successfully fetched content ({len(content)} characters)")
                    return content
                else:
                    error_msg = f"Error: Failed to fetch content from {url}. Status code: {response.status}"
                    if ctx:
                        ctx.error(error_msg)
                    return error_msg
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg

@mcp.tool()
async def extract_images(content: str, ctx: Context = None) -> list:
    """
    从各种文本内容中提取所有图片 URL。
    
    Args:
        content: 包含图片引用的文本内容（支持 Markdown、HTML 和其他文本格式）
        ctx: 用于进度报告的 MCP 上下文
        
    Returns:
        list: 在内容中找到的图片 URL 列表
    """
    if ctx:
        ctx.info("从内容中提取图片 URL")
    
    # 正则表达式模式
    # Markdown 图片语法: ![alt text](image_url)
    markdown_pattern = r'!\[.*?\]\((.*?)\)'
    
    # HTML 图片标签: <img src="image_url">
    html_pattern = r'<img\s+[^>]*?src=[\'"]([^\'"]+)[\'"][^>]*?>'
    
    # CSS 背景图片: background-image: url('image_url')
    css_pattern = r'background(-image)?:\s*url\([\'"]?([^\'"]+)[\'"]?\)'
    
    # 其他可能的 URL 模式 (简单的 http/https 链接，以常见图片扩展名结尾)
    url_pattern = r'https?://[^\s<>"\']+\.(?:jpg|jpeg|png|gif|webp|svg|bmp|tiff|ico)(?:\?[^\s<>"\']*)?\b'
    
    # 查找所有匹配项
    markdown_matches = re.findall(markdown_pattern, content)
    html_matches = re.findall(html_pattern, content)
    
    # 从 CSS 背景中提取
    css_matches = [match[1] for match in re.findall(css_pattern, content)]
    
    # 查找独立的图片 URL
    url_matches = re.findall(url_pattern, content)
    
    # 合并所有匹配项
    all_images = markdown_matches + html_matches + css_matches + url_matches
    
    # 去除重复项
    unique_images = list(dict.fromkeys(all_images))
    
    if ctx:
        ctx.info(f"在内容中找到 {len(unique_images)} 个唯一图片 URL")
    
    # 返回图片 URL 列表
    return unique_images

@mcp.tool()
async def download_images(image_urls: list, target_directory: str = None, ctx: Context = None) -> str:
    """
    Downloads images from a list of URLs to the specified directory.
    
    Args:
        image_urls: List of image URLs to download
        target_directory: Directory to save the downloaded images (defaults to DOWNLOAD_BASE_PATH)
        ctx: MCP context for progress reporting
        
    Returns:
        str: Status message with information about downloaded images
    """
    # If no target directory specified, use the environment variable
    if not target_directory:
        target_directory = DOWNLOAD_BASE_PATH
    
    if ctx:
        ctx.info(f"Preparing to download {len(image_urls)} images to {target_directory}")
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_directory, exist_ok=True)
    
    successful_downloads = 0
    failed_downloads = 0
    download_details = []
    
    async with aiohttp.ClientSession() as session:
        download_tasks = []
        
        for url in image_urls:
            # Get the filename from the URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # If filename is empty or doesn't have an extension, use a default name
            if not filename or '.' not in filename:
                filename = f"image_{len(download_tasks) + 1}.jpg"
            
            # Create full path for saving the image
            file_path = os.path.join(target_directory, filename)
            
            # Add download task
            download_task = asyncio.create_task(
                download_image(session, url, file_path, download_details, ctx)
            )
            download_tasks.append(download_task)
        
        # Wait for all downloads to complete
        for i, task in enumerate(asyncio.as_completed(download_tasks)):
            await task
            if ctx:
                # Report progress
                ctx.report_progress(i + 1, len(download_tasks))
    
    # Count successful and failed downloads
    for result in download_details:
        if result['success']:
            successful_downloads += 1
        else:
            failed_downloads += 1
    
    # Create status message
    status_message = f"Downloaded {successful_downloads} images to {target_directory}. "
    if failed_downloads > 0:
        status_message += f"Failed to download {failed_downloads} images."
    
    if ctx:
        ctx.info(status_message)
    
    return status_message

async def download_image(session, url, file_path, download_details, ctx=None):
    """Helper function to download an image."""
    try:
        if ctx:
            ctx.info(f"Downloading {url}")
        
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await response.read())
                download_details.append({
                    'url': url,
                    'path': file_path,
                    'success': True
                })
                if ctx:
                    ctx.info(f"Successfully downloaded {url} to {file_path}")
            else:
                error_msg = f"HTTP Error: {response.status}"
                download_details.append({
                    'url': url,
                    'error': error_msg,
                    'success': False
                })
                if ctx:
                    ctx.error(f"Failed to download {url}: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        download_details.append({
            'url': url,
            'error': error_msg,
            'success': False
        })
        if ctx:
            ctx.error(f"Error downloading {url}: {error_msg}")

# The main function is in __init__.py
# This allows the server to be run directly for testing
if __name__ == "__main__":
    # Run the MCP server
    print("Starting MCP server directly (for testing only)")
    mcp.run()