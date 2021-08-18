"""Module containing the logic for the Regex application."""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from os import path
from pathlib import Path
import webbrowser
from textwrap import dedent
from regexapp import RegexBuilder
from regexapp.collection import REF
from regexapp.collection import PatternReference
from regexapp import version
from regexapp import edition
from regexapp.core import enclose_string

import yaml
import re
import platform


__version__ = version
__edition__ = edition


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


def create_msgbox(title=None, error=None, warning=None, info=None,
                  question=None, okcancel=None, retrycancel=None,
                  yesno=None, yesnocancel=None, **options):
    """create tkinter.messagebox
    Parameters
    ----------
    title (str): a title of messagebox.  Default is None.
    error (str): an error message.  Default is None.
    warning (str): a warning message. Default is None.
    info (str): an information message.  Default is None.
    question (str): a question message.  Default is None.
    okcancel (str): an ok or cancel message.  Default is None.
    retrycancel (str): a retry or cancel message.  Default is None.
    yesno (str): a yes or no message.  Default is None.
    yesnocancel (str): a yes, no, or cancel message.  Default is None.
    options (dict): options for messagebox.

    Returns
    -------
    any: a string or boolean result
    """
    if error:
        # a return result is a "ok" string
        result = messagebox.showerror(title=title, message=error, **options)
    elif warning:
        # a return result is a "ok" string
        result = messagebox.showwarning(title=title, message=warning, **options)
    elif info:
        # a return result is a "ok" string
        result = messagebox.showinfo(title=title, message=info, **options)
    elif question:
        # a return result is a "yes" or "no" string
        result = messagebox.askquestion(title=title, message=question, **options)
    elif okcancel:
        # a return result is boolean
        result = messagebox.askokcancel(title=title, message=okcancel, **options)
    elif retrycancel:
        # a return result is boolean
        result = messagebox.askretrycancel(title=title, message=retrycancel, **options)
    elif yesno:
        # a return result is boolean
        result = messagebox.askyesno(title=title, message=yesno, **options)
    elif yesnocancel:
        # a return result is boolean or None
        result = messagebox.askyesnocancel(title=title, message=yesnocancel, **options)
    else:
        # a return result is a "ok" string
        result = messagebox.showinfo(title=title, message=info, **options)

    return result


