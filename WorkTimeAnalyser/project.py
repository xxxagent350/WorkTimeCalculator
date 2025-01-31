
class Project:
    def __init__(self, project_name, project_path, ignore = False):
        self.delta_time = 0
        self.project_name = project_name
        self.project_path = project_path
        self.ignore = ignore
