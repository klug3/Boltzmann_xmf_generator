# Boltzmann generator 1.0
# Program z GUI generujący skrypty do uśrednienia Boltzmannowskiego w programie SigmaPlot.

from tkinter import *


class Application(Frame):
    """Interfejs graficzny generatora."""
    def __init__(self, master):
        """Inicjalizuje ramkę."""
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Utwórz 3 zestawy widżetów Label + Entry oraz Button."""
        # utwórz pierwszy zestaw Label + Entry
        # utwórz etykietę z instrukcją - 1
        self.energy_lbl = Label(self, text="Wprowadź nazwę pliku zaw. pop. dE:")
        self.energy_lbl.grid(row=0, column=0, columnspan=2, sticky=W)

        # utwórz widżet Entry do przejęcia nazwy pliku
        self.energy_ent = Entry(self)
        self.energy_ent.grid(row=0, column=3, sticky=W)

        # utwórz pusty rząd dla lepszej czytelności
        self.empty1_lbl = Label(self,)
        self.empty1_lbl.grid(row=1, column=0, columnspan=2, sticky=W)

        # utwórz drugi zestaw Label + Entry
        # utwórz etykietę z instrukcją - 2
        self.gibbs_lbl = Label(self, text="Wprowadź nazwę pliku zaw. pop. ddG:")
        self.gibbs_lbl.grid(row=2, column=0, columnspan=2, sticky=W)

        # utwórz widżet Entry do przejęcia nazwy pliku
        self.gibbs_ent = Entry(self)
        self.gibbs_ent.grid(row=2, column=3, sticky=W)

        # utwórz pusty rząd dla lepszej czytelności
        self.empty2_lbl = Label(self, )
        self.empty2_lbl.grid(row=3, column=0, columnspan=2, sticky=W)

        # utwórz trzeci zestaw Label + Entry
        # utwórz etykietę z instrukcją - 3
        self.name_lbl = Label(self, text="Wprowadź nazwę pliku do wygenerowania:")
        self.name_lbl.grid(row=4, column=0, columnspan=2, sticky=W)

        # utwórz widżet Entry do przejęcia nazwy pliku
        self.name_ent = Entry(self)
        self.name_ent.grid(row=4, column=3, sticky=W)

        # utwórz pusty rząd dla lepszej czytelności
        self.empty3_lbl = Label(self, )
        self.empty3_lbl.grid(row=5, column=0, columnspan=2, sticky=W)

        # utwórz przycisk Akceptuj
        self.submit_bttn = Button(self, text="    Akceptuj    ", command=self.generate)
        self.submit_bttn.grid(row=6, column=1, columnspan=2)

    def file_names(self):
        """Przypisuje nazwy plików wprowadzone przez użytkownika do zmiennych"""
        self.energy_file_name = self.energy_ent.get() + ".txt"
        self.gibbs_file_name = self.gibbs_ent.get() + ".txt"
        self.results_file_name = self.name_ent.get() + ".xfm"

    @staticmethod
    def format_txt(list):
        """Formatuje pliki txt, eliminując znak \n ma końcu linii (jeżeli występuje)"""
        new_list = []
        for i in list:
            if "\n" in i:       # usuwa znak następnej linii
                i = i[:-1]
            if i != "":         # usuwa puste elementy listy (po enterach na końcu dokumentu)
                new_list.append(i)
        return new_list

    def read_files(self):
        """Odczytuje zawartość plików tekstowych, formatuje je i zamyka"""
        # odczytaj populacje dE
        self.energy_file = open(self.energy_file_name, "r")
        self.energy_pop = self.energy_file.readlines()
        self.energy_pop = self.format_txt(self.energy_pop)
        self.energy_file.close()

        # odczytaj populacje ddG
        self.gibbs_file = open(self.gibbs_file_name, "r")
        self.gibbs_pop = self.gibbs_file.readlines()
        self.gibbs_pop = self.format_txt(self.gibbs_pop)
        self.gibbs_file.close()

    @staticmethod
    def create_line(population, col_nr):
        """Tworzy gotową linię tekstu dla pliku wynikowego uwzględniając populację"""
        # określ numer kolumny początkowej
        col = col_nr % 300
        if col > 4:
            col -= 4

        # utwórz początek linii
        line_starter = "col(" + str(col_nr) + ")=0.01*("

        # utwórz środek linii
        line_body = ""
        j = 1
        for i in population:
            if j != len(population):
                line_body_part = i + "*col(" + str(col) + ")+"
                col += 10
                j += 1
            else:
                line_body_part = i + "*col(" + str(col) + ")"
            line_body += line_body_part

        # utwórz koniec linii
        line_end = ")"

        # utwórz całą linię
        line = line_starter + line_body + line_end
        return line

    def write_result(self):
        """Korzystając z populacji dE i ddG tworzy treść pliku wynikowego"""
        self.result = open(self.results_file_name, "w+")

        # zapisuje gotowe linie tekstu do pliku
        self.result.writelines("jsv5D.;")
        self.result.writelines("\n")
        self.result.writelines(self.create_line(self.energy_pop, 302))
        self.result.writelines("\n\n")
        self.result.writelines(self.create_line(self.energy_pop, 303))
        self.result.writelines("\n\n")
        self.result.writelines(self.create_line(self.energy_pop, 304))
        self.result.writelines("\n\n")
        self.result.writelines("\n\n")
        self.result.writelines(self.create_line(self.gibbs_pop, 306))
        self.result.writelines("\n\n")
        self.result.writelines(self.create_line(self.gibbs_pop, 307))
        self.result.writelines("\n\n")
        self.result.writelines(self.create_line(self.gibbs_pop, 308))

        # zamyka goowy plik tekstowy
        self.result.close()

    def generate(self):
        """Wykorzystuje wpisane przez użytkownika dane i generuje finalny plik"""
        self.file_names()
        self.read_files()
        self.write_result()


# część główna
root = Tk()
root.title("Boltzmann Generator")
root.geometry("360x155")

app = Application(root)

root.mainloop()
