import traceback
import time

class Debugger():
    def __init__(self,debug = False,path=None) -> None:
        self.debug = debug
        self.path = path
        if path is not None:
            self.logfile = open(path, "a")
    
    def turn_debugger_on(self):
        self.debug = True
        self.logfile = open(self.path, "a")

    def logger(self,message,state="DEBUG"):
        if self.debug:
            if self.path is None:
                print(f"[{state}] {message}")
            else:
                self.logfile.write(f"[{state}] {message}\n")
                self.logfile.flush()

    def trace_func(self,func):
        def wrapper(*args, **kwargs):
            self.logger(f"Calling {func.__name__} with args: {[type(i) for i in args]}, kwargs: {[type(i) for i in kwargs]}",state="FUNC_CALL")
            start_time = time.time()
            try:
                out = func(*args, **kwargs)
            except Exception as e:
                self.logger(f"{func.__name__} Exception:{e}",state="ERROR")
                self.logger(traceback.format_exc(), state="TRACEBACK")
                raise
            name = f"{args[0].__class__.__name__}.__init__" if func.__name__ == "__init__" else func.__name__
            self.logger(f"{name} returned: {type(out)} with shape/info: {getattr(out, 'shape', 'uk')}, {getattr(out, 'dtype', 'uk')}, Time taken:{time.time()-start_time}s",state="FUNC_RETURN")
            return out
        return wrapper

debug_state = Debugger()