def set_modal_dialog(dialog):
    """set dialog to become a modal dialog

    Parameters
    ----------
    dialog (tkinter.TK): a dialog or window application.
    """
    dialog.transient(dialog.master)
    dialog.wait_visibility()
    dialog.grab_set()
    dialog.wait_window()


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
        self._base_title = 'Regexapp {}'.format(edition)
        self.root = tk.Tk()
        self.root.geometry('940x600+100+100')
        self.root.minsize(200, 200)
        self.root.option_add('*tearOff', False)
        self.content = None

        self.panedwindow = None
        self.text_frame = None
        self.entry_frame = None
        self.result_frame = None
        self.save_as_btn = None
        self.copy_text_btn = None

        self.test_data = None

        self.radio_line_or_multiline_btn_var = tk.StringVar()
        self.radio_line_or_multiline_btn_var.set('multiline')
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

        self.new_pattern_name_var = tk.StringVar()

        self.textarea = None
        self.result_textarea = None
        self.line_radio_btn = None
        self.multiline_radio_btn = None

        self.set_title()
        self.build_menu()
        self.build_frame()
        self.build_textarea()
        self.build_entry()
        self.build_result()

    def get_pattern_args(self):
        """return arguments of RegexBuilder class"""
        result = dict(
            used_space=self.used_space_var.get(),
            ignore_case=self.ignore_case_var.get(),
            prepended_ws=self.prepended_ws_var.get(),
            appended_ws=self.appended_ws_var.get(),
            is_line=self.radio_line_or_multiline_btn_var.get() == 'line'
        )
        return result

    def get_builder_args(self):
        """return arguments of DynamicGenTestScript class"""
        result = dict(
            test_name=self.test_name_var.get(),
            test_cls_name=self.test_cls_name_var.get(),
            is_minimal=self.is_minimal_var.get(),
            max_words=self.max_words_var.get(),
            filename=self.filename_var.get(),
            author=self.author_var.get(),
            email=self.email_var.get(),
            company=self.company_var.get()
        )
        return result

    def set_default_setting(self):
        """reset to default setting"""
        self.used_space_var.set(True)
        self.prepended_ws_var.set(False)
        self.appended_ws_var.set(False)
        self.ignore_case_var.set(False)
        self.test_name_var.set('')
        self.test_cls_name_var.set('TestDynamicGenTestScript')
        self.is_minimal_var.set(True)
        self.max_words_var.set(6)
        self.filename_var.set('')
        self.author_var.set('')
        self.email_var.set('')
        self.company_var.set('')

    @classmethod
    def get_textarea(cls, node):
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
                self.test_data = content
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

        is_macos = platform.system() == 'Darwin'

        about = tk.Toplevel(self.root)
        self.set_title(node=about, title='About')
        width, height = 400, 400
        x, y = get_relative_center_location(self.root, width, height)
        about.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        about.resizable(False, False)

        panedwindow = ttk.Panedwindow(about, orient=tk.VERTICAL)
        panedwindow.pack(fill=tk.BOTH, expand=True, padx=8, pady=12)

        # company
        frame = tk.Frame(panedwindow, width=380, height=20)
        panedwindow.add(frame, weight=1)

        fmt = 'Regex GUI v{} ({} Edition)'
        company_lbl = tk.Label(frame, text=fmt.format(version, edition))
        company_lbl.pack(side=tk.LEFT)

        # URL
        frame = tk.Frame(panedwindow, width=380, height=20)
        panedwindow.add(frame, weight=1)

        url = Data.repo_url
        tk.Label(frame, text='URL:').pack(side=tk.LEFT)
        font_size = 12 if is_macos else 10
        url_lbl = tk.Label(frame, text=url, fg='blue', font=('sans-serif', font_size))
        url_lbl.default_font = ('sans-serif', font_size)
        url_lbl.pack(side=tk.LEFT)
        url_lbl.link = url

        url_lbl.bind('<Enter>', mouse_over)
        url_lbl.bind('<Leave>', mouse_out)
        url_lbl.bind('<Button-1>', mouse_press)

        # license textbox
        lframe = ttk.LabelFrame(
            panedwindow, height=300, width=380,
            text=Data.license_name
        )
        panedwindow.add(lframe, weight=7)

        width = 49 if is_macos else 43
        height = 19 if is_macos else 15
        txtbox = tk.Text(lframe, width=width, height=height, wrap='word')
        txtbox.grid(row=0, column=0, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(lframe, orient=tk.VERTICAL, command=txtbox.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        txtbox.config(yscrollcommand=scrollbar.set)
        txtbox.insert(tk.INSERT, Data.get_license())
        txtbox.config(state=tk.DISABLED)

        # footer - copyright
        frame = tk.Frame(panedwindow, width=380, height=20)
        panedwindow.add(frame, weight=1)

        footer = tk.Label(frame, text=Data.copyright_text)
        footer.pack(side=tk.LEFT)

        set_modal_dialog(about)

    def callback_preferences_settings(self):
        """Callback for Menu Preferences > Settings"""

        is_macos = platform.system() == 'Darwin'
        is_linux = platform.system() == 'Linux'

        settings = tk.Toplevel(self.root)
        self.set_title(node=settings, title='Settings')
        width = 540 if is_macos else 490 if is_linux else 400
        height = 370
        x, y = get_relative_center_location(self.root, width, height)
        settings.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        settings.resizable(False, False)

        # Settings - Pattern Arguments
        lframe_pattern_args = ttk.LabelFrame(
            settings, height=80, width=380,
            text='Pattern Arguments'
        )
        lframe_pattern_args.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # arguments checkboxes
        lst = [
            ['used_space', self.used_space_var, 0, 0],
            ['ignore_case', self.ignore_case_var, 0, 1],
            ['prepended_ws', self.prepended_ws_var, 1, 0],
            ['appended_ws', self.appended_ws_var, 1, 1]
        ]
        for text, variable, row, column in lst:
            tk.Checkbutton(
                lframe_pattern_args, text=text, variable=variable,
                onvalue=True, offvalue=False
            ).grid(row=row, column=column, padx=2, pady=2, sticky=tk.W)

        # Settings - Builder Arguments
        lframe_builder_args = ttk.LabelFrame(
            settings, height=280, width=380,
            text='Builder Arguments'
        )
        # lframe_builder_args.place(x=10, y=95)
        lframe_builder_args.grid(row=1, column=0, padx=10, pady=(0, 10), sticky=tk.W)

        pady = 0 if is_macos else 3

        ttk.Label(
            lframe_builder_args, text='max_words'
        ).grid(row=0, column=0, columnspan=2, padx=2, pady=(5, pady), sticky=tk.W)

        ttk.Entry(
            lframe_builder_args, width=5, textvariable=self.max_words_var
        ).grid(row=0, column=2, padx=2, pady=(5, pady), sticky=tk.W)

        tk.Checkbutton(
            lframe_builder_args, text='is_minimal',
            variable=self.is_minimal_var, onvalue=True, offvalue=False
        ).grid(row=0, column=3, columnspan=3, padx=2, pady=(5, pady), sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='test_name'
        ).grid(row=1, column=0, columnspan=2, padx=2, pady=pady, sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.test_name_var
        ).grid(row=1, column=2, columnspan=4, padx=2, pady=pady, sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='test_cls_name'
        ).grid(row=2, column=0, columnspan=2, padx=2, pady=pady, sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.test_cls_name_var
        ).grid(row=2, column=2, columnspan=4, padx=2, pady=pady, sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='filename'
        ).grid(row=3, column=0, columnspan=2, padx=2, pady=pady, sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.filename_var
        ).grid(row=3, column=2, columnspan=4, padx=2, pady=pady, sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='author'
        ).grid(row=4, column=0, columnspan=2, padx=2, pady=pady, sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.author_var
        ).grid(row=4, column=2, columnspan=4, padx=2, pady=pady, sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='email'
        ).grid(row=5, column=0, columnspan=2, padx=2, pady=pady, sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.email_var
        ).grid(row=5, column=2, columnspan=4, padx=2, pady=pady, sticky=tk.W)

        ttk.Label(
            lframe_builder_args, text='company'
        ).grid(row=6, column=0, columnspan=2, padx=2, pady=(pady, 10), sticky=tk.W)
        ttk.Entry(
            lframe_builder_args, width=45,
            textvariable=self.company_var
        ).grid(row=6, column=2, columnspan=4, padx=2, pady=(pady, 10), sticky=tk.W)

        # OK and Default buttons
        frame = tk.Frame(
            settings, height=20, width=380
        )
        frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E+tk.S)

        ttk.Button(
            frame, text='Default',
            command=lambda: self.set_default_setting(),
        ).grid(row=0, column=6, padx=1, pady=1, sticky=tk.E)

        ttk.Button(
            frame, text='OK',
            command=lambda: settings.destroy(),
        ).grid(row=0, column=7, padx=1, pady=1, sticky=tk.E)

        set_modal_dialog(settings)

    def callback_preferences_system_reference(self):
        """Callback for Menu Preferences > System References"""

        is_macos = platform.system() == 'Darwin'

        sys_ref = tk.Toplevel(self.root)
        self.set_title(node=sys_ref, title='System References')
        width, height = 600, 500
        x, y = get_relative_center_location(self.root, width, height)
        sys_ref.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        panedwindow = ttk.Panedwindow(sys_ref, orient=tk.VERTICAL)
        panedwindow.pack(fill=tk.BOTH, expand=True)

        text_frame = ttk.Frame(
            panedwindow, width=500, height=300, relief=tk.RIDGE
        )
        panedwindow.add(text_frame, weight=9)

        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        textarea = tk.Text(text_frame, width=20, height=5, wrap='none')
        with open(REF.sys_ref_loc) as stream:
            content = stream.read()
            self.set_textarea(textarea, content)

        textarea.grid(row=0, column=0, sticky='nswe')
        vscrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=textarea.yview
        )
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = ttk.Scrollbar(
            text_frame, orient=tk.HORIZONTAL, command=textarea.xview
        )
        hscrollbar.grid(row=1, column=0, sticky='ew')
        textarea.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set,
            state=tk.DISABLED
        )

        padx, pady = (0, 0) if is_macos else (2, 2)
        ttk.Button(sys_ref, text='OK',
                   command=lambda: sys_ref.destroy()
                   ).pack(side=tk.RIGHT, padx=padx, pady=pady)

        set_modal_dialog(sys_ref)

    def callback_preferences_user_reference(self):
        """Callback for Menu Preferences > User References"""
        def save(node):
            fn_ = REF.user_ref_loc
            origin_content = open(fn_).read()
            new_content = node.get('1.0', 'end')
            if new_content.strip() == origin_content.strip():
                return
            else:
                try:
                    REF.test(new_content)
                    open(fn_, 'w').write(new_content)

                    yaml_obj = yaml.load(new_content, Loader=yaml.SafeLoader)
                    REF.update(yaml_obj)

                except Exception as ex:
                    error = '{}: {}'.format(type(ex).__name__, ex)
                    create_msgbox(title='Invalid Format', error=error)

        def insert(var, node):
            name = var.get().strip()
            if not re.match(r'\w+$', name):
                error = 'Name of pattern must be alphanumeric and/or underscore'
                create_msgbox(title='Pattern Naming', error=error)
                return

            content_ = node.get('1.0', 'end')
            is_duplicated = False

            for line in content_.splitlines():
                if line.startswith('{}:'.format(name)):
                    is_duplicated = True
                    break

            if is_duplicated:
                fmt = 'This "{}" name already exist.  Please use a different name.'
                error = fmt.format(name)
                create_msgbox(title='Pattern Naming', error=error)
                return

            var.set('')
            pattern_layout = PatternReference.get_pattern_layout(name)
            pattern_layout = pattern_layout.replace('name_placeholder', name)
            new_content_ = '{}\n\n{}\n'.format(content_.strip(), pattern_layout).lstrip()
            node.delete("1.0", "end")
            node.insert(tk.INSERT, new_content_)

        is_macos = platform.system() == 'Darwin'

        fn = REF.user_ref_loc
        file_obj = Path(fn)
        if not file_obj.exists():
            question = '{!r} IS NOT EXISTED.\nDo you want to create?'.format(fn)
            result = create_msgbox(question=question)
            if result == 'yes':
                not file_obj.parent.exists() and file_obj.parent.mkdir()
                file_obj.touch()
            else:
                return

        user_ref = tk.Toplevel(self.root)
        # user_ref.bind("<FocusOut>", lambda event: user_ref.destroy())
        self.set_title(node=user_ref, title='User References ({})'.format(fn))
        width, height = 600, 500
        x, y = get_relative_center_location(self.root, width, height)
        user_ref.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        panedwindow = ttk.Panedwindow(user_ref, orient=tk.VERTICAL)
        panedwindow.pack(fill=tk.BOTH, expand=True)

        text_frame = ttk.Frame(
            panedwindow, width=500, height=300, relief=tk.RIDGE
        )
        panedwindow.add(text_frame, weight=9)

        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        textarea = tk.Text(text_frame, width=20, height=5, wrap='none')

        with open(REF.user_ref_loc) as stream:
            content = stream.read()
            self.set_textarea(textarea, content)

        textarea.grid(row=0, column=0, sticky='nswe')
        vscrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=textarea.yview
        )
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = ttk.Scrollbar(
            text_frame, orient=tk.HORIZONTAL, command=textarea.xview
        )
        hscrollbar.grid(row=1, column=0, sticky='ew')
        textarea.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set,
        )

        padx, pady = (0, 0) if is_macos else (2, 2)

        ttk.Button(
            user_ref, text='Save', command=lambda: save(textarea)
        ).pack(side=tk.RIGHT, padx=padx, pady=pady)

        ttk.Button(
            user_ref, text='Close', command=lambda: user_ref.destroy()
        ).pack(side=tk.RIGHT, padx=padx, pady=pady)

        tk.Label(user_ref, text='Name:').pack(side=tk.LEFT, padx=padx, pady=pady)

        ttk.Entry(
            user_ref, width=25, textvariable=self.new_pattern_name_var
        ).pack(side=tk.LEFT, padx=padx, pady=pady)

        ttk.Button(
            user_ref, text='Insert',
            command=lambda: insert(self.new_pattern_name_var, textarea),
        ).pack(side=tk.LEFT, padx=padx, pady=pady)

        set_modal_dialog(user_ref)

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
            command=lambda: self.callback_preferences_system_reference()
        )
        preferences.add_separator()
        preferences.add_command(
            label='User References',
            command=lambda: self.callback_preferences_user_reference()
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
        self.panedwindow.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

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
        def callback_build_btn():
            user_data = Application.get_textarea(self.textarea)
            if not user_data:
                create_msgbox(
                    title='Empty Data',
                    error="Can NOT build regex pattern without data."
                )
                return

            try:
                kwargs = self.get_pattern_args()
                factory = RegexBuilder(user_data=user_data, **kwargs)
                factory.build()

                patterns = factory.patterns
                total = len(patterns)
                if total >= 1:
                    if total == 1:
                        result = 'pattern = r{}'.format(enclose_string(patterns[0]))
                    else:
                        lst = []
                        fmt = 'pattern{} = r{}'
                        for index, pattern in enumerate(patterns, 1):
                            lst.append(fmt.format(index, enclose_string(pattern)))
                        result = '\n'.join(lst)
                    self.set_textarea(self.result_textarea, result)
                    self.save_as_btn.config(state=tk.NORMAL)
                    self.copy_text_btn.config(state=tk.NORMAL)
                else:
                    error = 'Something wrong with RegexBuilder.  Please report bug.'
                    create_msgbox(title='RegexBuilder Error', error=error)
            except Exception as ex:
                error = '{}: {}'.format(type(ex).__name__, ex)
                create_msgbox(title='RegexBuilder Error', error=error)

        def callback_save_as_btn():
            filename = filedialog.asksaveasfilename()
            if filename:
                with open(filename, 'w') as stream:
                    content = Application.get_textarea(self.result_textarea)
                    stream.write(content)

        def callback_clear_text_btn():
            self.textarea.delete("1.0", "end")
            self.result_textarea.delete("1.0", "end")
            self.save_as_btn.config(state=tk.DISABLED)
            self.copy_text_btn.config(state=tk.DISABLED)
            self.test_data = None
            # self.root.clipboard_clear()
            self.set_title()

        def callback_copy_text_btn():
            content = Application.get_textarea(self.result_textarea)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

        def callback_paste_text_btn():
            try:
                data = self.root.clipboard_get()
                if not data:
                    return

                self.test_data = data

                title = '<<PASTE - Clipboard>>'
                self.set_textarea(self.textarea, data, title=title)
            except Exception as ex:     # noqa
                create_msgbox(
                    title='Empty Clipboard',
                    info='CAN NOT paste because there is no data in pasteboard.'
                )

        def callback_snippet_btn():
            if self.test_data is None:
                create_msgbox(
                    title='No Test Data',
                    error=("Can NOT build Python test script without "
                           "test data.\nPlease use Open or Paste button "
                           "to load test data")
                )
                return

            user_data = Application.get_textarea(self.textarea)
            if not user_data:
                create_msgbox(
                    title='Empty Data',
                    error="Can NOT build Python test script without data."
                )
                return

            try:
                kwargs = self.get_pattern_args()
                factory = RegexBuilder(
                    user_data=user_data, test_data=self.test_data, **kwargs
                )

                kwargs = self.get_builder_args()
                script = factory.generate_python_test(**kwargs)
                self.set_textarea(self.result_textarea, script)
                self.save_as_btn.config(state=tk.NORMAL)
                self.copy_text_btn.config(state=tk.NORMAL)
            except Exception as ex:
                error = '{}: {}'.format(type(ex).__name__, ex)
                create_msgbox(title='RegexBuilder Error', error=error)

        def callback_unittest_btn():
            if self.test_data is None:
                create_msgbox(
                    title='No Test Data',
                    error=("Can NOT build Python Unittest script without "
                           "test data.\nPlease use Open or Paste button "
                           "to load test data")
                )
                return

            user_data = Application.get_textarea(self.textarea)
            if not user_data:
                create_msgbox(
                    title='Empty Data',
                    error="Can NOT build Python Unittest script without data."
                )
                return

            try:
                kwargs = self.get_pattern_args()
                factory = RegexBuilder(
                    user_data=user_data, test_data=self.test_data, **kwargs
                )

                kwargs = self.get_builder_args()
                script = factory.generate_unittest(**kwargs)
                self.set_textarea(self.result_textarea, script)
                self.save_as_btn.config(state=tk.NORMAL)
                self.copy_text_btn.config(state=tk.NORMAL)
            except Exception as ex:
                error = '{}: {}'.format(type(ex).__name__, ex)
                create_msgbox(title='RegexBuilder Error', error=error)

        def callback_pytest_btn():
            if self.test_data is None:
                create_msgbox(
                    title='No Test Data',
                    error=("Can NOT build Python Pytest script without "
                           "test data.\nPlease use Open or Paste button "
                           "to load test data")
                )
                return

            user_data = Application.get_textarea(self.textarea)
            if not user_data:
                create_msgbox(
                    title='Empty Data',
                    error="Can NOT build Python Pytest script without data."
                )
                return

            try:
                kwargs = self.get_pattern_args()
                factory = RegexBuilder(
                    user_data=user_data, test_data=self.test_data, **kwargs
                )

                kwargs = self.get_builder_args()
                script = factory.generate_pytest(**kwargs)
                self.set_textarea(self.result_textarea, script)
                self.save_as_btn.config(state=tk.NORMAL)
                self.copy_text_btn.config(state=tk.NORMAL)
            except Exception as ex:
                error = '{}: {}'.format(type(ex).__name__, ex)
                create_msgbox(title='RegexBuilder Error', error=error)

        # def callback_rf_btn():
        #     create_msgbox(
        #         title='Robotframework feature',
        #         info="Robotframework button is available in Pro or Enterprise Edition."
        #     )

        # radio buttons
        self.line_radio_btn = tk.Radiobutton(
            self.entry_frame, text='line',
            variable=self.radio_line_or_multiline_btn_var,
            value='line'
        )
        self.line_radio_btn.grid(row=0, column=0, padx=(4, 0))

        self.multiline_radio_btn = tk.Radiobutton(
            self.entry_frame, text='multiline',
            variable=self.radio_line_or_multiline_btn_var,
            value='multiline'
        )
        self.multiline_radio_btn.grid(row=0, column=1, padx=2)

        # open button
        open_file_btn = ttk.Button(self.entry_frame, text='Open',
                                   command=self.callback_file_open)
        open_file_btn.grid(row=0, column=2, pady=2)

        # Save As button
        self.save_as_btn = ttk.Button(self.entry_frame, text='Save As',
                                      command=callback_save_as_btn)
        self.save_as_btn.grid(row=0, column=3)
        self.save_as_btn.config(state=tk.DISABLED)

        # copy button
        self.copy_text_btn = ttk.Button(self.entry_frame, text='Copy',
                                        command=callback_copy_text_btn)
        self.copy_text_btn.grid(row=0, column=4)
        self.copy_text_btn.config(state=tk.DISABLED)

        # paste button
        paste_text_btn = ttk.Button(self.entry_frame, text='Paste',
                                    command=callback_paste_text_btn)
        paste_text_btn.grid(row=0, column=5)

        # clear button
        clear_text_btn = ttk.Button(self.entry_frame, text='Clear',
                                    command=callback_clear_text_btn)
        clear_text_btn.grid(row=0, column=6)

        # build button
        build_btn = ttk.Button(self.entry_frame, text='Build',
                               command=callback_build_btn)
        build_btn.grid(row=0, column=7)

        # snippet button
        snippet_btn = ttk.Button(self.entry_frame, text='Snippet',
                                 command=callback_snippet_btn)
        snippet_btn.grid(row=0, column=8)

        # unittest button
        unittest_btn = ttk.Button(self.entry_frame, text='Unittest',
                                  command=callback_unittest_btn)
        unittest_btn.grid(row=0, column=9)

        # pytest button
        pytest_btn = ttk.Button(self.entry_frame, text='Pytest',
                                command=callback_pytest_btn)
        pytest_btn.grid(row=0, column=10)

        # Robotframework button
        # rf_btn = ttk.Button(self.entry_frame, text='RF',
        #                     command=callback_rf_btn, width=4)
        # rf_btn.grid(row=0, column=11)

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
