class ErrorLog:
    def __init__(self, methode: str, error: Exception, message: str, inputs: []):
        """
        log an error that occured during the testing of the code
        :param methode: what method had been used to break the code
        :param error: the exception / error that was generated
        :param message: the message / hint associated with the function
        :param inputs: the potentials input that made the function break
        """
        self.methode = methode
        self.error = error
        self.message = message
        self.inputs = inputs
        pass
