import functions
############### Test zone #########################
class request():
    def __init__(self):
        self.args = {}
        self.args["event"] = "User enrolled in course"
request = request()
res = functions.statbyComponent(request)
print(res)