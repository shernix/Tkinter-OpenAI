from tkinter import *
import customtkinter
import openai
import os
import pickle

root = customtkinter.CTk()
root.title("OpenAI Chat")
root.geometry('700x600')
#root.iconbitmap('https://tkinter.com/ai_lt.ico')

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def speak():
    if chat_entry.get():
        api_entry.delete(0, END)
        filename = "api_key"
        try:

            if os.path.isfile(filename):
                input_file = open(filename, 'rb')
                load_file = pickle.load(input_file)
                
                #Query OpenAI
                openai.api_key = load_file
                openai.Model.list()
                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = chat_entry.get(),
                    temperature = 0,
                    max_tokens = 70,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0
                )
                my_text.insert(END, (response["choices"][0]["text"]).strip())
                my_text.insert(END, "\n\n")

            else:
                input_file = open(filename, 'wb')
                input_file.close()
                my_text.insert(END, "\n\n API key is needed\n\n")

        except Exception as e:
            my_text.insert(END, f"\n\n There was an error, could not open key. \n\n{e}")
        else:
            my_text.insert(END, "\n\n Please type something before sending it to Open AI\n\n")

def clear():
    my_text.delete(1.0, END)
    chat_entry.delete(0, END)

def key():
    api_entry.delete(0, END)
    filename = "api_key"

    try:

        if os.path.isfile(filename):
            input_file = open(filename, 'rb')
            load_file = pickle.load(input_file)
            api_entry.insert(END, load_file)
        else:
            input_file = open(filename, 'wb')
            input_file.close()

    except Exception as e:
        my_text.insert(END, f"\n\n There was an error, could not open key. \n\n{e}")

    root.geometry('700x750')
    api_frame.pack(pady=30)

def save_key():

    try:
        filename="api_key"
        output_file = open(filename, 'wb')
        pickle.dump(api_entry.get(), output_file)
        api_entry.delete(0, END)
        root.geometry('700x600')
        api_frame.pack_forget()

    except Exception as e:
        my_text.insert(END, f"\n\n There was an error \n\n{e}")

text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)


my_text = Text(text_frame,
               bg="#343638",
               width=65,
               bd=1,
               fg="#d6d6d6",
               relief="flat",
               wrap=WORD,
               selectbackground="#1f538d")

my_text.grid(row=0, column=0)

text_scroll = customtkinter.CTkScrollbar(text_frame,
                                        command=my_text.yview)

text_scroll.grid(row=0, column=1, sticky="ns")
my_text.configure(yscrollcommand=text_scroll.set)

chat_entry = customtkinter.CTkEntry(root,
                                    placeholder_text="Type something please",
                                    width=530,
                                    height=100,
                                    border_width=1)
chat_entry.pack(pady=10)

button_frame = customtkinter.CTkFrame(root,
                                        fg_color="#242424")
button_frame.pack(pady=10)

submit_button = customtkinter.CTkButton(button_frame,
                                        text="Send Message to OpenAI",
                                        command=speak)
                                        
submit_button.grid(row=0,column=0,padx=25)

clear_button = customtkinter.CTkButton(button_frame,
                                        text="Clear Screen",
                                        command=clear)
                                        
clear_button.grid(row=0,column=1,padx=25)

key_button = customtkinter.CTkButton(button_frame,
                                        text="Update API key",
                                        command=key)
                                        
key_button.grid(row=0,column=2,padx=25)


api_frame = customtkinter.CTkFrame(root, border_width=1)

api_entry = customtkinter.CTkEntry(api_frame,
                                    placeholder_text="Ender your API key",
                                    width=350,
                                    height=50,
                                    border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

api_save_button = customtkinter.CTkButton(api_frame,
                                            text="Save Key",
                                            command=save_key)

api_save_button.grid(row=0, column=1, padx=10)



root.mainloop()