''' credentials_connection.py '''
class User():

    def __init__(self, user):
        self.user = user

    def showUser(self):
        print(self.user)

    def getCredentials(self):
        import json
        credentials_file = open(".credentials.json")
        credentials = json.load(credentials_file)
        try:
            self.userName = credentials[self.user]['user']
            self.password = credentials[self.user]['password']
            self.token = credentials[self.user]['token']

        except Exception as e:
            print(str(e), " Invalid user")
        
    def sf_login(self):
        from simple_salesforce import Salesforce
        self.sf = Salesforce(username=self.userName, password=self.password,
                security_token=self.token)
        return self.sf
