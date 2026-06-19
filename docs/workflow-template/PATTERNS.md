# 通用架构模式

本文档记录从实际业务项目中提炼、可跨项目复用的架构模式。

---

## 模式 1：三模式适配器架构（Mock / 免费 / 付费）

### 适用场景

项目依赖外部 AI 模型服务，且满足以下条件：
- 开发和测试阶段需要免费/无网络依赖的 Mock
- 生产环境需要真实模型效果，但可选免费和付费两档

### 架构图

```
环境变量 TRYON_MODEL_MODE（或 {BIZ_PREFIX}_MODEL_MODE）
        │
        ▼
┌──────────────────────┐
│  create_adapter()    │  工厂函数
│  按 mode 分发         │
└──────┬───────┬───────┘
       │       │       │
  mock │   hf  │  real │
       ▼       ▼       ▼
┌──────┐ ┌──────┐ ┌──────┐
│Mock  │ │Free  │ │Paid  │
│Model │ │Model │ │Model │
└──────┘ └──────┘ └──────┘
 返回固定   调用免费    调用付费
 模拟结果   API/Space   API
```

### 模式定义

| 模式 | 值 | 实现类 | 外部依赖 | 费用 |
|------|-----|--------|----------|------|
| Mock | `mock`（默认） | `MockModel` | 无 | 免费 |
| Free | 自定义（如 `hf`） | `FreeModel` | 免费 API | 免费 |
| Paid | 自定义（如 `real`） | `PaidModel` | 付费 API | 按量付费 |

### 配置规范

```python
# config.py
MODEL_MODE = os.getenv(f"{BIZ_PREFIX}_MODEL_MODE", "mock")

# Mock 模式：无需额外配置
# Free 模式
FREE_ENDPOINT = os.getenv(f"{BIZ_PREFIX}_FREE_ENDPOINT", "")
FREE_TOKEN = os.getenv(f"{BIZ_PREFIX}_FREE_TOKEN", "")
# Paid 模式
PAID_API_TOKEN = os.getenv(f"{BIZ_PREFIX}_API_TOKEN", "")
PAID_MODEL = os.getenv(f"{BIZ_PREFIX}_MODEL", "")

# 降级开关
REAL_MODEL_FALLBACK_MOCK = os.getenv("REAL_MODEL_FALLBACK_MOCK", "true").lower() == "true"
```

### 工厂函数

```python
# model_adapter.py
from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def generate(self, *args, **kwargs) -> Result:
        ...

class MockModel(IModel):
    def generate(self, *args, **kwargs) -> Result:
        return Result(mock_url="...", source="mock")

class FreeModel(IModel):
    def generate(self, *args, **kwargs) -> Result:
        # 调用免费 API
        ...

class PaidModel(IModel):
    def generate(self, *args, **kwargs) -> Result:
        # 调用付费 API
        ...

def create_adapter() -> IModel:
    mode = config.MODEL_MODE
    if mode == "mock":
        return MockModel()
    elif mode == "<free_mode>":
        return FreeModel()
    elif mode == "<paid_mode>":
        return PaidModel()
    raise ValueError(f"Unknown mode: {mode}")
```

### 降级策略

免费/付费模式调用失败时，若 `REAL_MODEL_FALLBACK_MOCK=true`，自动降级为 Mock 结果：

```python
def generate(self, ...):
    try:
        return self._call_real_api(...)
    except Exception as e:
        if config.REAL_MODEL_FALLBACK_MOCK:
            mock = MockModel()
            result = mock.generate(...)
            result.fallback_used = True
            result.source = "mock_fallback"
            result.warning = f"真实模型调用失败，已降级为 Mock: {e}"
            return result
        raise
```

### 异常分类

免费/付费模式的异常必须分类，便于用户排查：

```python
except Exception as e:
    msg = str(e).lower()
    if "no space is running" in msg:
        raise ModelError("服务当前未运行，请等待启动...")
    elif "quota" in msg or "rate limit" in msg:
        raise ModelError("API 配额已用尽，请稍后重试...")
    elif "timeout" in msg:
        raise ModelError("请求超时，请重试...")
    elif "queue" in msg and "full" in msg:
        raise ModelError("排队已满，请稍后重试...")
    raise ModelError(f"模型调用失败: {e}")
```

### 启动校验

启动时按模式校验必要配置：

```python
# model_config_validator.py
def validate():
    mode = config.MODEL_MODE
    if mode == "mock":
        return  # 无需校验
    elif mode == "<free_mode>":
        if not config.FREE_ENDPOINT:
            raise ConfigError("FREE_ENDPOINT 未配置")
    elif mode == "<paid_mode>":
        if not config.PAID_API_TOKEN:
            raise ConfigError("PAID_API_TOKEN 未配置")
```

### 健康检查

各模式独立探测：

```python
# health_service.py
def check() -> HealthResult:
    mode = config.MODEL_MODE
    if mode == "mock":
        return HealthResult(status="healthy")
    elif mode == "<free_mode>":
        return _check_free_endpoint()
    elif mode == "<paid_mode>":
        return _check_paid_endpoint()
```

### 测试策略

| 测试类型 | Mock | Free | Paid |
|----------|------|------|------|
| 工厂分发 | ✅ mock 环境变量 | ✅ mock 环境变量 | ✅ mock 环境变量 |
| 成功路径 | ✅ 直接断言 | ✅ mock 外部客户端 | ✅ mock 外部客户端 |
| 错误分类 | N/A | ✅ mock 不同异常 | ✅ mock 不同异常 |
| 降级逻辑 | N/A | ✅ mock 异常+验证降级 | ✅ mock 异常+验证降级 |
| 配置校验 | N/A | ✅ mock 缺失配置 | ✅ mock 缺失配置 |
