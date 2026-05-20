from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3
import datetime

# ================= Database Setup =================
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    admission_date TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    appointment_date TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emergency(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    issue TEXT NOT NULL,
    date TEXT NOT NULL
)""")
conn.commit()


class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        path = os.path.dirname(__file__)

        # ================= Images =================
        try:
            raw_logo = Image.open(os.path.join(path, "logo.png"))
            resized_logo = raw_logo.resize((60, 60), Image.LANCZOS)
            self.logo_title = ImageTk.PhotoImage(resized_logo)
        except:
            self.logo_title = None

        try:
            raw_logo2 = Image.open(os.path.join(path, "image.png"))
            resized_logo2 = raw_logo2.resize((320, 320), Image.LANCZOS)
            self.logo_side = ImageTk.PhotoImage(resized_logo2)
        except:
            self.logo_side = None

        # ================= Header =================
        header = Label(self.root, text=" VIPUL SINGH MEDICAL HOSPITAL",
                       font=("Goudy Old Style", 20, "bold"),
                       image=self.logo_title, compound=LEFT,
                       padx=10, bg="#C5240F", fg="white")
        header.place(x=0, y=0, relwidth=1, height=50)

        # ================= Menu =================
        M_Frame = LabelFrame(self.root, text="Menu",
                             font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1320, height=60)

        Button(M_Frame, text="Home", command=self.show_home,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=10, y=5, width=150, height=30)
        Button(M_Frame, text="Statistics", command=self.show_statistics,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=170, y=5, width=150, height=30)
        Button(M_Frame, text="Patients", command=self.show_patients,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=330, y=5, width=150, height=30)
        Button(M_Frame, text="Appointments", command=self.show_appointments,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=490, y=5, width=150, height=30)
        Button(M_Frame, text="Staff", command=self.show_staff,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=650, y=5, width=150, height=30)
        Button(M_Frame, text="Emergency", command=self.show_emergency,
               font=("Goudy Old Style", 15, "bold"),
               bg="#77480b", fg="white").place(x=810, y=5, width=150, height=30)

        # ================= Content Frame =================
        self.content = Frame(self.root, bg="white")
        self.content.place(x=10, y=140, width=1330, height=500)

        self.show_home()

        # ================= Footer =================
        footer = Label(self.root,
                       text="HOSPITAL MANAGEMENT SYSTEM | Contact Support",
                       font=("Goudy Old Style", 12),
                       bg="#0FC588", fg="white")
        footer.pack(side=BOTTOM, fill=X)

    # ================= Utility =================
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ================= Screens =================
    def show_home(self):
        self.clear_content()
        Label(self.content, text="Welcome to Hospital Management System",
              font=("Arial", 25, "bold"), bg="white").pack(pady=20)
        if self.logo_side:
            Label(self.content, image=self.logo_side, bg="white").pack()

    # ================= Statistics =================
    def show_statistics(self):
        self.clear_content()
        Label(self.content, text="Hospital Statistics",
              font=("Arial", 25, "bold"), bg="white").pack(pady=20)

        stats_frame = Frame(self.content, bg="white")
        stats_frame.pack(pady=20, fill=X)

        # Fetch stats from database dynamically
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM staff")
        total_staff = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM emergency")
        total_emergency = cursor.fetchone()[0]

        stats = {
            "Total Patients": total_patients,
            "Total Staff": total_staff,
            "Total Appointments": total_appointments,
            "Emergency Cases": total_emergency
        }

        for key, val in stats.items():
            stat_box = Frame(stats_frame, bg="#b40ce7", bd=2, relief=RIDGE)
            stat_box.pack(side=LEFT, padx=20, ipadx=10, ipady=10)

            Label(stat_box, text=key, font=("Arial", 14), bg="#d36d6e").pack(pady=(10, 5))
            Label(stat_box, text=val, font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=(0, 10))

    # ================= Patients =================
    def show_patients(self):
        self.clear_content()
        Label(self.content, text="Patient Management",
              font=("Arial", 25, "bold"), bg="white").pack(pady=10)

        form_frame = Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Patient Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.patient_entry = Entry(form_frame)
        self.patient_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(form_frame, text="Add Patient", command=self.add_patient,
               bg="#0FC588", fg="white").grid(row=0, column=2, padx=5)

        Button(self.content, text="Edit Selected Patient", command=self.edit_patient,
               bg="#FFA500", fg="white").pack(pady=5)

        Button(self.content, text="Delete Selected Patient", command=self.delete_patient,
               bg="#FF0000", fg="white").pack(pady=5)

        table_frame = Frame(self.content)
        table_frame.pack(fill=BOTH, expand=True, pady=10)

        self.patient_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Date"), show='headings')
        self.patient_table.heading("ID", text="ID")
        self.patient_table.heading("Name", text="Name")
        self.patient_table.heading("Date", text="Admission Date")
        self.patient_table.column("ID", width=50)
        self.patient_table.column("Name", width=200)
        self.patient_table.column("Date", width=120)
        self.patient_table.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.patient_table.yview)
        self.patient_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.load_patients()

    def add_patient(self):
        name = self.patient_entry.get()
        if name == "":
            messagebox.showerror("Error", "Please enter patient name")
            return
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO patients(name, admission_date) VALUES (?,?)", (name, date_today))
        conn.commit()
        messagebox.showinfo("Success", f"Patient {name} added")
        self.patient_entry.delete(0, END)
        self.load_patients()

    def load_patients(self):
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)
        cursor.execute("SELECT * FROM patients ORDER BY id DESC")
        for patient in cursor.fetchall():
            self.patient_table.insert("", END, values=patient)

    def edit_patient(self):
        selected = self.patient_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to edit")
            return

        values = self.patient_table.item(selected, "values")
        patient_id = values[0]

        edit_win = Toplevel()
        edit_win.title("Edit Patient")
        edit_win.geometry("300x150")

        Label(edit_win, text="Patient Name:").pack(pady=10)
        name_entry = Entry(edit_win)
        name_entry.pack()
        name_entry.insert(0, values[1])

        def save_changes():
            new_name = name_entry.get()
            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            cursor.execute("UPDATE patients SET name=? WHERE id=?", (new_name, patient_id))
            conn.commit()
            messagebox.showinfo("Success", "Patient updated")
            edit_win.destroy()
            self.load_patients()

        Button(edit_win, text="Save Changes", command=save_changes, bg="#0FC588", fg="white").pack(pady=10)

    def delete_patient(self):
        selected = self.patient_table.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to delete")
            return

        values = self.patient_table.item(selected, "values")
        patient_id = values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete patient {values[1]}?")
        if confirm:
            cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
            conn.commit()
            messagebox.showinfo("Success", "Patient deleted")
            self.load_patients()

    # ================= Staff =================
    def show_staff(self):
        self.clear_content()
        Label(self.content, text="Staff Management",
              font=("Arial", 25, "bold"), bg="white").pack(pady=10)

        form_frame = Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Staff Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        staff_name = Entry(form_frame)
        staff_name.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Role:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        staff_role = Entry(form_frame)
        staff_role.grid(row=1, column=1, padx=5, pady=5)

        def add_staff():
            name = staff_name.get()
            role = staff_role.get()
            if not name or not role:
                messagebox.showerror("Error", "Please fill all fields")
                return
            cursor.execute("INSERT INTO staff(name, role) VALUES (?,?)", (name, role))
            conn.commit()
            messagebox.showinfo("Success", f"Staff {name} added")
            staff_name.delete(0, END)
            staff_role.delete(0, END)
            self.load_staff()

        Button(form_frame, text="Add Staff", command=add_staff, bg="#0FC588", fg="white").grid(row=2, column=0, columnspan=2, pady=5)

        table_frame = Frame(self.content)
        table_frame.pack(fill=BOTH, expand=True, pady=10)

        self.staff_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Role"), show='headings')
        self.staff_table.heading("ID", text="ID")
        self.staff_table.heading("Name", text="Name")
        self.staff_table.heading("Role", text="Role")
        self.staff_table.column("ID", width=50)
        self.staff_table.column("Name", width=200)
        self.staff_table.column("Role", width=150)
        self.staff_table.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.staff_table.yview)
        self.staff_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.load_staff()

    def load_staff(self):
        for row in self.staff_table.get_children():
            self.staff_table.delete(row)
        cursor.execute("SELECT * FROM staff ORDER BY id DESC")
        for s in cursor.fetchall():
            self.staff_table.insert("", END, values=s)

    # ================= Appointments =================
    def show_appointments(self):
        self.clear_content()
        Label(self.content, text="Appointments",
              font=("Arial", 25, "bold"), bg="white").pack(pady=10)

        form_frame = Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Patient Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        patient_name = Entry(form_frame)
        patient_name.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Doctor Name:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        doctor_name = Entry(form_frame)
        doctor_name.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Appointment Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, padx=5, pady=5)
        app_date = Entry(form_frame)
        app_date.grid(row=2, column=1, padx=5, pady=5)

        def add_appointment():
            p_name = patient_name.get()
            d_name = doctor_name.get()
            date = app_date.get()
            if not p_name or not d_name or not date:
                messagebox.showerror("Error", "Please fill all fields")
                return
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
            except:
                messagebox.showerror("Error", "Date must be YYYY-MM-DD")
                return
            cursor.execute("INSERT INTO appointments(patient_name, doctor_name, appointment_date) VALUES (?,?,?)",
                           (p_name, d_name, date))
            conn.commit()
            messagebox.showinfo("Success", "Appointment added")
            patient_name.delete(0, END)
            doctor_name.delete(0, END)
            app_date.delete(0, END)
            self.load_appointments()

        Button(form_frame, text="Add Appointment", command=add_appointment, bg="#0FC588", fg="white").grid(row=3, column=0, columnspan=2, pady=5)

        table_frame = Frame(self.content)
        table_frame.pack(fill=BOTH, expand=True, pady=10)

        self.app_table = ttk.Treeview(table_frame, columns=("ID", "Patient", "Doctor", "Date"), show='headings')
        self.app_table.heading("ID", text="ID")
        self.app_table.heading("Patient", text="Patient")
        self.app_table.heading("Doctor", text="Doctor")
        self.app_table.heading("Date", text="Appointment Date")
        self.app_table.column("ID", width=50)
        self.app_table.column("Patient", width=200)
        self.app_table.column("Doctor", width=200)
        self.app_table.column("Date", width=120)
        self.app_table.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.app_table.yview)
        self.app_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.load_appointments()

    def load_appointments(self):
        for row in self.app_table.get_children():
            self.app_table.delete(row)
        cursor.execute("SELECT * FROM appointments ORDER BY id DESC")
        for app in cursor.fetchall():
            self.app_table.insert("", END, values=app)

    # ================= Emergency =================
    def show_emergency(self):
        self.clear_content()
        Label(self.content, text="Emergency Cases",
              font=("Arial", 25, "bold"), bg="white").pack(pady=10)

        form_frame = Frame(self.content, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Patient Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        patient_name = Entry(form_frame)
        patient_name.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Issue:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        issue = Entry(form_frame)
        issue.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, padx=5, pady=5)
        date_entry = Entry(form_frame)
        date_entry.grid(row=2, column=1, padx=5, pady=5)

        def add_emergency():
            p_name = patient_name.get()
            p_issue = issue.get()
            date_val = date_entry.get()
            if not p_name or not p_issue or not date_val:
                messagebox.showerror("Error", "Please fill all fields")
                return
            try:
                datetime.datetime.strptime(date_val, "%Y-%m-%d")
            except:
                messagebox.showerror("Error")
                
if __name__ == "__main__":
    root = Tk()
    app = RMS(root)
    root.mainloop()