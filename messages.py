from gi.repository import Gtk


def on_info_clicked(widget, principal, secundaria):
    dialog = Gtk.MessageDialog(
        transient_for=widget,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text= principal,
    )
    dialog.format_secondary_text(
        secundaria
    )
    dialog.run()
    print("INFO dialog closed")

    dialog.destroy()


def on_error_clicked(widget, principal, secundaria):
    dialog = Gtk.MessageDialog(
        transient_for=widget,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=principal
    )
    dialog.format_secondary_text(
        secundaria
    )
    response = dialog.run()
    
    if response == Gtk.ResponseType.OK:
        print("WARN dialog closed by clicking OK button")
        print("ERROR dialog closed")
        dialog.destroy()
    

def on_warn_clicked(widget, principal, secundaria):
    dialog = Gtk.MessageDialog(
        transient_for=widget,
        flags=0,
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.OK,
        text=principal,
    )
    dialog.format_secondary_text(
        secundaria
    )
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        print("WARN dialog closed by clicking OK button")
    dialog.destroy()


def on_question_clicked(widget):
    dialog = Gtk.MessageDialog(
        transient_for=widget,
        flags=0,
        message_type=Gtk.MessageType.QUESTION,
        buttons=Gtk.ButtonsType.YES_NO,
        text="This is an QUESTION MessageDialog",
    )
    dialog.format_secondary_text(
        "And this is the secondary text that explains things."
    )
    response = dialog.run()
    if response == Gtk.ResponseType.YES:
        print("QUESTION dialog closed by clicking YES button")
    elif response == Gtk.ResponseType.NO:
        print("QUESTION dialog closed by clicking NO button")

    dialog.destroy()

