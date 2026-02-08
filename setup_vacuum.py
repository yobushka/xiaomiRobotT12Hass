import requests
import json
import os
import sys
import time

def load_env_manual(path='.env'):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip()

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

def ask_yn(prompt):
    while True:
        choice = input(f'{prompt} (y/n): ').lower()
        if choice in ['y', 'n']:
            return choice == 'y'

def cleanup_scripts():
    print('\n--- [ФАЗА 0: ОЧИСТКА] ---')
    print('Этот этап подготовит систему к генерации новых скриптов.')
    if ask_yn('Вы хотите очистить временный файл scripts_generated.yaml перед началом?'):
        if os.path.exists('scripts_generated.yaml'):
            os.remove('scripts_generated.yaml')
            print('✅ Файл очищен.')
        return True
    else:
        print('❌ Остановка скрипта по требованию пользователя.')
        sys.exit()

def check_ha(config):
    print('\n--- [ФАЗА 1: ДИАГНОСТИКА] ---')
    try:
        r = requests.get(f"{config['BASE_URL']}/config", headers=config['HEADERS'], timeout=5)
        if r.status_code == 200:
            print('✅ Связь с Home Assistant установлена.')
            components = r.json().get('components', [])
            if 'xiaomi_miot' in components:
                print('✅ Интеграция xiaomi_miot найдена.')
                return True
            print('❌ Интеграция xiaomi_miot НЕ найдена.')
    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')
    return False

def scan_rooms_interactive():
    print('\n--- [ФАЗА 2: НАСТРОЙКА КАРТЫ] ---')
    print('Введите ID комнат (10, 11, 12...) и их названия.')
    rooms = []
    while True:
        rid = input('Введите ID комнаты (или нажмите Enter для завершения): ')
        if not rid: break
        name = input(f'Введите название для комнаты {rid} (напр. Кухня): ')
        rooms.append({'id': rid, 'name': name, 'slug': name.lower().replace(' ', '_')})
        if not ask_yn('Добавить еще одну комнату?'): break
    return rooms

def generate_config(config, rooms):
    print('\n--- [ФАЗА 3: ГЕНЕРАЦИЯ КОМАНД] ---')
    use_max = ask_yn('Использовать режим Турбо + Макс. вода во всех скриптах?')
    
    yaml_content = '# Сгенерированные скрипты для Xiaomi T12\n'
    
    template_max = """
vacuum_clean_{slug}:
  alias: "🧹 Уборка: {name}"
  sequence:
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: {entity}
        siid: 7
        piid: 5
        value: 3 # Turbo
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: {entity}
        siid: 7
        piid: 6
        value: 2 # Max Water
    - service: xiaomi_miot.call_action
      data:
        entity_id: {entity}
        siid: 7
        aiid: 3
        params: ["{id}", 0, 1]
"""

    template_full = """
# {name}: Интенсивный режим
vacuum_clean_{slug}_intensive:
  alias: "🌪️ {name} (Интенсив)"
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: {entity}
        siid: 7
        aiid: 3
        params: ["{id}", 0, 1]

# {name}: Тихий режим
vacuum_clean_{slug}_quiet:
  alias: "🔇 {name} (Тихо)"
  sequence:
    - service: xiaomi_miot.set_miot_property
      data:
        entity_id: {entity}
        siid: 7
        piid: 5
        value: 0
    - service: xiaomi_miot.call_action
      data:
        entity_id: {entity}
        siid: 7
        aiid: 3
        params: ["{id}", 0, 1]
"""

    for r in rooms:
        if use_max:
            yaml_content += template_max.format(name=r['name'], slug=r['slug'], entity=config['ENTITY_ID'], id=r['id'])
        else:
            yaml_content += template_full.format(name=r['name'], slug=r['slug'], entity=config['ENTITY_ID'], id=r['id'])

    with open('scripts_generated.yaml', 'w') as f:
        f.write(yaml_content)
    print('✅ Файл scripts_generated.yaml создан.')

if __name__ == '__main__':
    load_env_manual()
    cfg = get_config()
    if not cfg['HASS_TOKEN']:
        print('❌ Ошибка: Токен не найден в .env')
        sys.exit()
        
    cleanup_scripts()
    if check_ha(cfg):
        rooms_list = scan_rooms_interactive()
        if rooms_list:
            generate_config(cfg, rooms_list)
            print('\n🏆 Настройка завершена!')
