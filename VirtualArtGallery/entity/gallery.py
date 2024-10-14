class Gallery:
    def __init__(self,galleryId,name,description,location,curator,openingHours):
        self.galleryId = galleryId
        self.name = name
        self.description = description
        self.location = location
        self.curator = curator
        self.openingHours = openingHours
    #Setters

    def set_galleryId(self,galleryId):
        self.galleryId = galleryId
    def set_name(self,name):
        self.name = name
    def set_description(self,description):
        self.description = description
    def set_location(self,location):
        self.location = location
    def set_curator(self,curator):
        self.curator = curator
    def set_openingHours(self,openingHours):
        self.openingHours = openingHours


    #Getters

    def get_galleryId(self):
        return self.galleryId
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_location(self):
        return self.location
    def get_curator(self):
        return self.curator
    def get_openingHours(self):
        return self.openingHours
    
