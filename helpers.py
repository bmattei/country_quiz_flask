def format_number(number):
    inum = int(number) # User can pass a string or a int
    if inum < 1_000_000:
        return str(inum)
    else:
        return f'{inum / 1_000_000:.2f} Million'