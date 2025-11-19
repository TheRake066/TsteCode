from InquirerPy import prompt

result = prompt(
    {"message": "Confirm order?", "type": "confirm", "default": False},
    style={"questionmark": "#ff9d00 bold"},
    vi_mode=True,
    style_override=False,
)
