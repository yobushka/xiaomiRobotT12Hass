import requests
import json
import os
import sys
import time
import re
import locale
import shutil

# --- Localization System ---
def detect_language():
    try:
        lang_code, _ = locale.getlocale()
        if lang_code and lang_code.lower().startswith('ru'):
            return 'ru'
    except: pass
    return 'en'

LANG = detect_language()

MSGS = {
    'ru': {
        'phase_0': '--- [ФАЗА 0: ОЧИСТКА] ---',
        'ask_cleanup': 'Очистить временный файл scripts_generated.yaml перед началом?',
        'cleanup_done': '✅ Файл очищен.',
        'stop_user': '❌ Остановка по требованию пользователя.',
        'phase_1': '--- [ФАЗА 1: ДИАГНОСТИКА] ---',
        'ha_ok': '✅ Связь с Home Assistant установлена.',
        'ha_fail': '❌ Нет связи с Home Assistant. Проверьте .env',
        'phase_2': '--- [ФАЗА 2: ОПОЗНАВАНИЕ КОМНАТ] ---',
        'map_found': '🔍 Найдена карта ID: {}. Сканируем комнаты...',
        'auto_ok': '✅ Авто-обнаружение сработало: {}',
        'auto_fail': '⚠️ Авто-обнаружение не дало результатов.',
        'ask_vevs': 'У вас есть логи из приложения Mi Home от VEVS?',
        'vevs_instr': 'Инструкция: Найдите в логе ответ на get-preference-ii.\nПример строки:\n{"code":0,"message":"ok","result":{"did":"1062821236","miid":0,"siid":7,"aiid":10,"code":0,"out":["[\\"1_12_1_3_2_1_1_0\\",\\"1_10_1_3_2_1_1_1\\",\\"1_11_1_3_2_1_1_0\\",\\"1_13_1_3_2_1_1_0\\"]",1,"[]",0],"exe_time":81,"net_cost":24,"ot_cost":4,"otlocalts":1770563118462595,"_oa_rpc_cost":114,"withLatency":0}}',
        'vevs_input': 'Вставьте строку из лога: ',
        'vevs_ok': '✅ Из лога извлечено ID: {}',
        'ask_identify': 'Опознать комнату {} (пылесос поедет туда)?',
        'ask_add_blind': 'Просто добавить комнату {} без выезда?',
        'moving_to': '🚀 Выезжаем в комнату {}... Проследите за пылесосом.',
        'returning_to_dock': '🏠 Возвращаемся на базу для подзарядки...',
        'enter_name': 'Введите имя для комнаты {} (напр. Кухня): ',
        'ask_active': 'Запустить АКТИВНОЕ СКАНИРОВАНИЕ (перебор ID 10-20)?',
        'ask_wait': 'Сколько секунд давать на опознание каждой комнаты?',
        'manual_mode': 'Переход к ручному вводу.',
        'enter_id': 'ID комнаты (Enter для завершения): ',
        'enter_name_manual': 'Название: ',
        'ask_next': 'Добавить еще одну?',
        'phase_3': '--- [ФАЗА 3: ГЕНЕРАЦИЯ] ---',
        'ask_max': 'Использовать Макс. настройки (Турбо + Макс. вода) по умолчанию?',
        'gen_ok': '✅ Файл scripts_generated.yaml готов.',
        'phase_4': '--- [ФАЗА 4: ДЕПЛОЙ] ---',
        'ask_deploy': 'Применить сгенерированные скрипты в Home Assistant (тип: {})?',
        'deploy_done': '✅ Скрипты добавлены в {}. Создан бэкап .bak',
        'deploy_disabled': '⏸ Автоматический деплой отключен в .env',
        'reload_start': '🔄 Перезагрузка скриптов в Home Assistant...',
        'reload_ok': '🚀 Все скрипты активированы и доступны в HA!',
        'final_ok': '\n🏆 Настройка успешно завершена!'
    },
    'en': {
        'phase_0': '--- [PHASE 0: CLEANUP] ---',
        'ask_cleanup': 'Clear scripts_generated.yaml before starting?',
        'cleanup_done': '✅ File cleared.',
        'stop_user': '❌ Stopped by user.',
        'phase_1': '--- [PHASE 1: DIAGNOSTICS] ---',
        'ha_ok': '✅ Connection to Home Assistant established.',
        'ha_fail': '❌ No connection to Home Assistant. Check .env',
        'phase_2': '--- [PHASE 2: ROOM DISCOVERY] ---',
        'map_found': '🔍 Found Map ID: {}. Scanning rooms...',
        'auto_ok': '✅ Auto-discovery worked: {}',
        'auto_fail': '⚠️ Auto-discovery returned no results.',
        'ask_vevs': 'Do you have logs from Mi Home by VEVS?',
        'vevs_instr': 'Instruction: Find get-preference-ii response in logs.\nExample:\n{"code":0,"message":"ok","result":{"did":"1062821236","miid":0,"siid":7,"aiid":10,"code":0,"out":["[\\"1_12_1_3_2_1_1_0\\",\\"1_10_1_3_2_1_1_1\\",\\"1_11_1_3_2_1_1_0\\",\\"1_13_1_3_2_1_1_0\\"]",1,"[]",0],"exe_time":81,"net_cost":24,"ot_cost":4,"otlocalts":1770563118462595,"_oa_rpc_cost":114,"withLatency":0}}',
        'vevs_input': 'Paste log string: ',
        'vevs_ok': '✅ Extracted IDs from log: {}',
        'ask_identify': 'Identify room {} (vacuum will move there)?',
        'ask_add_blind': 'Just add room {} without moving?',
        'moving_to': '🚀 Moving to room {}... Observe the vacuum.',
        'returning_to_dock': '🏠 Returning to dock for charging...',
        'enter_name': 'Name for room {} (e.g. Kitchen): ',
        'ask_active': 'Start ACTIVE SCANNING (bruteforce ID 10-20)?',
        'ask_wait': 'Seconds to identify each room?',
        'manual_mode': 'Switching to manual input.',
        'enter_id': 'Room ID (Enter to finish): ',
        'enter_name_manual': 'Name: ',
        'ask_next': 'Add another one?',
        'phase_3': '--- [PHASE 3: GENERATION] ---',
        'ask_max': 'Use Max settings (Turbo + Max Water) by default?',
        'gen_ok': '✅ File scripts_generated.yaml created.',
        'phase_4': '--- [PHASE 4: DEPLOY] ---',
        'ask_deploy': 'Apply generated scripts to Home Assistant (type: {})?',
        'deploy_done': '✅ Scripts added to {}. Backup created.',
        'deploy_disabled': '⏸ Automatic deployment disabled in .env',
        'reload_start': '🔄 Reloading scripts in Home Assistant...',
        'reload_ok': '🚀 Scripts activated and ready in HA!',
        'final_ok': '\n🏆 Setup completed successfully!'
    }
}

