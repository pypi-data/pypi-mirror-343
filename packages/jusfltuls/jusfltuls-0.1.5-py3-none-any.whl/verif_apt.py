import subprocess as sp

def main():
    print("Hello from verify!")

    ok = True
    CMD = ['/usr/bin/which','uconv']
    result = sp.run( CMD, capture_output=True, text=True )
    if result.returncode != 0:
        print("!... uconv not found... apt install icu-devtools")
        ok = False
    else:
        print("i... uconv found")

    #print()


if __name__ == "__main__":
    main()
