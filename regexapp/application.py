"""Module containing the logic for the Regex application."""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from os import path
import webbrowser
from textwrap import dedent
from regexapp import RegexBuilder


__version__ = '0.0.1'
version = __version__

__edition__ = 'Community Edition'
edition = __edition__


def get_relative_center_location(parent, width, height):
    """get relative a center location of parent window.

    Parameters
    ----------
    parent (tkinter): tkinter component instance.
    width (int): a width of a child window.
    height (int): a height of a child window..

    Returns
    -------
    tuple: x, y location.
    """
    pwh, px, py = parent.winfo_geometry().split('+')
    px, py = int(px), int(py)
    pw, ph = [int(i) for i in pwh.split('x')]

    x = int(px + (pw - width) / 2)
    y = int(py + (ph - height) / 2)
    return x, y


def create_msgbox(error=None, info=None, title=None):
    """create tkinter.messagebox
    Parameters
    ----------
    error (str): an error message.  Default is None.
    info (str): an information message.  Default is None.
    title (str): a title of messagebox.  Default is None.
    """
    if error:
        messagebox.showerror(title=title, message=error)
    else:
        messagebox.showinfo(title=title, message=info)


class Data:
    license_name = 'BSD 3-Clause License'
    repo_url = 'https://github.com/Geeks-Trident-LLC/regexapp'
    license_url = path.join(repo_url, 'blob/main/LICENSE')
    # TODO: Need to update wiki page for documentation_url instead of README.md.
    documentation_url = path.join(repo_url, 'blob/develop/README.md')
    copyright_text = 'Copyright @ 2021 Geeks Trident LLC.  All rights reserved.'

    @classmethod
    def get_license(cls):
        license_ = """
            BSD 3-Clause License

            Copyright (c) 2021, Geeks Trident LLC
            All rights reserved.

            Redistribution and use in source and binary forms, with or without
            modification, are permitted provided that the following conditions are met:

            1. Redistributions of source code must retain the above copyright notice, this
               list of conditions and the following disclaimer.

            2. Redistributions in binary form must reproduce the above copyright notice,
               this list of conditions and the following disclaimer in the documentation
               and/or other materials provided with the distribution.

            3. Neither the name of the copyright holder nor the names of its
               contributors may be used to endorse or promote products derived from
               this software without specific prior written permission.

            THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
            AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
            IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
            DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
            FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
            DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
            SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
            CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
            OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
            OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """
        license_ = dedent(license_).strip()
        return license_


