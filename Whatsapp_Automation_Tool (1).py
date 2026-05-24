import customtkinter as ctk
import pywhatkit
import pandas as pd
from tkinter import filedialog
from datetime import datetime
from PIL import Image
import schedule
import threading
import time
import hashlib
import json

ctk.set_appearance_mode("dark")

# ================= SECURITY =================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ================= USERS FILE =================

try:

    with open("users.json","r") as f:
        pass

except:

    default_data = {

        "users":[
            {
                "username":"admin",
                "password":hash_password("1234"),
                "profile_pic":"profile.png"
            }
        ],

        "remember_me":""
    }

    with open("users.json","w") as f:

        json.dump(
            default_data,
            f,
            indent=4
        )


# ================= LOGIN =================

login_app = ctk.CTk()

login_app.geometry("450x650")

login_app.title("Login")


login_title = ctk.CTkLabel(
    login_app,
    text="WhatsApp Automation Login",
    font=("Arial",26,"bold")
)

login_title.pack(pady=20)


# ================= PROFILE IMAGE =================

try:

    profile_image = ctk.CTkImage(
        light_image=Image.open("profile.png"),
        dark_image=Image.open("profile.png"),
        size=(120,120)
    )

    profile_label = ctk.CTkLabel(
        login_app,
        image=profile_image,
        text=""
    )

    profile_label.pack(pady=10)

except:
    pass


username_entry = ctk.CTkEntry(
    login_app,
    placeholder_text="Username",
    width=250
)

username_entry.pack(pady=10)


password_entry = ctk.CTkEntry(
    login_app,
    placeholder_text="Password",
    show="*",
    width=250
)

password_entry.pack(pady=10)


remember_var = ctk.StringVar(
    value="off"
)

remember_check = ctk.CTkCheckBox(
    login_app,
    text="Remember Me",
    variable=remember_var,
    onvalue="on",
    offvalue="off"
)

remember_check.pack(pady=10)


login_status = ctk.CTkLabel(
    login_app,
    text=""
)

login_status.pack(pady=10)


# ================= MAIN APP =================

