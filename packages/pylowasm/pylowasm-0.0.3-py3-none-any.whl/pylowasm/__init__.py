import os  
import ctypes  
import sys  
import platform  

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_BIN_DIR  = os.path.join(_BASE_DIR, "bin")

class RegisterBatch:
    def __init__(self):
        # Escolhe o nome correto da biblioteca nativa
        if platform.system() == "Windows":
            if sys.maxsize > 2**32:
                lib_name = "./64/pyregister.dll"
            else:
                lib_name = "./32/pyregister.dll"
        else:
            if sys.maxsize > 2**32:
                lib_name = "./64/libpyregister.so"
            else:
                lib_name = "./32/libpyregister.so"

        LibPath = os.path.join(_BIN_DIR, lib_name)
        if not os.path.exists(LibPath):
            raise FileNotFoundError(f"Bin not found: '{LibPath}'")

        self._dll = ctypes.CDLL(LibPath)

        self._dll.read_register.argtypes  = [ctypes.c_char_p]
        self._dll.read_register.restype   = None
        self._dll.write_register.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        self._dll.write_register.restype  = None
        self._dll.syscall.argtypes = []
        self._dll.syscall.restype  = None
        self._dll._int.argtypes = [ctypes.c_uint64]
        self._dll._int.restype  = None
        self._dll.execute.argtypes        = []
        self._dll.execute.restype         = ctypes.c_char_p

        self.rflag = None

    def write(self, reg: str, val: int) -> None:
        self._dll.write_register(reg.encode('ascii'), ctypes.c_uint32(val))

    def read(self, reg: str) -> None:
        self._dll.read_register(reg.encode('ascii'))
    
    def syscall(self) -> None:
        self._dll.syscall()
    
    def _int(self, val: int) -> None:
        self._dll._int(ctypes.c_uint64(val))
    
    def xchg(self, reg1: str, reg2: str) -> None:
        self.read(reg1)
        self.read(reg2)

        _exec = self.execute()

        self.write(reg1, _exec[reg2])
        self.write(reg2, _exec[reg1])
    
    def add(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] + val)

    def sub(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] - val)
    
    def mul(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] * val)
    
    def xor(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] ^ val)
    
    def _or(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] | val)
    
    def _and(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] & val)
    
    def shl(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] << val)
    
    def shr(self, reg: str, val: int) -> None:
        self.read(reg)

        self.write(reg, self.execute()[reg] >> val)
    
    def cmp(self, reg: str, val: int) -> None:
        self.read(reg)

        if self.execute()[reg] == val:
            self.rflag = True
        else:
            self.rflag = False
    
    def _not(self, reg: str) -> None:
        self.read(reg)

        self.write(reg, ~self.execute()[reg])
    
    def inc(self, reg: str) -> None:
        self.add(reg, 1)
    
    def dec(self, reg: str) -> None:
        self.sub(reg, 1)
    
    def neg(self, reg: str) -> None:
        self.read(reg)

        self.write(reg, -self.execute()[reg])

    def execute(self) -> dict:
        raw = self._dll.execute()
        if not raw:
            return {}
        text = raw.decode('ascii')
        parts = [p for p in text.split("[,013.,45gsd]") if p]
        res = {}
        for part in parts:
            r, v = part.split("[:567:]")
            res[r] = int(v)
        return res

    def execute_to_global(self) -> None:
        data = self.execute()
        main_mod = sys.modules['__main__']
        main_mod.__dict__.update(data)

__all__ = ["RegisterBatch"]