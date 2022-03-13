import os
import sys

def main() -> None:

    path = determinCwd()
    data = getFileData(path)
    entries = getEntries(data)
    verifyFile(entries)
    entries = entries[1:]

    entry_dict = processEntryData(entries)

    for k, v in entry_dict.items():
        print(f"{k}: {v}")


def determinCwd() -> str:

    try:
        os.chdir(os.getcwd() + '/' + sys.argv[1])
        path = os.getcwd()
    except IndexError:
        path = os.getcwd()

    return path

def getFileData(path: str) -> str:

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    sample_files = [f for f in files if "samples2" in f[-8:]]

    if len(sample_files) > 1:
        print(f"Multiple files found:")
        for f in sample_files:
            print(f"    {f}")
        print(f"\nPlease Specify:")

        untested_file = input()

        while(not os.path.isfile(untested_file)):
            print(f"File Not found")
            untested_file = input()

        file = untested_file

    else:
        file = sample_files[0]

    with open(path+'/'+file, 'rb') as f:
        data = f.read()

    return data

def verifyFile(entries: list[bytes]) -> None:

    num_of_entries = int.from_bytes(entries[0], byteorder='big', signed=True)
    len_of_entries = len(entries) - 1

    if not num_of_entries == len_of_entries:
        exit_msg = f"""
        File header did not match:

            Got: {entries[-1]} = {num_of_entries}
            Expected: {len_of_entries}

        Exiting
        """
        quit(exit_msg)

def getEntries(data: bytes) -> list[bytes]:

    entries = []
    entries.append(data[:4])

    data = data[12:]

    for e in range(int.from_bytes(entries[0], byteorder='big', signed=True)):
        len_of_text = int.from_bytes(data[8:10], byteorder='big', signed=False)
        len_of_entry = 10 + len_of_text

        entries.append(data[:len_of_entry])

        data = data[len_of_entry+8:]

    return entries

def processEntryData(entries: list[bytes]) -> dict:
    
    p_entries = {}
    i = 0

    for b in entries:
        p_entries[f"e{i}"] = {}
        p_entries[f"e{i}"]["text"] = b[10:].decode('ascii')

        p_entries[f"e{i}"]["x"] = int.from_bytes(b[:4], byteorder='big', signed=True)
        #print(b[:4])
        p_entries[f"e{i}"]["z"] = int.from_bytes(b[4:8], byteorder='big', signed=True)
        #print(f"{b[4:9]}\n")
        i += 1

    return p_entries

if __name__ == "__main__":
    main()