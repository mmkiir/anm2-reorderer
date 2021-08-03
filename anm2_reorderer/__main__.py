#!/usr/bin/env python

import wx
import xml.etree.ElementTree as ET
from typing import Any, Optional


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

        self.current_file_path: Optional[str] = None
        self.current_file_root: Optional[ET.ElementTree] = None

        file_menu: wx.Menu = wx.Menu()

        open_menu_item: wx.MenuItem = wx.MenuItem(
            file_menu, wx.ID_OPEN, "&Open...")
        self.Bind(wx.EVT_MENU, self.OnOpen, open_menu_item)
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
        self.Bind(wx.EVT_MENU, self.OnExit, exit_menu_item)
        file_menu.Append(exit_menu_item)

        menu_bar: wx.MenuBar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")

        self.SetMenuBar(menu_bar)

    def OnOpen(self, _) -> None:
        with wx.FileDialog(self, "Open", wildcard="ANM2 files (*.anm2)|*.anm2", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file_path = file_dialog.GetPath()
            try:
                with open(file_path, 'r') as file:
                    self.current_file_path = file_path
                    self.current_file_root = ET.parse(file_path)
            except IOError:
                wx.LogError(f"Cannot open file {file_path}")

    def OnExit(self, _) -> None:
        self.Close()


app = wx.App()

main_window = MainWindow(None, title="anm2_reorderer")
main_window.Show()

app.MainLoop()