def open_main_app(username):

    app = ctk.CTk()

    app.geometry("950x750")

    app.title("WhatsApp Automation")

    csv_path = ""
    stop_sending = False
    attachment_path = ""

    main_frame = ctk.CTkScrollableFrame(
        app,
        width=900,
        height=700
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ================= TITLE =================

    title = ctk.CTkLabel(
        main_frame,
        text="WhatsApp Automation Dashboard",
        font=("Arial",30,"bold")
    )

    title.pack(pady=(20,10))


    user_label = ctk.CTkLabel(
        main_frame,
        text=f"Logged in as: {username}",
        font=("Arial",15)
    )

    user_label.pack(pady=(0,15))


    clock_label = ctk.CTkLabel(
        main_frame,
        text="",
        font=("Arial",14)
    )

    clock_label.pack(pady=(0,20))


    # ================= CLOCK =================
    def update_clock():

        if not app.winfo_exists():
            return

        current = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        clock_label.configure(
            text=current
        )

        app.after(
            1000,
            update_clock
        )


    # ================= THEME =================

    theme_label = ctk.CTkLabel(
        main_frame,
        text="Theme"
    )

    theme_label.pack(pady=(10,5))


    theme_menu = ctk.CTkOptionMenu(
        main_frame,
        values=["Dark","Light"],
        command=lambda mode:
        ctk.set_appearance_mode(
            mode.lower()
        )
    )

    theme_menu.pack(pady=10)


    # ================= CSV =================

    def upload_csv():

        nonlocal csv_path

        csv_path = filedialog.askopenfilename(
            filetypes=[("CSV Files","*.csv")]
        )

        if csv_path:

            data = pd.read_csv(
                csv_path,
                dtype=str
            )

            total_label.configure(
                text=f"Contacts: {len(data)}"
            )

            file_label.configure(
                text=f"Loaded: {csv_path.split('/')[-1]}"
            )

            preview_box.delete(
                "1.0",
                "end"
            )

            for index,row in data.head(5).iterrows():

                preview_box.insert(
                    "end",
                    f"{row['Name']} - {row['Number']}\n"
                )


    file_btn = ctk.CTkButton(
        main_frame,
        text="Upload Contacts CSV",
        command=upload_csv
    )

    file_btn.pack(pady=15)


    file_label = ctk.CTkLabel(
        main_frame,
        text="No file selected"
    )

    file_label.pack(pady=5)


    total_label = ctk.CTkLabel(
        main_frame,
        text="Contacts: 0"
    )

    total_label.pack(pady=(0,15))


    # ================= ATTACHMENT =================

    def upload_attachment():

        nonlocal attachment_path

        attachment_path = filedialog.askopenfilename()

        if attachment_path:

            attachment_label.configure(
                text=attachment_path.split("/")[-1]
            )


    attachment_btn = ctk.CTkButton(
        main_frame,
        text="Upload Attachment",
        command=upload_attachment
    )

    attachment_btn.pack(pady=10)


    attachment_label = ctk.CTkLabel(
        main_frame,
        text="No attachment selected"
    )

    attachment_label.pack()


    # ================= SEARCH =================

    search_entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="Search Contact"
    )

    search_entry.pack(pady=10)


    def search_contact():

        if csv_path == "":
            return

        search = search_entry.get()

        data = pd.read_csv(
            csv_path,
            dtype=str
        )

        result = data[
            data["Name"].str.contains(
                search,
                case=False
            )
        ]

        status_label.configure(
            text=f"Found {len(result)} contact(s)"
        )


    search_btn = ctk.CTkButton(
        main_frame,
        text="Search",
        command=search_contact
    )

    search_btn.pack()


    # ================= PREVIEW =================

    preview_box = ctk.CTkTextbox(
        main_frame,
        width=450,
        height=100
    )

    preview_box.pack(pady=10)


    # ================= TEMPLATES =================

    templates = {

        "Birthday":
        "Happy Birthday! Have an amazing day 🎉",

        "Meeting":
        "Reminder: Meeting starts in 30 minutes.",

        "Good Morning":
        "Good Morning! Hope you have a productive day ☀️"
    }


    def load_template(choice):

        message_entry.delete(
            "1.0",
            "end"
        )

        message_entry.insert(
            "1.0",
            templates[choice]
        )


    template_menu = ctk.CTkOptionMenu(
        main_frame,
        values=list(templates.keys()),
        command=load_template
    )

    template_menu.pack(pady=15)


    # ================= EMOJIS =================

    emoji_label = ctk.CTkLabel(
        main_frame,
        text="Quick Emojis"
    )

    emoji_label.pack(pady=(10,5))


    emoji_frame = ctk.CTkFrame(
        main_frame
    )

    emoji_frame.pack(pady=10)


    def add_emoji(emoji):

        message_entry.insert(
            "end",
            " " + emoji
        )


    emoji_list = [
        "😀",
        "🎉",
        "❤️",
        "🚀",
        "👍",
        "😊",
        "🔥"
    ]


    for emoji in emoji_list:

        btn = ctk.CTkButton(
            emoji_frame,
            text=emoji,
            width=50,
            height=40,
            font=("Segoe UI Emoji",18),
            command=lambda e=emoji:
            add_emoji(e)
        )

        btn.pack(
            side="left",
            padx=5
        )


    # ================= MESSAGE =================

    message_entry = ctk.CTkTextbox(
        main_frame,
        width=600,
        height=180
    )

    message_entry.pack(pady=20)


    # ================= TIME =================

    time_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )

    time_frame.pack(pady=20)


    hour_entry = ctk.CTkEntry(
        time_frame,
        placeholder_text="Hour",
        width=100
    )

    hour_entry.pack(
        side="left",
        padx=10
    )


    min_entry = ctk.CTkEntry(
        time_frame,
        placeholder_text="Minute",
        width=100
    )

    min_entry.pack(
        side="left",
        padx=10
    )


    group_entry = ctk.CTkEntry(
        time_frame,
        placeholder_text="Group ID",
        width=200
    )

    group_entry.pack(
        side="left",
        padx=10
    )


    # ================= STATUS =================

    status_label = ctk.CTkLabel(
        main_frame,
        text="Status: Waiting"
    )

    status_label.pack(pady=10)


    progress = ctk.CTkProgressBar(
        main_frame,
        width=500
    )

    progress.pack(pady=15)

    progress.set(0)


    # ================= REPEAT =================

    repeat_menu = ctk.CTkOptionMenu(
        main_frame,
        values=[
            "Once",
            "Daily",
            "Weekly",
            "Monthly"
        ]
    )

    repeat_menu.pack(pady=10)


    # ================= POPUP =================

    def show_popup():

        popup = ctk.CTkToplevel()

        popup.geometry("300x150")

        popup.title("Completed")

        label = ctk.CTkLabel(
            popup,
            text="✓ Messages Sent Successfully",
            font=("Arial",16)
        )

        label.pack(pady=40)


    # ================= STOP =================

    def stop_messages():

        nonlocal stop_sending

        stop_sending = True

        status_label.configure(
            text="Sending stopped"
        )


    # ================= SEND =================

    def send_bulk():

        nonlocal stop_sending

        stop_sending = False

        if csv_path == "":

            status_label.configure(
                text="Upload CSV First"
            )

            return


        msg = message_entry.get(
            "1.0",
            "end"
        ).strip()


        if msg == "":

            status_label.configure(
                text="Enter Message"
            )

            return


        data = pd.read_csv(
            csv_path,
            dtype=str
        )

        data = data.drop_duplicates(
            subset=["Number"]
        )


        hour = int(hour_entry.get())

        minute = int(min_entry.get())

        total = len(data)


        status_label.configure(
            text="Sending..."
        )


        for index,row in data.iterrows():

            if stop_sending:

                status_label.configure(
                    text="Process Cancelled"
                )

                break


            try:

                name = row["Name"]

                number = str(
                    row["Number"]
                ).strip()


                if not number.startswith("+"):
                    number = "+91" + number


                personalized_msg = f"""
Hello {name},

{msg}

Regards,
{username}
"""


                pywhatkit.sendwhatmsg(
                    number,
                    personalized_msg,
                    hour,
                    minute
                )


                with open(
                    "logs.txt",
                    "a"
                ) as f:

                    f.write(
                        f"{datetime.now()} : Sent to {name} ({number})\n"
                    )


                progress.set(
                    (index+1)/total
                )

                app.update()

                minute += 2


            except Exception as e:

                print(e)


        status_label.configure(
            text="Completed"
        )

        show_popup()


    # ================= GROUP =================

    def send_group():

        group_id = group_entry.get()

        msg = message_entry.get(
            "1.0",
            "end"
        ).strip()


        hour = int(hour_entry.get())

        minute = int(min_entry.get())


        pywhatkit.sendwhatmsg_to_group(
            group_id,
            msg,
            hour,
            minute
        )


    # ================= EXPORT =================

    def export_logs():

        try:

            data = pd.read_csv(
                "logs.txt",
                sep=":",
                header=None
            )

            data.to_excel(
                "message_history.xlsx",
                index=False
            )

            status_label.configure(
                text="Logs Exported"
            )

        except:

            status_label.configure(
                text="No Logs Found"
            )


    # ================= RECURRING =================

    def recurring_send():

        while True:

            schedule.run_pending()

            time.sleep(1)


    def send_or_schedule():

        repeat_type = repeat_menu.get()

        if repeat_type == "Once":

            send_bulk()

        elif repeat_type == "Daily":

            schedule.every().day.at(
                f"{hour_entry.get()}:{min_entry.get()}"
            ).do(send_bulk)

        elif repeat_type == "Weekly":

            schedule.every().week.do(
                send_bulk
            )

        elif repeat_type == "Monthly":

            schedule.every(30).days.do(
                send_bulk
            )

        status_label.configure(
            text=f"{repeat_type} Schedule Started"
        )


    # ================= BUTTONS =================

    button_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )

    button_frame.pack(pady=25)


    send_btn = ctk.CTkButton(
        button_frame,
        text="Send / Schedule",
        command=send_or_schedule
    )

    send_btn.pack(
        side="left",
        padx=10
    )


    group_btn = ctk.CTkButton(
        button_frame,
        text="Group Send",
        command=send_group
    )

    group_btn.pack(
        side="left",
        padx=10
    )


    stop_btn = ctk.CTkButton(
        button_frame,
        text="Stop Sending",
        fg_color="red",
        hover_color="darkred",
        command=stop_messages
    )

    stop_btn.pack(
        side="left",
        padx=10
    )


    export_btn = ctk.CTkButton(
        button_frame,
        text="Export Logs",
        command=export_logs
    )

    export_btn.pack(
        side="left",
        padx=10
    )


    threading.Thread(
        target=recurring_send,
        daemon=True
    ).start()

    def on_closing():
        try:
            app.quit()
            app.destroy()
        except:
            pass

    app.protocol(
        "WM_DELETE_WINDOW",
        on_closing
    )
    app.mainloop()


