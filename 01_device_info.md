# Информация об устройстве

## Основные данные

| Параметр | Значение |
|----------|----------|
| Модель | Xiaomi Robot Vacuum T12 |
| Тип устройства | xiaomi.vacuum.b106bk |
| DID | 1062821236 |
| MAC адрес | b8:50:d8:15:80:7e |
| IP адрес | 192.168.1.X |
| Токен устройства | REDACTED_TOKEN |
| Entity ID в HA | vacuum.xiaomi_b106bk_807e_robot_cleaner |
| Версия ПО | 4.3.3_0010 |

## Текущее состояние

- **Батарея:** 78%
- **Статус:** Зарядка (status: 4)
- **Домашняя комната:** Спальня
- **ID текущей карты:** 1764966023
- **Количество карт:** 1

## Подключение

### Home Assistant
- URL: http://192.168.1.X:8123
- Интеграция: xiaomi_miot v1.1.2

### Сеть
- SSH: root@192.168.1.X
- Docker: homeassistant
- Конфигурация: /root/docker/homeassistant/config/

## Доступные кнопки (buttons)

- button.xiaomi_b106bk_807e_start_sweep - Начать уборку
- button.xiaomi_b106bk_807e_stop_sweeping - Остановить
- button.xiaomi_b106bk_807e_start_charge - На зарядку
- button.xiaomi_b106bk_807e_start_sweep_mop - Подметание + мытье
- button.xiaomi_b106bk_807e_start_only_sweep - Только подметание
- button.xiaomi_b106bk_807e_start_mop - Только мытье
- button.xiaomi_b106bk_807e_reset_consumable - Сброс расходников
- button.xiaomi_b106bk_807e_reset_map - Сброс карты

## Сенсоры

- sensor.xiaomi_b106bk_807e_battery_level - Уровень батареи
- sensor.xiaomi_b106bk_807e_vacuum_status - Статус
- sensor.xiaomi_b106bk_807e_sweep_cleaning_time - Время уборки
- sensor.xiaomi_b106bk_807e_sweep_cleaning_area - Площадь уборки

## Селекторы

- select.xiaomi_b106bk_807e_vacuum_mode - Режим мощности
- select.xiaomi_b106bk_807e_vacuum_sweep_type - Тип уборки

## MIoT Спецификация

### Service ID 4 (Sweep)
- AIID 1: start_sweep - Начать уборку
- AIID 4: (возможно segment_clean) - Уборка сегмента/комнаты

### Service ID 14 (Map)
- PIID 1: room_information - Информация о комнатах

## Проблемы

1. xiaomi_cloud_map_extractor не может авторизоваться в облаке
2. xiaomi_miot.get_properties не возвращает данные о комнатах
3. Уборка по комнатам через API не работает (команды отправляются, но пылесос не реагирует)
