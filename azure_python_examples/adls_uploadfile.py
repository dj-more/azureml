import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
global service_client
global file_system_client


def connect_to_azure(): 
    try:  
        global service_client
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https", storage_account_name), credential=storage_account_key)
    except Exception as e:
        print(e)

def get_adls_gen2_container():
    global file_system_client

    account_name = "adlsgen2encrypted"
    account_key  = "mVEft0AuOaK2eDpEmPJ+Nb+SesJQKVj/b4noCaAmcAXyiOwWxpExK5jf+ZGe5N+Vc938A5ShYbf4z3D1zaH4TA=="
    try:
        file_system_client = service_client.get_file_system_client(file_system="test")
    except Exception as e:
        print(e)

def list_directory_contents():
    try:
        paths = file_system_client.get_paths(path="Level1")
    except Exception as e:
        print(e) 
    for path in paths:
        print(path.name + '\n')

def main():
    connect_to_azure()
    get_adls_gen2_container()
    list_directory_contents()

if __name__ == "__main__":
    main()