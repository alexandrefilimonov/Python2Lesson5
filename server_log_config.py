#В директории проекта создать каталог log , в котором для клиентской и серверной сторон в
#отдельных модулях формата client_log_config.py и server_log_config.py создать логгеры;
#2. В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
#a. Создание именованного логгера;
#b. Сообщения лога должны иметь следующий формат: "<дата-время>
#<уровень_важности> <имя_модуля> <сообщение>" ;
#c. Журналирование должно производиться в лог-файл;
#d. На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
#3. Реализовать применение созданных логгеров для решения двух задач:
#a. Журналирование обработки исключений try/except . Вместо функции print()
#использовать журналирование и обеспечить вывод служебных сообщений в лог-файл;
#b. Журналирование функций, исполняемых на серверной и клиентской сторонах при
#работе мессенджера.
#python server_log_config.py -a 127.0.0.1 -p 8888

import logging
import sys
from socket import *
import time
import json 
from typing import Any, Dict 
import argparse

format = logging.Formatter("%(asctime)s %(levelname)-10s %(message)s")
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(format)

log = logging.getLogger('app_server')
log.addHandler(crit_hand)
log.critical( 'Start server log!\n' )

def get_args():
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script retrieves schedules from a given server')
    # Add arguments
    parser.add_argument(
        '-a', '--server', type=str, help='Server name', required=True)
    parser.add_argument(
        '-p', '--port', type=str, help='Port number', required=True, nargs='+')
    #parser.add_argument(
    #    '-k', '--keyword', type=str, help='Keyword search', required=False, default=None)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    server = args.server
    port = args.port[0].split(",")
    ##keyword = args.keyword
    # Return all variable values
    return server, port 

#class Response:
#    def: __init__(self, status_code:int)
#        self.status_code = status_code
#    def: to_json(self)-> str 
#         return json.dumps({'response':self_status_code})
				
def handle_authenticate(request) :
    if request['user']=={'account_name':'alex','password':'alex_pwd'}:
        return {"response": 200, "alert": "User alex authorized and authenticated successfully!"}
    else:
        return {"response": 402, "alert": "Error of authentication!"}

def handle_message(request) :
    return {"response": 200, "message": request['message']}

def handle_quit(request) :
    return {"response": 200, "action": "quit"}
		
mapping = {
    'authenticate': handle_authenticate, 
    'msg': handle_message, 
    'quit': handle_quit
}

def handler(request: Dict[str, object]) :
    log.critical('Client sent {request}\n')
    response=mapping[request['action']] (request)
    log.critical(f'Response {response}\n')
    return response 

try :
   server, port = get_args()
   port_number = 8000
   for p in port:
      port_number=int(p)
   
   s = socket(AF_INET, SOCK_STREAM) # Создает сокет TCP
   s.bind(( '' , port_number )) # Присваивает порт 8888
   # одновременно обслуживает не более 5 запросов.
   while True :
       s.listen( 5 ) # Переходит в режим ожидания запросов;
       client, addr = s.accept()
       with client: 
           data_b = client.recv( 1000000 )
           data = json.loads(data_b, encoding='utf-8')
           response = handler(data) 
           client.send(json.dumps(response).encode('utf-8'))		
           if (data['action']=='quit') :
               client.close()
               break

except OSError as e:      
    logging.getLogger( 'app_server.log' ).setLevel(logging.ERROR)       
    log.error('Error:', e.strerror)

