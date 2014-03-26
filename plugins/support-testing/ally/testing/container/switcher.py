'''
Created on Mar 24, 2014

@package: support testing
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database switcher.
'''

from ally.container._impl._assembly import Assembly, Setup
from ally.container._impl._setup import SetupFunction, register, SetupSource
from ally.container.error import SetupError
from ally.support.util_sys import callerLocals
from ally.container._impl._call import WithCall


# --------------------------------------------------------------------
class Switcher:
    ''' Provides the switching mechanism for ioc.'''
    
    def __init__(self):
        self.isMain = True
        
    def switch(self, main):
        '''
        Decorator for main setup functions that provides the switch between the target setup function
        and decorated function.
        
        @param main: SetupFunction
            The setup function to be the main switched setup.
        '''
        assert isinstance(main, SetupFunction), 'Invalid setup main %s' % main
        def decorator(alternate):
            assert isinstance(alternate, SetupFunction), 'Invalid setup alternate %s' % alternate
            register(SetupSwitcher(self, main, alternate), callerLocals())
            return alternate
        return decorator
    
    def switchCall(self, main, alternate):
        '''
        Creates a call that invokes wither main or alternate based on the witcher.
        
        @param main: callable
            The main call.
        @param alternate: callable
            The alternate call.
        '''
        assert callable(main), 'Invalid main call %s' % main
        assert callable(alternate), 'Invalid alternate call %s' % alternate
        def switched(*args, **keyargs):
            if self.isMain: return main(*args, **keyargs)
            return alternate(*args, **keyargs)
        return switched

    # ----------------------------------------------------------------
    
    def switchToMain(self):
        ''' Switches to main database.'''
        self.isMain = True
    
    def switchToAlternate(self):
        ''' Switches to alternate database.'''
        self.isMain = False

# --------------------------------------------------------------------

class CallSwitcher(WithCall):
    '''
    Call that provides data based on switcher.
    '''

    def __init__(self, switcher, main, alternate):
        assert isinstance(switcher, Switcher), 'Invalid switcher %s' % switcher
        assert callable(alternate), 'Invalid alternate call %s' % alternate
        WithCall.__init__(self, main)
        
        self.switcher = switcher
        self.alternate = alternate

    def __call__(self):
        '''
        Provides the call for the entity.
        '''
        if self.switcher.isMain: return self.call()
        return self.alternate()

class SetupSwitcher(Setup):
    '''
    Provides the setup for switching event setup function.
    '''
    priority_assemble = 100

    def __init__(self, switcher, main, alternate):
        assert isinstance(switcher, Switcher), 'Invalid switcher %s' % switcher
        assert isinstance(main, SetupSource), 'Invalid main setup %s' % main
        assert isinstance(alternate, SetupSource), 'Invalid alternate setup %s' % alternate
        
        self.switcher = switcher
        self.main = main
        self.alternate = alternate

    def assemble(self, assembly):
        '''
        @see: Setup.assemble
        '''
        assert isinstance(assembly, Assembly), 'Invalid assembly %s' % assembly
        if self.main.name not in assembly.calls:
            raise SetupError('There is no setup main call for name \'%s\' to be switched by:%s' % 
                             (self.main.name, self.alternate))
        if self.alternate.name not in assembly.calls:
            raise SetupError('There is no setup alternate call for name \'%s\' to be switched for:%s' % 
                             (self.alternate.name, self.main))
        assembly.calls[self.main.name] = CallSwitcher(self.switcher, assembly.calls[self.main.name],
                                                      assembly.calls[self.alternate.name])
        
    def __str__(self):
        return '%s switch %s' % (self.main, self.alternate)