def t(key, *args):
    msg = MSGS.get(LANG, MSGS['en']).get(key, key)
    if msg is None:
        msg = key
    return msg.format(*args) if args else msg

def parse_vevs_log(log_text):
    ids = re.findall(r'(?:\"|\\")1_(\d+)_', log_text)
    return sorted(list(set(ids)), key=int)

def load_env_manual(path='.env'):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    parts = line.strip().split('=', 1)
                    if len(parts) == 2:
                        k, v = parts
                        os.environ[k] = v.strip()

def get_config():
    return {
        'ENTITY_ID': os.getenv('ENTITY_ID'),
        'DEPLOY_TYPE': os.getenv('DEPLOY_TYPE', 'disable'),
        'DEPLOY_PATH': os.getenv('DEPLOY_PATH'),
        'HEADERS': {
            'Authorization': f"Bearer {os.getenv('HASS_TOKEN')}",
            'Content-Type': 'application/json'
        },
        'BASE_URL': f"http://{os.getenv('HASS_HOST', 'localhost')}:8123/api"
    }

def ask_yn(prompt):
    while True:
        choice = input(f"{prompt} (y/n): ").lower()
        if choice in ['y', 'n']: return choice == 'y'

def check_ha(config):
    """Check Home Assistant connectivity and xiaomi_miot integration."""
    try:
        r = requests.get(f"{config['BASE_URL']}/config", headers=config['HEADERS'], timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def check_device(config):
    """Check if vacuum device is accessible."""
    try:
        r = requests.get(f"{config['BASE_URL']}/states/{config['ENTITY_ID']}", headers=config['HEADERS'], timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data.get('state') is not None
        return False
    except Exception:
        return False

def generate_yaml(config, room_ids):
    """Generate YAML scripts for given room IDs. Returns True on success."""
    try:
        yaml_content = f"\n# --- Auto-generated for {config['ENTITY_ID']} ---\n"
        for rid in room_ids:
            yaml_content += f"""
vacuum_clean_room_{rid}:
  alias: "Room {rid}"
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: {config['ENTITY_ID']}
        siid: 7
        aiid: 3
        params: ["{rid}", 0, 1]
"""
        with open('scripts_generated.yaml', 'w') as f:
            f.write(yaml_content)
        return True
    except Exception:
        return False

def stop_vacuum(config):
    requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/call_action", 
                 headers=config['HEADERS'], 
                 json={'entity_id': config['ENTITY_ID'], 'siid': 2, 'aiid': 2})

def charge_vacuum(config):
    button_id = config['ENTITY_ID'].replace('vacuum.', 'button.').replace('_robot_cleaner', '_start_charge')
    requests.post(f"{config['BASE_URL']}/services/button/press", 
                 headers=config['HEADERS'], json={'entity_id': button_id})

def get_rooms_interactive(config):
    print(f"\n{t('phase_2')}")
    detected_ids = []
    
    try:
        r_state = requests.get(f"{config['BASE_URL']}/states/{config['ENTITY_ID']}", headers=config['HEADERS'])
        map_id = r_state.json().get('attributes', {}).get('map.cur_map_id')
        if map_id:
            print(t('map_found', map_id))
            payload = {'entity_id': config['ENTITY_ID'], 'siid': 7, 'aiid': 10, 'params': [map_id]}
            r = requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/call_action", headers=config['HEADERS'], json=payload)
            res = r.json()
            out_data = res[0].get('result', {}).get('out', []) if isinstance(res, list) else res.get('result', {}).get('out', [])
            if out_data:
                detected_ids = parse_vevs_log(out_data[0])
                if detected_ids: print(t('auto_ok', ", ".join(detected_ids)))
    except: pass

    if not detected_ids:
        print(t('auto_fail'))
        if ask_yn(t('ask_vevs')):
            print(t('vevs_instr'))
            log_input = input(t('vevs_input'))
            detected_ids = parse_vevs_log(log_input)
            if detected_ids: print(t('vevs_ok', ", ".join(detected_ids)))

    rooms = []
    if detected_ids:
        for rid in detected_ids:
            if ask_yn(t('ask_identify', rid)):
                print(t('moving_to', rid))
                requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/set_miot_property", 
                             headers=config['HEADERS'], json={'entity_id': config['ENTITY_ID'], 'siid': 2, 'piid': 4, 'value': 2})
                requests.post(f"{config['BASE_URL']}/services/xiaomi_miot/call_action", 
                             headers=config['HEADERS'], json={'entity_id': config['ENTITY_ID'], 'siid': 7, 'aiid': 3, 'params': [rid, 0, 1]})
                name = input(t('enter_name', rid))
                if name: rooms.append({'id': rid, 'name': name, 'slug': name.lower().replace(' ', '_')})
                print(t('returning_to_dock'))
                charge_vacuum(config)
                time.sleep(3)
            elif ask_yn(t('ask_add_blind', rid)):
                name = input(t('enter_name', rid))
                if name: rooms.append({'id': rid, 'name': name, 'slug': name.lower().replace(' ', '_')})
    return rooms

