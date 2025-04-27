# CSToolbox (ChatSpeed Toolbox)

简体中文 | [English](README.MD)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CSToolbox 是 [ChatSpeed](https://github.com/aidyou/chatspeed) 的扩展工具集，通过 MCP 协议提供网络搜索、网页内容爬取和图表生成等功能。

## 协议

本项目采用 [MIT 协议](LICENSE) 开源，您可以自由使用、修改和分发本软件。

## 功能特性

- 🔍 **网络搜索** - 支持多种搜索引擎（Google、Bing、百度等）
- 🕷️ **网页爬取** - 从网页提取结构化内容（支持 Markdown/HTML 格式）
- 📊 **图表生成** - 快速生成各类数据可视化图表，支持曲线图、柱状图和饼图
- 📄 **PDF处理** - 从PDF URL 下载文档并提取文本内容

## 如何使用

### mcp 客户端配置

``` json
{
  "mcpServers": {
    "cstoolbox": {
      "command": "uvx",
      "args": [
        "cstoolbox"
      ],
      "env": {
        "CS_LOG_LEVEL": "DEBUG",
        "CS_LOG_DIR": "logs",
        "CS_PROXY": "http://localhost:15154",
        "CS_BROWSER_TZ": "Asia/Shanghai",
        "CS_BROWSER_LANG": "zh-CN",
        "CS_BROWSER_POOL_MIN_SIZE": "2",
        "CS_BROWSER_POOL_MAX_SIZE": "10",
        "CS_REGION": "com",
        "CS_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
        "CS_HEADLESS": "true",
        "CS_SCREENSHOT": "false",
        "CS_USER_AGENT_MODE": "random",
        "CS_USER_DATA_DIR": None
      }
    }
  }
}
```

#### 环境变量说明

- `CS_LOG_LEVEL`：日志级别，可选值为 `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL`，默认为 `INFO`
- `CS_LOG_DIR`：日志目录，默认为 `logs`
- `CS_PROXY`：代理服务器地址，有些地区无法访问 `google.com` 或者 `bing.com` 搜索引擎，因此需要设置代理，另外，有些网站对用户所在地区有限制，如果没有代理也是访问不了的
- `CS_BROWSER_TZ`：时区，默认为 `Etc/UTC`
- `CS_BROWSER_LANG`：浏览器语言，默认为 `en-US`
- `CS_BROWSER_POOL_MIN_SIZE`：浏览器对象池最小大小，默认为 `2`。当 MCP 服务启动时默认创建的浏览器对象最小数量，浏览器对象池可以用来提高数据爬取的效率
- `CS_BROWSER_POOL_MAX_SIZE`：浏览器对象池最大大小，默认为 `10`
- `CS_REGION`：搜索引擎区域，可选值为 `com`、`cn`、`us`、`uk`等，默认为 `com`
- `CS_USER_AGENT`：用户代理，默认为 `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36`
- `CS_HEADLESS`：是否启用无头模式，默认为 `true`
- `CS_SCREENSHOT`：是否启用截图功能，默认为 `false`,启用截屏后，每次抓取数据都会将当前页面的界面截图保存到日志目录下
- `CS_USER_AGENT_MODE`：用户代理模式，可选值为 `random`、None，默认为 None。当设置为 `random` 时，每次请求都会随机选择一个用户代理，否则会使用 `CS_USER_AGENT` 配置的用户代理
- `CS_USER_DATA_DIR`：用户数据目录，默认为 `None`

#### ⚠️注意事项

- 部分地区使用 `google` 或者 `bing` 进行网络搜索时需确保代理设置正确

### python 调用示例

更多 python 调用示例请参考`tests/mcp_client.py`文件

```python
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

project_root = Path(__file__).resolve().parent.parent

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",
    args=[f"{project_root}/src/cstoolbox/main.py"],  # Path to cstoolbox mcp main.py
    env={
        "CS_PROXY": "http://localhost:15154",
        "CS_BROWSER_TZ": "Asia/Shanghai",
        "CS_BROWSER_LANG": "zh-CN"
    },
)


# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # Call a web search tool
            result = await session.call_tool(
                "web_search",
                arguments={"provider": "bing", "kw": "deepseek r2", "number": 10, "page": 1, "time_period": "month"},
            )
            print(result)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())

```

## 开发

1. 克隆源代码仓库:

```bash
git clone https://github.com/aidyou/cstoolbox.git
cd cstoolbox
```

2. 安装 uv
**Macos/Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**使用`irm`下载并安装

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. 创建并激活venv环境:

```bash
uv venv --python=python3.12
source .venv/bin/activate
```

4. 安装依赖:

```bash
uv pip install .
```

5. 启动测试:

```bash
mcp dev src/cstoolbox/main.py
```

现在你可以通过`http://127.0.0.1:6274/#tools` 进行功能测试

6. http 接口测试
在`.vscode/launch.json`文件中添加以下配置

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "http dev",
            "type": "debugpy",
            "request": "launch",
            "module": "cstoolbox.http_api",
            "args": [
            ],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src",
                "CS_TZ": "Asia/Shanghai",
                "CS_BROWSER_LANG": "zh-CN",
                "CS_LOG_LEVEL": "DEBUG",
                "CS_SCREENSHOT": "true",
                "CS_PROXY": "http://localhost:15154"
            },
            "python": "${workspaceFolder}/.venv/bin/python"
        }
    ]
}
```

`env`配置中`CS_*`请根据实际情况进行调整，在 vscode 中启动调试后即可通过如下接口进行测试：

- 搜索： `curl http://localhost:12321/chp/web_search?provider=google&kw=deepseek+r2&number=10&page=1`
- 内容抓取：`curl http://localhost:12321/chp/web_crawler?url=https://medium.com/@lbq999/deepseek-r2-is-around-the-corner-c449a41bfec6`
