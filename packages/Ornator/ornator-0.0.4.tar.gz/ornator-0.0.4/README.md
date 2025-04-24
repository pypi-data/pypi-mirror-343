# 🎯 Python Advanced Decorators Library
> A comprehensive collection of flexible and reusable decorators for functions, methods, and classes.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-up%20to%20date-brightgreen.svg)](README.md)

## 📑 Table of Contents
- [Overview](#-overview)
- [Installation](#-installation)
- [Function & Method Decorators](#-function--method-decorators)
- [Class Decorators](#-class-decorators)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Overview

This library provides a robust set of decorators for enhancing Python code functionality. It includes:

- 🔧 Base decorator classes for extensibility
- 📊 Monitoring and logging capabilities
- 🔒 Validation and security features
- 💾 Caching and performance optimization
- 🏭 Support for both functions and classes

## 🚀 Installation

```bash
pip install ornator
```

## 🛠 Function & Method Decorators

### Base Decorators

#### BeforeDecorator
> Executes logic before the function call

```python
from ornator import BeforeDecorator

class LoggingDecorator(BeforeDecorator):
    def __init__(self):
        super().__init__()
        self.pre = self.log_call

    def log_call(self, *args, **kwargs):
        print(f"[LOG] Function call with: {args}, {kwargs}")
        return args

logger = LoggingDecorator().before

@logger()
def process_data(data, pre=None):
    return f"Processing: {data}"
```

#### AfterDecorator
> Modifies the function's return value

```python
from ornator import AfterDecorator

class ResponseTransformer(AfterDecorator):
    def __init__(self):
        super().__init__()
        self.pos = self.transform_response

    def transform_response(self, result, format="json"):
        if format == "json":
            return json.dumps(result)
        return result

transformer = ResponseTransformer().after

@transformer(format="json")
def get_data():
    return {"key": "value"}
```

#### DualDecorator
> Executes logic before and after the function call

```python
from ornator import DualDecorator

class PerformanceMonitor(DualDecorator):
    def __init__(self):
        super().__init__()
        self.pre = self.start_timer
        self.pos = self.end_timer
        self.times = []

    def start_timer(self, *args, **kwargs):
        return time.time()

    def end_timer(self, result, *args, **kwargs):
        execution_time = time.time() - kwargs['pre']
        self.times.append(execution_time)
        return result

monitor = PerformanceMonitor().dual

@monitor()
def expensive_operation(pre):
    time.sleep(1)
    return "Done"
```

#### EmptyDecorator
> Provides complete flexibility for custom logic

```python
from ornator import EmptyDecorator

class Validator(EmptyDecorator):
    def validate(self, func, *args, **kwargs):
        if not args:
            raise ValueError("Arguments required")
        return func(*args, **kwargs)

validator = Validator().empty

@validator(handler=Validator().validate)
def process_data(*args):
    return sum(args)
```

## 🏗 Class Decorators

### Base Class Decorators

#### BeforeClassDecorator
> Executes logic during class instantiation

```python
from ornator import BeforeClassDecorator

class LoggingClassDecorator(BeforeClassDecorator):
    def __init__(self):
        super().__init__()
        self.pre = self.log_instantiation
        self._log = []

    def log_instantiation(self, cls, *args, **kwargs):
        log_entry = {
            "timestamp": datetime.now(),
            "class": cls.__name__,
            "args": args
        }
        self._log.append(log_entry)
        return log_entry

logger = LoggingClassDecorator().before

@logger()
class User:
    def __init__(self, name):
        self.name = name
```

#### AfterClassDecorator
> Modifies the class after its definition

```python
from ornator import AfterClassDecorator

class ValidationDecorator(AfterClassDecorator):
    def __init__(self):
        super().__init__()
        self.pos = self.add_validation

    def add_validation(self, cls):
        original_init = cls.__init__

        def validated_init(instance, *args, **kwargs):
            for key, value in kwargs.items():
                if not isinstance(value, cls.__annotations__.get(key, object)):
                    raise TypeError(f"Invalid type for {key}")
            original_init(instance, *args, **kwargs)

        cls.__init__ = validated_init
        return cls

validator = ValidationDecorator().after

@validator()
class Person:
    name: str
    age: int
```

## 🌟 Examples

### Real-World Use Cases

#### 1. API Rate Limiting
```python
from ornator import BeforeDecorator
import time

class RateLimiter(BeforeDecorator):
    def __init__(self, calls_per_second=1):
        super().__init__()
        self.pre = self.check_rate
        self.calls = []
        self.calls_per_second = calls_per_second

    def check_rate(self, *args, **kwargs):
        now = time.time()
        self.calls = [call for call in self.calls if now - call < 1.0]
        if len(self.calls) >= self.calls_per_second:
            raise Exception("Rate limit exceeded")
        self.calls.append(now)
        return args

limiter = RateLimiter(calls_per_second=2).before

@limiter()
def api_call(pre):
    return "API response"
```

#### 2. Caching with Expiration
```python
from ornator import DualDecorator
from datetime import datetime, timedelta

class CacheWithExpiration(DualDecorator):
    def __init__(self, expiration_minutes=60):
        super().__init__()
        self.pre = self.check_cache
        self.pos = self.update_cache
        self.cache = {}
        self.expiration = expiration_minutes

    def check_cache(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(minutes=self.expiration):
                return value
        return None

    def update_cache(self, result, *args, **kwargs):
        key = str(args) + str(kwargs)
        self.cache[key] = (result, datetime.now())
        return result

cache = CacheWithExpiration(expiration_minutes=30).dual

@cache()
def expensive_computation(pre, x, y):
    if pre is not None:
        return pre
    return x + y
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Advanced Usage

### Creating Custom Decorators

You can easily extend the base decorators to create your own:

```python
class MyCustomDecorator(DualDecorator):
    def __init__(self):
        super().__init__()
        self.pre = self.my_pre_logic
        self.pos = self.my_post_logic

    def my_pre_logic(self, *args, **kwargs):
        # Your custom pre-execution logic
        return modified_args

    def my_post_logic(self, result, *args, **kwargs):
        # Your custom post-execution logic
        return modified_result
```

### Chaining Decorators

Decorators can be chained for combined functionality:

```python
@cache()
@validator()
@logger()
def complex_operation(*args, **kwargs):
    return result
```

## 🔧 Configuration

Each decorator can be configured through its constructor or decorator arguments:

```python
# Configure through constructor
logger = LoggingDecorator(log_level='DEBUG').before

# Configure through decorator
@logger(format='json', timestamp=True)
def my_function():
    pass
```

## 📊 Performance Considerations

- Use `EmptyDecorator` for maximum performance when custom logic is needed
- Consider using `BeforeDecorator` instead of `DualDecorator` when post-processing isn't required
- Cache decorator results when appropriate

## 🚨 Error Handling

All decorators include built-in error handling and will raise appropriate exceptions:

- `TypeError`: When invalid types are provided
- `ValueError`: When required values are missing
- `RuntimeError`: For execution-related errors

## 💡 Best Practices

1. Always extend from the appropriate base decorator
2. Document your custom decorators
3. Use type hints for better code clarity
4. Follow the Single Responsibility Principle
5. Test your decorators thoroughly

## 🔍 Debugging

To debug decorated functions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

class DebugDecorator(BeforeDecorator):
    def __init__(self):
        super().__init__()
        self.pre = self.debug_call

    def debug_call(self, *args, **kwargs):
        logging.debug(f"Function call: args={args}, kwargs={kwargs}")
        return args

debug = DebugDecorator().before
```
