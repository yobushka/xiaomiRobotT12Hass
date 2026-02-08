# Рабочие скрипты и команды

## ✅ Гарантированно работающие команды

### 1. Полная уборка

**Скрипт:**
```yaml
service: script.vacuum_clean_all
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_start_sweep
```

### 2. Подметание + влажная уборка

**Скрипт:**
```yaml
service: script.vacuum_clean_sweep_mop
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_start_sweep_mop
```

### 3. Только подметание

**Скрипт:**
```yaml
service: script.vacuum_clean_sweep_only
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_start_only_sweep
```

### 4. Только влажная уборка

**Скрипт:**
```yaml
service: script.vacuum_clean_mop_only
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_start_mop
```

### 5. Возврат на базу

**Скрипт:**
```yaml
service: script.vacuum_return_to_base
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_start_charge
```

### 6. Остановить уборку

**Скрипт:**
```yaml
service: script.vacuum_stop
data: {}
```

**Прямой вызов:**
```yaml
service: button.press
target:
  entity_id: button.xiaomi_b106bk_807e_stop_sweeping
```

## 📋 Полный список скриптов

Файл скриптов: `/root/docker/homeassistant/config/scripts.yaml`
Копия: `/root/vacuum_robot/scripts.yaml`

### Базовые (работают):
- vacuum_clean_all
- vacuum_clean_sweep_mop
- vacuum_clean_sweep_only
- vacuum_clean_mop_only
- vacuum_return_to_base
- vacuum_stop

### По комнатам (НЕ работают):
- vacuum_clean_room_10
- vacuum_clean_room_11
- vacuum_clean_room_12
- vacuum_clean_room_13
- vacuum_clean_room_14
- vacuum_clean_room_15
- vacuum_clean_room_16
- vacuum_clean_room_17
- vacuum_clean_room_18
- vacuum_clean_room_19
- vacuum_clean_room_20

### Несколько комнат (НЕ работают):
- vacuum_clean_rooms_10_11
- vacuum_clean_rooms_10_11_12

## 🔧 Примеры автоматизации

### Уборка по расписанию

```yaml
automation:
  - alias: "Ежедневная уборка в 10:00"
    trigger:
      - platform: time
        at: "10:00:00"
    condition:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: script.vacuum_clean_all
```

### Уборка после ухода из дома

```yaml
automation:
  - alias: "Уборка когда никого нет дома"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "not_home"
        for: "00:10:00"
    action:
      - service: script.vacuum_clean_all
```

### Возврат на базу при низком заряде

```yaml
automation:
  - alias: "Вернуться при низком заряде"
    trigger:
      - platform: numeric_state
        entity_id: sensor.xiaomi_b106bk_807e_battery_level
        below: 20
    action:
      - service: script.vacuum_return_to_base
```

## 🎨 Lovelace карточка

Пример карточки для панели управления:

```yaml
type: entities
title: Пылесос Xiaomi T12
entities:
  - entity: vacuum.xiaomi_b106bk_807e_robot_cleaner
  - entity: sensor.xiaomi_b106bk_807e_battery_level
  - type: divider
  - entity: script.vacuum_clean_all
    name: Полная уборка
  - entity: script.vacuum_clean_sweep_mop
    name: Подметание + мытье
  - entity: script.vacuum_return_to_base
    name: На базу
  - entity: script.vacuum_stop
    name: Остановить
```

## 📱 Через API (с токеном)

```bash
TOKEN="your_token_here"

# Полная уборка
curl -X POST http://192.168.1.X:8123/api/services/script/vacuum_clean_all \
  -H "Authorization: Bearer " \
  -H "Content-Type: application/json" \
  -d '{}'

# Возврат на базу
curl -X POST http://192.168.1.X:8123/api/services/script/vacuum_return_to_base \
  -H "Authorization: Bearer " \
  -H "Content-Type: application/json" \
  -d '{}'
```

## ⚠️ Важные примечания

1. **Перезагрузка скриптов** после изменения:
   ```yaml
   service: script.reload
   ```

2. **Проверка статуса** пылесоса:
   ```yaml
   service: homeassistant.update_entity
   target:
     entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
   ```

3. **Логи** для отладки:
   ```bash
   docker logs -f homeassistant | grep -i vacuum
   ```
