# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import os
import sys
base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'ssh_connection' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)
import subprocess

module = GetParams("module")
global con
global host
global user
global path

if module == "connect_pem":
    path = GetParams("path")
    host = GetParams("host")
    user = GetParams("user")
    result = GetParams("result")

    command = "{lib}ssh.exe {user}@{host} -i {path}".format(lib=cur_path, host=host, user=user, path=path)

    try:
        con = subprocess.Popen(command,
                                    stdin=subprocess.PIPE, 
                                    stdout = subprocess.PIPE,
                                    shell=True)
        out, err = con.communicate()
        
        if not out.decode():
            raise Exception("Could not resolve hostname {host}".format(host=host))

    except Exception as e:
        PrintException()
        raise e

    
if module == "execute":
    command = GetParams("command")
    result = GetParams("result")

    try:
        comm = "{lib}ssh.exe {user}@{host} -i {path} {command}".format(lib=cur_path, host=host, user=user, path=path, command=command)
        con = subprocess.Popen(comm,
                                    stdin=subprocess.PIPE, 
                                    stdout = subprocess.PIPE,
                                    shell=True)
        out, err = con.communicate()
        
        if result:
            SetVar(result, out.decode())
    except Exception as e:
        PrintException()
        raise e

if module == "close":
    try:
        con.close()
    except Exception as e:
        PrintException()
        raise e
