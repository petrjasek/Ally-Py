'''
Created on Nov 14, 2012

@package: gateway
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the setup files for gateway.
'''

# --------------------------------------------------------------------

NAME = 'gateway'
GROUP = 'gateway'
VERSION = '1.0'
DESCRIPTION = \
'''
This plugin provides the default gateway service. 
'''
INSTALL_REQUIRES = ['support-sqlalchemy>=1.0']
LONG_DESCRIPTION = '''This plugin provides the Gateway API and also the means of setting up custom gateways, for instance allowing for a certain IP full access to REST models. The gateway plugin is agnostic to the actual services that are published by the REST server and any type of URLs and rules can be placed with this plugin.'''