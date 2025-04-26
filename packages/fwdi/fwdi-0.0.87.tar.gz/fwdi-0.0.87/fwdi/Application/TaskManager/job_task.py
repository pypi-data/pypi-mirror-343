from typing import Type, TypeVar
from fwdi.Utilites.waitable_event import WaitableEvents


_T = TypeVar('_T')

class JobTask():
    def __init__(self, fn:callable, args:list) -> None:
        self._fn:callable = fn
        self._args:dict = args
        self._event:WaitableEvents = WaitableEvents()
    
    def get_result(self)->_T:
        if not self._event.result is None:
            return self._event.result
        else:
            return None

    def wait(self)->_T:
        ret, result = self._event.wait()
        return result if ret else None
    
    def __repr__(self):
        return f"fnc:{self._fn}, args:{self._args}"
    
    def __str__(self):
        return f"fnc:{self._fn}, args:{self._args}"