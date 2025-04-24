import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError
import time
from datetime import datetime
from typing import Literal, Mapping, Any
from ._function_doctor import _log_errors
from ._function_share import _current_time_zone
from service_init import ShadowBotAssistant as SBA

def _data_storage_run(
        sba: SBA, 
        name: Literal['service_init', 'breakpoint_controller', 'time_diff_calculator', 'progress_manager', None] = None,  
        task: str = None,  
        data: Mapping[str, Any] = None,
        **kwargs
        ):
    
    url_rt = f'{sba.app_serverAddressHttp}://{sba.app_serverAddressIp}:{sba.app_serverAddressPort}/sba/data_storage'
    
    if name == 'service_init':
        url, payload, timeout, max_retries, retry_delay = _config_service_init(name, sba, url_rt, data)

    try:
        
        response_data = _send_request_with_retries(url, payload, timeout, max_retries, retry_delay, **kwargs)

    except Exception as e:
        print("请求失败:", e)
        sba.package.variables['sba_work_flow_countErr'] += 1  
    else:
        if response_data['state'] != 0:
            sba.package.variables['sba_work_flow_countErr'] += 1  


def _config_service_init(task, sba, url, data):
    
    url = f'{url}/service_init'

    
    _, local_tz, trigger_time = _current_time_zone()
    trigger_time = datetime.fromisoformat(trigger_time).strftime('%Y-%m-%d %H:%M:%S.%f')

    
    payload = {
        'task': task,
        'data': {
            'client_id': sba.client_id,
            'rpa_key': sba.app_rpaKey,
            'rpa_name': sba.app_rpaName,
            'persistent_services': sba.app_persistentServices,
            'abnormal_control': sba.app_abnormalControl,
            'flow_key': sba.app_flowKey,
            'flow_node': sba.app_flowNode,
            'local_ip_intranet': sba.local_ip_intranet,
            'local_ip_public': sba.local_ip_public,
            'server_address': sba.app_serverAddress,
            'local_tz': local_tz,
            'update_time': trigger_time,
            'create_time': sba.app_flowNode,
            }
        }

    
    timeout = 60

    
    max_retries = 3

    
    retry_delay = 5

    return url, payload, timeout, max_retries, retry_delay

@_log_errors(print_to_console=True)
def _send_request_with_retries(url, payload, timeout, max_retries, retry_delay, **kwargs):
    retries = 0
    error_list = []
    while retries < max_retries:
        try:
            
            response = requests.post(url, json=payload, timeout=timeout, **kwargs)
            
            
            response.raise_for_status()  
            
            
            response_data = response.json()
            
            
            if 'state' not in response_data:
                raise ValueError("响应JSON中缺少'state'字段")
            
            
            return response_data

        except Timeout:
            error_info = f"请求超时。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)
        except HTTPError as http_err:
            error_info = f"HTTP错误: {http_err}。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)
        except ConnectionError as conn_err:
            error_info = f"连接错误: {conn_err}。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)
        except ValueError as json_err:
            error_info = f"JSON解析失败或响应结构无效: {json_err}。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)
        except RequestException as req_err:
            error_info = f"请求过程中发生错误: {req_err}。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)
        except Exception as e:
            error_info = f"发生未知错误: {e}。{retry_delay}秒后重试... (第 {retries + 1} 次重试，最多 {max_retries} 次)"
            print(error_info)
            error_list.append(error_info)

        
        retries += 1
        if retries < max_retries:
            time.sleep(retry_delay)

    
    raise Exception(f"请求失败，已重试 {max_retries} 次。")



























            


            


            



            






























