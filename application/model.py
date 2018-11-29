

class User:
    def __init__(self, id, firstname, lastname, othername, email, phonenumber, username, registered, isAdmin):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.email= email
        self.phonenumber = phonenumber
        self.username = username
        self.registered = registered
        self.isAdmin = isAdmin


class Incident:
    def __init__(self, id, createdOn, createdBy, incident_type, location, status, comment):
        self.id = id
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.incident_type = incident_type
        self.location = location
        self.status = status
        self.comment = comment


