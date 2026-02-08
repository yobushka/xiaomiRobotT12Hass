---
Level: 2 (Operational)
Category: Guide
Status: Verified
---

# 🎛️ Расширенные настройки (Advanced Controls)

Вы можете управлять режимами уборки, мощностью всасывания и подачей воды.

## ⚠️ Важное замечание (Verification Note)
В ходе тестов 2026-02-08 было установлено, что устройство часто игнорирует команды `set_miot_property`, когда находится на док-станции (режим `idle`). Рекомендуется отправлять настройки непосредственно перед вызовом уборки (`call_action`) или во время работы.

## 📋 Таблица параметров (Parameters Table)

| Функция (Function) | Service ID (siid) | Property ID (piid) | Значения (Values) | Верификация |
|-------------------|-------------------|--------------------|-------------------|-------------|
| **Режим (Mode)** | 2 (Vacuum) | 4 | **0**: Пылесос (Sweep)<br>**1**: Пылесос + Швабра (Sweep & Mop)<br>**2**: Швабра (Mop) | ✅ |
| **Мощность (Suction)** | 7 (Sweep) | 5 | **0**: Тихий (Silent)<br>**1**: Стандарт (Standard)<br>**2**: Средний (Medium)<br>**3**: Турбо (Turbo) | ✅ |
| **Вода (Water Level)** | 7 (Sweep) | 6 | **0**: Низкий (Low)<br>**1**: Средний (Mid)<br>**2**: Высокий (High) | ✅ |
| **Маршрут мытья (Mop Route)** | 7 (Sweep) | 7 | **0**: S-образный<br>**1**: Y-образный (Professional) | ✅ |

## 🔍 Соответствие атрибутам Home Assistant (Attributes Mapping)

Текущие значения этих параметров можно отслеживать напрямую в атрибутах сущности `vacuum.xiaomi_b106bk_807e_robot_cleaner`:

| MIoT Свойство | Атрибут в HA | Значение в примере | Описание |
|---------------|--------------|--------------------|----------|
| **siid 2, piid 4** | `vacuum.mode` | `1` | Режим: Пылесос + Швабра |
| **siid 7, piid 5** | `sweep.suction_state` | `3` | Мощность: Турбо |
| **siid 7, piid 6** | `sweep.water_state` | `2` | Вода: Высокий уровень |
| **siid 7, piid 7** | `sweep.mop_route` | `1` | Маршрут: Y-образный |

Также в атрибуте `fan_speed` отображается текстовое название режима мощности (например, `Turbo`).

## 🛠 Примеры скриптов (Script Examples)

### Установить режим "Только пылесос"
```yaml
service: xiaomi_miot.set_miot_property
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 2
  piid: 4
  value: 0
```

### Установить мощность "Турбо"
```yaml
service: xiaomi_miot.set_miot_property
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 7
  piid: 5
  value: 3
```

### Установить высокий уровень воды
```yaml
service: xiaomi_miot.set_miot_property
data:
  entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
  siid: 7
  piid: 6
  value: 2
```

## 🧩 Комбинированный скрипт (Complex Script)

Пример скрипта "Мощная уборка кухни":
1. Установить режим "Пылесос + Швабра"
2. Включить Турбо мощность
3. Включить Максимальную воду
4. Начать уборку кухни

```yaml
vacuum_heavy_clean_kitchen:
  alias: "🌪️ Мощная уборка кухни"
  sequence:
    # 1. Mode: Sweep & Mop
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 2
        piid: 4
        value: 1
    # 2. Suction: Turbo
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 7
        piid: 5
        value: 3
    # 3. Water: High
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 7
        piid: 6
        value: 2
    # 4. Start Cleaning Room 11 (Kitchen)
    - service: xiaomi_miot.call_action
      data:
        entity_id: vacuum.xiaomi_b106bk_807e_robot_cleaner
        siid: 7
        aiid: 3
        params: ["11", 0, 1]
```
