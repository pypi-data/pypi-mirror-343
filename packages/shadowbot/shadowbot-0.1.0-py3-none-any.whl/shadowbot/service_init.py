import socket
import requests, re, datetime, sys
from typing import Literal, Sequence, Union
from .utils._function_share import _client_id, _m_sha256, _current_time_zone
from .utils._data_storage import _data_storage_run

class ShadowBotAssistant:
    def __init__(self, xbot, package):
        self.xbot = xbot
        self.package = package
        self.client_id = _client_id()  
        self.app_rpaKey = None  
        self.app_rpaName = None  
        self.app_persistentServices = False  
        self.app_flowKey = None
        self.app_flowNode = None
        self.hostport = self.hostport_check()
        self.local_ip_intranet = self.get_local_ip_intranet()
        self.local_ip_public = self.get_local_ip_public()
        self.app_serverAddressHttp = None  
        self.app_serverAddressIp = None  
        self.app_serverAddressPort = None  
        self._init_generate()  
        '''
        parameter:
        ...
        '''

    def get_local_ip_intranet(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("192.168.1.1", 80))  
                return s.getsockname()[0]
        except Exception as e:
            print(f"⚠️ socket 获取内网IP失败: {e}")
            print("⚠️ socket 获取内网IP失败: 正在重试")

        return "127.0.0.1"
    
    def get_local_ip_public(self):
        try:
            response = requests.get('http://ip-api.com/json')
            response.raise_for_status()  
            ip_details = response.json()
            
            if ip_details['status'] == 'success':
                translations = {
                    'status': '状态',
                    'query': '查询IP',
                    'country': '国家',
                }
                translated_details = {translation: ip_details[key] for key, translation in translations.items() if key in ip_details}
                return translated_details
            else:
                return None
        except requests.RequestException as e:
            return None
    
    def hostport_check(self):
        def check_address(serverAddress):
            pattern = r'^https?://(?:\d{1,3}\.){3}\d{1,3}:\d+$'
            if not re.match(pattern, serverAddress):
                self.xbot.app.dialog.show_message_box(
                    title='RPA助手异常', 
                    message='''
                            \nserverAddress 为必填项
                            \n- 格式：http://<ip>:<port>
                            \n- 如果忽略该参数，服务端无法正常接收消息
                        ''',
                    timeout=10,
                    button='ok'
                    )
                
                return False
            return True
        def check_port(host, port, timeout=5):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                try:
                    sock.connect((host, int(port)))
                    return True
                except (socket.timeout, socket.error) as e:
                    self.xbot.app.dialog.show_message_box(
                        title='RPA助手异常', 
                        message=f'无法连接到 {host}:{port}，端口可能未开放或被防火墙阻止。',
                        timeout=10,
                        button='ok'
                        )
                    return False
                
        url = self.package.variables.get('shadowBot_assistant_APP_serverAddress')
        if check_address(url):
            http, _, hostport= url.split('/', )  
            hostname, _, port = hostport.partition(':')  
            
            if check_port(hostname, port):
                self.app_serverAddressHttp = http
                self.app_serverAddressIp = hostname
                self.app_serverAddressPort = port
                self.app_serverAddress = f'{self.app_serverAddressHttp}://{self.app_serverAddressIp}:{self.app_serverAddressPort}'
                print(f"端口 {port} 在 {hostname} 上开放")
                return True
            else:
                print(f"无法连接到 {hostname}:{port}，端口可能未开放或被防火墙阻止。")
                return False
        else:
            return False
        
    def _init_generate(self):
        if 'shadowBot_assistant_APP_rpaKey' in self.package.variables and self.package.variables.get('shadowBot_assistant_APP_rpaKey') not in [None, '']:
            self.app_rpaKey = self.package.variables.get('shadowBot_assistant_APP_rpaKey')
        else:
            self.app_rpaKey = _m_sha256(key=self.client_id, message='rpaKey')
        
        if 'shadowBot_assistant_APP_rpaName' in self.package.variables and self.package.variables.get('shadowBot_assistant_APP_rpaName') not in [None, '']:
            self.app_rpaName = self.package.variables.get('shadowBot_assistant_APP_rpaName')
        else:
            self.app_rpaName = self.app_rpaKey

        if 'shadowBot_assistant_APP_persistentServices' in self.package.variables and self.package.variables.get('shadowBot_assistant_APP_persistentServices') in [False, True]:
            self.app_persistentServices = self.package.variables.get('shadowBot_assistant_APP_persistentServices')
        else:
            self.app_persistentServices = False

        self.app_flowKey = _m_sha256(key=self.client_id, message='flowKey')
        
        _, _, trigger_time = _current_time_zone()
        self.app_flowNode = datetime.fromisoformat(trigger_time).strftime('%Y-%m-%d %H:%M:%S.%f')

        if 'shadowBot_assistant_APP_abnormalControl' in self.package.variables and self.package.variables.get('shadowBot_assistant_APP_abnormalControl') not in [None, '']:
            self.app_abnormalControl = self.package.variables.get('shadowBot_assistant_APP_abnormalControl')
        else:
            self.app_abnormalControl = 'connect'
        
        
def service_init(
        sba: ShadowBotAssistant,
        init: bool = False
        ):
    result = _data_storage_run(
        sba=sba,
        task='service_init',
        data={}
    )
        
        
        
        
        