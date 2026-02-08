# Xiaomi Robot Vacuum T12 (b106bk) Home Assistant Setup / Настройка в Home Assistant

**Model / Модель:** Xiaomi Robot Vacuum T12
**Technical ID / Технический ID:** `xiaomi.vacuum.b106bk`
**Firmware / Прошивка:** 4.3.3_0010
**Last Updated / Дата обновления:** 2026-02-08

---

## 🇬🇧 English Documentation

### 🛠 Prerequisites (Required Plugins)
To control this vacuum in Home Assistant, you need the following:

1.  **HACS (Home Assistant Community Store)**
    *   Required to install custom integrations.
    *   [Installation Guide](https://hacs.xyz/docs/setup/download)
2.  **Xiaomi Miot Auto**
    *   The main integration used to communicate with the vacuum via the MIoT protocol.
    *   **Install via HACS:** Search for "Xiaomi Miot Auto".
    *   **GitHub:** [al-one/hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot)
    *   **Setup:** Add integration -> Select "Xiaomi Miot Auto" -> Log in with your Xiaomi Account -> Select device.

### ⚠️ The Problem
This specific model **does not support**:
1. Standard `vacuum.send_command` (`app_segment_clean`).
2. Standard MIoT properties for retrieving the room list (returns empty).
3. Standard room cleaning services (SIID 2 or 4).

### ✅ The Solution
To clean specific rooms, you must use **Service 7 (Sweep)** and **Action 3 (set-room-clean)**.

#### 1. Command Format
Use the `xiaomi_miot.call_action` service:

```yaml
service: xiaomi_miot.call_action
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 7
  aiid: 3
  params: ["ROOM_ID", 0, 1]
```

**Parameters:**
* `"ROOM_ID"`: String containing the ID (must be quoted, e.g., "10").
* `0`: Cleaning Mode (0 = Global/Normal, 1 = Edge).
* `1`: Operation (0 = Stop, 1 = Start).

#### 2. How to find Room IDs
Since the room list cannot be retrieved programmatically, use one of these methods:

**Method A: Modified App (Recommended)**
Use the **MiHome by VEVS** app to get the logs.
- **Why:** Safest and most accurate way to see exact IDs.
- **How:** Enable logging in VEVS app, open map, connect phone via MTP, check `/vevs/logs/rpctalk/`. Look for response to `get-preference-ii`.

**Method B: Trial & Error (No 3rd party apps)**
- **Why:** Easiest method if you don't want to install modified APKs.
- **How:**
  1. For this model, Room IDs almost always start at **10** and go up (10, 11, 12...).
  2. Create a test script in Home Assistant with `params: ["10", 0, 1]`.
  3. Run it. If the vacuum goes to the Kitchen -> ID 10 is Kitchen.
  4. Repeat for 11, 12, 13, etc. until all rooms are mapped.

**Method C: Traffic Interception (Advanced)**
- **Why:** If you want to use the official app but are technically proficient.
- **Note:** **We have not tested this method.** There may be difficulties configuring Android devices (SSL pinning, certificate installation).
- **How:** Use tools like Charles Proxy or mitmproxy to intercept the `set-room-clean` JSON request from the official Mi Home app.

### 3. Room Mapping (For this device)

| ID | Name | Status |
|----|------|--------|
| **10** | 🧸 Nursery | Confirmed |
| **11** | 🍳 Kitchen | Confirmed |
| **12** | 🛏️ Bedroom | Confirmed |
| **13** | 🚶 Corridor | Confirmed |

## 🚀 Автоматическая настройка (Recommended)

Для быстрой настройки используйте скрипт `setup_vacuum.py`. Он проверит вашу интеграцию и создаст готовый `scripts.yaml`.

```mermaid
sequence_target
    participant User
    participant Script as setup_vacuum.py
    participant HA as Home Assistant
    participant Vacuum

    User->>Script: Run with .env
    Script->>HA: check_ha() (Auth & Plugins)
    HA-->>Script: Status 200 + components
    Script->>HA: check_device() (Status & Model)
    HA-->>Script: Entity State
    Script->>HA: scan_rooms() (MIoT Action 7,10)
    HA-->>Script: Room ID list
    Script->>HA: test_run() (Start/Stop Test)
    HA->>Vacuum: Move & Halt
    Script->>User: Generate scripts_generated.yaml
```

### Алгоритм работы `setup_vacuum.py`:
1.  **Auth Validation**: Проверка токена и доступности API Home Assistant.
2.  **Plugin Check**: Поиск установленного компонента `xiaomi_miot` в реестре HA.
3.  **Device Discovery**: Получение атрибутов `entity_id` для подтверждения модели `b106bk`.
4.  **MIoT Scanning**: Вызов скрытой функции `get-preference-ii` для получения списка идентификаторов комнат из памяти пылесоса.
5.  **Operational Test**: Кратковременный запуск уборки для подтверждения, что команды доходят до исполнительного механизма.
6.  **Config Generation**: Сборка YAML-файла со скриптами, готовыми к вставке в `configuration.yaml`.

---

## 🛠 Применение и Обслуживание

### Как использовать сгенерированные скрипты:
1. Скрипты автоматически добавляются в `scripts.yaml` вашего Home Assistant.
2. После выполнения скрипта `setup_vacuum.py`, выполните "Перезагрузку скриптов" в HA (Настройки -> Инструменты разработчика -> YAML -> Скрипты).
3. Теперь вы можете вызывать их из интерфейса, автоматизаций или через API.

### Интеграция с Алисой:
1. Откройте приложение **"Дом с Алисой"**.
2. Обновите список устройств.
3. Новые скрипты появятся как "Сценарии" или "Команды".
4. Создайте голосовую команду (например, "Алиса, пропылесось в детской"), привязав её к соответствующему скрипту `vacuum_clean_room_10`.

---

## 📋 Фиксация рабочих методов (Proven Only)

В ходе верификации 2026-02-08 были оставлены только гарантированно рабочие команды:
- **Уборка комнаты**: `siid: 7, aiid: 3, params: ["ID", 0, 1]`
- **Остановка**: `siid: 2, aiid: 2`
- **Настройка**: `xiaomi_miot.set_miot_property` (siid 7, piid 5/6)


---

## 🇷🇺 Русская документация

### 🛠 Необходимые компоненты (Плагины)
Для управления этим пылесосом в Home Assistant вам понадобятся:

1.  **HACS (Home Assistant Community Store)**
    *   Необходим для установки пользовательских интеграций.
    *   [Инструкция по установке](https://hacs.xyz/docs/setup/download)
2.  **Xiaomi Miot Auto**
    *   Основная интеграция для взаимодействия с пылесосом по протоколу MIoT.
    *   **Установка через HACS:** Найдите в поиске "Xiaomi Miot Auto".
    *   **GitHub:** [al-one/hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot)
    *   **Настройка:** Добавить интеграцию -> Выбрать "Xiaomi Miot Auto" -> Войти через Xiaomi аккаунт -> Выбрать устройство.

### ⚠️ Проблема
Эта модель **не поддерживает**:
1. Стандартные команды `vacuum.send_command` (`app_segment_clean`).
2. Стандартные свойства MIoT для получения списка комнат (возвращает пустоту).
3. Стандартный сервис очистки комнат (SIID 2 или 4).

### ✅ Решение
Для запуска уборки по комнатам необходимо использовать **Service 7 (Sweep)** и **Action 3 (set-room-clean)**.

#### 1. Формат команды
Используйте сервис `xiaomi_miot.call_action`:

```yaml
service: xiaomi_miot.call_action
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 7
  aiid: 3
  params: ["ID_КОМНАТЫ", 0, 1]
```

**Расшифровка параметров:**
* `"ID_КОМНАТЫ"`: Строка с ID (обязательно в кавычках, например, "10").
* `0`: Режим уборки (0 = Обычный/Global, 1 = Вдоль стен/Edge).
* `1`: Операция (0 = Стоп, 1 = Старт).

#### 2. Как найти ID комнат
Так как программно получить список не удается, используйте один из методов:

**Метод А: Модифицированное приложение (Рекомендуемый)**
Используйте приложение **MiHome от VEVS**.
- **Зачем:** Самый точный способ увидеть логи пылесоса.
- **Как:** Включить логирование в VEVS, открыть карту, подключить телефон по MTP. Логи в `/vevs/logs/rpctalk/`. Искать ответ на `get-preference-ii`.

**Метод Б: Метод перебора (Без сторонних приложений)**
- **Зачем:** Если вы не хотите устанавливать модифицированные APK.
- **Как:**
  1. У этой серии пылесосов ID комнат обычно начинаются с **10** и идут по порядку (10, 11, 12...).
  2. Создайте в HA скрипт с параметром `["10", 0, 1]`.
  3. Запустите. Если пылесос поехал на кухню — запишите: 10 = Кухня.
  4. Пробуйте 11, 12, 13 и так далее, пока не найдете все комнаты.

**Метод В: Перехват трафика (Для экспертов)**
- **Зачем:** Чтобы использовать официальное приложение Mi Home.
- **Примечание:** **Мы не проверяли этот метод.** Возможны сложности с настройкой Android-устройства (SSL pinning, установка сертификатов).
- **Как:** Используйте Charles Proxy или mitmproxy для перехвата JSON-запроса `set-room-clean` из официального приложения.

### 3. Карта комнат (Для этого устройства)

| ID | Название | Статус |
|----|----------|--------|
| **10** | 🧸 Детская | Подтверждено |
| **11** | 🍳 Кухня | Подтверждено |
| **12** | 🛏️ Спальня | Подтверждено |
| **13** | 🚶 Коридор | Подтверждено |

### 4. Пример конфигурации (scripts.yaml)

```yaml
vacuum_clean_kitchen:
  alias: "🍳 Уборка кухни"
  icon: mdi:silverware-fork-knife
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 7
        aiid: 3
        params: ["11", 0, 1]
```

### 📂 Файлы проекта
*   **[scripts.yaml](./scripts.yaml)** - Готовые скрипты для Home Assistant.
*   **[10_project_summary_2026_02_08.md](./10_project_summary_2026_02_08.md)** - Детальный технический отчет и история решения.
*   **[log.json](./log.json)** - Пример файла логов (Очищенный), где была найдена конфигурация комнат.
*   **[11_advanced_controls.md](./11_advanced_controls.md)** - Инструкция по управлению режимами, мощностью и водой.

