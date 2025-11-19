from InquirerPy import inquirer

keybindings = {
    "skip": [{"key": "c-c"}],
    "interrupt": [{"key": "c-d"}],
    "toggle-all": [{"key": ["c-a", "space"]}],
}

result = inquirer.select(
    message="Select one:",
    choices=["Fruit", "Meat", "Drinks", "Vegetable"],
    keybindings=keybindings,
    multiselect=True
).execute()
