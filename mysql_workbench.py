#!/usr/bin/env python
# coding=utf-8

# Ce script permet l'ajout / la suppression et la visualisation de certains paramètres
import sys, getopt, os
import subprocess
import re
import xml.etree.ElementTree as ET
from xml.etree.cElementTree import tostring
from xml.dom import minidom
import uuid
import time

#global variable, will be better to use class but it is too much time to do it now
connectionId = ''


def syntaxOptions():
    print """Usage : ./mysql_workbench.py
    --host=192.168.0.2 (mandatory)
    --port=3306
    --user=root (mandatory)
    --password=myrootpass (mandatory)
    --database=mysql
    --name=
    """
    os._exit(1)

def buildTree(host, user, password, database, port, xmlFilePath, name):
    try:
        #generate new guid for connection like "04CA46BC-F5AC-433B-9891-831A306101B1" if two connections have the same uuid file is reset by workbench
        guid = str(uuid.uuid1()).upper()
        #generate connection name
        connectionName = user + '@' + host + ':' + str(port)
        print port

        #allelements = list(root.iter())
        #print allelements
        #get firstchild to import in it
        database=''

        #ET.dump(tree)
         #build tree
        tree = ET.parse(xmlFilePath)
        rootReal = tree.getroot()
        #rootReal[0].insert(0, root)

        #print root.tag
        #build new element

        value = ET.SubElement(rootReal[0],"value")
        value.set('struct-checksum',"0x96ba47d8")
        value.set('id',guid)
        value.set('struct-name',"db.mgmt.Connection")
        value.set('type','object')
        link = ET.SubElement(value,'link')
        link.set('key', 'driver')
        link.set('struct-name',"db.mgmt.Driver")
        link.set('type','object')
        link.text ='com.mysql.rdbms.mysql.driver.native'
        value2 = ET.SubElement(value,"value")
        value2.set('key', 'hostIdentifier')
        value2.set('type','string')
        value2.text = connectionName
        value3 = ET.SubElement(value,'value')
        value3.set('key','isDefault')
        value3.set('type','int')
        value3.text = '0'
        value4 = ET.SubElement(value,"value")
        value4.set('key', 'modules')
        value4.set('type', 'dict')
        value4.set('_ptr_', '0x7fcb93c00d00')
        dic = ET.SubElement(value,'value')
        dic.set('_ptr_','0x7fcb93c00d60')
        dic.set('type', 'dict')
        dic.set('key', 'parameterValues')
        #sublevel
        parameters = ET.SubElement(dic,'value')
        parameters.set('key','SQL_MODE')
        parameters.set('type','string')
        hostname =  ET.SubElement(dic,'value')
        hostname.set('key', 'hostName')
        hostname.set('type','string')
        hostname.text = host
        myPassword = ET.SubElement(dic,'value')
        myPassword.set('key','password')
        myPassword.set('type','string')
        myPassword.text = password
        myPort = ET.SubElement(dic,'value')
        myPort.set('key','port')
        myPort.set('type','int')
        myPort.text = str(port)
        schema = ET.SubElement(dic,'value')
        schema.set('key','schema')
        schema.set('type','string')
        schema.text = database
        sslCA = ET.SubElement(dic,'value')
        sslCA.set('key','sslCA')
        sslCA.set('type','string')
        sslCA.text = ''
        sslCert = ET.SubElement(dic,'value')
        sslCert.set('key','sslCert')
        sslCert.set('type','string')
        sslCert.text = ''
        sslCipher = ET.SubElement(dic,'value')
        sslCipher.set('key','sslCipher')
        sslCipher.set('type','string')
        sslCipher.text = ''
        sslKey = ET.SubElement(dic,'value')
        sslKey.set('key','sslKey')
        sslKey.set('type','string')
        sslKey.text = ''
        useSSL = ET.SubElement(dic,'value')
        useSSL.set('key','useSSL')
        useSSL.set('type','int')
        useSSL.text = '1'
        userName = ET.SubElement(dic,'value')
        userName.set('key','userName')
        userName.set('type','string')
        userName.text = user
        name = ET.SubElement(value,'value')
        name.set('key','name')
        name.set('type','string')
        name.text = name
        #tree = ET.ElementTree(rootReal)
        tempXML = tostring(tree.getroot()) #, method='html')
        tempXML = minidom.parseString(tempXML).toprettyxml(indent='  ')
        tempXML = tempXML.replace('/>', '></value>')
        tempXML = tempXML.replace("\n\n", '')
        tempXML = tempXML.replace('"dict"></value>', '"dict"/>')
        print tempXML
        #before writing the right file, write a complete copy
        dt = time.strftime("%Y%m%d-%H%M%S")
        f = open(xmlFilePath + '.copy' + dt,'w')
        f.write(tempXML)
        f.close()
        #final write
        f = open(xmlFilePath, 'w')
        f.write(tempXML)
        f.close()
    except IOError:
        print 'Error: connections.xml file not found on specified path'
