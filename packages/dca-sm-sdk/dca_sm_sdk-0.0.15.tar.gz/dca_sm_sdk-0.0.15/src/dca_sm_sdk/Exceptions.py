
class SM_EXCEPTION(Exception):
    @staticmethod
    def StatusCode():
        return 550


class PathException(SM_EXCEPTION):
    @staticmethod
    def StatusCode():
        return 551

class NotInitStateException(SM_EXCEPTION):

    @staticmethod
    def StatusCode():
        return 552