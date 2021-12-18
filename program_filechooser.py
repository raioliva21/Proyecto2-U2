import gi
# Selecciona que la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa Gtk
from gi.repository import Gtk


class DlgFileChooser():

    def __init__(self, mode="open_mode"):
        builder = Gtk.Builder()
        builder.add_from_file("proyecto.ui")
        # Asociamos a atributos cada uno de los elementos del glade (ID)
        self.filechooser = builder.get_object("filechooser")
        self.filechooser.set_title("SELECCION ARCHIVOS")
        
        titulo = self.filechooser.get_title()
        print(titulo)

        if mode == "open_mode":
            self.filechooser.add_buttons(Gtk.STOCK_CANCEL,
                                         Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN,
                                         Gtk.ResponseType.OK)
        elif mode == "save_mode":
            self.filechooser.set_action(Gtk.FileChooserAction.SAVE)
            self.filechooser.add_buttons(Gtk.STOCK_CANCEL,
                                         Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_SAVE,
                                         Gtk.ResponseType.ACCEPT)

        self.filechooser.show_all()
