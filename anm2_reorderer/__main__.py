#!/usr/bin/env python

import wx


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)


app = wx.App()

main_window = MainWindow(None, title="anm2_reorderer")
main_window.Show()

app.MainLoop()
