#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Seminarski rad
# Ime: Softver za Odredivanje Dijagnoze Pacijenta
# Datum: 3.3.2019.


import wx
import wx.lib.scrolledpanel as scrolled
import ui.registration_panel


MONTHS = {0: 'Siječanj',
          1: 'Veljača',
          2: 'Ožujak',
          3: 'Travanj',
          4: 'Svibanj',
          5: 'Lipanj',
          6: 'Srpanj',
          7: 'Kolovoz',
          8: 'Rujan',
          9: 'Listopad',
          10: 'Studeni',
          11: 'Prosinac'}

TEXTCTRL_SIZE = (0, 21)  # 150, 21


class HyperLink(wx.StaticText):  # code used from: http://zetcode.com/wxpython/customwidgets/

    def __init__(self, parent, label):
        super().__init__(parent, label=label)

        self.font1 = wx.Font(7, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Verdana')
        self.font2 = wx.Font(7, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana')

        self.SetFont(self.font2)
        self.SetForegroundColour('#0000ff')

        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        self.Bind(wx.EVT_MOTION, self.on_mouse_event)

    def on_mouse_event(self, event):
        if event.Moving():
            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.SetFont(self.font1)
        elif event.LeftUp():
            print("Registracija")
            switch_panel(UI.REGISTRATION_PANEL)
        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.font2)
        event.Skip()


class MainPanel(wx.Panel):

    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_grid_sizer = wx.GridBagSizer(10, 10)

        # wx.StaticBitmap(self, -1, wx.Image('bg.bmp', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), (0, 0))

        text = wx.StaticText(self, label='Korisničko ime: ')
        self.input_grid_sizer.Add(text, pos=(0, 0), flag=wx.ALIGN_LEFT | wx.ALL, border=5)

        self.username_input = wx.TextCtrl(self)
        self.input_grid_sizer.Add(self.username_input, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)

        text = wx.StaticText(self, label='Lozinka: ')
        self.input_grid_sizer.Add(text, pos=(1, 0), flag=wx.ALIGN_LEFT | wx.ALL, border=5)

        self.password_input = wx.TextCtrl(self)
        self.input_grid_sizer.Add(self.password_input, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        self.sing_in_button = wx.Button(self, label='Prijava')
        self.Bind(wx.EVT_BUTTON, self.on_sign_in, self.sing_in_button)
        self.input_grid_sizer.Add(self.sing_in_button, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        self.input_grid_sizer.AddGrowableCol(1, proportion=2)

        self.main_sizer.AddSpacer(100)
        self.main_sizer.Add(self.input_grid_sizer, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=160)

        self.register_hyperlink = HyperLink(self, label='Registracija')
        self.main_sizer.Add(self.register_hyperlink, flag=wx.ALIGN_LEFT | wx.ALL, border=50)

        self.SetSizer(self.main_sizer)

        self.SetFocusIgnoringChildren()  # removing focus from 'text box' at the beginning

    def on_sign_in(self, event):
        print("Prijava")
        switch_panel(UI.SYMPTOM_CHOICE_PANEL)


class RegistrationPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.widget_objects = dict()
        self.main_sizer = wx.GridBagSizer(10, 10)

        # ====================PERSONAL DATA BLOCK====================

        row, column = 0, 0
        sizer = wx.GridBagSizer(10, 10)
        border = 2
        for label in ["Ime", "Prezime", "Spol", "Datum rođenja\n(Dan|Mjesec|Godina)", "Mjesto rođenja", "E-mail", "Broj telefona", "Broj mobitela"]:
            if label == "Spol":
                column = 1
                flag_list = [wx.ALIGN_LEFT, wx.ALIGN_RIGHT]
                for gender in ["Muško", "Žensko"]:
                    widget = wx.RadioButton(parent=self, label=gender)
                    sizer.Add(widget, pos=(row, column), flag=wx.EXPAND | flag_list[column - 1] | wx.ALL, border=border)
                    self.widget_objects['{} - {}'.format(label, gender)] = widget
                    column += 1
            elif "Datum rođenja" in label:
                combo_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
                all_choices = {"Dan": (str(x) for x in range(1, 32)),
                               "Mjesec": (MONTHS[x] for x in range(0, 12)),
                               "Godina": (str(x) for x in range(1920, 2020))}
                for key in all_choices:
                    widget = wx.ComboBox(self, choices=list(all_choices[key]), style=wx.CB_READONLY)
                    combo_box_sizer.Add(widget, proportion=0)
                    self.widget_objects['{} - {}'.format(label, key)] = widget
                sizer.Add(combo_box_sizer, pos=(row, 1), span=(1, 2), flag=wx.ALL, border=border)
            else:
                text_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
                widget = wx.TextCtrl(parent=self, size=TEXTCTRL_SIZE)
                text_ctrl_sizer.Add(widget, proportion=1)
                sizer.Add(text_ctrl_sizer, pos=(row, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=border)
                self.widget_objects[label] = widget
            widget = wx.StaticText(parent=self, label=label)
            sizer.Add(widget, pos=(row, 0), flag=wx.EXPAND | wx.ALL, border=border)
            row += 1
        self.add_growable_rows(sizer)
        sizer.AddGrowableCol(2)
        box = wx.StaticBox(self, label="Osobni podatci")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        box_sizer.Add(sizer, proportion=1, flag=wx.EXPAND)
        self.main_sizer.Add(box_sizer, pos=(0, 0), span=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.main_sizer.AddGrowableRow(0)
        self.main_sizer.AddGrowableRow(1)
        self.main_sizer.AddGrowableCol(0)

        # ====================IDENTIFICATION NUMBERS BLOCK====================

        row, column = 0, 0
        sizer = wx.GridBagSizer(10, 10)
        for label in ["OIB", "MBO", "BOO"]:
            sizer.Add(wx.StaticText(self, label=label), pos=(row, 0), flag=wx.ALL, border=border)
            text_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
            widget = wx.TextCtrl(self, size=TEXTCTRL_SIZE)
            text_ctrl_sizer.Add(widget, proportion=1)
            sizer.Add(text_ctrl_sizer, pos=(row, 1), span=(1, 2), flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, border=border)
            self.widget_objects[label] = widget
            row += 1
        self.add_growable_rows(sizer)
        sizer.AddGrowableCol(2)
        box = wx.StaticBox(self, label="Identifikacijski brojevi")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        box_sizer.Add(sizer, proportion=1, flag=wx.EXPAND)
        self.main_sizer.Add(box_sizer, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.main_sizer.AddGrowableCol(1)

        # ====================PARENT PERSONAL DATA BLOCK====================

        row, column = 0, 0
        sizer = wx.GridBagSizer(10, 10)
        text_box_size = (160, 21)
        for label in ["Ime", "Prezime", "E-mail", "Broj mobitela"]:
            sizer.Add(wx.StaticText(self, label=label), pos=(row, 0), flag=wx.ALL, border=border)
            text_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
            widget = wx.TextCtrl(self, size=text_box_size)
            text_ctrl_sizer.Add(widget, proportion=1)
            sizer.Add(text_ctrl_sizer, pos=(row, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=border)
            self.widget_objects['{} - skrbnik'.format(label)] = widget
            row += 1
        self.add_growable_rows(sizer)
        sizer.AddGrowableCol(2)
        box = wx.StaticBox(self, label="Osobni podatci skrbnika")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        box_sizer.AddSpacer(5)
        box_sizer.Add(sizer, proportion=1, flag=wx.EXPAND)
        self.main_sizer.Add(box_sizer, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # ====================BUTTON BLOCK====================

        add_spacer = True
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        bind_funcs = [self.on_cancel, self.on_confirm]
        index = 0
        for label in ["Poništi", "Potvrdi"]:
            widget = wx.Button(self, label=label)
            widget.Bind(wx.EVT_BUTTON, bind_funcs[index])
            sizer.Add(widget, proportion=1)
            self.widget_objects[label] = widget
            if add_spacer:
                sizer.AddSpacer(10)
                add_spacer = False
            index += 1
        self.main_sizer.Add(sizer, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)
        self.main_sizer.AddGrowableRow(2)

        self.SetSizer(self.main_sizer)

    def add_growable_rows(self, sizer):
        row = 0
        while True:
            try:
                sizer.AddGrowableRow(row)
            except Exception:
                return
            else:
                row += 1

    def on_cancel(self, event):
        print("Poništi")
        switch_panel(UI.MAIN_PANEL)

    def on_confirm(self, event):
        print("Potvrdi")


class SymptomChoicePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_sizer.Add(wx.StaticText(self, label="Odaberite simptome koje ste opazili: "), flag=wx.LEFT | wx.TOP | wx.RIGHT, border=30)

        self.vscrolled_panel = VScrolledPanel(self)
        self.main_sizer.Add(self.vscrolled_panel, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, border=30)

        self.hscrolled_panel = HScrolledPanel(self)
        text = wx.StaticText(self.hscrolled_panel, label="Odabrani simptomi: ")
        self.hscrolled_panel.add(text)
        # self.main_sizer.Add(self.hscrolled_panel, proportion=0, flag=wx.EXPAND)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.back_button = wx.Button(self, label="Natrag")
        self.Bind(wx.EVT_BUTTON, self.on_back, self.back_button)
        self.button_sizer.Add(self.back_button, flag=wx.TOP, border=-18)
        self.button_sizer.AddSpacer(20)
        self.cancel_button = wx.Button(self, label="Poništi odabir")
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)
        self.button_sizer.Add(self.cancel_button, flag=wx.TOP, border=-18)
        self.button_sizer.AddSpacer(20)
        self.confirm_button = wx.Button(self, label="Potvrdi")
        self.Bind(wx.EVT_BUTTON, self.on_confirm, self.confirm_button)
        self.button_sizer.Add(self.confirm_button, flag=wx.TOP, border=-18)

        self.main_sizer.Add(self.button_sizer, proportion=0, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=20)

        self.SetSizer(self.main_sizer)

    def on_back(self, event):
        print("Natrag")
        switch_panel(UI.MAIN_PANEL)

    def on_cancel(self, event):
        print("Poništi odabir")

    def on_confirm(self, event):
        print("Potvrdi")


class VScrolledPanel(scrolled.ScrolledPanel):
# code used from: https://www.daniweb.com/programming/software-development/threads/177558/how-do-i-use-the-wxpython-scrolledpanel-widget

    def __init__(self, parent):
        super().__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.grid_sizer = wx.GridBagSizer(30, 30)

        self.static_box = wx.StaticBox(self, label="Simptomi")

        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

        self.setup_symptoms()

        self.static_box_sizer.Add(self.grid_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.main_sizer.Add(self.static_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(True)  # Layout function to be called automatically when the window is resized
        self.SetupScrolling()

    def setup_symptoms(self):
        # temp_solution, test version for adding symptoms
        # use generator if number of syamptoms is bigger than cca 350 ?
        symptoms = ['Simptom {}'.format(x + 1) for x in range(148)]  # replace this with list of symptoms from xml file
        number_of_columns = 3
        number_of_symptoms = len(symptoms)
        full_rows = number_of_symptoms // number_of_columns
        symptom_index = 0
        row, column = 0, 0

        for row in range(full_rows):
            for column in range(number_of_columns):
                symptom = symptoms[symptom_index]
                self.grid_sizer.Add(wx.CheckBox(self, label="{}".format(symptom)),
                                    pos=(row, column), flag=wx.EXPAND)
                symptom_index += 1

        row += 1
        for column in range(number_of_symptoms % number_of_columns):
            symptom = symptoms[symptom_index]
            self.grid_sizer.Add(wx.CheckBox(self, label="{}".format(symptom)),
                                pos=(row, column), flag=wx.EXPAND)
            symptom_index += 1

        for column in range(number_of_columns):
            self.grid_sizer.AddGrowableCol(column)


class HScrolledPanel(scrolled.ScrolledPanel):  # WIP

    def __init__(self, parent):
        super().__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.SetSizer(self.main_sizer)

    def add(self, widget):
        self.main_sizer.Add(widget, flag=wx.EXPAND)


class UI(wx.Frame):

    MAIN_PANEL = None
    REGISTRATION_PANEL = None
    SYMPTOM_CHOICE_PANEL = None
    ACTIVE_PANEL = None

    def __init__(self):
        super().__init__(None, title='Softver za određivanje dijagnoze pacijenata*', size=(650, 400))

        self.main_panel = MainPanel(self)
        self.registration_panel = RegistrationPanel(self)
        self.symptom_choice_panel = SymptomChoicePanel(self)

        UI.MAIN_PANEL = self.main_panel
        UI.REGISTRATION_PANEL = self.registration_panel
        UI.SYMPTOM_CHOICE_PANEL = self.symptom_choice_panel
        UI.ACTIVE_PANEL = self.main_panel

        self.registration_panel.Hide()
        self.symptom_choice_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.sizer.Add(self.registration_panel, 1, wx.EXPAND)
        self.sizer.Add(self.symptom_choice_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.SetMinSize((650, 400))  # useful?


def switch_panel(panel):
    # With methods Freeze() and Thaw(), we reduce our UI from appearing to flicker
    window.Freeze()  # Freeze() prevents the window from updating while it is frozen
    UI.ACTIVE_PANEL.Hide()
    UI.ACTIVE_PANEL = panel
    panel.Show()
    window.Layout()
    window.Thaw()  # Thaw() will enable user to see the update


def main():
    global panel_control, window
    app = wx.App()
    window = UI()
    window.Show()
    panel_control = None  # PanelControl(window)
    app.MainLoop()


if __name__ == '__main__':
    main()
