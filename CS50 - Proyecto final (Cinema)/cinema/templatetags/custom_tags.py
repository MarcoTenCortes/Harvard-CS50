from django import template

register = template.Library()

@register.simple_tag
def concat_row_as_letter_and_seat(row, seat_number):
    """Converts the row number to a letter and concatenates with the seat number."""
    # Convert row number to corresponding letter (1 -> A, 2 -> B, etc.)
    row_letter = chr(64 + row)  # 64 + 1 = 65 -> 'A'
    return f"{row_letter}{seat_number}"