#instancePath path to file named server_instances.xml
#system Linux/windows/other
#confFile full path th my.cnf file
#startCommand command to start mysqld
#stopCommand command to stop mysqld
#sshHost ssh host
#sshUser ssh user
#sshKey private ssh key 
#connectionId id of the connection previously generated
#sudo use sudo or not to launch command
def buildRemoteManagement(serverInstance):
    try:
        print ''
         #<value type="object" struct-name="db.mgmt.ServerInstance" id="669DA21E-ACD9-4137-94F4-12EEB9A21BB8" struct-checksum="0x367436e2">
      #<link type="object" struct-name="db.mgmt.Connection" key="connection">5EB33C2B-C940-4374-8087-1696F32B5EB2</link>
      #<value _ptr_="0x7ffc3c9d6960" type="dict" key="loginInfo">
      
       
      
       
      #</value>
         #tree = ET.parse(serverInstance)
         
        guid = str(uuid.uuid1()).upper()
        print serverInstance.instancePath
        tree = ET.parse('/Users/work/Library/Application Support/MySQL/Workbench/server_instances.xml')
        rootReal = tree.getroot()
        #rootReal[0].insert(0, root)

        #print root.tag
        #build new element

        value = ET.SubElement(rootReal[0],"value")
        value.set('type',"object")
        value.set('struct-checksum',"0x367436e2")
        value.set('id',guid)
        value.set('struct-name',"db.mgmt.ServerInstance")
        link = ET.SubElement(value,'link')
        link.set('type', 'object')
        link.set('key', 'connection')
        link.set('struct-name',"db.mgmt.Connection")
        link.text = serverInstance.connectionId
        loginInfo = ET.SubElement(value,'value')
        loginInfo.set('_ptr_', '0x7ffc3c9d6960')
        loginInfo.set('type', 'dict')
        loginInfo.set('key', 'loginInfo')
        # <value type="string" key="ssh.hostName">172.16.1.128</value>
        sshHostName = ET.SubElement(loginInfo,'value')
        sshHostName.set('type', 'string')
        sshHostName.set('key', 'ssh.hostName')
        sshHostName.text = serverInstance.host
        # <value type="string" key="ssh.key">/Users/work/.ssh/id_rsa</value>
        sshKey = ET.SubElement(loginInfo,'value')
        sshKey.set('type', 'string')
        sshKey.set('key','ssh.key')
        sshKey.text = serverInstance.privateKey
        # <value type="int" key="ssh.useKey">1</value>
        sshUseKey = ET.SubElement(loginInfo,'value')
        sshUseKey.set('type', 'int')
        sshUseKey.set('key', 'ssh.useKey')
        sshUseKey.text = '1'
        #<value type="string" key="ssh.userName">toto</value>
        sshUserName = ET.SubElement(loginInfo,'value')
        sshUserName.set('type','string')
        sshUserName.set('key', 'ssh.userName')
        sshUserName.text = serverInstance.sshUser
        #<value _ptr_="0x7ffc3c9d69c0" type="dict" key="serverInfo">
        serverInfo = ET.SubElement(value,'value')
        serverInfo.set('_ptr_', "0x7ffc3c9d69c0")
        serverInfo.set('type','dict')
        serverInfo.set('key','serverInfo')
        #<value type="string" key="sys.config.path">/etc/my.cnf</value>
        configPath =  ET.SubElement(serverInfo,'value')
        configPath.set('type','string')
        configPath.set('key','sys.config.path')
        configPath.text = serverInstance.mycnfPath
        #<value type="string" key="sys.config.section">mysqld</value>
        configSection =  ET.SubElement(serverInfo,'value')
        configSection.set('type','string')
        configSection.set('key','sys.config.section')
        configSection.text = 'mysqld'
        #<value type="string" key="sys.mysqld.start">systemctl start mysqld</value>
        mysqldStart =  ET.SubElement(serverInfo,'value')
        mysqldStart.set('type','string')
        mysqldStart.set('key','sys.mysqld.start')
        mysqldStart.text = serverInstance.startCommand
        #<value type="string" key="sys.mysqld.stop">systemctl stop mysqld</value>
        mysqldStop =  ET.SubElement(serverInfo,'value')
        mysqldStop.set('type','string')
        mysqldStop.set('key','sys.mysqld.stop')
        mysqldStop.text = serverInstance.stopCommand
        #<value type="string" key="sys.system">Linux</value>
        system = ET.SubElement(serverInfo,'value')
        system.set('type','string')
        system.set('key','sys.system')
        system.text = 'Linux'
        #<value type="int" key="remoteAdmin">1</value>
        remoteAdmin = ET.SubElement(serverInfo,'value')
        remoteAdmin.set('type','int')
        remoteAdmin.set('key', 'remoteAdmin')
        remoteAdmin.text = '1'
        #<value type="int" key="setupPending">1</value>
        setupPending = ET.SubElement(serverInfo,'value')
        setupPending.set('type','int')
        setupPending.set('key', 'setupPending')
        setupPending.text = '1'
        #name
        #<value type="string" key="name">toto</value>
        connectionName = ET.SubElement(value,'value')
        connectionName.set('type','string')
        connectionName.set('key','name')
        
        tempXML = tostring(tree.getroot()) #, method='html')
        tempXML = minidom.parseString(tempXML).toprettyxml(indent='  ')
        tempXML = tempXML.replace('/>', '></value>')
        tempXML = tempXML.replace("\n\n", '')
        tempXML = tempXML.replace('"dict"></value>', '"dict"/>')
        print tempXML
         
    except IOError:
        print ''
    
