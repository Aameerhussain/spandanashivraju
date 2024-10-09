import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

class PDFSummarizer:
    def __init__(self, master):
        self.master = master
        master.title("PDF Summarizer")

        self.label = tk.Label(master, text="Upload a PDF and enter a heading to search.")
        self.label.pack()

        self.upload_button = tk.Button(master, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack()

        self.search_label = tk.Label(master, text="Search Heading:")
        self.search_label.pack()

        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_heading)
        self.search_button.pack()

        self.output_text = tk.Text(master, height=15, width=60)
        self.output_text.pack()

        self.pdf_file = None

    def upload_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not self.pdf_file:
            messagebox.showwarning("Warning", "Please select a PDF file.")

    def search_heading(self):
        if not self.pdf_file or not self.search_entry.get():
            messagebox.showwarning("Warning", "Please upload a PDF and enter a heading to search.")
            return

        heading = self.search_entry.get()
        results = self.extract_text_and_search(heading)

        if results:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "\n".join(results))
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f'No heading "{heading}" found in the PDF.')

    def extract_text_and_search(self, heading):
        results = []
        with open(self.pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                text = page.extract_text()

                if heading.lower() in text.lower():
                    results.append(f'--- Page {i + 1} ---\n{text}')

        return results

if __name__ == "__main__":
    root = tk.Tk()
    pdf_summarizer = PDFSummarizer(root)
    root.mainloop()
