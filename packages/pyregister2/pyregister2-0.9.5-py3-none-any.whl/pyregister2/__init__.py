import os  
import ctypes  
import sys  
import platform  

# Diretórios base e bin, calculados a partir deste arquivo
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta src/pyregister  
_BIN_DIR  = os.path.join(_BASE_DIR, "bin")             # src/pyregister/bin  

class RegisterBatch:
    def __init__(self):
        # Escolhe o nome correto da biblioteca nativa
        if platform.system() == "Windows":
            lib_name = "pyregister.dll"
        else:
            lib_name = "libpyregister.so"

        # Monta o caminho completo
        LibPath = os.path.join(_BIN_DIR, lib_name)
        if not os.path.exists(LibPath):
            raise FileNotFoundError(f"Bin not found: '{LibPath}'")  # :contentReference[oaicite:0]{index=0}

        # Carrega a DLL ou .so
        self._dll = ctypes.CDLL(LibPath)  # :contentReference[oaicite:1]{index=1}
        # Define assinaturas (argtypes/restype) para segurança
        self._dll.read_register.argtypes  = [ctypes.c_char_p]
        self._dll.read_register.restype   = None
        self._dll.write_register.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
        self._dll.write_register.restype  = None
        self._dll.execute.argtypes        = []
        self._dll.execute.restype         = ctypes.c_char_p

    def write(self, reg: str, val: int):
        """Escreve valor em registrador via DLL."""
        self._dll.write_register(reg.encode('ascii'), ctypes.c_uint32(val))

    def read(self, reg: str):
        """Dispara leitura de registrador (resultado ficará em buffer interno)."""
        self._dll.read_register(reg.encode('ascii'))

    def execute(self) -> dict:
        """Executa a leitura pendente e retorna dict {registrador: valor}."""
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

    def execute_to_global(self):
        """Roda execute() e injeta resultados no namespace global de main."""
        data = self.execute()
        main_mod = sys.modules['__main__']
        main_mod.__dict__.update(data)

# Expõe publicamente somente RegisterBatch
__all__ = ["RegisterBatch"]