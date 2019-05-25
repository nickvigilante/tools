from tkinter import *
import secrets, string, os, base64
import configparser as cp

def qe(str):
    return base64.b64encode(bytes(str, 'utf-8'))

def qd(str):
    return base64.b64decode(eval(str)).decode('utf-8')


class Config:

    def __init__(self):

        if not os.path.isfile('./config.ini'):
            self.build_config()
        self.cfg = self.read_config_ini_from_file()
    def build_config(self):
        settings = {
        'Character Sets':
            {
                'lc_set': string.ascii_lowercase,
                'uc_set': string.ascii_uppercase,
                'num_set': string.digits,
                'sym_set': qe(string.punctuation)
            },
        'User Preferences':
            {
                'use_lc': 1,
                'use_uc': 1,
                'use_num': 1,
                'use_sym': 0,
                'use_cs': 0,
                'cust_sym': 'b\'\'',
                'pass_len': 30,
            }
        }
        config = cp.ConfigParser()
        config.read_dict(settings)
        config.write(open('config.ini', 'w'))

    def read_config_ini_from_file(self):
        config = cp.ConfigParser()
        config.read('config.ini')
        return config


class PWApp(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        #define configuration
        self.cfg = Config().cfg
        master.protocol("WM_DELETE_WINDOW", self.save_and_quit)
        master.title("PassGen")
        self.vcscmd = (self.register(self.validate_symbols), '%S', '%s')

        # define frame containers
        self.bg = "gray25"
        self.fg = "gray90"

        self.settings = LabelFrame(master, text="Settings", padx=5, pady=5, bg=self.bg, fg=self.fg)
        self.settings.grid(row=0, column=0)

        self.buttons = LabelFrame(master, padx=6, pady=41, bg=self.bg, fg=self.fg, highlightcolor=self.bg, highlightbackground=self.bg, highlightthickness=0)
        self.buttons.grid(row=0, column=1)

        self.output = LabelFrame(master, text = "Output", padx=79, pady=5, bg=self.bg, fg=self.fg)
        self.output.grid(row=1, column=0, columnspan = 2)

        self.declare_vars()
        self.create_elements()
        self.create_cs_rb()

    def declare_vars(self):
        for sec in self.cfg.sections():
            for key in self.cfg[sec]:
                exec("self.{0} = StringVar(); self.{0}.set(self.cfg.get('{1}', '{0}'))".format(key, sec))

        self.cust_sym_dec = StringVar()
        self.cust_sym_dec.set(qd(self.cust_sym.get()))
        self.pwd = StringVar()

    def create_elements(self):
        # implement form elements
        self.lc = Checkbutton(self.settings, text="a-z", variable=self.use_lc, bg=self.bg, fg=self.fg)
        self.lc.grid(row=0, column=0)

        self.uc = Checkbutton(self.settings, text="A-Z", variable=self.use_uc, bg=self.bg, fg=self.fg)
        self.uc.grid(row=0, column=1)

        self.num = Checkbutton(self.settings, text="0-9", variable=self.use_num, bg=self.bg, fg=self.fg)
        self.num.grid(row=0, column=2)

        self.sym = Checkbutton(self.settings, text="!@#$", variable=self.use_sym, command=self.create_cs_rb, bg=self.bg, fg=self.fg)
        self.sym.grid(row=0, column=3)

        self.cs_opt_1 = Radiobutton(self.settings, text="Use custom symbols:", variable=self.use_cs, value=1, bg=self.bg, fg=self.fg)
        self.cs_opt_1.grid(row=2, column=0, columnspan=2)
        self.cs_opt_2 = Radiobutton(self.settings, text="Use default symbols", variable=self.use_cs, value=0, bg=self.bg, fg=self.fg)
        self.cs_opt_2.grid(row=3, column=0, columnspan=2)

        self.len_label = Label(self.settings, text="Password Length:", bg=self.bg, fg=self.fg)
        self.len_label.grid(row=1, column=0, columnspan=2)

        self.len = Entry(self.settings, text="Password Length", textvariable=self.pass_len, bg=self.bg, fg=self.fg)
        self.len.grid(row=1, column=2, columnspan=2)

        self.pwd_label = Label(self.output, text = "Password:", bg=self.bg, fg=self.fg)
        self.pwd_label.grid(row=0, column=0)

        self.pwd_field = Entry(self.output, text="Password", textvariable=self.pwd, width=30, bg=self.bg, fg=self.fg)
        self.pwd_field.grid(row=0, column=1)

        self.generate_button = Button(self.buttons, text="Generate Password", command=self.gen_pwd, bg=self.bg, fg="black", highlightcolor="black", highlightbackground=self.bg)
        self.generate_button.grid(row=0, column=0)

        self.quit_button = Button(self.buttons, text="Save and Quit", fg="red", command=self.save_and_quit, bg=self.bg, activebackground=self.bg, highlightcolor="black", highlightbackground="black")
        self.quit_button.grid(row=1, column=0)

    def create_cs_rb(self):
        disable_sym_rb = "DISABLED" if not getboolean(int(self.use_sym.get())) else "NORMAL"
        exec("self.cs_opt_1 = Radiobutton(self.settings, text='Use custom symbols:', variable=self.use_cs, value=1, command=self.create_cs_field, state={0}, bg=self.bg, fg=self.fg)".format(disable_sym_rb))
        self.cs_opt_1.grid(row=2, column=0, columnspan=2)
        exec("self.cs_opt_2 = Radiobutton(self.settings, text='Use default symbols', variable=self.use_cs, value=0, command=self.create_cs_field, state={0}, bg=self.bg, fg=self.fg)".format(disable_sym_rb))
        self.cs_opt_2.grid(row=3, column=0, columnspan=2)
        self.create_cs_field()

    def create_cs_field(self):

        disable_cs_field = "NORMAL" if getboolean(int(self.use_sym.get())) and getboolean(int(self.use_cs.get())) else "DISABLED"
        exec('self.cs = Entry(self.settings, text="Custom Symbols:", textvariable=self.cust_sym_dec, state={0}, validate="all", validatecommand=self.vcscmd, bg=self.bg, fg=self.fg, disabledforeground="gray30", disabledbackground="gray20")'.format(disable_cs_field))
        self.cs.grid(row=2, column=2, columnspan=2)

    def validate_symbols(self, S, s):
        result = (S not in self.lc_set.get()[:] + self.uc_set.get()[:] + self.num_set.get()[:] or S == ' ') and S not in self.cust_sym_dec.get()[:] and S not in s
        return result

    def gen_pwd(self):
        self.save_config()

        char_set = []

        getboolean(int(self.use_lc.get())) and char_set.extend(set(str(self.lc_set.get())))
        getboolean(int(self.use_uc.get())) and char_set.extend(set(str(self.uc_set.get())))
        getboolean(int(self.use_num.get())) and char_set.extend(set(str(self.num_set.get())))
        getboolean(int(self.use_sym.get())) and not getboolean(int(self.use_cs.get())) and char_set.extend(set(str(qd(self.sym_set.get()))))
        getboolean(int(self.use_sym.get())) and getboolean(int(self.use_cs.get())) and char_set.extend(set(str(qd(self.cust_sym.get()))))

        password = ''
        for i in range(0, int(self.pass_len.get())):
            password += secrets.choice(char_set)

        self.pwd.set(password)

    def save_config(self):
        self.cust_sym.set(qe(self.cust_sym_dec.get()))
        for key in self.cfg['User Preferences']:
            exec("self.cfg.set('User Preferences', '{0}', str(self.{0}.get()))".format(key))
        self.cfg.write(open('config.ini', 'w'))

    def save_and_quit(self):
        self.save_config()
        root.quit()


root = Tk()
app = PWApp(root)
root.mainloop()
