'''
A simple class to hold the state of the thermal control machine.
This is *NOT* a full blow state machine class
'''
class MachineState:
    
    def __init__(self):
        self.states = ('Off', 'Preheating', 'Heating')
        self.currentState = self.states[0]
        
    def changeState(self, state):
        if state in self.states:
            self.currentState = self.states.index(state)
        else:
            raise Exception('State of {0} not a member of the allowable states')

    def getCurrentState(self):
        return self.states[self.currentState]
    
    #TODO:  work out what parameters are needed to determine if the state should change
    def getNextState(self):
        pass
    