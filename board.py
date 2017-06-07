from tkinter import *

class Baord(Frame):
    def __init__(self, root, x, y):
        self._widget = {}
        self._create_baord(root, x, y)

    def _create_baord(self, root, x, y):
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)

        #Create & Configure frame
        frame=Frame(root)
        frame.grid(row=0, column=0, sticky=N+S+E+W)

        root.geometry('400x400+300+100')
        root.title('My app')

        #Create a 5x10 (rows x columns) grid of buttons inside the frame
        for row_index in range(x):
            Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(y):
                Grid.columnconfigure(frame, col_index, weight=1)
                btn = Button(frame,
                    borderwidth=1, command = lambda i=row_index, j = col_index: self._show_cordinate(i, j), bg='White', fg= 'Black')
                btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)
                self._widget[(row_index, col_index)] = btn

    def _show_cordinate (self, r, c):
        print(r, c)
        self._widget[(r, c)].configure(text='R%s C%s'%(r,c), state="disabled")

if __name__=='__main__':
    root = Tk()
    app_view = Baord(root, 3, 3)
    # app_view.pack(side='top', fill='both', expand=True)
    root.mainloop()