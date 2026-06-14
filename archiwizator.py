import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from narzedzia import kompresator


class Aplikacja(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Archiwizator :)")
        self.geometry("700x500")
        self.resizable(False, False)
        self.folder = tk.StringVar(value="Brak wybranego folderu")
        self.kompresja_plik = tk.StringVar()
        self.dek_kody = tk.StringVar()
        self.dek_paczka = tk.StringVar()
        self.dek_wyjscie = tk.StringVar()

        self._buduj_interfejs()

    def _buduj_interfejs(self):
        ramka_folder = ttk.LabelFrame(self, text="Folder roboczy")
        ramka_folder.pack(fill="x", padx=10, pady=10)

        ttk.Label(ramka_folder, textvariable=self.folder).pack(side="left", padx=10, pady=10)
        ttk.Button(ramka_folder, text="Wybierz folder", command=self.wybierz_folder).pack(side="right", padx=10, pady=10)

        ramka_kompresja = ttk.LabelFrame(self, text="Kompresja")
        ramka_kompresja.pack(fill="x", padx=10, pady=10)

        ttk.Label(ramka_kompresja, text="Plik do skompresowania:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.combo_kompresja = ttk.Combobox(ramka_kompresja, textvariable=self.kompresja_plik, width=50, state="readonly")
        self.combo_kompresja.grid(row=0, column=1, padx=10, pady=8)
        ttk.Button(ramka_kompresja, text="Odśwież listę", command=self.odswiez_pliki).grid(row=0, column=2, padx=10, pady=8)
        ttk.Button(ramka_kompresja, text="Kompresuj", command=self.kompresuj).grid(row=1, column=1, padx=10, pady=8)

        ramka_dekompresja = ttk.LabelFrame(self, text="Dekompresja")
        ramka_dekompresja.pack(fill="x", padx=10, pady=10)

        ttk.Label(ramka_dekompresja, text="Plik z kodami (.huffcode):").grid(row=0, column=0, padx=10, pady=6, sticky="w")
        ttk.Entry(ramka_dekompresja, textvariable=self.dek_kody, width=55).grid(row=0, column=1, padx=10, pady=6)
        ttk.Button(ramka_dekompresja, text="Wybierz", command=self.wybierz_kody).grid(row=0, column=2, padx=10, pady=6)

        ttk.Label(ramka_dekompresja, text="Plik zakodowany (.huff):").grid(row=1, column=0, padx=10, pady=6, sticky="w")
        ttk.Entry(ramka_dekompresja, textvariable=self.dek_paczka, width=55).grid(row=1, column=1, padx=10, pady=6)
        ttk.Button(ramka_dekompresja, text="Wybierz", command=self.wybierz_paczke).grid(row=1, column=2, padx=10, pady=6)

        ttk.Label(ramka_dekompresja, text="Plik wynikowy:").grid(row=2, column=0, padx=10, pady=6, sticky="w")
        ttk.Entry(ramka_dekompresja, textvariable=self.dek_wyjscie, width=55).grid(row=2, column=1, padx=10, pady=6)

        ttk.Button(ramka_dekompresja, text="Dekompresuj", command=self.dekompresuj).grid(row=3, column=1, padx=10, pady=10)

        ramka_info = ttk.LabelFrame(self, text="Informacja")
        ramka_info.pack(fill="both", expand=True, padx=10, pady=10)

        self.etykieta_info = tk.Label(
            ramka_info,
            text="Wybierz folder, a potem pliki z tego folderu.",
            anchor="w",
            justify="left"
        )
        self.etykieta_info.pack(fill="both", expand=True, padx=10, pady=10)

    def wybierz_folder(self):
        wybrany = filedialog.askdirectory(title="Wybierz folder roboczy")
        if wybrany:
            self.folder.set(wybrany)
            self.odswiez_pliki()

    def odswiez_pliki(self):
        folder = self.folder.get()
        if folder == "Brak wybranego folderu" or not os.path.isdir(folder):
            messagebox.showwarning("Uwaga", "Najpierw wybierz folder.")
            return

        pliki = []
        for nazwa in os.listdir(folder):
            sciezka = os.path.join(folder, nazwa)
            if os.path.isfile(sciezka):
                pliki.append(nazwa)

        self.combo_kompresja["values"] = pliki
        if pliki:
            self.combo_kompresja.current(0)
        else:
            self.kompresja_plik.set("")

    def kompresuj(self):
        folder = self.folder.get()
        plik = self.kompresja_plik.get()

        if not os.path.isdir(folder):
            messagebox.showerror("Błąd", "Najpierw wybierz folder.")
            return

        if not plik:
            messagebox.showerror("Błąd", "Wybierz plik do kompresji.")
            return

        sciezka = os.path.join(folder, plik)

        try:
            start = time.perf_counter()
            kompresator.kompresja(sciezka)
            czas = time.perf_counter() - start

            messagebox.showinfo("Sukces", f"Skompresowano:\n{plik}\n\nCzas: {czas:.4f} s")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się skompresować pliku:\n{e}")

    def wybierz_kody(self):
        plik = filedialog.askopenfilename(
            title="Wybierz plik z kodami",
            filetypes=[("Pliki kodów", "*.huffcode"), ("Wszystkie pliki", "*.*")]
        )
        if plik:
            self.dek_kody.set(plik)

    def wybierz_paczke(self):
        plik = filedialog.askopenfilename(
            title="Wybierz plik zakodowany",
            filetypes=[("Pliki Huffmana", "*.huff"), ("Wszystkie pliki", "*.*")]
        )
        if plik:
            self.dek_paczka.set(plik)

    def dekompresuj(self):
        kody = self.dek_kody.get()
        paczka = self.dek_paczka.get()
        wyjscie = self.dek_wyjscie.get()

        if not kody or not os.path.isfile(kody):
            messagebox.showerror("Błąd", "Wybierz poprawny plik z kodami.")
            return

        if not paczka or not os.path.isfile(paczka):
            messagebox.showerror("Błąd", "Wybierz poprawny plik zakodowany.")
            return

        if not wyjscie:
            messagebox.showerror("Błąd", "Podaj nazwę pliku wynikowego.")
            return

        try:
            start = time.perf_counter()
            kompresator.dekompresja(wyjscie, kody, paczka)
            czas = time.perf_counter() - start

            messagebox.showinfo("Sukces", f"Dekompresowano do:\n{wyjscie}\n\nCzas: {czas:.4f} s")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zdekompresować pliku:\n{e}")


if __name__ == "__main__":
    app = Aplikacja()
    app.mainloop()