# ================= LOGIN =================

def login():

    username = username_entry.get()

    password = hash_password(
        password_entry.get()
    )

    with open("users.json","r") as f:

        users_data = json.load(f)


    for user in users_data["users"]:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):

            if remember_var.get() == "on":

                users_data["remember_me"] = username

                with open(
                    "users.json",
                    "w"
                ) as fw:

                    json.dump(
                        users_data,
                        fw,
                        indent=4
                    )

            login_app.destroy()

            open_main_app(username)

            return


    login_status.configure(
        text="Invalid Credentials"
    )


# ================= REGISTER =================

def register_user():

    username = username_entry.get()

    password = hash_password(
        password_entry.get()
    )

    with open("users.json","r") as f:

        users_data = json.load(f)


    for user in users_data["users"]:

        if user["username"] == username:

            login_status.configure(
                text="User already exists"
            )

            return


    users_data["users"].append({

        "username": username,

        "password": password,

        "profile_pic": "profile.png"

    })


    with open(
        "users.json",
        "w"
    ) as fw:

        json.dump(
            users_data,
            fw,
            indent=4
        )


    login_status.configure(
        text="User Registered"
    )


# ================= REMEMBER ME =================

with open("users.json","r") as f:

    users_data = json.load(f)

remembered_user = users_data.get(
    "remember_me",
    ""
)

if remembered_user != "":

    username_entry.insert(
        0,
        remembered_user
    )

    remember_check.select()


# ================= BUTTONS =================

login_btn = ctk.CTkButton(
    login_app,
    text="Login",
    command=login
)

login_btn.pack(pady=15)


register_btn = ctk.CTkButton(
    login_app,
    text="Register",
    command=register_user
)

register_btn.pack(pady=10)

login_app.mainloop()