> **⚠️ АРХИВ / HISTORY FILE**
> Этот файл является частью истории разработки и может содержать устаревшие данные.

---

# Попытки настройки уборки по комнатам

## 🎯 Цель
Настроить уборку пылесоса по отдельным комнатам через команды Home Assistant.

## 📊 Результат
❌ **Не достигнуто** - команды отправляются, но пылесос не реагирует.

---

## Попытка #1: Получение списка комнат

### Метод: xiaomi_miot.get_properties

**Команда:**
```yaml
service: xiaomi_miot.get_properties
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  mapping:
    - siid: 14
      piid: 1
```

**Результат:** ❌ Нет ответа, сервис не возвращает данные

---

## Попытка #2: Скрипт с параметром room_id

### Метод: Универсальный скрипт с полем room_id

**Код скрипта:**
```yaml
vacuum_clean_room_by_id:
  alias: "Уборка комнаты по ID"
  fields:
    room_id:
      description: "ID комнаты"
      example: "16"
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 4
        aiid: 1
      data_template:
        in:
          - "{{ room_id | int }}"
```

**Вызов:**
```yaml
service: script.vacuum_clean_room_by_id
data:
  room_id: 10
```

**Результат:** ❌ Ошибка: `extra keys not allowed @ data[in]. Got None`

**Причина:** Параметр `in` не поддерживается в формате вызова

---

## Попытка #3: Прямой вызов xiaomi_miot.call_action (UI)

### Метод: Через Developer Tools → Services

**Команда (вариант 1):**
```yaml
service: xiaomi_miot.call_action
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 4
  aiid: 1
  in:
    - 10
```

**Результат:** ❌ Ошибка: `extra keys not allowed @ data[in]. Got None`

---

## Попытка #4: API с токеном - параметр params

### Метод: curl запрос к HA API

**Токен:** (см. файл api_token.txt)

**Команда:**
```bash
curl -X POST http://localhost:8123/api/services/xiaomi_miot/call_action \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner,
