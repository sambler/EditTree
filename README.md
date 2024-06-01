
EditTree
========


A tkinter treeview that has cells that can be edited in place.

Also includes support for a ttkbootstrap Tableview.



install as editable module

```sh
python -m pip install --user -e .
```

---
Use in your project
===================

The `EditTree` inherits `ttk.Treeview` and should be a straight replacement for it.

Install module, and add
```python
from edit_tree import EditTree
```
then change `ttk.Treeview` to `EditTree`

OR if your using ttkbootstrap, add
```python
from edit_tree.tableview import EditTree
```
and change `ttk.tableview.Tableview` to `EditTree`


Bind to event `<<ET_Accept>>` to respond to data changes.
```python
table.bind('<<ET_Accept>>', data_edited)
```

Values available from event parameter:-
```python
event.widget.last_edit_cell # data index (row, col)
evnt.widget.last_edit_start # cell value at begin edit
evnt.widget.last_edit_end   # cell value at accept edit
```

---
Known issues
============

* When scrolling the underlying Treeview, destroying the entry widget is not always handled.

* The unbind_all used to remove the scrollwheel binding can also remove bindings added elsewhere.
