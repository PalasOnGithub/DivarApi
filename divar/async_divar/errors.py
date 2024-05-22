class invalid_url(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class empty_pagination(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class invalid_header(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class rpc_error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class invalid_auth(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

