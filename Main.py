import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
import math
from reportlab.lib import colors

def get_department_info():
    departments = []
    try:
        num_departments = int(simpledialog.askstring("Departments", "Enter the number of departments:"))
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of departments.")
        return None
    
    for i in range(num_departments):
        department_name = simpledialog.askstring("Department", f"Enter the name of department {i + 1}:")
        if not department_name:
            messagebox.showerror("Error", "Department name cannot be empty.")
            return None
        departments.append(department_name)
    
    return departments

def get_roll_numbers(department):
    try:
        start = int(simpledialog.askstring("Roll Numbers", f"Enter the Starting Roll No for {department}:"))
        end = int(simpledialog.askstring("Roll Numbers", f"Enter the Ending Roll No for {department}:"))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid starting and ending roll numbers.")
        return None
    
    return start, end

def generate_seating_chart():
    departments = get_department_info()
    
    if not departments:
        return
    
    depts = []
    e = []
    
    for department in departments:
        depts.append(department)
        year = simpledialog.askstring("Year", f"Enter the year for department {department}:")
        year = year[2:]
        
        mtech = "ES" + year + "CJ"
        csd = "ES" + year + "CD"
        it = "ES" + year + "IT"
        cse = "ES" + year + "CS"
        ece = "ES" + year + "EC"
        agri = "ES" + year + "AG"
        bme = "ES" + year + "BM"
        aids = "ES" + year + "AD"
        eie = "ES" + year + "EI"
        rie = "ES" + year + "RE"
        civil = "ES" + year + "CI"
        chem = "ES" + year + "CH"
        mech = "ES" + year + "ME"
        eee = "ES" + year + "EE"
        mba = "ES" + year + "MB"
        biotech = "ES" + year + "BT"
        
        dept = {"biotech": biotech, "mba": mba, "eee": eee, "mech": mech, "chem": chem, "civil": civil, "bme": bme,
                "mtech": mtech, "m.tech": mtech, "csd": csd, "it": it, "cse": cse, "m.tech(cse)": mtech,
                "mtech(cse)": mtech, "ece": ece, "agri": agri, "aids": aids, "eie": eie, "rie": rie}
        
        roll = dept[department.lower()]
        start, end = get_roll_numbers(department)
        
        if start is None or end is None:
            return
        
        l = []
        
        for i in range(start, end + 1):
            if len(str(i)) == 1:
                i = "0" + str(i)
            else:
                i = str(i)
            l.append(roll + i)
        
        e.append(l)
    
    f = [0 for x in range(len(depts))]
    n = len(depts)
    alloted = []
    maxi = sum(len(dept) for dept in e)
    count = 1
    last_added = ''
    
    try:
        rows = int(simpledialog.askstring("Classroom Dimensions", "Enter the number of rows in the classroom:"))
        cols = int(simpledialog.askstring("Classroom Dimensions", "Enter the number of columns in the classroom:"))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values for rows and columns.")
        return
    
    while count <= maxi:
        for i in range(n):
            if f[i] < len(e[i]) and last_added != i:
                alloted.append(e[i][f[i]])
                f[i] += 1
                count += 1
                last_added = i
            else:
                alloted.append(" ")
                last_added = ' '
    
    classes = math.ceil(len(alloted) / (rows * cols))
    idx = 0
    resulting = ['000000']
    for i in range(classes):
        for j in range(cols):
            count = 0
            
            while count < cols:
                if idx < len(alloted):
                    if alloted[idx] == ' ' and resulting[-1] != ' ':
                        resulting.append(' ')
                        idx += 1
                        count += 1
                    else:
                        resulting.append(alloted[idx])
                        idx += 1
                        count += 1
                else:
                    break
    
    resulting = resulting[1:]
    alloted = []
    for i in range(len(resulting)-1):
        if resulting[i]!=resulting[i+1]:
            alloted.append(resulting[i])
    num_pages = math.ceil(len(alloted) / (rows * cols))
    doc = SimpleDocTemplate("exam_hall_chart.pdf", pagesize=landscape(letter))
    tables = []
    
    for i in range(num_pages):
        class_table_data = []
        
        for j in range(rows):
            row_data = []
            
            for k in range(cols):
                idx = i * (rows * cols) + j * cols + k
                
                if idx < len(alloted):
                    student = alloted[idx]
                    row_data.append(student)
                else:
                    row_data.append("")
            
            class_table_data.append(row_data)
        
        class_table = Table(class_table_data, colWidths=120, rowHeights=70)
        class_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        tables.append(class_table)
        if i < num_pages - 1:
            tables.append(PageBreak())
    doc.build(tables)
    messagebox.showinfo("Success", "PDF generated successfully.")

def main():
    root = tk.Tk()
    root.title("Seating Chart Generator")
    root.geometry("400x200")  # Set the initial window size
    
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12))
    
    generate_button = ttk.Button(root, text="Generate Seating Chart", command=generate_seating_chart)
    generate_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
