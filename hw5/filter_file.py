def filter_file(file, wordlist: list[str]):
    if not isinstance(wordlist, list):
        raise TypeError("wordlist must be a list")
    if any([not isinstance(i, str) for i in wordlist]):
        raise ValueError("wordlist must contain only str values")
    f = None
    if hasattr(file, 'readable'):
        if file.readable:
            f = file
    elif isinstance(file, str):
        f = open(file, "r")
    else:
        raise TypeError("test_file must be a valid test_file or filename")
    for line in f:
        if any([word in line.lower().split() for word in map(lambda x: x.lower(), wordlist)]):
            yield line.removesuffix('\n')
