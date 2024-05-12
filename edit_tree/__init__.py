# __init__.py
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


import sys
import tkinter as tk
from tkinter import ttk

from . import __version__ as vers


class InplaceEntry(ttk.Entry):
    def __init__(self, parent, et, rowid, colid, txt, **kwargs):
        super().__init__(parent, **kwargs)
        self.edit_tree = et
        self.rowid = rowid
        self.colid = colid
        self.start_txt = txt

        self.insert(0, txt)
        self['exportselection'] = False

        self.focus_force()
        self.select_all()
        self.bind('<Return>', self.accept_edit)
        self.bind('<KP_Enter>', self.accept_edit)
        self.bind('<Tab>', self.accept_edit)
        self.bind('<FocusOut>', self.accept_edit)
        if sys.platform.startswith('osx') or sys.platform.startswith('win'):
            self.funcid1 = self.bind_all('<MouseWheel>', self.accept_edit, '+')
        else:
            self.funcid1 = self.bind_all('<Button-4>', self.accept_edit, '+')
            self.funcid2 = self.bind_all('<Button-5>', self.accept_edit, '+')
        self.bind('<Control-a>', self.select_all)
        self.bind('<Escape>', self.cancel_edit)

    def select_all(self, evnt=None):
        self.selection_range(0, tk.END)
        return 'break'

    def clear_scroll_binding(self):
        # how can we store a bind_all funcid and only
        # unbind the bindings that we added??
        if sys.platform.startswith('osx') or sys.platform.startswith('win'):
            self.unbind_all('<MouseWheel>')
        else:
            self.unbind_all('<Button-4>')
            self.unbind_all('<Button-5>')

    def cancel_edit(self, evnt=None):
        self.clear_scroll_binding()
        self.destroy()

    def accept_edit(self, evnt=None):
        self.clear_scroll_binding()
        values = self.edit_tree.item(self.rowid, 'values')
        values = list(values)
        values[self.colid] = self.get()
        if self.start_txt != values[self.colid]:
            self.edit_tree.item(self.rowid, values=values)
            self.event_generate('<<ET_Accept>>')
        self.destroy()


class EditTree(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind('<Double-1>', self.start_edit)

    def start_edit(self, evnt=None):
        try:
            self.edit_entry.destroy()
        except AttributeError:
            pass

        rowid = self.identify_row(evnt.y)
        if rowid == '': return
        colid = self.identify_column(evnt.x)
        self.last_edit_cell = (int(rowid[1:], base=16)-1, int(colid[1:])-1)

        x, y, w, h = self.bbox(rowid, colid)
        pady = (h // 2) + h

        txt = self.item(rowid, 'values')[int(colid[1:])-1]
        self.last_edit_start = txt
        self.edit_entry = InplaceEntry(self.master, self, rowid, int(colid[1:])-1, txt)
        self.edit_entry.place(x=x, y=y+pady, width=w, height=h, anchor=tk.W)
        self.edit_entry.bind('<<ET_Accept>>', self.end_edit)

    def end_edit(self, evnt=None):
        self.last_edit_end = evnt.widget.get()
        self.event_generate('<<ET_Accept>>')
