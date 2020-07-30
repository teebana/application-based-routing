from tkinter import *
from PIL import ImageTk, Image

class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        #self.create_widgets()

        #root = Tk()
        canvas = Canvas(root, width = 1000, height = 1080)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open("assets/logo.jpg"), master=canvas)
        #canvas.create_image(640,412, anchor=S, image=img)

        canvas.netflix = Checkbutton(root, image = img, command = self.say_hi)
        root.mainloop()

    def create_widgets(self):
        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        

        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.netflix = Checkbutton(self)
        self.netflix["text"] = "Netflix"
        self.netflix["command"] = self.say_hi
        self.netflix.pack(side="top")

        

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()
app = Application(master=root)
#app.mainloop()