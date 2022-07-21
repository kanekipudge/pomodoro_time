from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pas():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_symbols + password_numbers + password_letters
    random.shuffle(password_list)

    password_input.insert(0, ''.join(password_list))
    pyperclip.copy(password_input.get())


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    web_data = web_input.get()
    login_data = login_input.get()
    pass_data = password_input.get()
    new_data = {
        web_data: {
            "email": login_data,
            "password": pass_data,
        }
    }

    if not web_data or not pass_data or not login_data:
        messagebox.showinfo(title="Caution", message="Please do not left any fields empty")
    else:
        try:
            with open("data_log.json", "r") as data_file:
                # Смотрим старые данные
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data_log.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Обновляем старые данные новыми
            data.update(new_data)

            with open("data_log.json", "w") as data_file:
                # Сохраняем обновленные данные
                json.dump(data, data_file, indent=4)
        finally:
            login_input.delete(0, END)
            web_input.delete(0, END)
            password_input.delete(0, END)


# ----------------------------- SEARCH -------------------------------- #
def find_password():
    website_name = web_input.get()
    try:
        # Проверяем json на наличие нужных данных
        with open("data_log.json", "r") as data_file:
            data = json.load(data_file)
            try:
                # Получаем данные с json'a
                user_input_search = data.get(website_name)
                messagebox.showinfo(title="Info", message=f"Login: {user_input_search['email']}"
                                                          f" \n Password: {user_input_search['password']}")
                # Данные по запросу не найдены
            except:
                messagebox.showinfo(title="Warning", message="No details for  the website exist")
    except FileNotFoundError:
        messagebox.showinfo(title="Warning", message="There is no data")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
password = Label(text="Password:")
login_name = Label(text="Email/Username:")
website.grid(column=0, row=1)
login_name.grid(column=0, row=2)
password.grid(column=0, row=3)

web_input = Entry(bd=1, width=41)
web_input.focus()
password_input = Entry(bd=1, width=41)
login_input = Entry(bd=1, width=50)
web_input.grid(column=1, row=1)
login_input.grid(column=1, row=2, columnspan=2)
password_input.grid(column=1, row=3)

add_button = Button(text="Add", width=43, bd=1, command=save_data)
gen_button = Button(text='Generate', width=7, bd=1, command=gen_pas)
add_button.grid(column=1, row=4, columnspan=2)
gen_button.grid(column=2, row=3)
search_button = Button(text="Search", width=7, bd=1, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
