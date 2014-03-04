'''
Created on Oct 9, 2013

@package: ally http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Special module that is used in application deploy.
'''

import logging
from os import path, makedirs
from uuid import uuid4

from ally.container import ioc, support, context, deploy
from ally_start import options, parser

from ..ally.deploy import FLAG_START, saveConfigurations, prepareActions
from ..ally_http.server import server_port, server_type
from .server import send_spec, send_ident, recv_spec, recv_ident
import ally_start


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

FLAG_CONFIG_MONGREL2 = 'configMongrel2'
# Flag indicating the management of full access IPs.

# --------------------------------------------------------------------

@ioc.after(prepareActions)
def prepareMongrel2Actions():
    
    options.mongrel2Folder = None
    options.registerFlag(FLAG_CONFIG_MONGREL2, FLAG_START)
    options.registerFlagLink('mongrel2Folder', FLAG_CONFIG_MONGREL2)
    
    parser.add_argument('-cfg-mongrel2', metavar='folder', dest='mongrel2Folder', nargs='?',
                        help='Provide this option to create the mongrel2 workspace, by default the mongrel2 '
                        'workspace will be created by default in "workspace" in the application folder, '
                        'just provide a new mongrel2 workspace if thats the case, the path can be relative to '
                        'the application folder or absolute')

# --------------------------------------------------------------------

