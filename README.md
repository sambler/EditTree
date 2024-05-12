
EditTable
=========


A tkinter treeview that has cells that can be edited in place.

Also includes support for a ttkbootstrap Tableview.



install as editable module

```sh
python -m pip install --user -e .
```

Run examples after install
```sh
EditTreeSample
```
or
```sh
EditTreeSample_ttkbootstrap
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

---

Known issues
============

* When scrolling the underlying Treeview, destroying the entry widget is not always handled.

* The unbind_all used to remove the scrollwheel binding can also remove bindings added elsewhere.
