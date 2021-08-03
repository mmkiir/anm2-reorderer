#!/usr/bin/env python

import wx


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

        file_menu: wx.Menu = wx.Menu()

        open_menu_item: wx.MenuItem = wx.MenuItem(
            file_menu, wx.ID_OPEN, "&Open...")
        file_menu.Append(open_menu_item)

        save_menu_item: wx.MenuItem = wx.MenuItem(
            file_menu, wx.ID_SAVE, "&Save")
        file_menu.Append(save_menu_item)

        saveas_menu_item: wx.MenuItem = wx.MenuItem(
            file_menu, wx.ID_SAVEAS, "&Save As...")
        file_menu.Append(saveas_menu_item)

        file_menu.AppendSeparator()

        exit_menu_item: wx.MenuItem = wx.MenuItem(
            file_menu, wx.ID_EXIT, "Exit")
        file_menu.Append(exit_menu_item)

        menu_bar: wx.MenuBar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")

        self.SetMenuBar(menu_bar)


app = wx.App()

main_window = MainWindow(None, title="anm2_reorderer")
main_window.Show()

app.MainLoop()
