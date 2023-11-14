from tkinter import *
from PIL import Image , ImageTk
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
from tkinter import ttk , messagebox
import sqlite3

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result File Management System")  
        self.root.geometry("1500x750+0+0")
        self.root.config(bg='white')

        original_image = Image.open("images/srm.png")
        resized_image = original_image.resize((65, 65))
        self.logo_dash = ImageTk.PhotoImage(resized_image)

        title = Label(self.root,text="Student Result Management System",padx = 10,image = self.logo_dash ,compound = LEFT,font = ("Times New Roman",20,"bold"),bg="#0b5377",fg="white").place(x=0,y=0,relwidth=1,height = 50)

        #Menu
        M_Frame = LabelFrame(self.root,text = "Menu",font = ("Times New Roman",15),bg = "white").place(x=10,y=70,width = 1450 , height=80)

        btn_course =  Button(M_Frame,text = "Course",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2",command=self.add_course).place(x=70,y=100,width = 200 , height = 40)
        btn_student = Button(M_Frame,text = "Student",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2",command=self.add_student).place(x=290,y=100,width = 200 , height = 40)
        btn_result =  Button(M_Frame,text = "Result",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2",command = self.add_result).place(x=510,y=100,width = 200 , height = 40)
        btn_view =    Button(M_Frame,text = "View",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2",command = self.add_view).place(x=730,y=100,width = 200 , height = 40)
        btn_login =   Button(M_Frame,text = "Login",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2").place(x=950,y=100,width = 200 , height = 40)
        btn_exit =    Button(M_Frame,text = "Exit",font = ("goudy old style",15,"bold"),bg="#0b5377",fg = "white",cursor = "hand2",command = self.add_result).place(x=1170,y=100,width = 200 , height = 40)

        #content
        self.bg_image = Image.open("images/boy.png")
        self.bg_image= self.bg_image.resize((300, 300))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.lbl_bg = Label(self.root,image = self.bg_image).place(x=800,y=200,width = 400,height = 300)

        #labelbox
        self.lbl_course = Label(self.root,text = "Total Courses\n[0]",font = ("goudy old style",20),bd = 10,relief = RIDGE,bg="#e43b06",fg="white").place(x=550,y=550,width = 300,height =100)
        self.lbl_student = Label(self.root,text = "Total Courses\n[0]",font = ("goudy old style",20),bd = 10,relief = RIDGE,bg="#0676ad",fg="white").place(x=850,y=550,width = 300,height =100)
        self.lbl_result = Label(self.root,text = "Total Results\n[0]",font = ("goudy old style",20),bd = 10,relief = RIDGE,bg="#038074",fg="white").place(x=1150,y=550,width = 300,height =100)


        #footer
        footer = Label(self.root,text="SRM - Student Result Management System\nContact Us for Technical Issue : 999xxxxx9",image = self.logo_dash ,compound = LEFT,font = ("Times New Roman",12),bg="#0b5377",fg="white").pack(side = BOTTOM,fill =X)


        self.database_widget = LabelFrame(self.root, text="Database Usage", font=("Times New Roman", 18), bg="white")
        self.database_widget.place(x=10, y=170, width=400, height=120)

        self.storage_label = Label(self.database_widget, text="", font=("goudy old style", 15))
        self.storage_label.pack()

        # Connect to your SQLite database and retrieve usage information
        try:
            conn = sqlite3.connect("rms.db")
            cursor = conn.cursor()
            cursor.execute("PRAGMA page_size;")  # Get the page size
            page_size = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_count;")  # Get the total page count
            page_count = cursor.fetchone()[0]
            database_size = page_size * page_count

            # Convert bytes to a human-readable format
            if database_size > 1024 ** 3:
                database_size_str = f"{database_size / (1024 ** 3):.2f} GB"
            elif database_size > 1024 ** 2:
                database_size_str = f"{database_size / (1024 ** 2):.2f} MB"
            else:
                database_size_str = f"{database_size / 1024:.2f} KB"

            self.storage_label.config(text=f"Storage Usage: {database_size_str}")
        except Exception as e:
            # Handle errors gracefully
            self.storage_label.config(text=f"Storage Usage: Error")
    
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=studentClass(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=resultClass(self.new_win)

    def add_view(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=reportClass(self.new_win)

 





    





if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()

