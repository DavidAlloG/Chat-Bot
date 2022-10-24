import tkinter as tk

class GUI():
    def __init__(self, response_funct):
        #Basic setup
        self.base = tk.Tk()
        self.base.title('ChatBot')
        self.base.geometry('400x500')
        self.base.resizable(width=False, height=False)
        #Creating all elements
        self.create_all()
        #Response function variable
        self.response_func = response_funct

    def create_chat(self):
        self.ChatLog = tk.Text(self.base, bd=0, bg='white', height=8, width=50, font='Arial')
        self.ChatLog.config(state=tk.DISABLED)
        self.ChatLog.place(x=6,y=6, height=386, width=370)

    def create_scrollbar(self):
        self.ScrollBar = tk.Scrollbar(self.base, command=self.ChatLog.yview)
        self.ChatLog['yscrollcommand'] = self.ScrollBar.set
        self.ScrollBar.place(x=376,y=6, height=386)

    def create_entrybox(self):
        self.EntryBox = tk.Text(self.base, bd=0, bg="white",width="29", height="5", font="Arial")
        self.EntryBox.place(x=6, y=401, height=90, width=265)

    def create_button(self):
        self.SendButton = tk.Button(self.base, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command=self.send_message)
        self.SendButton.place(x=272, y=401, height=90, width=128)

    def create_all(self):
        self.create_chat()
        self.create_scrollbar()
        self.create_entrybox()
        self.create_button()

    def send_message(self):
        message = self.EntryBox.get('1.0', 'end-1c').strip()
        self.EntryBox.delete('0.0', tk.END)

        if message != '':
            self.ChatLog.config(state=tk.NORMAL)
            self.ChatLog.insert(tk.END, 'You: ' + message + '\n\n')
            self.ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

            response = self.response_func(message)
            self.ChatLog.insert(tk.END, 'Bot: ' + response +'\n\n')

            self.ChatLog.config(state=tk.DISABLED)
            self.ChatLog.yview(tk.END)

    def update(self):
        self.base.mainloop()
