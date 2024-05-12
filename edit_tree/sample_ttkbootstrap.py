#  sample_ttkbootstrap.py
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
#


import screeninfo
import sys
import tkinter as tk
import ttkbootstrap as ttk
from tkinter.messagebox import showinfo

from . import __version__ as vers
from . import tableview as tv

PADDING = 3
BORDER = 5


class EditTreeSampleTTKB(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('EditTree Sample')
        self.geometry(self.center_on_monitor(500, 600))
        self.minsize(450, 200)
        self.setupMenus()
        self.bind('<Control-KeyPress-q>', lambda e: self.destroy())
        self.layout()

    def setupMenus(self):
        self.mainmenu = tk.Menu(self)

        # File
        self.filemenu = tk.Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label='Quit', command=self.destroy)
        self.mainmenu.add_cascade(label='File', menu=self.filemenu)

        # Help
        self.helpmenu = tk.Menu(self.mainmenu, tearoff=0)
        #self.helpmenu.add_command(label='Documentation', command=self.placeholder)
        self.helpmenu.add_command(label='About', command=self.about_me)
        self.mainmenu.add_cascade(label='Help', menu=self.helpmenu)

        self.config(menu=self.mainmenu)

    def layout(self):
        l = ttk.Label(self, text='Base: ttkbootstrap.tableview.Tableview')
        l.grid(row=0, column=0, sticky=tk.W, padx=PADDING, pady=PADDING)

        col_names = [{'text': 'col1', 'width': 121},
                    {'text': 'col2', 'width': 121},
                    {'text': 'col3', 'width': 121},
                    {'text': 'col4', 'width': 121},
                    ]
        row_data = []
        for r in range(1, 101):
            row_data.append((f'cell-{r}-1', f'cell-{r}-2', f'cell-{r}-3', f'cell-{r}-4'))
        t = tv.EditTree(self,
                        coldata=col_names,
                        rowdata=row_data,
                        stripecolor=('#373737', None))
        t.grid(row=1, column=0, sticky=tk.NSEW)

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=t.view.yview)
        t.view.configure(yscroll=s.set)
        s.grid(row=1, column=1, sticky=tk.NS)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def mouse_on_monitor(self):
        xy = self.winfo_pointerxy()
        for m in screeninfo.get_monitors():
            mon = [ int(getattr(m, 'x')),
                    int(getattr(m, 'y')),
                    int(getattr(m, 'x')) + int(getattr(m, 'width')),
                    int(getattr(m, 'y')) + int(getattr(m, 'height')),
                    ]
            if mon[0] < xy[0] and xy[0] < mon[2]:
                if mon[1] < xy[1] and xy[1] < mon[3]:
                    return mon
        return None

    def center_on_monitor(self, w, h):
        # mon is rectangle [x1, y1, x2, y2]
        mon = self.mouse_on_monitor()
        if mon is None: return ''
        xpos = (((mon[2] - mon[0]) - w) // 2) + mon[0]
        ypos = (((mon[3] - mon[1]) - h) // 2) + mon[1]
        return f'{w}x{h}+{xpos}+{ypos}'

    def about_me(self):
        showinfo('About EditTree sample v'+vers.__version__, message='Example project to showcase the EditTree widget using ttkbootstrap.')

    def main(self, args=None):
        return self.mainloop()


def main():
    mw = EditTreeSampleTTKB(themename='darkly')
    sys.exit(mw.main(sys.argv))

if __name__ == '__main__':
    main()
