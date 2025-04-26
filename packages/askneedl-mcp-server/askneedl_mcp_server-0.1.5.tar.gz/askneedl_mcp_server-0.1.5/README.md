# 🚀 AskNeedl MCP Server Setup

## For Claude Desktop
### Install `askneedl-mcp-server`:

```bash
pip install askneedl-mcp-server
```
**Note**: Possibly install in the base python environment, as the `claude` executable might not be able to access the `askneedl-mcp-server` package if installed in a different environment or conda environments.

### Configure claude desktop:

Add the below code to the respective  `claude_desktop_config.json` file: (example `.config/Claude/claude_desktop_config.json` for linux):
```json
{
    "mcpServers": {
		"askneedl-mcp-server": {
			"command": <YOUR-PYTHON-EXECUTABLE-PATH>,
			"args": [
			"-m",
			"askneedl_mcp_server"
			],
			"shell": true,
			"env": {
				"NEEDL_API_KEY": <YOUR-NEEDL-API-KEY>,
				"USER_UUID": <YOUR-PUBLIC-UUID>,
				"env": "prod"
			}
		}
	}
}
```

## For local development and debugging:
### Run the server:
```bash
python -m askneedl_mcp_server
```

### Install `uv`:
- Refer this - https://docs.astral.sh/uv/getting-started/installation/

For macOS and Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

(If you are facing installation errors, please refer the the uv installation guide(referenced above) for troubleshooting)