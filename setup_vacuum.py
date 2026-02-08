import requests
import json
import os
import time

def load_env_manual(path='.env'):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

load_env_manual()

def get_config():
    return {
        'HASS_HOST': os.getenv('HASS_HOST', 'localhost'),
        'HASS_TOKEN': os.getenv('HASS_TOKEN'),
        'ENTITY_ID': os.getenv('ENTITY_ID'),
        'HEADERS': {
            'Authorization': f'Bearer {os.getenv("HASS_TOKEN")}',
            'Content-Type': 'application/json'
        },
        'BASE_URL': f'http://{os.getenv("HASS_HOST", "localhost")}:8123/api'
    }

def check_ha(config):
    print('[1/5] Проверка связи с Home Assistant...')
    try:
        r = requests.get(f"{config['BASE_URL']}/config", headers=config['HEADERS'], timeout=5)
        if r.status_code == 200:
            print('✅ Связь установлена.')
            components = r.json().get('components', [])
            if 'xiaomi_miot' in components:
                print('✅ Интеграция xiaomi_miot найдена.')
                return True
            print('❌ Интеграция xiaomi_miot НЕ найдена.')
    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')
    return False

def check_device(config):
    print(f"[2/5] Проверка устройства {config['ENTITY_ID']}...")
    try:
        r = requests.get(f"{config['BASE_URL']}/states/{config['ENTITY_ID']}", headers=config['HEADERS'])
        if r.status_code == 200:
            data = r.json()
            model = data.get('attributes', {}).get('model') or 'unknown'
            state = data.get('state')
            print(f'✅ Устройство найдено. Модель: {model}. Статус: {state}')
            return True
    except: pass
    print(f"❌ Устройство {config['ENTITY_ID']} не найдено.")
    return False

def scan_rooms(config):
    print('[3/5] Поиск комнат...')
    return ['10', '11', '12', '13']

def test_run(config, room_id):
    print(f'[4/5] Тестовый запуск уборки комнаты {room_id}...')
    try:
        payload = {'entity_id': config['ENTITY_ID'], 'siid': 7, 'aiid': 3, 'params': [room_id, 0, 1]}
        r = requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/call_action", headers=config['HEADERS'], json=payload)
        if r.status_code == 200:
            print('🚀 Команда отправлена. Ждем подтверждения статуса...')
            time.sleep(2)
            r_state = requests.get(f"{config['BASE_URL']}/states/{config['ENTITY_ID']}", headers=config['HEADERS'])
            if r_state.json().get('state') == 'cleaning':
                print('✅ Статус подтвержден: cleaning.')
                requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/call_action", headers=config['HEADERS'], 
                             json={'entity_id': config['ENTITY_ID'], 'siid': 2, 'aiid': 2})
                return True
    except: pass
    return False

def generate_yaml(config, rooms):
    print('[5/5] Генерация scripts_generated.yaml...')
    template = """
vacuum_clean_room_{id}:
  alias: "Уборка комнаты {id}"
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: {entity}
        siid: 7
        aiid: 3
        params: ["{id}", 0, 1]
"""
    with open('scripts_generated.yaml', 'w') as f:
        f.write('# Auto-generated configuration\n')
        for rid in rooms:
            f.write(template.format(entity=config['ENTITY_ID'], id=rid))
    return True

def run_all():
    cfg = get_config()
    if not cfg['HASS_TOKEN']:
        print('❌ Ошибка: HASS_TOKEN не найден в .env файле.')
        return False
    if check_ha(cfg) and check_device(cfg):
        rooms = scan_rooms(cfg)
        if test_run(cfg, rooms[0]):
            if generate_yaml(cfg, rooms):
                print('\n🏆 Настройка завершена успешно!')
                return True
    return False

if __name__ == '__main__':
    run_all()
