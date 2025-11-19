from InquirerPy import inquirer

name = inquirer.text(message="qual é seu nome?").execute()
fav_lang = inquirer.select(
    message="qual é a sua linguagem favorita:",
    choices=["Go", "Python", "Rust", "JavaScript"],
).execute()
confirm = inquirer.confirm(message="Tem certeza?").execute()

print(name, fav_lang, confirm)

