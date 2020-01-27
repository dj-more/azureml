import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient

def list_directory_contents():
    try:
        
        file_system_client = service_client.get_file_system_client(file_system="test")

        paths = file_system_client.get_paths(path="test")

        for path in paths:
            print(path.name + '\n')

    except Exception as e:
     print(e)

try:  
    global service_client
        
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https", 'adlsgen2encrypted'), credential='mVEft0AuOaK2eDpEmPJ+Nb+SesJQKVj/b4noCaAmcAXyiOwWxpExK5jf+ZGe5N+Vc938A5ShYbf4z3D1zaH4TA==')
    
except Exception as e:
    print(e)

list_directory_contents();


