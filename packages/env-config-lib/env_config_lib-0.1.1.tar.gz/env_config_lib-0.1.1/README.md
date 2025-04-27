# env-config-lib

Удобная работа с переменными окружения через валидацию по схеме.

## Установка

1. python -m venv .venv
2. Активация вертуального окружения 
3. pip install env_config_lib

---

## Пример использования

```python
from env_config_lib import EnvConfig

env = EnvConfig(schema={"TEST": str})
print(env.get("TEST"))

```

