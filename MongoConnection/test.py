import functions
############### Test zone #########################
class request():
    def __init__(self):
        self.args = {}
        self.args["id"] = "187IT23616"

query = "id=197PM33774&component=System"
print(functions.findbyAttr(query))