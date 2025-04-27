from src.pyregister2 import *

if __name__ == "__main__":
    batch = RegisterBatch()

    batch.read("RAX")

    batch.execute_to_global()

    batch.add("EBX", RAX)

    batch.dec("EBX")

    batch.read("EBX")

    batch.execute_to_global()

    batch.sub("RAX", EBX)

    batch.xchg("RAX", "EBX")

    batch.execute_to_global()

    batch.shl("RAX", EBX)

    batch.execute_to_global()

    batch.xor("EBX", RAX)

    batch.read("EBX")
    batch.read("RAX")

    batch.execute_to_global()

    print(RAX)
    print(EBX)