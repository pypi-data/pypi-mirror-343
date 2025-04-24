# Unisound Agent Framework

## 一、项目介绍
Unisound Agent Framework 是一个基于 FastAPI 的智能代理服务框架，用于快速构建和部署 AI 服务。该框架提供了完整的服务生命周期管理、并发控制、大模型连接池管理等功能，使开发者能够专注于业务逻辑的实现。

## 二、依赖 Python3.5+ 版本
本框架要求 Python 3.5 或更高版本。主要依赖包括：
- fastapi>=0.68.0
- uvicorn>=0.15.0
- sqlalchemy>=1.4.0
- aiofiles>=0.8.0
- aioredis>=2.0.0
- pyyaml>=6.0
- python-multipart>=0.0.5
- aiomysql>=0.1.1
- aiohttp>=3.8.0
- loguru>=0.6.0
- starlette>=0.21.0

## 三、开发框架使用流程
1. 开发环境安装框架流程
   - 1.2 安装框架依赖
      pip install -r requirements.txt

   - 1.3. 安装框架包（开发环境）
      pip install --no-index --find-links=D:\pythonworkspace\unisound-agent-frame\dist unisound-agent-frame==0.1.3

2. 正式环境框架安装
   pip install unisound-agent-frame==version

3. 初始化服务配置
   - 执行 `unisound-agent-frame-init` 命令，该命令会自动：
     - 创建 config 目录并创建配置文件模板
     - 创建 scripts 目录并创建启动脚本
   - 注意：如果不执行此命令，需要手动创建 config 目录及所有配置文件和 service.py

4. 配置服务
   - 修改配置文件模板（.yml 文件）
   - 根据实际需求调整配置参数
   - 详细配置说明请参考 6.1 配置文件说明

5. 开发业务逻辑
   - 继承 Agent 类，实现具体的工作流程
   - 实现 init() 和 run() 方法

6. 集成大模型（可选）
   - 如需调用大模型，可使用框架提供的大模型连接池
   - 具体使用方法请参考 6.3 大模型连接池（LLMPool）
   
7. 启动服务的方式
   - 开发工具中启动，直接运行service.py
   - docker/k8s方式，使用scripts/Dockerfile
   - 命令启动，cd到scripts目录下运行startup.sh|startup.bat|startup.command
8. 服务关闭方式
   - 命令关闭，cd到scripts目录下运行shutdown.sh|shutdown.bat|shutdown.command

   

## 四、接口功能介绍
1. `/analyze` - POST 接口
   - 功能：处理分析请求
   - 参数：AnalyzeRequest 对象（注意：agent_id 参数必须与 frame_${env}.yml 中 agent_mapping 的 key 保持一致）
   - 返回：AnalyzeResponse 对象

2. `/get_result` - POST 接口
   - 功能：获取分析结果
   - 参数：AnalyzeRequest 对象
   - 返回：AnalyzeResponse 对象

3. `/health` - POST 接口
   - 功能：健康检查
   - 参数：HealthCheckRequest 对象（可选）
   - 返回：HealthCheckResponse 对象

4. `/metrics` - POST 接口
   - 功能：获取服务指标
   - 参数：MetricsRequest 对象（可选）
   - 返回：MetricsResponse 对象

5. `/set_model_max_concurrent` - POST 接口
   - 功能：设置模型最大并发数
   - 参数：model_type（字符串）, max_concurrent（整数）

6. `/reset_agent_concurrency` - POST 接口
   - 功能：重置 agent 当前并发数
   - 参数：current_concurrent（整数）

## 五、项目结构介绍
```
unisound-agent-frame/
├── .gitignore
├── LICENSE
├── README.md
├── agent/                     # Agent 相关实现
│   ├── agent.py              # Agent 基类定义
│   └── agent_registry.py     # Agent 注册和管理机制
├── base/                     # 框架核心组件
│   └── framework.py          # 框架主类实现
├── concurrency/             # 并发控制模块
│   ├── agent_concurrency.py
│   └── distributed_concurrency.py
├── demo/                   # 示例代码
│   └── agent/
│       └── DemoAgent.py
├── domain/                 # 数据模型定义
│   ├── models.py          # 数据模型
│   ├── request_model.py   # 请求对象模型
│   └── response_model.py  # 响应对象模型
├── exception/             # 异常处理模块
│   └── business_exception.py #异常处理类
├── llm/                  # 大模型集成模块
│   ├── gpt4_llm_connection.py
│   ├── llm_connection.py
│   ├── llm_connection_factory.py
│   ├── llm_pool.py
│   └── unigpt_llm_connection.py
├── requirements.txt      # 项目依赖清单
├── scripts/             # 启动和部署脚本
│   ├── .dockerignore   
│   ├── Dockerfile         #docker打包脚本
│   ├── shutdown.bat       #window:命令行关闭服务脚本
│   ├── shutdown.command   #macos:命令行关闭服务脚本
│   ├── shutdown.sh        #linux:命令行关闭服务脚本
│   ├── startup.bat        #window:命令行启动服务脚本
│   ├── startup.command    #macos:命令行启动服务脚本
│   ├── startup.sh         #linux:命令行启动服务脚本
│   └── supervisord.conf   #进程监控脚本
├── service.py           # 服务入口文件
├── template/           # 配置文件模板
│   ├── demo_agent.template      #工作流配置文件模版
│   ├── frame_dev.template       #开发环境框架配置文件模版
│   ├── frame_uat.template       #uat环境框架配置文件模版
│   ├── frame_prod.template       #prod环境框架配置文件模版
│   └── settings.template        #框架基本配置文件模版
├── test/               # 测试目录
├── util/              # 工具类
│   ├── config_reader.py         #读取yml配置文件工具类
│   ├── data_logger.py           #大模型调用日志工具类
│   ├── logger.py                #服务日志工具类
│   └── mysql_util.py            #mysql日志工具类
```

