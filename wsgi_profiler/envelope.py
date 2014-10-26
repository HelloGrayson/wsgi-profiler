
class Envelope(object):

    def __init__(self, profile, elapsed, request_path, request_method):

        self.profile = profile
        self.elapsed = elapsed
        self.request_path = request_path
        self.request_method = request_method
