from tkinter import *  # for GUI app
from tkinter import messagebox, Frame  # for pop up messages
import re  # for email validation function
import psycopg2  # For using link between Postgres Sql and PYTHON
from time import strftime  # For using live clock in Homepage

x = 1

# Database Link PostgresSQL
MyPass = '9515306769'
my_connection = psycopg2.connect(
    database="sanjay_travels",
    user="postgres",
    password=MyPass
)

# Retrieving Sanjay Travels ADMIN password from database it enables the change password function
cur5 = my_connection.cursor()
cur5.execute("SELECT admin_pass FROM admin_password ORDER BY change_time DESC LIMIT 1")
temp_pass = str(cur5.fetchone())
temp_pass = temp_pass.replace("('", '')
temp_pass = temp_pass.replace("',)", '')
admin_real_password = temp_pass

# Windows and Frames
Window = Tk()
Contact_frame = Frame(Window, bg="black", width=1536, height=864)
Customer_email_frame = Frame(Contact_frame, bg="black", width=1536, height=864)
LoginAsCustomerFrame = Frame(Window, bg="black", width=1536, height=864)
CaluclateFrame = Frame(LoginAsCustomerFrame, bg="black", width=1536, height=864)
PassWord_frame = Frame(Window, bg="black", width=1536, height=864)
AdvancedOptionsFrame = Frame(PassWord_frame, bg="black", width=1536, height=864)
AdminPasswordChange_Frame = Frame(AdvancedOptionsFrame, bg="black", width=1536, height=864)
KmCostUpdate_Frame = Frame(AdvancedOptionsFrame, bg="black", width=1536, height=864)
NewDestination_Frame = Frame(AdvancedOptionsFrame, bg="black", width=1536, height=864)

# HomePage (main Window)
Window.state('zoomed')
Window.configure(bg="black", padx=200, pady=20)
Window.title("Sanjay Travels->Lovely Professional University")
Window.minsize(width=1536, height=864)
Header_label = Label(text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34), bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(text="Lovely Professional University,Phagwara, \nPunjab (144411)", font=("Arial", 24, "bold"),
                bg="black", fg="#00FFAB")
address.place(x=210, y=90)
comment = Label(text="We Provide different kinds of vehicles for various purposes from LPU at nominal fare\nSpecially"
                     " for students in LPU.",
                font=("Courier New", 12, "bold"), bg="black", fg="#73777B")
comment.place(x=140, y=650)
text = Label(text="Please select your role below to continue:-", font=("Verdana", 16, "bold"),
             bg="black", fg="#F806CC")
text.place(x=280, y=210)
clock = Label(font=("Courier New", 12, "bold"), bg="black", fg="#73777B")
clock.place(x=770, y=0)


# email validation program
def validate(s):
    pat = "^[a-z0-9-_]+@[a-z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, s):
        return True
    return False


def my_time():
    time_string = strftime("%H:%M:%S\n%A")
    clock.config(text=time_string)
    clock.after(1000, my_time)


def customer():
    LoginAsCustomerFrame.tkraise()
    LoginAsCustomerFrame.pack(fill="both", expand=1)


def admin():
    PassWord_frame.tkraise()
    PassWord_frame.pack(fill="both", expand=1)


def contact():
    Contact_frame.tkraise()
    Contact_frame.pack(fill="both", expand=1)


def okcontinue():
    Customer_email_frame.tkraise()
    Customer_email_frame.pack(fill="both", expand=1)
    print("Pressed Continue")


def oksubmit():
    correctness = validate(customer_email.get())
    if correctness:
        messagebox.showinfo(title="Thanks a lot ! We will contact you soon.",
                            message="Sanjay Kumar Konakandla\nPh.9515306769\n"
                                    "Email:sanjaykumarkonakandla@gmail.com")
        # For sending email id to the database
        cur = my_connection.cursor()
        cur.execute(f"INSERT INTO emails(cust_email,date_time) VALUES ('{customer_email.get()}',CURRENT_TIMESTAMP)")
        my_connection.commit()
        cur.close()


    else:
        if len(customer_email.get()) < 7:
            messagebox.showwarning(title="Sorry:-( You entered invalid email id.",
                                   message=f"The email id size is very shorter\n"
                                           f"Please enter correct email id to get contact details")
        else:
            messagebox.showwarning(title="Sorry:-( You entered invalid email id.",
                                   message=f"{customer_email.get()} is an invalid email id\n"
                                           f"Please enter correct email id to get contact details")
    customer_email.delete(0, END)


