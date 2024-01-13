class Set:
    def __init__(self, name, teacher):
        self.setName = name
        self.setTeacher = teacher
        
    def sayTeacher(self):
        print(self.setTeacher)

mf2 = Set("13mf2", "ray healy")
mf2.sayTeacher()

##############################################################################################################################################

class PasswordManager:
    def __init__ (self,masterUsername,masterPassword,loginSystem):
        self.username = masterUsername
        self.password = masterPassword
        self.loginSystem = loginSystem