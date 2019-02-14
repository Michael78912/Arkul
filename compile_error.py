"""class for errors caused at compile time."""

class CompileError(Exception):
    def __init__(self, details, lineno=0):
        self.details = details
        super().__init__(details)
        self.lineno = lineno
    
    def get_message(self):
        """return message based on context"""
        if self.lineno:
            return "Compilation error at line %d: %s" % (self.lineno, self.details)
        else:
            return "Compilation error: " + self.details
    
    