def AC6():
    carselected(1)


def NAC6():
    carselected(2)


def AC4():
    carselected(3)


def NAC4():
    carselected(4)


def BUS():
    carselected(5)


def carselected(a):
    global x
    cur3 = my_connection.cursor()
    cur3.execute(f"SELECT cost FROM car_costs WHERE car_type = {a}")
    x = str(cur3.fetchone())
    x = x.replace("(", '')
    x = x.replace(",)", '')
    x = int(x)
    CaluclateFrame.tkraise()
    CaluclateFrame.pack(fill="both", expand=1)


def caluclate_cost(dist):
    global x
    dist = str(dist)
    dist = dist.replace("(", '')
    dist = dist.replace(",)", '')
    dist = int(dist)
    final = x * dist
    global final_cost
    final_cost.configure(text=f"₹ {final} /-")


def destination(dest_name):
    # Formatting as per requirements of query
    our_dest = str(dest_name)
    our_dest = our_dest.replace("('", '')
    our_dest = our_dest.replace("',)", '')
    cur2 = my_connection.cursor()
    cur2.execute(f"SELECT distance FROM distances WHERE dest_name = '{our_dest}'")
    dist = cur2.fetchone()
    caluclate_cost(dist)


def password_entered():
    if admin_pass.get() == admin_real_password:
        AdvancedOptionsFrame.tkraise()
        AdvancedOptionsFrame.pack(fill="both", expand=1)
    else:
        messagebox.showwarning(title="Incorrect Password",
                               message="Please Enter the correct password to get access to Admin options")


def getallmails():
    with open("Customer_Emails_List", mode="w") as file:
        cur4 = my_connection.cursor()
        cur4.execute("SELECT DISTINCT cust_email FROM emails")
        file.write("Customers Emails will be saved below and only distinct emails will be shown\n\n")
        mail_list = cur4.fetchall()
        for m in mail_list:
            m = str(m)
            m = m.replace("('", '')
            m = m.replace("',)", '')
            file.write("\t" + m + "\n")
    done = messagebox.askyesno(title="Saving done !", message="All the customer emails are saved in to the file"
                                                              "named 'Customer_Email_List' in this project folder"
                                                              "\n\n\n\nWould you like to close portal now")
    if done:
        quit()


def changecostsbutton():
    KmCostUpdate_Frame.tkraise()
    KmCostUpdate_Frame.pack(fill="both", expand=1)
    car_6sac.focus()


def update_costs():
    if len(car_6sac.get()) == 0 or len(car_6snac.get()) == 0 or len(car_4sac.get()) == 0 or len(
            car_4snac.get()) == 0 or len(BUS_cost_update.get()) == 0:
        messagebox.showerror(title="Required fields are empty",
                             message="Please enter all the values of the below text boxes even "
                                     "if they are not required to update")
    else:
        new6sac = car_6sac.get()
        new6snac = car_6snac.get()
        new4sac = car_4sac.get()
        new4snac = car_4snac.get()
        newBuscost = BUS_cost_update.get()

        try:
            new6sac = int(new6sac)
            new6snac = int(new6snac)
            new4sac = int(new4sac)
            new4snac = int(new4snac)
            newBuscost = int(newBuscost)

        except ValueError:
            messagebox.showerror(title="Required fields are empty",
                                 message="Please enter all the values in numbers only\n"
                                         "Alphabets and decimals are not allowed")
        else:
            cur9 = my_connection.cursor()
            # UPDATE car_costs SET cost = 45 WHERE car_type = 1
            cur9.execute(f"UPDATE car_costs SET cost = {new6sac} WHERE car_type = 1")
            cur9.execute(f"UPDATE car_costs SET cost = {new6snac} WHERE car_type = 2")
            cur9.execute(f"UPDATE car_costs SET cost = {new4sac} WHERE car_type = 3")
            cur9.execute(f"UPDATE car_costs SET cost = {new4snac} WHERE car_type = 4")
            cur9.execute(f"UPDATE car_costs SET cost = {newBuscost} WHERE car_type = 5")

            my_connection.commit()
            text1.config(text="✔ All costs have been successfully updated", fg="green")
            update_costs_button.config(text="Close", command=quit)


def add_dest_button():
    NewDestination_Frame.tkraise()
    NewDestination_Frame.pack(fill="both", expand=1)
    new_dest_name_entry.focus()


