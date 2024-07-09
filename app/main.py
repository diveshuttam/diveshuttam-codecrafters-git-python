import sys
import os
import zlib
import hashlib

def print(*args, **kwargs):
    # redirect to stderr to avoid mixing logs with data
    kwargs['file'] = sys.stderr
    __builtins__.print(*args, **kwargs) # call the original print

def dprint(*args, **kwargs):
    # print data in a human-readable format
    __builtins__.print(*args, **kwargs)

import struct

def parse_git_tree(data):
    


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        # cat-file -p <hash>
        hash = sys.argv[3]
        print(f"Hash: {hash}")
        with open(f".git/objects/{hash[:2]}/{hash[2:]}", "rb") as f:
            data = getCat(f)
            dprint(data.decode(), end="")
    elif command == "hash-object":
        # hash-object -w <filename>
        filename = sys.argv[3]
        with open(filename, "rb") as f:
            data = f.read()
            # add header to data
            header = f"blob {len(data)}\x00".encode()
            # find hash of data
            hash = hashlib.sha1(header + data).hexdigest()
            # compress data with zlib
            compressed_data = zlib.compress(header + data)
            # write data to file
            os.makedirs(f".git/objects/{hash[:2]}", exist_ok=True)
            with open(f".git/objects/{hash[:2]}/{hash[2:]}", "wb") as f:
                f.write(compressed_data)
            dprint(hash)
    elif command == "ls-tree":
        # --name-only
        hash = sys.argv[3]
        with open(f".git/objects/{hash[:2]}/{hash[2:]}", "rb") as f:
            # decode data with zlib
            data = getCat(f)
            print(data)
            # for entry in parsed_entries:
            #     dprint(entry)
        
    else:
        raise RuntimeError(f"Unknown command #{command}")

def getCat(f):
    data = f.read()
            # decode data with zlib
    data = zlib.decompress(data)
            # skip till \x00
    data = data[data.index(b'\x00')+1:]
    return data


if __name__ == "__main__":
    main()
