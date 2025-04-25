import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd


class SplitExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Split Expense App")
        self.geometry("800x600")

        # Data structures
        self.people = []  # list of people's names
        self.items = []  # list of items; each item is a dict with description, cost, tax, payer, participants

        # Frames
        self.create_people_frame()
        self.create_item_frame()
        self.create_action_frame()

    def create_people_frame(self):
        frame = ttk.LabelFrame(self, text="People")
        frame.pack(fill=tk.X, padx=10, pady=10)

        # Entry to add person
        self.person_entry = ttk.Entry(frame, width=30)
        self.person_entry.pack(side=tk.LEFT, padx=5, pady=5)

        add_button = ttk.Button(frame, text="Add Person", command=self.add_person)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        # List of added people
        self.people_listbox = tk.Listbox(frame, height=5)
        self.people_listbox.pack(fill=tk.X, padx=5, pady=5)

    def add_person(self):
        name = self.person_entry.get().strip()
        if not name:
            messagebox.showwarning("Input error", "Please enter a name.")
            return
        if name in self.people:
            messagebox.showwarning("Duplicate", "This person is already added.")
            return
        self.people.append(name)
        self.people_listbox.insert(tk.END, name)
        self.person_entry.delete(0, tk.END)
        self.update_people_in_item_section()

    def create_item_frame(self):
        self.item_frame = ttk.LabelFrame(self, text="Add Item")
        self.item_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Item description and cost/tax entries
        top_frame = ttk.Frame(self.item_frame)
        top_frame.pack(pady=5, fill=tk.X)

        ttk.Label(top_frame, text="Description:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.desc_entry = ttk.Entry(top_frame, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(top_frame, text="Cost:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.cost_entry = ttk.Entry(top_frame, width=20)
        self.cost_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Label(top_frame, text="Tax (optional):").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.tax_entry = ttk.Entry(top_frame, width=20)
        self.tax_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)

        # Section for selecting participating people checkboxes
        self.participants_frame = ttk.LabelFrame(self.item_frame, text="Select Participants")
        self.participants_frame.pack(fill=tk.X, padx=5, pady=5)
        self.participant_vars = {}  # Will hold BooleanVar for each person

        # Section for selecting the payer
        payer_frame = ttk.Frame(self.item_frame)
        payer_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(payer_frame, text="Select Payer:").pack(side=tk.LEFT, padx=5)
        self.payer_var = tk.StringVar()
        self.payer_menu = ttk.OptionMenu(payer_frame, self.payer_var, None)
        self.payer_menu.pack(side=tk.LEFT, padx=5)

        # Button to add item
        add_item_button = ttk.Button(self.item_frame, text="Add Item", command=self.add_item)
        add_item_button.pack(pady=10)

    def update_people_in_item_section(self):
        # Clear old checkboxes
        for widget in self.participants_frame.winfo_children():
            widget.destroy()
        self.participant_vars = {}

        for person in self.people:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.participants_frame, text=person, variable=var)
            chk.pack(side=tk.LEFT, padx=5, pady=2)
            self.participant_vars[person] = var

        # Update payer OptionMenu
        menu = self.payer_menu["menu"]
        menu.delete(0, "end")
        for person in self.people:
            menu.add_command(label=person, command=lambda p=person: self.payer_var.set(p))
        if self.people and self.payer_var.get() not in self.people:
            self.payer_var.set(self.people[0])

    def add_item(self):
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showwarning("Input error", "Please enter an item description.")
            return

        try:
            cost = float(self.cost_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Input error", "Please enter a valid cost.")
            return

        # Allow tax to be empty; default to 0 if blank.
        tax_str = self.tax_entry.get().strip()
        try:
            tax = float(tax_str) if tax_str else 0.0
        except ValueError:
            messagebox.showwarning("Input error", "Please enter a valid tax amount (or leave empty).")
            return

        # Check participants selection
        selected_participants = [p for p, var in self.participant_vars.items() if var.get()]
        if not selected_participants:
            messagebox.showwarning("Selection error", "Please select at least one participant for the item.")
            return

        # Validate payer selection
        payer = self.payer_var.get()
        if payer not in self.people:
            messagebox.showwarning("Selection error", "Please select a valid payer from the list of people.")
            return

        # Save item data into our list
        item = {
            "description": description,
            "cost": cost,
            "tax": tax,
            "payer": payer,
            "participants": selected_participants
        }
        self.items.append(item)

        # Clear the item entries
        self.desc_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        for var in self.participant_vars.values():
            var.set(False)

        messagebox.showinfo("Item added", f"Item '{description}' added successfully!")

    def create_action_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=10)

        export_button = ttk.Button(frame, text="Export Items & Summary to Excel", command=self.export_to_excel)
        export_button.pack(side=tk.LEFT, padx=5)

        summary_button = ttk.Button(frame, text="Show Summary", command=self.show_summary)
        summary_button.pack(side=tk.LEFT, padx=5)

    def export_to_excel(self):
        if not self.items:
            messagebox.showwarning("No items", "No items have been added to export.")
            return

        # Prepare detailed items data
        items_data = []
        for item in self.items:
            items_data.append({
                "Description": item["description"],
                "Cost": item["cost"],
                "Tax": item["tax"],
                "Total": item["cost"] + item["tax"],
                "Payer": item["payer"],
                "Participants": ", ".join(item["participants"])
            })
        df_items = pd.DataFrame(items_data)

        # Compute summary (for each item, divide total cost among non-payer participants)
        # We collect transactions as: (payer, participant, amount)
        transactions = []
        for item in self.items:
            total = item["cost"] + item["tax"]
            num_participants = len(item["participants"])
            if num_participants == 0:
                continue
            share = total / num_participants
            for person in item["participants"]:
                if person != item["payer"]:
                    transactions.append({
                        "Item": item["description"],
                        "From": person,
                        "To": item["payer"],
                        "Amount": share
                    })

        df_transactions = pd.DataFrame(transactions)

        # Save to Excel: two sheets "Items" and "Summary"
        output_file = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not output_file:
            return  # User cancelled
        with pd.ExcelWriter(output_file) as writer:
            df_items.to_excel(writer, sheet_name="Items", index=False)
            df_transactions.to_excel(writer, sheet_name="Summary", index=False)
        messagebox.showinfo("Exported", f"Data exported successfully to {output_file}")

    def show_summary(self):
        # Compute and display summary in a new window.
        # This summary calculates net amounts for each person.
        # For each transaction (from -> to, amount), calculate net pay amounts.
        net = {person: 0 for person in self.people}
        details = ""
        for item in self.items:
            total = item["cost"] + item["tax"]
            num_participants = len(item["participants"])
            share = total / num_participants if num_participants > 0 else 0
            details += f"Item: {item['description']}\n"
            details += f"  Total: {total:.2f}, Share per person: {share:.2f}\n"
            details += f"  Payer: {item['payer']}\n"
            for person in item["participants"]:
                if person == item["payer"]:
                    details += f"    {person} (payer)\n"
                else:
                    details += f"    {person} owes {share:.2f} to {item['payer']}\n"
                    net[person] -= share
                    net[item["payer"]] += share
            details += "\n"

        details += "Net Balances:\n"
        for person, amount in net.items():
            details += f"  {person}: {amount:.2f}\n"

        summary_window = tk.Toplevel(self)
        summary_window.title("Expense Summary")
        text = tk.Text(summary_window, width=80, height=25)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, details)
        text.config(state=tk.DISABLED)


def main():
    app = SplitExpenseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
