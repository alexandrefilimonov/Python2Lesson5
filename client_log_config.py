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
#python client_log_config.py -a 127.0.0.1 -p 8888

import logging 
import sys
import json 
from typing import Any, Dict 
from socket import *
import argparse

format = logging.Formatter("%(asctime)s %(levelname)-10s %(message)s")
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(format)

log = logging.getLogger('app.client.log')
log.addHandler(crit_hand)
log.critical( 'Start client log!' )

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

try :
    server, port = get_args()
    port_number = 8000
    for p in port:
       port_number=int(p)

    while True :
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action" : "authenticate", "user" : {"account_name" : "alex", "password" : "alex_pwd"}}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        log.critical('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes')

        s.close()
    
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action" : "msg", "to" : "room #1", "from" : "alex_account", "message" : "Hello, server!"}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        log.critical('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes' )
        s.close()
    
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect(( 'localhost' , port_number )) 
        msg = {"action": "quit", "message": "Quit"}
        msg_str = json.dumps(msg)
        s.send(msg_str.encode( 'utf-8' ))
        data = s.recv( 1000000 )
        log.critical('The message from server: '+data.decode( 'utf-8' )+', length '+str(len(data))+'bytes' )
        s.close()
        break

except OSError as e:      
    logging.getLogger( 'app.client.log' ).setLevel(logging.ERROR)       
    log.error('Error:', e.strerror)
    
