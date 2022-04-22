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

from SSHService import SSH
global ssh_sessions

SESSION_DEFAULT = "default"
try:
    if not ssh_sessions :
        ssh_sessions = {SESSION_DEFAULT:{}}
except NameError:
    ssh_sessions = {SESSION_DEFAULT:{}}

module = GetParams("module")

try:
    if module == "connect":
        hostname = GetParams("hostname")
        username = GetParams("username")
        password = GetParams("password")
        publicKeyFile = GetParams("publicKeyFile")
        
        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT
        try:
            if not publicKeyFile:
                ssh_sessions[session] = SSH(hostname, username)
                ssh_sessions[session].connect_with_password(password)
            else:
                ssh_sessions[session] = SSH(hostname, username)
                ssh_sessions[session].connect_whit_private_key(publicKeyFile)
            response = True
        except:
            response = False

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, response)
        

        

    if module == "createFolder":
        folderName = GetParams("folderName")

        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT

        ssh_sessions[session].create_folder(folderName)

    if module == "changeDirectory":
        pathToGo = GetParams("pathToGo")

        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT

        ssh_sessions[session].cd(pathToGo)

    if module == "run":
        commandToExecute = GetParams("commandToExecute")

        try:
            commandToExecute = eval(commandToExecute)
        except:
            pass

        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT
        
        response = ssh_sessions[session].run(commandToExecute)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, response.output.split("\n"))

    if module == "writeTextInFile":
        pathToFile = GetParams("pathToFile")
        textToWrite = GetParams("textToWrite")

        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT

        ssh_sessions[session].write_text_file(pathToFile, textToWrite)

    if module == "readTextFromFile":
        pathToFile = GetParams("pathToFile")

        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT

        response = ssh_sessions[session].read_text_file(pathToFile)

        whereToStore = GetParams("whereToStore")
        print(response)
        SetVar(whereToStore, response)

    if module == "disconnect":
        session = GetParams("session")
        if not session:
            session = SESSION_DEFAULT

        ssh_sessions[session].disconnect()

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException()
    raise e
