# tableview.py
#
#  Copyright (c)2024 Shane Ambler <Develop@ShaneWare.biz>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview

from . import __version__ as vers
from . import InplaceEntry


class EditTree(Tableview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.view.bind('<Double-1>', self.start_edit)

    def start_edit(self, evnt=None):
        try:
            self.edit_entry.destroy()
        except AttributeError:
            pass

        self.view.update()
        rowid = self.view.identify_row(evnt.y)
        if rowid == '': return
        colid = self.view.identify_column(evnt.x)
        self.last_edit_cell = (int(rowid[1:], base=16)-1, int(colid[1:])-1)

        x, y, w, h = self.view.bbox(rowid, colid)
        pady = (h // 2)

        txt = self.view.item(rowid, 'values')[int(colid[1:])-1]
        self.last_edit_start = txt
        self.edit_entry = InplaceEntry(self, self.view, rowid, int(colid[1:])-1, txt)
        self.edit_entry.place(in_=self.view, x=x, y=y-pady, width=w, height=h*1.75)
        self.edit_entry.bind('<<ET_Accept>>', self.end_edit)

    def end_edit(self, evnt=None):
        self.last_edit_end = evnt.widget.get()
        self.event_generate('<<ET_Accept>>')
