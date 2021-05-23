import functions
############### Test zone #########################
class request():
    def __init__(self):
        self.args = {}
        self.args["id"] = "187IT23616"

query = "component=File"
print(functions.statbyComponent(query))