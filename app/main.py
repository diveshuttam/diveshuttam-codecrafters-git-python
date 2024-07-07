import sys
import os

def print(*args, **kwargs):
    # redirect to stderr to avoid mixing logs with data
    kwargs['file'] = sys.stderr
    __builtins__.print(*args, **kwargs) # call the original print

def dprint(data):
    # print data in a human-readable format
    print(data)


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
            data = f.read()
            # find the encoding of the data
            print(data)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