@deploy.start
def configureMongrel2():
    if not options.isFlag(FLAG_CONFIG_MONGREL2): return
    workspace = ally_start.options.mongrel2Folder or 'workspace'
    folders = [path.join('mongrel2', name) for name in ('logs', 'run', 'tmp')]
    folders.append(path.join('shared', 'upload'))

    for name in folders:
        folder = path.join(workspace, name)
        if not path.isdir(folder): makedirs(folder)
    
    updateConfig = False
    if server_type() != 'mongrel2':
        updateConfig = True
        support.persist(server_type, 'mongrel2')
    
    sendIdent = send_ident()
    if sendIdent is None:
        updateConfig = True
        sendIdent = str(uuid4())
        support.persist(send_ident, sendIdent)

    if updateConfig: saveConfigurations(context.configurationsExtract())
    
    # Writing ally.conf
    with open(path.join(workspace, 'ally.conf'), 'w') as f: 
        print(
'''
# --------------------------------------------------------------------------------------
# Sample configuration for Mongrel2 and ally-py
# load this file in linux by using: m2sh load -config ally.conf
# start mongrle2 in linux by using: m2sh start -host localhost
# Attention!!! Do not use '_' in any of the values that you place in *_spec or *_ident 
# --------------------------------------------------------------------------------------
''', file=f)
        print(
'''
server_main = Handler(send_spec='%s', send_ident='%s', recv_spec='%s', recv_ident='%s', protocol='tnetstring')
''' % (send_spec(), sendIdent, recv_spec(), recv_ident()), file=f)
    
        try:
            from ..ally_core_http.server import root_uri_resources
            routes = '\'%s\': server_main' % (root_uri_resources()  or '/')
        except ImportError: routes = '\'/\': server_main'
    
        try:
            from ..ally_cdm.server import server_provide_content, root_uri_content
            isContent = server_provide_content()
        except ImportError: isContent = False
        if isContent:
            routes = '%s, \'%s\': server_cdm' % (routes, root_uri_content() or '/')
            print(
'''
server_cdm = Dir(base='shared/cdm/', index_file='index.html', default_ctype='text/plain')
''', file=f)
    
        print(
'''
# Main host
mongrel2 = Host(name="localhost", routes={%s})

# The server to run them all
main = Server(
    uuid="2f62bd5-9e59-49cd-993c-3b6013c28f05",
    chroot="./",
    access_log="/mongrel2/logs/access.log",
    error_log="/mongrel2/logs/error.log",
    pid_file="/mongrel2/run/mongrel2.pid",
    default_host="localhost",
    name="main",
    port=%s,
    hosts=[mongrel2]
)

settings = {'zeromq.threads': 1, 'upload.temp_store': 'shared/upload/upload.XXXXXX', 'upload.temp_store_mode': '0666'}

servers = [main]
''' % (routes, server_port()), file=f)
    
    # Writing README-Mongrel2.txt
    with open(path.join(workspace, 'README-Mongrel2.txt'), 'w') as f:
        print(
'''
IMPORTANT NOTE: We currently recommend the installation of Live Desk with Mongrel2 only for advanced users, i.e. people who
are well versed in server administration.

The ZeroMQ library is not part of the ally-py distribution like SQLAlchemy for instance, this is because ZeroMQ uses native
coding that needs to be compiled. So the first steps in using the ZeroMQ and Mongrel2 servers are the installation of these
tools. The described installations steps have been made on Ubuntu 12.04 but they should work fine on any Debian based
distributions.

Installing ZeroMQ
-----------------------------------------------------------------------------------------------

First we fetch the zeromg POSIX tarball, you can access "http://www.zeromq.org/intro:get-the-software" and download the 
POSIX tarball or:
    wget http://download.zeromq.org/zeromq-3.2.3.tar.gz

The we insall the zeromq:
    tar -xzvf zeromq-3.2.3.tar.gz
    cd zeromq-3.2.3/
    ./configure 
    make
    sudo make install

Installing Mongrel2
-----------------------------------------------------------------------------------------------
    
Now we have the zeromq installed, we need now sqlite3 for Mongrel2 web server, this is in case you do not have it installed
already, attention you need also the dev version:
    sudo apt-get install sqlite3
    sudo apt-get install libsqlite3-dev
    
We install now the Mongrel2 web server, you can also check the steps at "http://mongrel2.org/wiki/quick_start.html":
    wget https://github.com/zedshaw/mongrel2/tarball/v1.8.0
    mv v1.8.0 mongrel2-1.8.0.tar.gz
    tar -xzvf mongrel2-1.8.0.tar.gz
    cd zedshaw-mongrel2-bc721eb
    make clean all
    sudo make install
We will continue with Mongrel2 latter on.

Installing pyzmq
-----------------------------------------------------------------------------------------------
    
You also need a python3.2:
    sudo apt-get install python3
    sudo apt-get install python3-dev
    
You also need the python setup tools if you don't have them:
    sudo apt-get install python3-setuptools
    
After this we just easy install pyzmq:
    sudo easy_install3 pyzmq
When I installed pyzmq I get an error at the end:

    File "/usr/local/lib/python3.2/dist-packages/pyzmq-2.2.0.1-py3.2-linux-x86_64.egg/zmq/green/core.py", line 117
        except gevent.Timeout, t:
                             ^
    SyntaxError: invalid syntax
    
just ignore this.

Configuring superdesk
-----------------------------------------------------------------------------------------------

 We consider that you already have an ally-py distribution so we whon't got through the
steps of getting the superdesk. We consider the path for superdesk distribution as being:
    "../rest_api/superdesk/distribution"

Let use the distribution as the root folder.
    cd ../rest_api/superdesk/distribution

First we create the configuration (properties) files for superdesk:
    python3 application.py -dump
We now have in the distribution folder two new files "application.properties" and "plugin.properties", we need to adjust some
configurations here.

Now we tell ally-py to prepare the workspace for Mongrel2:
    python3 application.py -cfg-mongrel2
This will create the required folders and update the configurations accordingly

Starting Mongrel2
-----------------------------------------------------------------------------------------------

Change the root directory to the distribution workspace:
    cd workspace

Now we configure Mongrel2:
    m2sh load -config ally.conf

And then start Mongrel2:
    m2sh start -host localhost

Starting SuperDesk
-----------------------------------------------------------------------------------------------

Open a new terminal and move to distribution:
    cd ../rest_api/superdesk/distribution

And then start the application (-OO is for production mode):
    python3 -OO application.py
    
If defaults are used this will start the ally py application using an in processor communication protocol, the application
is single threaded and will only consume on processor from the machine, in order to add more instances that are load
balanced by ZeromMQ you just need to start the application again, but before this we need to adjust some configurations
in order to avoid unnecessary operations that are done by ally-py.
So we will call the started application as being the main application and the next applications that we will start we call
them as being support application.

Creating support application configurations
-----------------------------------------------------------------------------------------------

So we already have the "application.properties" and "plugins.properties" from the main application:
Open a new terminal and move to distribution:
    cd ../rest_api/superdesk/distribution
we just need to create copies for the support application:
    cp application.properties application_support.properties
    cp plugins.properties plugins_support.properties

Now we need to adjust the "application_support.properties", change the following configurations to:
    configurations_file_path: plugins_support.properties

And in "plugins_support.properties", change the following configurations to:
    publish_gui_resources: false
this is to prevent the unnecessary publication of client files again by the support applications
    perform_cleanup: false
this prevents the superdesk authorization to clean the expired sessions and login tokens by the support applications

Starting support SuperDesk
-----------------------------------------------------------------------------------------------

Now simply start the application (-OO is for production mode):
    python3 -OO application.py --ccfg application_support.properties

You can start now as many support applications as you need but you should keep this number less or equal with the number
of CPUs that the computer has.
''', file=f)
        
    log.info('Configured \'%s\' mongrel2 workspace' % folder)