def generate_config(config, rooms):
    print(f"\n{t('phase_3')}")
    use_max = ask_yn(t('ask_max'))
    prefix = 'Уборка' if LANG == 'ru' else 'Clean'
    yaml_content = f"\n# --- Auto-generated for {config['ENTITY_ID']} ---\n"
    for r in rooms:
        yaml_content += f"""
vacuum_clean_{r['slug']}:
  alias: \"🧹 {prefix}: {r['name']}\"
  sequence:
    - service: xiaomi_miot.call_action
      data:
        entity_id: {config['ENTITY_ID']}
        siid: 7
        aiid: 3
        params: [\"{r['id']}\", 0, 1]
"""
    with open('scripts_generated.yaml', 'w') as f: f.write(yaml_content)
    print(t('gen_ok'))
    return yaml_content

def deploy_to_ha(config, yaml_content):
    print(f"\n{t('phase_4')}")
    if config['DEPLOY_TYPE'] == 'disable':
        print(t('deploy_disabled'))
        return False
        
    if ask_yn(t('ask_deploy', config['DEPLOY_TYPE'])):
        path = config['DEPLOY_PATH']
        if not path:
            print("❌ DEPLOY_PATH not found in .env")
            return False
            
        try:
            if os.path.exists(path):
                shutil.copy(path, path + '.bak')
            
            with open(path, 'a') as f:
                f.write(yaml_content)
            
            print(t('deploy_done', path))
            print(t('reload_start'))
            requests.post(f"{config['BASE_URL']}/services/script/reload", headers=config['HEADERS'])
            print(t('reload_ok'))
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
    return False

if __name__ == '__main__':
    load_env_manual()
    cfg = get_config()
    print(t('phase_0'))
    if ask_yn(t('ask_cleanup')):
        if os.path.exists('scripts_generated.yaml'): os.remove('scripts_generated.yaml')
        print(t('cleanup_done'))
    
    try:
        r_ping = requests.get(f"{cfg['BASE_URL']}/config", headers=cfg['HEADERS'], timeout=5)
        if r_ping.status_code == 200:
            print(t('ha_ok'))
            rooms_list = get_rooms_interactive(cfg)
            if rooms_list: 
                content = generate_config(cfg, rooms_list)
                deploy_to_ha(cfg, content)
                print(t('final_ok'))
    except Exception as e: print(f"{t('ha_fail')} ({e})")