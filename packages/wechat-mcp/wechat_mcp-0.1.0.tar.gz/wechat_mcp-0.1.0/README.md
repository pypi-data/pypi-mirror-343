# init
```bash
git clone https://github.com/DarkNoah/wechat-mcp
uv sync
```

# login wechat(pc)

# start
```bash
# start sse
uv run main.py --wxid "your_wechat_id" --port 8000

# start stdio
uv run main.py --wxid "your_wechat_id" --transport stdio
```