## 六、框架介绍

### 6.1 配置文件说明
在使用框架的服务中创建 config 目录，存放三种配置文件，如下是配置文件样例：
1. `settings.yml` - 设置框架使用的环境（dev/uat/prod）
```code
service_name: "Unisound Agent Framework"
service_description: "Unisound Agent Framework"
service_version: "1.0.0"

service_env: "dev"
```
2. `frame_${env}.yml` - 框架配置文件
```code

#设置服务名称
service_id: "base_frame_work"

agent_max_concurrent: 1000

# MySQL配置
mysql:
  host: "localhost"
  port: 3306
  user: "root"
  password: "root"
  database: "test1"
agent_log:
  file_path: "D:\audio\test\"#/app/logs/
# Redis配置
redis:
  host: "localhost"
  port: 6379
  password: "root"
  db: 0

# 记录接口数据配置
data_logger:
  storage_type: "mysql"  # file 或 mysql
  log_path: "logs"


#设置使用哪个大模型,与大模型配置的名字要一致
llm_model:  "UniGpt"
# 大模型配置
models:
  UniGpt:
    max_concurrent: 10
    model_name: "model_name"
    api_url: "http://unigpt-api.hivoice.cn/rest/v1/chat/completions"
    api_key: "api_key"
    api_secret: "secret"
    api_vendor: "api_vendor"
    temperature: 0.6        # 新增默认配置
    max_new_tokens: 10240   # 新增默认配置
  Claude:
    max_concurrent: 100
    api_url: "https://api.anthropic.com/v1"
    api_key: "your_claude_api_key"
    api_secret: "your_claude_api_secret"
  GPT4:
    max_concurrent: 50
    api_url: "https://api.openai.com/v1"
    api_key: "your_openai_api_key"

# LLM连接池配置
llm_pool:
  max_size: 2
  min_size: 1
  connection_timeout: 30

# Agent配置
agent_mapping:
  demo_agent: "demo.agent.DemoAgent.DemoAgent"

# 服务配置
server:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  reload: false 
```
3. `${工作流agent名称}.yml` - Agent 配置文件
   - ${工作流agent名称}与frame_${env}.yml 文件 agent_mapping下的key一致

#### 6.1.1 配置说明
框架配置文件（frame_${env}.yml）包含以下主要配置：
- MySQL 配置
- agent_mapping 配置具体的agent的名称和实现类地址，框架自动根据这个加载
- models下配置具体的大模型
- agent_log.file_path服务日志的保存路径
- agent_max_concurrent 设置agent服务的最大并发
- service_id 配置服务id
- data_logger保存大模型接口调用的数据配置
- llm_model配置具体使用哪个大模型，值对应models的大模型，如果不配置默认使用models中第一个大模型
- llm_pool 大模型连接池的设置，llm_pool.connection_timeout 可以配置为-1，默认不超时


### 6.2 agent工作流实现(继承 Agent 类)
创建自定义 Agent 需要继承 `Agent` 基类并实现以下方法：
```python
class CustomAgent(Agent):
    async def init(self, agent_config: str):
        # 初始化逻辑
        pass

    async def run(self, request: AnalyzeRequest, save_result_func: SaveResultFunc):
        # 运行逻辑
        pass
```

### 6.3 大模型连接池（LLMPool）
Agent 算法实现类中可以直接使用 LLMPool 获取连接调用大模型接口：

#### 6.3.1 获取连接
```python
connection = await llm_pool.get_connection()
```

#### 6.3.2 调用聊天接口
```python
result = await connection.chat(messages=messages, task_id=task_id)
```

#### 6.3.3 释放连接
```python
await llm_pool.release_connection(connection)
```

#### 6.3.4 保存最终结果
```python
await save_result_func(result, status, message)
```
