import tkinter as tk
from pypresence import Presence
import threading
import time
from tkinter import messagebox

class DiscordRPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord RPC Creator")
        self.root.geometry("302x451")
        self.root.configure(bg="#36393F")  
        self.root.iconbitmap("app.ico")  

        self.create_entry("Your Client ID", entry_var="client_id_entry")
        self.create_entry("Details (Line 1)", entry_var="details_entry")
        self.create_entry("State (Line 2)", entry_var="state_entry")
        self.create_entry("Big Image URL", entry_var="large_image_entry")
        self.create_entry("Big Image Tooltip", entry_var="large_text_entry")
        self.create_entry("Small Image URL", entry_var="small_image_entry")
        self.create_entry("Small Image Tooltip", entry_var="small_text_entry")

        self.create_entry("Button 1 Label", entry_var="button1_label_entry")
        self.create_entry("Button 1 URL", entry_var="button1_url_entry")
        self.create_entry("Button 2 Label", entry_var="button2_label_entry")
        self.create_entry("Button 2 URL", entry_var="button2_url_entry")

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_rpc, bg="#4CAF50", fg="white", width=15)
        self.connect_button.pack(pady=10)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect_rpc, state=tk.DISABLED, bg="#F44336", fg="white", width=15)
        self.disconnect_button.pack(pady=10)

        self.presence_label = tk.Label(self.root, text="Status: Not Connected", bg="#36393F", fg="white")
        self.presence_label.pack(pady=10)

        self.rpc = None
        self.connected = False

    def create_entry(self, placeholder, entry_var):
        entry = tk.Entry(self.root, width=30)
        entry.insert(0, placeholder)
        entry.pack(pady=5)
        setattr(self, entry_var, entry)

    def connect_rpc(self):
        client_id = self.client_id_entry.get()

        if client_id:
            try:
                self.rpc = Presence(client_id)
                self.rpc.connect()
                self.connected = True

                self.presence_label.config(text="Status: Connected!", fg="#4CAF50")
                self.connect_button.config(state=tk.DISABLED, bg="#888888")
                self.disconnect_button.config(state=tk.NORMAL, bg="#F44336")

                threading.Thread(target=self.update_presence_thread).start()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error connecting to Discord: {str(e)}")
        else:
            tk.messagebox.showerror("Error", "Please enter a valid client ID.")

    def disconnect_rpc(self):
        if self.connected:
            self.connected = False
            if self.rpc:
                try:
                    self.rpc.close()
                except Exception as e:
                    print(f"Error closing Discord connection: {str(e)}")
                finally:
                    self.rpc = None

            self.presence_label.config(text="Status: Not Connected", fg="#F44336")
            self.connect_button.config(state=tk.NORMAL, bg="#4CAF50")
            self.disconnect_button.config(state=tk.DISABLED, bg="#888888")

    def update_presence_thread(self):
        while self.connected:
            try:
                buttons = [
                    {
                        'label': self.button1_label_entry.get(),
                        'url': self.button1_url_entry.get(),
                    },
                    {
                        'label': self.button2_label_entry.get(),
                        'url': self.button2_url_entry.get(),
                    }
                ]

                if self.connected:
                    self.rpc.update(
                        details=self.details_entry.get(),
                        state=self.state_entry.get(),
                        large_image=self.large_image_entry.get(),
                        large_text=self.large_text_entry.get(),
                        small_image=self.small_image_entry.get(),
                        small_text=self.small_text_entry.get(),
                        buttons=buttons
                    )
                time.sleep(15) 
            except Exception as e:
                print(f"Error updating presence: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordRPCApp(root)
    root.withdraw()  
    root.update_idletasks()  
    width = root.winfo_width()
    height = root.winfo_height()
    x_pos = (root.winfo_screenwidth() // 2) - (width // 2)
    y_pos = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x_pos, y_pos))
    root.deiconify()  
    root.mainloop()
    print(f"Button 1 URL: {self.button1_url_entry.get()}")
    print(f"Button 2 URL: {self.button2_url_entry.get()}")
