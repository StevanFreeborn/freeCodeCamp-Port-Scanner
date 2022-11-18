import socket
import re
from common_ports import ports_and_services

def get_open_ports(host, port_range, isVerbose=False):
  open_ports = []
  
  start_port = port_range[0]
  stop_port = port_range[1] + 1
  ports = range(port_range[0], port_range[1] + 1)

  try:
    ip = socket.gethostbyname(host)

    print(f'\nScanning ports {start_port} to {stop_port} of {host}.')
  
    for port in ports:
      print(f'Scanned port {port}...', end='')
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(5)
  
      isOpen = s.connect_ex((ip,port)) == 0
      
      if isOpen:
        print(f'port {port} is open.')
        open_ports.append(port)
      else:
        print(f'port {port} is closed.')
      s.close()

  except KeyboardInterrupt:
    return 'Exiting program.'
  except socket.gaierror:
    if(re.search('[a-zA-Z]', host)):
      return 'Error: Invalid hostname'
    return 'Error: Invalid IP address'

  print('Scan completed.')
  print('\n')
  
  if isVerbose is False:
    return open_ports
  
  host_name = None
  
  try:
    host_name = socket.gethostbyaddr(ip)[0]
  except socket.herror:
    host_name = None

  final_result = 'Open ports for '

  if host_name != None:
    final_result += f'{host_name} ({ip})\n'
  else:
    final_result += f'{ip}\n'

  final_result += 'PORT     SERVICE\n'

  last_open_port = open_ports[len(open_ports) - 1]
  
  for port in open_ports:
    max_spaces = 9
    port_len = len(str(port))
    num_of_spaces = max_spaces - port_len
    spaces = ' ' * num_of_spaces
    service = ports_and_services.get(port)
    final_result += f'{port}{spaces}{service}'

    if port != last_open_port:
      final_result += '\n'
  
  return final_result