class ServerInstance:
    filePath       = '/Users/work/'
    instancePath   = ''
    OS             = 'Linux'
    mycnfPath      = ''
    startCommand   = ''
    stopCommand    = ''
    host           = '' 
    sshUser        = ''
    privateKey     = ''
    connectionId   = '5EB33C2B-C940-4374-8087-1696F32B5EB2'
    sudo           = 1
    logPath        = ''
    slowLogPath    = ''
    generalLogPath = ''
    mycnfSection   = 'mysqld'
    basedir        = '/usr'
    datadir        = '/var/lib/mysql'
        
 
def main(argv):
    #user for connection
    user = False
    #password for connection
    password = False
    #database context for connection
    database = False
    #port for connection
    port = 3306
    #host for connection
    host = False
    #path to connections.xml file
    xmlFilePath = '$HOME/.mysql/workbench/connections.xml'
    #connection name displayed in workbench
    name = ''
    #
    sshUser = ''

    try:
        opts, args = getopt.getopt(argv, "u:H:p:l:n:", ["help", "user=", "password=", "database=", "port=", "host=", "name=", "sshuser="])
    except getopt.GetoptError:
        syntaxOptions()
        #if launch without argument
    if len(sys.argv) == 1:
        syntaxOptions()
    for opt, arg in opts:
        if opt in ("-h","--help"):
                syntaxOptions()
        elif opt in ("-u","--user"):
            user = arg
        elif opt in ("-d","--database"):
            database = arg
        elif opt in ("-u","--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-v","--host"):
            host = arg
        elif opt in ("-n","--name"):
             name = arg
        elif opt in ("--sshuser"):
             sshuser = arg
    #check for mandatory option
    if True:
    #if user and isinstance(user, basestring) and password and isinstance(password, basestring) and host and isinstance(host,basestring) and database and isinstance(database,basestring):
        #buildTree(host, user, password, database, port, xmlFilePath, name)
        
        instance = ServerInstance()
        instance.host = host
        instance.instancePath = '/Users/work/Library/Application Support/MySQL/Workbench/server_instances.xml'
        instance.startCommand = 'systemctl start mysqld'
        instance.stopCommand = 'systemctl stop mysqld'
        instance.privateKey = '/Users/work/.ssh/id_rsa'
        instance.mycnfPath = '/etc/my.cnf'
        
        instance.sshUser = sshUser
        
        
        
        buildRemoteManagement(instance)
    else:
        syntaxOptions()

if __name__ == "__main__":
    main(sys.argv[1:])
os._exit(1)
