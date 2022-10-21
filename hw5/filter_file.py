def filter_file(file, wordlist: list[str]):
    if not isinstance(wordlist, list):
        raise TypeError("wordlist must be a list")
    if any(not isinstance(i, str) for i in wordlist):
        raise ValueError("wordlist must contain only str values")
    if hasattr(file, "readable"):
        if not file.readable:
            raise ValueError("Given file does not allow reading")
        for line in file:
            if any(
                word in line.lower().split()
                for word in map(lambda x: x.lower(), wordlist)
            ):
                yield line.removesuffix("\n")
    elif isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_instance:
            for line in file_instance:
                if any(
                    word in line.lower().split()
                    for word in map(lambda x: x.lower(), wordlist)
                ):
                    yield line.removesuffix("\n")
    else:
        raise TypeError("test_file must be a valid test_file or filename")
