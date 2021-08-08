#!/usr/bin/env python

import wx
import xml.etree.ElementTree as ET
from functools import partial
from typing import Any, Optional, cast


def get_animations(root: ET.Element) -> Optional[ET.Element]:
    return root.find('Animations')


def get_animation(root: ET.Element, name: str) -> Optional[ET.Element]:
    return root.find(f'Animations/Animation[@Name="{name}"]')


def move_animation(new_index: int, animations: ET.Element, animation: ET.Element) -> None:
    animations.remove(animation)
    animations.insert(new_index, animation)


def shift_animation(shift_by: int, animations: ET.Element, animation: ET.Element) -> None:
    index: int = list(animations.iter('Animation')).index(animation)

    if shift_by < 0 and index == 0 or shift_by > 0 and index == len(list(animation.iter('Animations'))) - 1:
        return

    move_animation(index + shift_by, animations, animation)


shift_animation_up: partial = partial(shift_animation, -1)


shift_animation_down: partial = partial(shift_animation, 1)


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

        self.file_path: Optional[str] = None
        self.file_is_saved: bool = False
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None

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

        panel: wx.Panel = wx.Panel(self)

        h_box: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.list_box: wx.ListBox = wx.ListBox(panel)

        h_box.Add(self.list_box, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        button_panel: wx.Panel = wx.Panel(panel)

        v_box: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

        move_up_button: wx.Button = wx.Button(
            button_panel, wx.ID_ANY, 'Move up')

        self.Bind(wx.EVT_BUTTON, self.OnMoveUp, move_up_button)

        move_down_button: wx.Button = wx.Button(
            button_panel, wx.ID_ANY, 'Move down')
        self.Bind(wx.EVT_BUTTON, self.OnMoveDown, move_down_button)

        rename_button: wx.Button = wx.Button(
            button_panel, wx.ID_ANY, 'Rename')
        self.Bind(wx.EVT_BUTTON, self.OnRename, rename_button)

        delete_button: wx.Button = wx.Button(
            button_panel, wx.ID_ANY, 'Delete')
        self.Bind(wx.EVT_BUTTON, self.OnDelete, delete_button)

        v_box.Add(move_up_button, 0, wx.EXPAND | wx.RIGHT)
        v_box.Add(move_down_button, 0, wx.EXPAND | wx.RIGHT)
        v_box.Add(rename_button, 0, wx.EXPAND | wx.RIGHT)
        v_box.Add(delete_button, 0, wx.EXPAND | wx.RIGHT)

        button_panel.SetSizer(v_box)

        h_box.Add(button_panel, 0, wx.EXPAND | wx.RIGHT, 20)

        panel.SetSizer(h_box)

    def OnOpen(self, _) -> None:
        with wx.FileDialog(self, "Open", wildcard="ANM2 files (*.anm2)|*.anm2", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file_path = file_dialog.GetPath()
            try:
                with open(file_path, 'r') as file:
                    self.file_path = file_path
                    self.file_is_saved = True
                    self.tree = ET.parse(file_path)
                    self.root = self.tree.getroot()

                    animations = get_animations(self.root)

                    if not animations:
                        return

                    assert animations is not None

                    self.list_box.InsertItems(
                        [animation.attrib['Name'] for animation in animations.iter('Animation')], 0)

            except IOError:
                wx.LogError(f"Cannot open file {file_path}")

    def OnExit(self, _) -> None:
        self.Close()

    def OnMoveUp(self, _) -> None:
        if not self.root:
            return

        assert self.root is not None

        animations = get_animations(self.root)

        if not animations:
            return

        assert animations is not None

        animation = get_animation(
            self.root, self.list_box.GetStringSelection())

        if not animation:
            return

        assert animation is not None

        shift_animation_up(animations, animation)

        self.list_box.Clear()
        self.list_box.InsertItems([animation.attrib['Name']
                                  for animation in animations.iter('Animation')], 0)
        self.list_box.SetStringSelection(animation.attrib['Name'])

    def OnMoveDown(self, _) -> None:
        if not self.root:
            return

        assert self.root is not None

        animations = get_animations(self.root)

        if not animations:
            return

        assert animations is not None

        animation = get_animation(
            self.root, self.list_box.GetStringSelection())

        if not animation:
            return

        assert animation is not None

        shift_animation_down(animations, animation)

        self.list_box.Clear()
        self.list_box.InsertItems([animation.attrib['Name']
                                  for animation in animations.iter('Animation')], 0)
        self.list_box.SetStringSelection(animation.attrib['Name'])

    def OnRename(self, _) -> None:
        pass

    def OnDelete(self, _) -> None:
        pass


app = wx.App()

main_window = MainWindow(None, title="anm2_reorderer")
main_window.Show()

app.MainLoop()
