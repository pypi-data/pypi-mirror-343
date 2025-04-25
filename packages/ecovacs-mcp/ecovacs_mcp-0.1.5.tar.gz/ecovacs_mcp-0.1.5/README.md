# 扫地机器人控制API

本项目提供了一套用于控制扫地机器人的API接口，基于MCP协议。
依赖MCP Python SDK和MCP Typescript SDK开发，任意支持MCP协议的智能体助手（如Claude、Cursor以及千帆AppBuilder等）都可以快速接入。

# 开始

## 安装

### github本地安装
```bash
git clone git@github.com:ecovacs-ai/ecovacs-mcp.git

uv add "mcp[cli]" mcp requests

uv run ecovacs_mcp/robot_mcp_stdio.py
```

### pipy
```bash
pip install robot-mcp-stdio

python3 -m robot-mcp-stdio
```

## 工具接口说明

### 设备列表查询

获取用户绑定的所有机器人列表。

#### Input:
无参数

#### Returns:
```json
{
  "status": 0,
  "message": "success",
  "data": [
    {
      "nickname": "机器人昵称",
    }
  ]
}
```

### 启动清扫

控制扫地机器人开始、暂停、恢复或停止清扫。

#### Input:
- `nickname`: 机器人的昵称，用于查找设备，支持模糊匹配
- `act`: 清扫行为
  - `s`: 开始清扫
  - `r`: 恢复清扫
  - `p`: 暂停清扫
  - `h`: 停止清扫

#### Returns:
```json
{
  "msg": "OK",
  "code": 0,
  "data": []
}
```

### 控制回充

控制机器人开始或停止回充。

#### Input:
- `nickname`: 机器人昵称，用于查找设备
- `act`: 机器行为
  - `go-start`: 开始回充
  - `stopGo`: 结束回充

#### Returns:
```json
{
  "msg": "OK",
  "code": 0,
  "data": []
}
```

### 查询工作状态

查询机器人当前的工作状态。

#### Input:
- `nickname`: 机器人昵称，用于查找设备

#### Returns:
```json
{
  "msg": "OK",
  "code": 0,
  "data": {
    "status": "cleaning",
    "battery": 80,
    "cleanTime": 30
  }
}
```

## 环境变量

- `ECO_API_KEY`: API访问密钥，用于验证接口调用权限

## 使用示例

```python
# 使用stdio方式调用接口
import subprocess
import json

# 获取设备列表
proc = subprocess.Popen(['robot-mcp-stdio'], 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE)
                        
request = {
    "name": "get_device_list",
    "parameters": {
        "random_string": "dummy"
    }
}

proc.stdin.write((json.dumps(request) + '\n').encode())
proc.stdin.flush()
response = json.loads(proc.stdout.readline())
print(response)

# 启动清扫
request = {
    "name": "set_cleaning",
    "parameters": {
        "nickname": "客厅扫地机",
        "act": "s"
    }
}

proc.stdin.write((json.dumps(request) + '\n').encode())
proc.stdin.flush()
response = json.loads(proc.stdout.readline())
print(response)
```

## 许可证

MIT 

