from utils.api_utils import ApiUtils


class BaseHelper:
    ROOT_ENDPOINT = None

    def __init__(self, api_utils: ApiUtils):
        self.api_utils = api_utils
