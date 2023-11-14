from tkinter import *
from PIL import Image , ImageTk
from tkinter import ttk , messagebox
import sqlite3
import threading
import time
class CourseClass :
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result File Management System")  
        self.root.geometry("1200x600+150+100")
        self.root.config(bg='white')
        self.root.focus_force()
        self.semaphore = threading.Semaphore(1)  # Initialize a semaphore with a value of 1

        # Create a button that triggers a function protected by the semaphore
        self.btn_protected = Button(self.root, text="Protected Operation",font=("goudy ols style",15,"bold"),bg="black",fg="white",cursor="hand2", command=self.protected_operation)
        self.btn_protected.place(x=180,y=500,width=200,height=40)

        title = Label(self.root,text="Manage Course Details",padx = 10,font = ("Times New Roman",20,"bold"),bg="#0b5377",fg="white").place(x=0,y=0,relwidth=1,height = 50)

        #variables
        self.var_course   =  StringVar()
        self.var_duration =  StringVar()
        self.var_charges  =  StringVar()


        #Widgets
        lbl_coursename  = Label(self.root,text="Course Name",font = ("Times New Roman",15,"bold"),bg="white").place(x=10,y=60)
        lbl_duration    = Label(self.root,text="Duration",font = ("Times New Roman",15,"bold"),bg="white").place(x=10,y=100)
        lbl_charges     = Label(self.root,text="Charges",font = ("Times New Roman",15,"bold"),bg="white").place(x=10,y=140)
        lbl_description = Label(self.root,text="Description",font = ("Times New Roman",15,"bold"),bg="white").place(x=10,y=180)

        #Entry
        self.txt_coursename  = Entry(self.root,textvariable=self.var_course,font = ("Times New Roman",15,"bold"),bg="lightyellow")
        self.txt_coursename.place(x=150,y=60,width=200)
        txt_duration    = Entry(self.root,textvariable=self.var_duration,font = ("Times New Roman",15,"bold"),bg="lightyellow").place(x=150,y=100,width=200)
        txt_charges     = Entry(self.root,textvariable=self.var_charges,font = ("Times New Roman",15,"bold"),bg="lightyellow").place(x=150,y=140,width=200)
        self.txt_description = Text(self.root,font = ("Times New Roman",15,"bold"),bg="lightyellow")
        self.txt_description.place(x=150,y=180,width=420,height=150)

        #Buttons
        self.btn_add=Button(self.root,text="Save",font=("goudy ols style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=100,y=400,width=110,height=40)

        self.btn_update=Button(self.root,text="Update",font=("goudy ols style",15,"bold"),bg="green",fg="white",cursor="hand2",command = self.update)
        self.btn_update.place(x=220,y=400,width=110,height=40)

        self.btn_delete=Button(self.root,text="Delete",font=("goudy ols style",15,"bold"),bg="red",fg="white",cursor="hand2",command = self.delete)
        self.btn_delete.place(x=340,y=400,width=110,height=40)

        self.btn_clear=Button(self.root,text="Clear",font=("goudy ols style",15,"bold"),bg="grey",fg="white",cursor="hand2",command = self.clear)
        self.btn_clear.place(x=460,y=400,width=110,height=40)

        #Search
        self.var_search = StringVar()
        lbl_search_coursename  = Label(self.root,text="Course Name",font = ("Times New Roman",15,"bold"),bg="white").place(x=700,y=60)
        txt_coursename  = Entry(self.root,textvariable=self.var_search,font = ("Times New Roman",15,"bold"),bg="lightyellow").place(x=850,y=60,width=180)
        btn_search=Button(self.root,text="Search",font=("goudy ols style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2",command=self.search_thread).place(x=1050,y=60,width=110,height=30)

        #Frame
        self.C_Frame = Frame(self.root,bd=2,relief = RIDGE)
        self.C_Frame.place(x=700,y=100,width = 460,height = 340)

        scrolly = Scrollbar(self.C_Frame,orient = VERTICAL)
        scrollx = Scrollbar(self.C_Frame,orient = HORIZONTAL)

        self.CourseTable=ttk.Treeview(self.C_Frame,columns = ("cid","name","duration","charges","description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

        scrollx.pack(side = BOTTOM,fill=X)
        scrolly.pack(side = RIGHT,fill=Y)

        scrollx.config(command = self.CourseTable.xview)
        scrolly.config(command = self.CourseTable.yview)

        self.CourseTable.heading("cid",text = "Course ID")
        self.CourseTable.heading("name",text = "Name")
        self.CourseTable.heading("duration",text = "Duration")
        self.CourseTable.heading("charges",text = "Charges")
        self.CourseTable.heading("description",text = "Description")
        self.CourseTable['show'] = 'headings'
        self.CourseTable.column("cid",width = 100)
        self.CourseTable.column("name",width = 100)
        self.CourseTable.column("duration",width = 100)
        self.CourseTable.column("charges",width = 100)
        self.CourseTable.column("description",width = 150)
        self.CourseTable.pack(fill=BOTH,expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0",END)
        self.txt_coursename.config(state = NORMAL)


    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name is Mandatory",parent = self.root)
            else:
                cur.execute("select * from course where name = ?",(self.var_course.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course From the list.",parent = self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to Delete?",parent = self.root)
                    if op==True:
                        cur.execute("delete from course where name = ?",(self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Course Deleted Successfully",parent=self.root)
                        self.clear()



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")



    def get_data(self,ev):
        self.txt_coursename.config(state = 'readonly')
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        #print(row)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        #self.var_course.set(row[4])
        self.txt_description.delete("1.0",END)
        self.txt_description.insert(END,row[4])


    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name is Mandatory",parent = self.root)
            else:
                cur.execute("select * from course where name = ?",(self.var_course.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course Name is Already Present",parent = self.root)
                else:
                    cur.execute("insert into course (name,duration,charges,description) values(?,?,?,?)",(
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END)
                    ))

                    con.commit()
                    messagebox.showinfo("Success","Details Added SuccessFully",parent = self.root)
                    self.show()


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name is Mandatory",parent = self.root)
            else:
                cur.execute("select * from course where name = ?",(self.var_course.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course From List",parent = self.root)
                else:
                    cur.execute("update course set duration=?,charges=?,description=? where name=?",(
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END),
                        self.var_course.get(),
                    ))

                    con.commit()
                    messagebox.showinfo("Success","Details Updated SuccessFully",parent = self.root)
                    self.show()


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")



    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def search_thread(self):
        # Create a new thread to perform the search
        thread = threading.Thread(target=self.search)
        thread.daemon = True  # Ensure the thread terminates when the main GUI thread exits
        thread.start()

    def protected_operation(self):
        # Acquire the semaphore to protect this section of code
        self.semaphore.acquire()
        
        try:
            # Your protected code goes here
            print("Protected operation started...")
            time.sleep(2)  # Simulate a time-consuming operation
            print("Protected operation completed.")
        finally:
            # Release the semaphore to allow other threads to enter this section
            self.semaphore.release()


    
     

   
     

        



        














if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)

    

    root.mainloop()