#!/usr/bin/env python

#importan librerias
import json
import gi
import pandas
# Selecciona que la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa writer class desde csv module
from csv import writer
# Importa Gtk
from gi.repository import Gtk
from program_filechooser import DlgFileChooser
from messages import on_error_clicked, on_warn_clicked

"""abre archivo json"""
def open_file(file):
    try:
        with open(file, 'r') as archivo:
            data = json.load(archivo)
    except IOError:
        print("archivo no encontrado")
        data = []
    return data


"""ventana principal"""
class Ventana():

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto.ui")
        self.window = builder.get_object("ventana")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.resize(600, 400)

        boton_abrir = builder.get_object("boton_abrir")
        boton_abrir.connect("clicked", self.open_btn_clicked, "open_mode")

        years = open_file("years.json")

        lista = ["Seleccione un año"] + years[0]['year']

        # comboboxtext
        self.comboboxtext = builder.get_object("comboboxtext")
        for item in lista:
            self.comboboxtext.append_text(item)

        self.comboboxtext.set_active(0)

        self.comboboxtext.connect("changed", self.comboboxtext_change)

        self.tree = builder.get_object("tree")
        self.review = builder.get_object("review")
        self.boton_about = builder.get_object("boton_about")
        self.boton_about.connect("clicked", self.click_boton_about)
        self.boton_edit = builder.get_object("boton_editar")
        self.boton_edit.connect("clicked", self.edit_select_data)
        
        self.window.show_all()
        self.review.hide()
    
    def open_btn_clicked(self, btn=None, mode=None):

        dialogo = DlgFileChooser(mode)
        filechooser = dialogo.filechooser

        filter_csv = Gtk.FileFilter()
        filter_csv.add_mime_type("text/csv")
        filter_csv.set_name("Archivos CSV")
        filechooser.add_filter(filter_csv)

        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            print("Presionó el boton OK")
            self.create_tree(filechooser.get_filename())

        # if response == Gtk.ResponseType.CANCEL:
        filechooser.destroy()

    def comboboxtext_change(self, cmb=None):

        year = self.comboboxtext.get_active_text()

        if self.comboboxtext.get_active() != 0:
            path_file = f'data_{year}.csv'
            self.create_tree(path_file)
        
        self.tree.connect("row-activated", self.click_column)

        #self.review.show()

        
    def click_column(self, btn=None, path=None, column=None):

        model, iterador = self.tree.get_selection().get_selected()

        if model is None or iterador is None:
            return

        for item in range (0,6):
            print(model.get_value(iterador, item))

        self.review.show()        
    
        self.review.set_label(model.get_value(iterador, 3))


    def create_tree(self, path_file):

        try:
            data = pandas.read_csv(path_file)
        except NameError:
            texto_principal = "Error en el programa"
            texto_secundario = "Archivo seleccionado no ha sido encontrado."
            on_error_clicked(self.window,
                            texto_principal,
                            texto_secundario)

        if self.tree.get_columns():
            for column in self.tree.get_columns():
                self.tree.remove_column(column)

        largo_columnas = len(data.columns)
        modelo = Gtk.ListStore(*(largo_columnas * [str]))
        self.tree.set_model(model=modelo)

        cell = Gtk.CellRendererText()

        for item in range(len(data.columns)):
            column = Gtk.TreeViewColumn(data.columns[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)
            column.set_sort_column_id(item)

        for item in data.values:
            line = [str(x) for x in item]
            modelo.append(line)
        

    def click_boton_about(self, cmb=None):
        about = Gtk.AboutDialog()
        about.set_modal(True)
        about.set_title("Drug review")
        about.set_program_name("Proyecto Programación 1")
        about.set_name("Example")
        about.set_authors(["Fabio Durán-Verdugo / Raimundo Oliva San Felú"])
        about.set_comments("The program's purpose is to display/edit data that provides patient reviews of specific medications")
        about.set_logo_icon_name("go-home")

        about.run()
        about.destroy()
    
    def edit_select_data(self, cm=None):

        """Edita datos seleccionados."""
        model, it = self.tree.get_selection().get_selected()
        # Validación no selección
        if model is None or it is None:
            return

        ventana_dialogo = Ventana_Dialogo()
        
        ventana_dialogo.ID_entry.set_label(model.get_value(it, 0))
        ventana_dialogo.drug_name_entry.set_label(model.get_value(it, 1))
        ventana_dialogo.condition_entry.set_label(model.get_value(it, 2))


        fecha = model.get_value(it,5)
        fecha = fecha.split("-")
        day = int(fecha[0])
        month = {"Jan":0,"Feb":1,"Mar":2,"Apr":3,
                "May":4,"Jun":5,"Jul":6,"Aug":7,
                "Sep":8,"Oct":9,"Nov":10,"Dec":12}
        year = f"20{fecha[2]}"

        ventana_dialogo.calendar.select_day(day)
        ventana_dialogo.calendar.select_month(int(month[fecha[1]]),int(year))

        buffer_review = ventana_dialogo.comment_entry.get_buffer()
        
        response = ventana_dialogo.dialogo.run()

        if response == Gtk.ResponseType.CANCEL:
            ventana_dialogo.dialogo.destroy()

        elif response == Gtk.ResponseType.OK:
            
            print("presionó el boton ok dialogo")

            new_comment = buffer_review.props.text
            new_date = ventana_dialogo.calendar.get_date()
            new_rating = ventana_dialogo.rating_entry.get_text()
            ID_selected = model.get_value(it, 0)
            drug_name = model.get_value(it, 1)
            condition = model.get_value(it, 2)

            new_date = str(new_date)
            splits = new_date.split(",")
            self.year = splits[0][-4:]
            self.month = splits[1][-2:]
            self.day = splits[2][-3:-1]

            if self.month.isdigit():
                pass
            else:
                print("se corrigue el mes")
                self.month = self.month[-1:]
            if self.day.isdigit():
                pass
            else:
                self.day = self.day[-1:]

            if new_comment == "" or "" == new_date or new_rating == "":
                print("Advertencia! casilla vacia.")
                texto_principal = "ADVERTENCIA!"
                texto_secundario = "Existe una o mas casillas sin llenar."
                on_warn_clicked(self.window,
                            texto_principal,
                            texto_secundario)
            else:
                archivocsv = f"data_{year}.csv"
                print("el archivo csv es ", archivocsv)
                ID_selected = int(ID_selected)
                data = pandas.read_csv(archivocsv, index_col ="uniqueID" )
                data.drop(ID_selected, inplace = True)

                List = [ID_selected, drug_name, condition, new_comment, new_rating, new_date]

                try:

                    # Abre archivo csv existente como 'archivo'
                    # archivo es abierto en modo 'a'
                    with open(archivocsv, 'a') as archivo:
                        # pasa archivo a csv.writer()
                        # y se obtiene writer object
                        writer_object = writer(archivo)
                    
                        # utiliza funcion writerow()
                        writer_object.writerow(List)
                    
                        # se cierra archivo
                        archivo.close()
                except IOError:
                    print("archivo no encontrado")
                    data = []

            ventana_dialogo.dialogo.destroy()

        

class Ventana_Dialogo():

    def __init__(self):

        print("se entra a ventana dialogo")

        builder = Gtk.Builder()
        builder.add_from_file("proyecto.ui")

        self.dialogo = builder.get_object("Ventana_Dialogo")
        
        self.ID = builder.get_object("ID")
        self.ID.set_label("ID: ")
        self.ID_entry = builder.get_object("ID_entry")

        self.drug_name = builder.get_object("drug_name")
        self.drug_name.set_label("Drug name: ")
        self.drug_name_entry = builder.get_object("drug_name_entry")


        self.condition = builder.get_object("condition")
        self.condition.set_label("Condition: ")
        self.condition_entry = builder.get_object("condition_entry")

        self.date = builder.get_object("date")
        self.date.set_label("Date: ")
        self.calendar = builder.get_object("calendar")

        self.rating = builder.get_object("rating")
        self.rating.set_label("Rating: ")
        self.rating_entry = builder.get_object("rating_entry")

        self.comment = builder.get_object("comment")
        self.comment.set_label("Comment: ")
        self.comment_entry = builder.get_object("comment_entry")
        self.comment_entry.set_wrap_mode(2)


        self.dialogo.show_all()

if __name__ == "__main__":
    Ventana()
    Gtk.main()