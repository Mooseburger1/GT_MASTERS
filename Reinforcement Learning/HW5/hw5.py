import numpy as np

class Kwik:
    def __init__(self, num_of_patrons):
        self.num_of_patrons = num_of_patrons
        self.memory = {}
        self.instigator_list = set(range(self.num_of_patrons))
        self.peacemaker_list = set(range(self.num_of_patrons))
        self.instigator = None
        self.peacemaker = None
        self.solved = False
        self.idn = 0
        
    def scenario(self, patrons, result):
        patrons = tuple(patrons)
        
        #check if we already know who is who
        if self.solved:
            return self.check_solved(patrons)
        #case where we have seen scenario before
        if patrons in self.memory:
            return self.memory[patrons]
        
        #check if we know peacemaker and if he is present
        if self.peacemaker is not None:
            if patrons[self.peacemaker]:
                return self.no_fight()
            
        #case when we haven't seen scenario before
        self.memory[patrons] = int(result)
        solved = self._comprehend(patrons, result)

        if solved == 'solved':
            return self.check_solved(patrons)
        
        if solved == 'no_fight':
            return self.no_fight()
        
        if solved == 'dont_know':
            return -1
#             self.idn+=1
#             print('IDK: ', self.idn)
            
            
    def _comprehend(self, patrons, fight):
        #case when everyone is present
        if all(patrons):
            print('A')
            return 'no_fight'
        
        #case when no one is present
        if all([1 if not x else 0 for x in patrons]):
            print('B')
            return 'no_fight'
        
        #case when one is present and fight and you don't know who instigator is - this person is the instigator
        if fight and np.sum([1 if x else 0 for x in patrons]) == 1 and self.instigator ==None:
            print('C')
            self.instigator = np.argmax(patrons)
            if self.peacemaker is not None:
                self.solved = True
                return 'dont_know'
            self.peacemaker_list.discard(self.instigator)
            if len(self.peacemaker_list) == 1:
                self.peacemaker = self.peacemaker_list.pop()
                self.solved = True
                return 'dont_know'
            
        
            
#         #case when one is present and not fight and you know who peacemaker is
#         if not fight and np.sum([1 if x else 0 for x in patrons]) == 1 and self.peacemaker ==None:
#             self.peacemaker = np.argmax(patrons)
#             if self.instigator is not None:
#                 self.solved = True
#                 return 'dont_know'
#             self.instigator_list.discard(self.peacemaker)
#             if len(self.instigator_list) == 1:
#                 self.instigator = self.instigator_list.pop()
#                 self.solved = True
#                 return 'dont_know'
#             else:
#                 return 'dont_know'
        
        #case when there is a fight and there's only 2 options
        if fight and len(patrons) == 2:
            print('D')
            self.instigator = np.argmax(patrons)
            self.peacemaker = np.argmin(patrons)
            self.solved = True
            return 'dont_know'
           
                
        #case when there isn't a fight and there's only 2 options
        if not fight and len(patrons) == 2:
            print('E')
            self.peacemaker = np.argmax(patrons)
            self.instigator = np.argmin(patrons)
            self.solved = True
            return 'dont_know'
                
        #case when there is a fight and more than two people, remove indices as possible peacemakers
        if fight and self.peacemaker == None:
            print('F')
            not_peacemakers = [pos for pos, x in enumerate(patrons) if x]
            for idx in not_peacemakers:
                self.peacemaker_list.discard(idx)
            
            if len(self.peacemaker_list) == 1:
                self.peacemaker = self.peacemaker_list.pop()
                self.instigator_list.discard(self.peacemaker)
                if len(self.instigator_list) == 1:
                    self.instigator = self.instigator_list.pop()
                if self.instigator != None:
                    self.solved = True
                    return 'dont_know'
                
                
        #case when there is a fight and more than two people, instigator is present, remove non present indices as possible instigators
        if fight and self.instigator == None:
            print('G')
            not_instigators = [pos for pos, x in enumerate(patrons) if not x]
            for idx in not_instigators:
                self.instigator_list.discard(idx)
            
            if len(self.instigator_list) == 1:
                self.instigator = self.instigator_list.pop()
                self.peacemaker_list.discard(self.instigator)
                if len(self.peacemaker_list) == 1:
                    self.peacemaker = self.peacemaker_list.pop()
                if self.peacemaker != None:
                    self.solved = True
                    return 'dont_know'
                
            
            
                
        #case when there isn't a fight and there's only 3 people with 2 present and peacemaker isn't known, peacemaker must be one of the present remove the non present people
        if not fight and self.peacemaker == None and len(patrons) == 3 and np.sum(patrons)==2:
            print('H')
            not_peacemakers = [pos for pos, x in enumerate(patrons) if not x]
            for idx in not_peacemakers:
                self.peacemaker_list.discard(idx)
                
            if len(self.peacemaker_list) == 1:
                self.peacemaker = self.peacemaker_list.pop()
                self.instigator_list.discard(self.peacemaker)
                if len(self.instigator_list) == 1:
                    self.instigator = self.instigator_list.pop()
                if self.instigator != None:
                    self.solved = True
                    return 'dont_know'
                
                
        #case when there isn't a fight and instigator isn't known and peacemaker isn't known and there's all present except 1 - that one can't be peacemaker
        if not fight and self.instigator == None and self.peacemaker == None and len(patrons) >2 and (len(patrons)-1) == np.sum(patrons):
            print('I')
            not_peacemaker = np.argmin(patrons)
            self.peacemaker_list.discard(not_peacemaker)
                
            if len(self.peacemaker_list) == 1:
                self.peacemaker = self.peacemaker_list.pop()
                self.instigator_list.discard(self.peacemaker)
                if len(self.instigator_list) == 1:
                    self.instigator = self.instigator_list.pop()
                if self.peacemaker != None:
                    self.solved=True
                    return 'dont_know'
                
                
        #case when instigator is known and present and and not fight is the response - peacemaker is present, drop indices of not present
        if not fight and self.instigator != None and patrons[self.instigator] == 1:
            print('J')
            not_peacemakers = [pos for pos, x in enumerate(patrons) if not x]
            for idx in not_peacemakers:
                self.peacemaker_list.discard(idx)
                
            if len(self.peacemaker_list) == 1:
                self.peacemaker = self.peacemaker_list.pop()
                self.instigator_list.discard(self.peacemaker)
                if len(self.instigator_list) == 1:
                    self.instigator = self.instigator_list.pop()
                if self.instigator != None:
                    self.solved = True
                    return 'dont_know'
                
                
        #case when only 1 present and no fight - can't be instigator
        if not fight and self.instigator == None and np.sum(patrons) == 1:
            print('K')
            not_instigators = np.argmax(patrons)
            self.instigator_list.discard(not_instigators)
            
            if len(self.instigator_list) == 1:
                self.instigator = self.instigator_list.pop()
                self.peacemaker_list.discard(self.instigator)
                if len(self.peacemaker_list) == 1:
                    self.peacemaker = self.peacemaker_list.pop()
                if self.peacemaker != None:
                    self.solved = True
                    return 'dont_know'
                
            
        
        
        return 'dont_know'
           
            
    def no_fight(self):
        return 0
    
    def yes_fight(self):
        return 1
        
    
    def check_solved(self, patrons):

        if patrons[self.peacemaker] == True:
            
            return self.no_fight()
        
        if patrons[self.instigator] == True:

            return self.yes_fight()
        
        self.no_fight()
            