def fmt(amount: float) -> str:
    """Formats the amount as money, including two decimal places and thousands separator."""
    return '{:,.2f}'.format(amount)

def fmt_with_currency(amount: float, currency: str) -> str:
    """Formats the amount as money, including two decimal places and thousands separator, and adds the currency symbol."""
    return f'{currency} {fmt(amount)}'