class Application:
    """A regex GUI class.

    Attributes
    ----------
    root (tkinter.Tk): a top tkinter app.
    content (Content): a Content instance.

    Methods
    -------
    build_menu() -> None
    run() -> None
    callback_file_open() -> None
    callback_file_exit() -> None
    callback_help_documentation() -> None
    callback_help_view_licenses() -> None
    callback_help_about() -> None
    """

    browser = webbrowser

    def __init__(self):
        self._base_title = 'Regex GUI'
        self.root = tk.Tk()
        self.root.geometry('800x600+100+100')
        self.root.minsize(200, 200)
        self.root.option_add('*tearOff', False)
        self.content = None

        self.panedwindow = None
        self.text_frame = None
        self.entry_frame = None
        self.result_frame = None

        self.radio_btn_var = tk.StringVar()
        self.used_space_var = tk.BooleanVar()
        self.used_space_var.set(True)
        self.prepended_ws_var = tk.BooleanVar()
        self.appended_ws_var = tk.BooleanVar()
        self.ignore_case_var = tk.BooleanVar()
        self.test_name_var = tk.StringVar()
        self.test_cls_name_var = tk.StringVar()
        self.test_cls_name_var.set('TestDynamicGenTestScript')
        self.is_minimal_var = tk.BooleanVar()
        self.is_minimal_var.set(True)
        self.max_words_var = tk.IntVar()
        self.max_words_var.set(6)
        self.filename_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.company_var = tk.StringVar()
        self.result = None

        self.textarea = None
        self.result_textarea = None
        self.line_radio_btn = None
        self.block_radio_btn = None

        self.set_title()
        self.build_menu()
        self.build_frame()
        self.build_textarea()
        self.build_entry()
        self.build_result()

    def get_textarea(self, node):
        """Get data from TextArea component
        Parameters
        ----------
        node (tk.Text): a tk.Text component
        Returns
        -------
        str: a text from TextArea component
        """
        text = node.get('1.0', 'end')
        last_char = text[-1]
        last_two_chars = text[-2:]
        if last_char == '\r' or last_char == '\n':
            return text[:-1]
        elif last_two_chars == '\r\n':
            return text[:-2]
        else:
            return text

    def set_textarea(self, node, data, title=''):
        """set data for TextArea component
        Parameters
        ----------
        node (tk.Text): a tk.Text component
        data (any): a data
        title (str): a title of window
        """
        data, title = str(data), str(title).strip()

        title and self.set_title(title=title)
        node.delete("1.0", "end")
        node.insert(tk.INSERT, data)

    def set_title(self, node=None, title=''):
        """Set a new title for tkinter component.

        Parameters
        ----------
        node (tkinter): a tkinter component.
        title (str): a title.  Default is empty.
        """
        node = node or self.root
        btitle = self._base_title
        title = '{} - {}'.format(title, btitle) if title else btitle
        node.title(title)

    def callback_file_exit(self):
        """Callback for Menu File > Exit."""
        self.root.quit()

    def callback_file_open(self):
        """Callback for Menu File > Open."""
        filetypes = [
            ('Text Files (*.txt)', '*.txt'),
            ('All Dot Files (*.*)', '*.*'),
            ('All Files', '*'),
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            with open(filename) as stream:
                content = stream.read()
                self.set_textarea(self.textarea, content, title=filename)

    def callback_help_documentation(self):
        """Callback for Menu Help > Getting Started."""
        self.browser.open_new_tab(Data.documentation_url)

    def callback_help_view_licenses(self):
        """Callback for Menu Help > View Licenses."""
        self.browser.open_new_tab(Data.license_url)

    def callback_help_about(self):
        """Callback for Menu Help > About"""
        def mouse_over(event):
            url_lbl.config(font=url_lbl.default_font + ('underline',))
            url_lbl.config(cursor='hand2')

        def mouse_out(event):
            url_lbl.config(font=url_lbl.default_font)
            url_lbl.config(cursor='arrow')

        def mouse_press(event):
            self.browser.open_new_tab(url_lbl.link)

        about = tk.Toplevel(self.root)
        self.set_title(node=about, title='About')
        width, height = 400, 400
        x, y = get_relative_center_location(self.root, width, height)
        about.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        about.resizable(False, False)

        # company
        fmt = 'Regex GUI v{} ({})'
        company_lbl = tk.Label(about, text=fmt.format(version, edition))
        company_lbl.place(x=10, y=10)

        # URL
        url = Data.repo_url
        tk.Label(about, text='URL:').place(x=10, y=40)
        url_lbl = tk.Label(about, text=url, fg='blue', font=('sans-serif', 10))
        url_lbl.default_font = ('sans-serif', 10)
        url_lbl.place(x=36, y=40)
        url_lbl.link = url

        url_lbl.bind('<Enter>', mouse_over)
        url_lbl.bind('<Leave>', mouse_out)
        url_lbl.bind('<Button-1>', mouse_press)

        # license textbox
        lframe = ttk.LabelFrame(
            about, height=280, width=380,
            text=Data.license_name
        )
        lframe.place(x=10, y=80)
        txtbox = tk.Text(lframe, width=45, height=14, wrap='word')
        txtbox.grid(row=0, column=0)
        scrollbar = ttk.Scrollbar(lframe, orient=tk.VERTICAL, command=txtbox.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        txtbox.config(yscrollcommand=scrollbar.set)
        txtbox.insert(tk.INSERT, Data.get_license())
        txtbox.config(state=tk.DISABLED)

        # footer - copyright
        footer = tk.Label(about, text=Data.copyright_text)
        footer.place(x=10, y=360)

    def callback_preferences_settings(self):
        """Callback for Menu Preferences > Settings"""

        settings = tk.Toplevel(self.root)
        self.set_title(node=settings, title='Settings')
        width, height = 400, 400
        x, y = get_relative_center_location(self.root, width, height)
        settings.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        settings.resizable(False, False)

        # Settings - Pattern Arguments
        lframe_pattern_args = ttk.LabelFrame(
            settings, height=80, width=380,
            text='Pattern Arguments'
        )
        lframe_pattern_args.place(x=10, y=10)

        # arguments checkboxes
        lst = [
            ['used_space', self.used_space_var, 5, 5],
            ['ignore_case', self.ignore_case_var, 120, 5],
            ['prepended_ws', self.prepended_ws_var, 5, 30],
            ['appended_ws', self.appended_ws_var, 120, 30]
        ]
        for text, variable, x, y in lst:
            ttk.Checkbutton(lframe_pattern_args, text=text, variable=variable,
                            onvalue=True, offvalue=False).place(x=x, y=y)

        # Settings - Regexapp Arguments
        lframe_regexapp_args = ttk.LabelFrame(
            settings, height=210, width=380,
            text='Regexapp Arguments'
        )
        lframe_regexapp_args.place(x=10, y=95)

        ttk.Label(lframe_regexapp_args, text='max_words').place(x=5, y=5)
        ttk.Entry(lframe_regexapp_args, width=5,
                  textvariable=self.max_words_var).place(x=88, y=5)

        ttk.Checkbutton(lframe_regexapp_args, text='is_minimal',
                        variable=self.is_minimal_var,
                        onvalue=True, offvalue=False).place(x=200, y=5)

        ttk.Label(lframe_regexapp_args, text='test_name').place(x=5, y=30)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.test_name_var).place(x=88, y=30)

        ttk.Label(lframe_regexapp_args, text='test_cls_name').place(x=5, y=55)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.test_cls_name_var).place(x=88, y=55)

        ttk.Label(lframe_regexapp_args, text='filename').place(x=5, y=80)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.filename_var).place(x=88, y=80)

        ttk.Label(lframe_regexapp_args, text='author').place(x=5, y=105)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.author_var).place(x=88, y=105)

        ttk.Label(lframe_regexapp_args, text='email').place(x=5, y=130)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.email_var).place(x=88, y=130)

        ttk.Label(lframe_regexapp_args, text='company').place(x=5, y=155)
        ttk.Entry(lframe_regexapp_args, width=45,
                  textvariable=self.company_var).place(x=88, y=155)

    def build_menu(self):
        """Build menubar for Regex GUI."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file = tk.Menu(menu_bar)
        preferences = tk.Menu(menu_bar)
        help_ = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=file, label='File')
        menu_bar.add_cascade(menu=preferences, label='Preferences')
        menu_bar.add_cascade(menu=help_, label='Help')

        file.add_command(label='Open', command=lambda: self.callback_file_open())
        file.add_separator()
        file.add_command(label='Quit', command=lambda: self.callback_file_exit())

        preferences.add_command(
            label='Settings',
            command=lambda: self.callback_preferences_settings()
        )
        preferences.add_separator()
        preferences.add_command(
            label='System References',
            command=lambda: create_msgbox(
                title='TODO item',
                info='TODO - Need to implement System References Window'
            )
        )
        preferences.add_separator()
        preferences.add_command(
            label='User References',
            command=lambda: create_msgbox(
                title='TODO item',
                info='TODO - Need to implement User References Window'
            )
        )

        help_.add_command(label='Documentation',
                          command=lambda: self.callback_help_documentation())
        help_.add_command(label='View Licenses',
                          command=lambda: self.callback_help_view_licenses())
        help_.add_separator()
        help_.add_command(label='About', command=lambda: self.callback_help_about())

    def build_frame(self):
        """Build layout for regex GUI."""
        self.panedwindow = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        self.text_frame = ttk.Frame(
            self.panedwindow, width=600, height=300, relief=tk.RIDGE
        )
        self.entry_frame = ttk.Frame(
            self.panedwindow, width=600, height=40, relief=tk.RIDGE
        )
        self.result_frame = ttk.Frame(
            self.panedwindow, width=600, height=350, relief=tk.RIDGE
        )
        self.panedwindow.add(self.text_frame, weight=4)
        self.panedwindow.add(self.entry_frame)
        self.panedwindow.add(self.result_frame, weight=5)

    def build_textarea(self):
        """Build input text for regex GUI."""

        self.text_frame.rowconfigure(0, weight=1)
        self.text_frame.columnconfigure(0, weight=1)
        self.textarea = tk.Text(self.text_frame, width=20, height=5, wrap='none')
        self.textarea.grid(row=0, column=0, sticky='nswe')
        vscrollbar = ttk.Scrollbar(
            self.text_frame, orient=tk.VERTICAL, command=self.textarea.yview
        )
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = ttk.Scrollbar(
            self.text_frame, orient=tk.HORIZONTAL, command=self.textarea.xview
        )
        hscrollbar.grid(row=1, column=0, sticky='ew')
        self.textarea.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set
        )

    def build_entry(self):
        """Build input entry for regex GUI."""
        def callback_run_btn():
            user_data = self.get_textarea(self.textarea)
            if not user_data:
                create_msgbox(
                    title='Empty Data',
                    error="Can not build regex pattern without data."
                )
                return

            is_line = self.radio_btn_var.get() == 'line'
            factory = RegexBuilder(user_data=user_data, is_line=is_line)
            factory.build()

            lst = []
            for user_data, pattern in factory.user_data_pattern_table.items():
                lst.append('# {}'.format('-' * 10))
                lst.append('# user data      : {}'.format(user_data))
                lst.append('# created pattern: {}'.format(pattern))

            result = '\n'.join(lst)
            self.set_textarea(self.result_textarea, result)

        def callback_clear_text_btn():
            self.textarea.delete("1.0", "end")
            self.result_textarea.delete("1.0", "end")
            self.result = None
            self.set_title()

        def callback_paste_text_btn():
            data = self.root.clipboard_get()
            if not data:
                return

            title = '<<PASTE - Clipboard>>'
            self.set_textarea(self.textarea, data, title=title)

        def callback_snippet_btn():
            create_msgbox(
                title='TODO item',
                info="TODO - Need to implement a function for snippet button"
            )

        def callback_unittest_btn():
            create_msgbox(
                title='TODO item',
                info="TODO - Need to implement a function for unittest button"
            )

        def callback_pytest_btn():
            create_msgbox(
                title='TODO item',
                info="TODO - Need to implement a function for pytest button"
            )

        def callback_rf_btn():
            create_msgbox(
                title='TODO item',
                info="TODO - Need to implement a function for Robotframework button"
            )

        # radio buttons
        self.line_radio_btn = ttk.Radiobutton(
            self.entry_frame, text='line', variable=self.radio_btn_var,
            value='line'
        )
        self.line_radio_btn.place(x=10, y=10)

        self.block_radio_btn = ttk.Radiobutton(
            self.entry_frame, text='block', variable=self.radio_btn_var,
            value='block'
        )
        self.block_radio_btn.place(x=55, y=10)
        self.block_radio_btn.invoke()

        # open button
        open_file_btn = ttk.Button(self.entry_frame, text='Open',
                                   command=self.callback_file_open, width=8)
        open_file_btn.place(x=110, y=10)

        # paste button
        paste_text_btn = ttk.Button(self.entry_frame, text='Paste',
                                    command=callback_paste_text_btn, width=8)
        paste_text_btn.place(x=170, y=10)

        # clear button
        clear_text_btn = ttk.Button(self.entry_frame, text='Clear',
                                    command=callback_clear_text_btn, width=8)
        clear_text_btn.place(x=230, y=10)

        # run button
        run_btn = ttk.Button(self.entry_frame, text='Run',
                             command=callback_run_btn, width=8)
        run_btn.place(x=290, y=10)

        # snippet button
        snippet_btn = ttk.Button(self.entry_frame, text='Snippet',
                                 command=callback_snippet_btn, width=8)
        snippet_btn.place(x=350, y=10)

        # unittest button
        unittest_btn = ttk.Button(self.entry_frame, text='Unittest',
                                  command=callback_unittest_btn, width=8)
        unittest_btn.place(x=410, y=10)

        # pytest button
        pytest_btn = ttk.Button(self.entry_frame, text='Pytest',
                                command=callback_pytest_btn, width=8)
        pytest_btn.place(x=470, y=10)

        # Robotframework button
        rf_btn = ttk.Button(self.entry_frame, text='Robotframework',
                            command=callback_rf_btn, width=16)
        rf_btn.place(x=530, y=10)

    def build_result(self):
        """Build result text"""
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.columnconfigure(0, weight=1)
        self.result_textarea = tk.Text(
            self.result_frame, width=20, height=5, wrap='none'
        )
        self.result_textarea.grid(row=0, column=0, sticky='nswe')
        vscrollbar = ttk.Scrollbar(
            self.result_frame, orient=tk.VERTICAL,
            command=self.result_textarea.yview
        )
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = ttk.Scrollbar(
            self.result_frame, orient=tk.HORIZONTAL,
            command=self.result_textarea.xview
        )
        hscrollbar.grid(row=1, column=0, sticky='ew')
        self.result_textarea.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set
        )

    def run(self):
        """Launch regex GUI."""
        self.root.mainloop()


def execute():
    """Launch regex GUI."""
    app = Application()
    app.run()
