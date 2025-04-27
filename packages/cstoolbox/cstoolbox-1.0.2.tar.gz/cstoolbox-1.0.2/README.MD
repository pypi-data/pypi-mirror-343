# ChatSpeed Toolbox (CSToolbox)

[简体中文](README-Zh.MD) | English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CSToolbox is an extension toolkit for [ChatSpeed](https://github.com/aidyou/chatspeed), providing web search, web content crawling, and chart generation capabilities via MCP protocol.

## License

This project is open-sourced under the [MIT License](LICENSE). You are free to use, modify, and distribute this software.

## Features

- 🔍 **Web Search** - Supports multiple search engines (Google, Bing, Baidu, etc.)
- 🕷️ **Web Crawling** - Extracts structured content from web pages (supports Markdown/HTML formats)
- 📊 **Chart Generation** - Quickly generates various data visualization charts including line charts, bar charts and pie charts
- 📄 **PDF Processing** - Downloads and extracts text content from PDF documents

## Usage

### MCP Client Configuration

```json
{
  "mcpServers": {
    "cstoolbox": {
      "command": "uvx",
      "args": ["cstoolbox"],
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
        "CS_USER_DATA_DIR": null
      }
    }
  }
}
```

#### Environment Variables

- `CS_LOG_LEVEL`: Log level, options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (default: `INFO`)
- `CS_LOG_DIR`: Log directory (default: `logs`)
- `CS_PROXY`: Proxy server address (required for accessing Google/Bing in some regions)
- `CS_BROWSER_TZ`: Timezone (default: `Etc/UTC`)
- `CS_BROWSER_LANG`: Browser language (default: `en-US`)
- `CS_BROWSER_POOL_MIN_SIZE`: Minimum browser pool size (default: `2`)
- `CS_BROWSER_POOL_MAX_SIZE`: Maximum browser pool size (default: `10`)
- `CS_REGION`: Search engine region (options: `com`, `cn`, `us`, `uk`, etc., default: `com`)
- `CS_USER_AGENT`: User agent string
- `CS_HEADLESS`: Headless mode (default: `true`)
- `CS_SCREENSHOT`: Enable screenshots (default: `false`)
- `CS_USER_AGENT_MODE`: User agent mode (`random` or None, default: None)
- `CS_USER_DATA_DIR`: Browser user data directory

#### ⚠️ Important Notes

- Ensure proper proxy settings when using Google/Bing search in restricted regions

### Python Example

Refer to `tests/mcp_client.py` for more examples

```python
from pathlib import Path
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

project_root = Path(__file__).resolve().parent.parent

server_params = StdioServerParameters(
    command="python",
    args=[f"{project_root}/src/cstoolbox/main.py"],
    env={
        "CS_PROXY": "http://localhost:15154",
        "CS_BROWSER_TZ": "Asia/Shanghai",
        "CS_BROWSER_LANG": "zh-CN"
    },
)

async def handle_sampling_message(message: types.CreateMessageRequestParams):
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(type="text", text="Hello, world! from model"),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool(
                "web_search",
                arguments={"provider": "bing", "kw": "deepseek r2", "number": 10, "page": 1, "time_period": "month"},
            )
            print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
```

## Development

1. Clone repository:

```bash
git clone https://github.com/aidyou/cstoolbox.git
cd cstoolbox
```

2. Install uv:
**MacOS/Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Create and activate venv:

```bash
uv venv --python=python3.12
source .venv/bin/activate
```

4. Install dependencies:

```bash
uv pip install .
```

5. Start development server:

```bash
mcp dev src/cstoolbox/main.py
```

Now you can test the features at `http://127.0.0.1:6274/#tools`
