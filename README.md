# API Automation Framework

这是一个基于 Python + pytest + requests 的接口自动化测试项目，当前主要用于对本地运行的后端服务进行 smoke 测试，覆盖用户注册、登录和用户资料更新等接口场景。

## 1. 项目定位

该项目属于接口自动化测试框架，特点如下：

- 使用 pytest 组织和执行测试用例
- 通过 requests 封装接口请求，统一处理 URL、请求方法、响应解析与日志记录
- 使用 YAML 管理测试数据，降低用例与数据耦合
- 使用 MySQL 数据库 fixture 做数据准备与清理
- 提供统一断言封装与日志输出，便于定位失败原因
- 支持生成测试报告，便于后续回归与排查

## 2. 当前项目结构

```text
my_pro/
├── api/                      # 接口请求封装层
├── configs/                  # 配置文件
├── logs/                     # 日志模块
├── stu/                      # 备用或扩展目录
├── test_cases/               # 测试用例目录
├── test_data/                # YAML 测试数据
├── test_report/              # 测试报告输出目录
├── utils/                    # 工具类：断言、数据读取、辅助函数
├── conftest.py               # pytest 全局 fixture
├── runner.py                 # 测试执行入口
└── README.md                 # 项目说明文档
```

## 3. 核心模块说明

### 3.1 接口请求封装

- 文件：api/interface_log.py
- 作用：封装 requests 的 session 请求，统一处理 GET/POST/PUT/DELETE，并记录请求 URL、方法、参数以及响应结果。

### 3.2 配置管理

- 文件：configs/config.py
- 作用：定义测试环境地址、数据库连接信息、日志目录、测试数据目录、测试报告目录等公共配置。

### 3.3 测试数据管理

- 文件：test_data/smoke_test_data.yaml
- 作用：将接口测试参数与用例数据分离，当前包含注册、登录、更新用户资料等测试参数。

### 3.4 测试用例

- 文件：test_cases/test_smoke.py
- 作用：定义 smoke 测试用例，当前覆盖：
  - 用户注册
  - 用户登录
  - 用户资料更新

### 3.5 断言与日志

- 文件：utils/api_assertions.py
- 作用：封装 HTTP 状态码断言、JSON 字段断言等，统一提升用例可读性。

- 文件：logs/mylog.py
- 作用：统一日志输出，便于追踪接口调用和测试执行过程。

### 3.6 pytest fixture

- 文件：conftest.py
- 作用：提供测试前后公共初始化逻辑，例如日志输出、数据库连接 fixture 等。

## 4. 环境准备

运行本项目前，需要准备以下环境：

- Python 3.8+
- pytest
- requests
- pymysql
- PyYAML
- xlrd

可通过以下命令安装依赖：

```bash
pip install pytest requests pymysql pyyaml xlrd
```

同时需要确保以下服务可用：

- 后端接口服务运行在 http://localhost:90
- MySQL 服务可访问，数据库名为 finance
- 默认数据库账号为 root，密码为 root

## 5. 如何执行测试

### 5.1 使用执行入口

```bash
python runner.py
```

当前脚本会调用 pytest 并生成 HTML 报告到 test_report 目录。

### 5.2 直接运行 pytest

```bash
pytest -v -k "test_register or test_login or test_updateUserProfile"
```

如需生成测试报告，可结合 pytest-html 或在当前脚本中使用对应参数。

## 6. 测试报告与日志

- 日志文件输出到 logs/ 目录，按日期生成
- 测试报告输出到 test_report/ 目录
- 失败用例会通过日志和断言信息帮助定位问题

## 7. 适用场景

本项目适用于以下场景：

- 对本地或测试环境接口做快速 smoke 验证
- 对接口请求流程进行自动化回归验证
- 将接口参数与测试用例分离，便于后续维护

## 8. 后续建议

建议后续根据实际业务继续完善：

- 增加更多接口测试场景
- 引入 allure 报告替代或补充现有 HTML 报告
- 将数据库配置抽离为环境变量，避免硬编码
- 增加 README 中的测试环境启动步骤与常见问题说明
