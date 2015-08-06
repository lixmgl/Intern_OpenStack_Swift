import ConfigParser

class Parse(object):    
    """  Class to parse config file"""
    def __init__(self, file): 
        self.file = file 
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(self.file)

    def get_section(self, section):
        """Returns a section of the config file""" 
        section_list = []
        data = self.Config.items(section) 
        for line in data:
            section_list.append(line)
        return section_list
        
    def get_value(self, section, value):
        """Returns a specific value"""
        i = 0
        section_list = self.get_section(section)
        while i < len(section_list):
            if section_list[i][0] == value:
                return section_list[i][1]
            i += 1