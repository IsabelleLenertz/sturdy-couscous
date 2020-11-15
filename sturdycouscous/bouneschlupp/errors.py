class BadResponseError(Exception):
    """ Exception raised for non-200 http(s) request reponses 

    Attributes:
        response_code -- the response code
    """

    def __init__(self, response_code):
        self.response_code = response_code