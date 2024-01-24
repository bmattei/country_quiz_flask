def format_number(number):
    if number < 1_000_000:
        return str(number)
    else:
        return f'{number / 1_000_000:.2f} Million'