def new_dest_confirm():
    final_new_dest_name = str(new_dest_name_entry.get())
    try:
        final_new_dist = int(new_dist_name_entry.get())
    except ValueError:
        messagebox.showerror(title="All fields are required",
                             message="Please enter all the values in numbers only\n"
                                     "Alphabets and decimals are not allowed in distance")
    else:
        final_new_dest_name = final_new_dest_name.title()
        final_new_dest_name = final_new_dest_name.replace(' ', '_')
        try:
            cur10 = my_connection.cursor()
            cur10.execute(f"INSERT INTO distances(dest_name, distance) VALUES('{final_new_dest_name}',"
                          f"{final_new_dist})")
            my_connection.commit()
        except psycopg2.errors.UniqueViolation:
            messagebox.showerror(title=f"Destination {final_new_dest_name} already exists",
                                 message="Please enter the values of new destinations only.")
        else:
            text.config(text=f"✔✔ New destination {final_new_dest_name} has been added at a "
                             f"distance of {final_new_dist}", fg="green")
            add_dest_confirm_button.config(command=quit, text="Done")



def change_password_button():
    AdminPasswordChange_Frame.tkraise()
    AdminPasswordChange_Frame.pack(fill="both", expand=1)
    new_admin_pass.focus()


def new_pass_confirm():
    cur7 = my_connection.cursor()
    cur7.execute(
        f"INSERT INTO admin_password(admin_pass, change_time) VALUES('{new_admin_pass.get()}', CURRENT_TIMESTAMP)")
    my_connection.commit()
    text2.config(text=f"✔ Password Updated to >> {new_admin_pass.get()}", fg="green")
    confirm_button.config(text="Close", command=quit, padx=0)
    confirm_button.place(x=500, y=450)


my_time()
customer_button = Button(text="Customer", command=customer, bg="black", fg="#FAF3E3",
                         font=("Comic Sans MS", 40, "bold"))
admin_button = Button(text="Admin", command=admin, bg="black", fg="#FAF3E3",
                      font=("Comic Sans MS", 40, "bold"))
contact_button = Button(text="Contact Us !", command=contact, bg="black", fg="#FAF3E3",
                        font=("Comic Sans MS", 16, "bold"), padx=200)
