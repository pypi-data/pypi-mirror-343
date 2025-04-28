from chatgpt_uoapi.backend import ChatGPTAPI

api = ChatGPTAPI()


# If wanna chat in the console
api.chat()


# If wanna make single request
# response = api.make_request('Only provide accurate translation of "Automation make the life a lot easier." in urdu.')
# print(response)