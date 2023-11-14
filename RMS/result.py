from tkinter import * #here we imported tkinter library
from PIL import Image,ImageTk #here we installed pillow(pip install pillow)
from tkinter import ttk,messagebox
import sqlite3
class resultClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student result management system")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        #this is the title.......
        title=Label(self.root,text="Add Student Results",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)
        #variables.........
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_subject=StringVar()
        self.var_marks=StringVar()
        self.var_full_Marks=StringVar()
        self.roll_list=[]
        self.fetch_roll()

        #widgets...............
        lbl_select=Label(self.root,text="Select Student",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=100)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=160)
        lbl_subject=Label(self.root,text="Subject",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=220)
        lbl_marks=Label(self.root,text="Marks",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=280)
        lbl_full_marks=Label(self.root,text="Full Marks",font=("goudy old style",20,'bold'),bg='white').place(x=50,y=340)

        self.txt_student=ttk.Combobox(self.root,textvariable=self.var_roll,values=self.roll_list,font=("goudy old style",15,'bold'),state='readonly',justify=CENTER)
        self.txt_student.place(x=280,y=100,width=200)
        self.txt_student.set("SELECT")
        
        btn_search=Button(self.root,text='Search',font=("goudy old style",15,'bold'),bg="#03a9f4",fg="white",cursor="hand2",command=self.search).place(x=500,y=100,width=100,height=28)
        
        txt_Name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20,'bold'),bg='lightyellow',state="readonly").place(x=280,y=160,width=320)
        txt_Subject=Entry(self.root,textvariable=self.var_subject,font=("goudy old style",20,'bold'),bg='lightyellow',state="readonly").place(x=280,y=220,width=320)
        txt_Marks=Entry(self.root,textvariable=self.var_marks,font=("goudy old style",20,'bold'),bg='lightyellow').place(x=280,y=280,width=320)
        txt_full_Marks=Entry(self.root,textvariable=self.var_full_Marks,font=("goudy old style",20,'bold'),bg='lightyellow').place(x=280,y=340,width=320)

        #buttons.................
        btn_add=Button(self.root,text='Submit',font=("times new roman",15),bg="green",fg="white",activebackground="lightgreen",cursor="hand2",command=self.add)
        btn_add.place(x=300,y=420,width=120,height=35)
        btn_clear=Button(self.root,text='Clear',font=("times new roman",15),bg="gray",fg="white",activebackground="lightgray",cursor="hand2",command=self.clear)
        btn_clear.place(x=430,y=420,width=120,height=35)

        #image
        self.bg_img=Image.open("images/result.jpg")
        self.bg_img=self.bg_img.resize((500,300))
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=650,y=100)

    #functions start here.............
    def fetch_roll(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select roll from student")
            rows=cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("ERROR",f"ERROR DUE TO {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select name,subject from student where roll=?",(self.var_roll.get(),))
            row=cur.fetchone()
            if row!=None:
                self.var_name.set(row[0])
                self.var_subject.set(row[1])
            else:
                messagebox.showerror("ERROR","NO RECORD FOUND",parent=self.root)
        except Exception as ex:
            messagebox.showerror("ERROR",f"ERROR DUE TO {str(ex)}",)

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("ERROR","PLEASE FIRST SEARCH STUDENT RECORD",parent=self.root)
            else:
                cur.execute("select * from result where roll=? and subject=?",(self.var_roll.get(),self.var_subject.get(),))
                row=cur.fetchone()
                if row !=None:
                    messagebox.showerror("ERROR","RESULT ALREADY PRESENT",parent=self.root)
                else:
                    per=(int(self.var_marks.get())*100)/int(self.var_full_Marks.get())
                    cur.execute("insert into result (roll,name,subject,marks_ob,full_marks,per) values(?,?,?,?,?,?)",(
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_subject.get(),
                        self.var_marks.get(),
                        self.var_full_Marks.get(),
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo("SUCCESS","RESULT ADDED SUCCESSFULLY",parent=self.root)
        except Exception as ex:
            messagebox.showerror("ERROR",f"ERROR DUE TO {str(ex)}")

    def clear(self):
        self.var_roll.set("select")
        self.var_name.set("")
        self.var_subject.set("")
        self.var_marks.set("")
        self.var_full_Marks.set("")
                        
if __name__=="__main__":
    root=Tk()
    obj=resultClass(root)
    root.mainloop()