close_button = Button(text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
customer_button.place(x=260, y=250)
admin_button.place(x=600, y=250)
contact_button.place(x=260, y=450)

# Contact frame
Header_label = Label(Contact_frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(Contact_frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
text = Label(Contact_frame, text="You have to give your email id to get contact details.", font=("Verdana", 16, "bold"),
             bg="black", fg="#F806CC")
text.place(x=210, y=180)
continue_button = Button(Contact_frame, text="OK, Continue", command=okcontinue, bg="black", fg="#FAF3E3",
                         font=("Comic Sans MS", 16, "bold"), padx=200)
continue_button.place(x=260, y=250)
close_button = Button(Contact_frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)

# Customer Email Frame
Header_label = Label(Customer_email_frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(Customer_email_frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
text = Label(Customer_email_frame, text="Please provide your email below.", font=("Verdana", 16, "bold"),
             bg="black", fg="#FF9F29")
text.place(x=210, y=300)
customer_email = Entry(Customer_email_frame, width=41, bg="black", fg="#FAF3E3", insertbackground="white",
                       font=("Times New Roman", 24, "bold"), )

customer_email.place(x=210, y=360)
customer_email.focus()

submit_button = Button(Customer_email_frame, text="Submit", command=oksubmit, bg="black", fg="#FAF3E3",
                       font=("Comic Sans MS", 16, "bold"), padx=200)
submit_button.place(x=260, y=450)
close_button = Button(Customer_email_frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
# Login As Customer Frame
Header_label = Label(LoginAsCustomerFrame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(LoginAsCustomerFrame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
welcome = Label(LoginAsCustomerFrame, text="Welcome !\nPlease select your choice below",
                font=("Adlery Pro", 36, "bold"),
                bg="black", fg="#E0DECA")
welcome.place(x=270, y=200)
seater6ACcar = Button(LoginAsCustomerFrame, text="6-Seater A/C", command=AC6, bg="black", fg="white",
                      font=("Gloss And Bloom", 20))
seater6car = Button(LoginAsCustomerFrame, text="6-Seater", command=NAC6, bg="black", fg="white",
                    font=("Gloss And Bloom", 20))
seater4ACcar = Button(LoginAsCustomerFrame, text="4-Seater A/C", command=AC4, bg="black", fg="white",
                      font=("Gloss And Bloom", 20))
seater4car = Button(LoginAsCustomerFrame, text="4-Seater", command=NAC4, bg="black", fg="white",
                    font=("Gloss And Bloom", 20))
miniBus = Button(LoginAsCustomerFrame, text="Mini Bus 30-Seater", command=BUS, bg="black", fg="white",
                 font=("Gloss And Bloom", 20), padx=63)
close_button = Button(LoginAsCustomerFrame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")

close_button.place(x=900, y=0)
seater6car.place(x=590, y=300)
seater6ACcar.place(x=320, y=300)
seater4car.place(x=590, y=420)
seater4ACcar.place(x=320, y=420)
miniBus.place(x=320, y=540)

# Caluclate Frame
cur1 = my_connection.cursor()
cur1.execute("SELECT dest_name FROM distances")
dest_options = cur1.fetchall()
clicked = StringVar()
clicked.set("Select here")
drop = OptionMenu(CaluclateFrame, clicked, *dest_options, command=destination)
drop.config(font=("Times New Roman", 20), bg="black", fg="#FAEA48")
drop.place(x=565, y=345)
cur1.close()

Header_label = Label(CaluclateFrame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(CaluclateFrame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
choose_dest_text = Label(CaluclateFrame, text="Available !\nPlease select your destination below",
                         font=("Gloss And Bloom", 26, "bold"), bg="black", fg="red")
choose_dest_text.place(x=240, y=170)
close_button = Button(text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
dest_text = Label(CaluclateFrame, text="Destination: ", font=("Gloss And Bloom", 36, "bold"), bg="black", fg="gray")
dest_text.place(x=270, y=320)
close_button = Button(CaluclateFrame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
terms = Label(CaluclateFrame, text="*This is expected cost only.Real cost may slightly vary. Contact us for exact cost."
                                   "\nThank You.", font=("Courier New", 12, "bold"), bg="black", fg="#73777B")
terms.place(x=170, y=650)
estim_text = Label(CaluclateFrame, text="Estimation: ", font=("Gloss And Bloom", 36, "bold"), bg="black", fg="gray")
estim_text.place(x=280, y=420)
final_cost = Label(CaluclateFrame, text="₹ 0/-", font=("Gloss And Bloom", 36, "bold"), bg="black", fg="#0af3f7")
final_cost.place(x=560, y=420)
close_button = Button(CaluclateFrame, text="Ok, Close", command=quit, bg="black", fg="white",
                      font=("Comic Sans MS", 20, "bold"), padx=10, activebackground="gray")
close_button.place(x=750, y=550)

# PassWord Frame
Header_label = Label(PassWord_frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(PassWord_frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
text = Label(PassWord_frame, text="Please provide Administrator password to continue", font=("Verdana", 16, "bold"),
             bg="black", fg="#FF9F29")
text.place(x=210, y=300)
admin_pass = Entry(PassWord_frame, width=41, bg="black", fg="#FAF3E3", insertbackground="white",
                   font=("Times New Roman", 24, "bold"), show="●")

admin_pass.place(x=210, y=360)
admin_pass.focus()

submit_button = Button(PassWord_frame, text="Submit", command=password_entered, bg="black", fg="#FAF3E3",
                       font=("Comic Sans MS", 16, "bold"), padx=200)
submit_button.place(x=260, y=450)
close_button = Button(PassWord_frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)

# Advanced Options Frame
Header_label = Label(AdvancedOptionsFrame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(AdvancedOptionsFrame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
close_button = Button(AdvancedOptionsFrame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
email_list_button = Button(AdvancedOptionsFrame, text="Save customers E-mail List", command=getallmails, bg="black",
                           fg="gray", font=("Comic Sans MS", 26, "bold"))
email_list_button.place(x=300, y=220)
change_cost_button = Button(AdvancedOptionsFrame, text="Change PerKm Cost", command=changecostsbutton, bg="black",
                            fg="gray", font=("Comic Sans MS", 26, "bold"))
change_cost_button.place(x=370, y=340)
add_destination_button = Button(AdvancedOptionsFrame, text="Add a new Destination", command=add_dest_button, bg="black",
                                fg="gray", font=("Comic Sans MS", 26, "bold"))
add_destination_button.place(x=345, y=460)
change_cost_button = Button(AdvancedOptionsFrame, text="Change Admin password", command=change_password_button,
                            bg="black", fg="gray", font=("Comic Sans MS", 26, "bold"))
change_cost_button.place(x=335, y=580)

# Admin Password Change Frame
Header_label = Label(AdminPasswordChange_Frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(AdminPasswordChange_Frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
close_button = Button(AdminPasswordChange_Frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
text2 = Label(AdminPasswordChange_Frame, text="Please enter the new password you want to choose",
              font=("Verdana", 16, "bold"), bg="black", fg="#FF9F29")
text2.place(x=210, y=300)
new_admin_pass = Entry(AdminPasswordChange_Frame, width=41, bg="black", fg="#FAF3E3", insertbackground="white",
                       font=("Times New Roman", 24, "bold"))

new_admin_pass.place(x=210, y=360)
confirm_button = Button(AdminPasswordChange_Frame, text="Confirm", command=new_pass_confirm, bg="black", fg="#FAF3E3",
                        font=("Comic Sans MS", 16, "bold"), padx=200)
confirm_button.place(x=260, y=450)

# Km Cost Update_Frame
Header_label = Label(KmCostUpdate_Frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(KmCostUpdate_Frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
close_button = Button(KmCostUpdate_Frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
text1 = Label(KmCostUpdate_Frame, text="Please update your costs below\n **All fields are required",
              font=("Verdana", 16, "bold"), bg="black", fg="#FF9F29")
text1.place(x=210, y=200)
cars_text = Label(KmCostUpdate_Frame, text="6SAC:\n\n6SNAC:\n\n4SAC:\n\n4SNAC:\n\nBUS:",
                  font=("Verdana", 16, "bold"), bg="black", fg="#F806CC")
cars_text.place(x=210, y=300)
car_6sac = Entry(KmCostUpdate_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                 insertbackground="white")
car_6sac.place(x=315, y=300)
car_6snac = Entry(KmCostUpdate_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                  insertbackground="white")
car_6snac.place(x=315, y=349)
car_4sac = Entry(KmCostUpdate_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                 insertbackground="white")
car_4sac.place(x=315, y=398)
car_4snac = Entry(KmCostUpdate_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                  insertbackground="white")
car_4snac.place(x=315, y=447)
BUS_cost_update = Entry(KmCostUpdate_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                        insertbackground="white")
BUS_cost_update.place(x=315, y=496)
update_costs_button = Button(KmCostUpdate_Frame, text="Update", command=update_costs, bg="red", fg="#FAF3E3",
                             font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
update_costs_button.place(x=700, y=447)

# New Destination Frame
Header_label = Label(NewDestination_Frame, text="🚗 Sanjay Travels 🚘", font=("Gloss And Bloom", 34),
                     bg="black", fg="#34B3F1")
Header_label.place(x=265, y=0)
address = Label(NewDestination_Frame, text="Lovely Professional University,Phagwara, \nPunjab (144411)",
                font=("Arial", 24, "bold"), bg="black", fg="#00FFAB")
address.place(x=210, y=90)
close_button = Button(NewDestination_Frame, text="X", command=quit, bg="red", fg="#FAF3E3",
                      font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
close_button.place(x=900, y=0)
text = Label(NewDestination_Frame, text="Add the details below to insert new destination",
             font=("Verdana", 16, "bold"), bg="black", fg="#FF9F29")
text.place(x=210, y=200)
new_dest_text = Label(NewDestination_Frame, text="Destination name: ", font=("Verdana", 16, "bold"),
                      bg="black", fg="#DFF6FF")
new_dest_text.place(x=210, y=300)
new_dest_name_entry = Entry(NewDestination_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                            insertbackground="white")
new_dest_name_entry.place(x=440, y=300)
new_dist_text = Label(NewDestination_Frame, text="Distance: ", font=("Verdana", 16, "bold"),
                      bg="black", fg="#DFF6FF")
new_dist_text.place(x=316, y=350)
new_dist_name_entry = Entry(NewDestination_Frame, width=20, bg="black", fg="white", font=("Arial Black", 16, "bold"),
                            insertbackground="white")
new_dist_name_entry.place(x=440, y=350)
add_dest_confirm_button = Button(NewDestination_Frame, text="Add", command=new_dest_confirm, bg="red", fg="#FAF3E3",
                                 font=("Comic Sans MS", 10, "bold"), padx=10, activebackground="gray")
add_dest_confirm_button.place(x=670, y=400)
comment2 = Label(NewDestination_Frame,
                 text="Duplicate values are not allowed,\nPlease view the already available list in customer section.",
                 font=("Courier New", 12, "bold"), bg="black", fg="#73777B")
comment2.place(x=240, y=500)
Window.mainloop()