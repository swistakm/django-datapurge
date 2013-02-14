# -*- coding: utf-8 -*-
class BaseDatapurgeException(BaseException):
    """Base datapurge app exception"""

class AmbiguousSettingsError(BaseException):
    """ Raises when datapurge settings appear to be ambiguous
    """