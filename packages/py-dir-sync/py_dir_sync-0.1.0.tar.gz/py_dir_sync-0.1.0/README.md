
# 🚀 Py Dir Sync

    pip install py-dir-sync

Простая библиотека Python для односторонней _живой_ синхронизации каталогов. Отслеживает изменения в исходном каталоге `source` и применяет их к целевому каталогу `destination`, поддерживая структуру директорий.

![](./py_dir_sync_demo.gif)

## Основные возможности

* **Односторонняя синхронизация:** Изменения переносятся из `source` в `destination`.
* **Фильтрация:** Гибкие правила включения и исключения файлов и папок через паттерны `fnmatch`.
* **События:** Предоставляет детальную информацию о том, какие файлы были созданы, изменены, перемещены или удалены через обработчик `ChangeHandler`.
* **Гибкая настройка:**
    *   Автосинхронизация при запуске `auto_sync=True`.
    *   Удаление пустых директорий в `dest` `remove_empty=True`.
    *   Форс-синхронизация при ошибках с контролем количества попыток `force_sync=5` и интервалов `force_sync_interval=1`.
* **Основан на** [`watchdog`](https://github.com/gorakhargosh/watchdog)
* **Требования:** Python **3.12**+.

## Пример использования

Демонстрационный пример [py_dir_sync_run.py](./py_dir_sync_run.py), который можно опробовать на реальных директориях.

```py
from pathlib import Path, PurePath
from typing import AbstractSet
from py_dir_sync import DirSync, SyncPathPair

# Обработчик может ничего не делать,
# но DirSync требует функцию ChangeHandler(Protocol)
def handler(
    created: None | set[Path] = None,
    modified: None | set[Path] = None,
    moved: None | AbstractSet[tuple[PurePath, Path]] = None,
    deleted: None | AbstractSet[PurePath] = None,
    error: None | Exception = None,
) -> None:
    pass

# Пара путей для синхронизации
path_pair = SyncPathPair("C:/src", "C:/dest")

# Паттерны для фильтрации (относительно корня src)
# include применяется только к файлам после проверки exclude.
exclude = [".*", "*/.*"]
include = ["*.py", "*.json", "*.md", "*.txt"]

# Создание экземпляра DirSync
dir_sync = DirSync(
      handler=handler,
      path_pair=path_pair,
      exclude=exclude,
      include=include,
      auto_sync=True,    # синхронизировать при start()
      remove_empty=True, # удалять пустые каталоги
      force_sync=3, # при ошибке синхронизировать весь каталог(3 попытки)
      force_sync_interval=2, # 2 секунды между попытками
  ) 

# Запустите и наблюдайте за изменениями
dir_sync.start()

# Остановка запланирована автоматически, но это можно сделать явно
dir_sync.stop()
```

**Паттерны exclude/include**

* Используется стандартный синтаксис [fnmatch](https://docs.python.org/3/library/fnmatch.html).
* `exclude` проверяется первой, затем `include` применяется только к файлам.
* Путь всегда относительно `source`-каталога.

**auto_sync**

* Синхронизирует каталоги при вызове `DirSync.start()`

**remove_empty**

* По умолчанию наблюдатель нацелен на события файлов, и не всегда может корректно определить, стоит ли удалять пустую директорию.
* Опция `remove_empty=True` заставляет дополнительно проверять родительскую директорию при удалении или перемещении файлов/каталогов.
* Если директория окажется пустой, она будет удалена.

**force_sync/force_sync_interval**

* Любая ошибка при обработке событий может вызвать рассинхронизацию. По умолчанию ошибки создания/удаления/перемещения доступны через параметр `error` обработчика `ChangeHandler(error:Exception)`.
* Для автоматической корректировки состояния укажите:
  + `force_sync > 0` — максимальное количество попыток вызвать синхронизацию.
  + `force_sync_interval = 1` (в секундах, можно float) — интервал между попытками.
