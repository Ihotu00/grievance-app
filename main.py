from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
import sqlite3
from kivy.properties import ObjectProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu 
from kivy.uix.anchorlayout import AnchorLayout 
from kivymd.uix.button import MDRaisedButton
from kivy.uix.widget import Widget



class Login(Screen):
    pass

class CreateAcc(Screen):
    pass

class WinMan(ScreenManager):
    pass

class Com(Screen):
    pass

class Home(Screen):
    pass

class Ahome(Screen):
    pass

class Update(Screen):
    pass

class Grievance2(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"        

        return Builder.load_file("students.kv")


    def cre(self):
        fname = self.root.get_screen("create").ids.fname.text
        lname = self.root.get_screen("create").ids.lname.text
        mno = self.root.get_screen("create").ids.mno.text 
        uname = self.root.get_screen("create").ids.uname.text
        passw = self.root.get_screen("create").ids.passw.text

        conn = sqlite3.connect("whynot.db")
        c = conn.cursor()

        sql = ("""INSERT INTO users
                    (First_Name, Last_Name, Mat_No, Username, Password)
                    VALUES (?, ?, ?, ?, ?);""")
        udata = (str(fname), str(lname), str(mno), str(uname), str(passw))
        c.execute(sql, udata)       
        # self.root.get_screen("home").data.text = f"Welcome {str(uname)}"     

        conn.commit()
        conn.close()        


    def log(self): 
        user = self.root.get_screen("log").ids.user.text
        passw1 = self.root.get_screen("log").ids.passw1.text


        conn = sqlite3.connect("whynot.db")
        c = conn.cursor()

        mop = ("""SELECT * from users
                    WHERE Username = ? AND Password = ? """)
        uin = (str(user), str(passw1))
        c.execute(mop, uin)
        dat = c.fetchall()
        amop = ("""SELECT * from admins
                        WHERE Username = ? AND Password = ? """)
        c.execute(amop, uin)
        adat = c.fetchall()
        if (len(dat) >= 1):
            self.root.current = "home"
        elif (len(adat) >= 1):
            self.root.current = "ahome"
        else:
            self.root.get_screen("log").ids.welcome_label.text = "Account not found"
            self.root.get_screen("log").ids.user.text = ""
            self.root.get_screen("log").ids.passw1.text = ""

        # self.root.get_screen("home").data.text = f"Welcome {str(user)}" 
               
        conn.commit()
        conn.close()


    def submit(self):
        dmnt = self.root.get_screen("comt").ids.dmnt.text
        griev = self.root.get_screen("comt").ids.griev.text
        sup = self.root.get_screen("log").ids.user.text

        conn = sqlite3.connect("whynot.db")
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        sub = ("""INSERT INTO grievance
                    (Department, Grievance, Supplicant)
                    VALUES (?, ?, ?);""")
        gdata = (str(dmnt), str(griev), str(sup))
        c.execute(sub, gdata)

        conn.commit()
        conn.close() 

        self.root.get_screen("comt").ids.dmnt.text = ""  
        self.root.get_screen("comt").ids.griev.text = ""


    def table(self):
        conn = sqlite3.connect("whynot.db")
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")


        supl = self.root.get_screen("log").ids.user.text
        c.execute("""SELECT Department, Grievance, Status from grievance
                    WHERE Supplicant = ? """, [supl])
        
        rows = c.fetchall()
        conn.commit()
        conn.close() 

        hm = self.root.get_screen("home")
        self.gtable = MDDataTable( 
            pos_hint = {"center_x": 0.5, "center_y": 0.5}, 
            use_pagination = True,
            size_hint = (0.9, 0.6),
            column_data = [
                ("Depratment", dp(100)),
                ("Grievance", dp(100)),
                ("Status", dp(100)),
            ],
            row_data = rows
            
        )
        hm.add_widget(self.gtable)
        return hm

        # self.root.get_screen("home").ids.layout.add_widget(self.gtable)
        

    def atable(self):
        conn = sqlite3.connect("whynot.db")
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        alog = (self.root.get_screen("log").ids.user.text)

        c.execute("""SELECT grievance.Grievance, grievance.Status from grievance 
                        INNER JOIN admins  ON grievance.Department = admins.Department
                        WHERE admins.Username = ?""", [alog])
        glist = c.fetchall()

        conn.commit()
        conn.close() 


        # dropdown_button = MDRaisedButton(text = "Select a status", size_hint = (None, None))

        # def callback(instance):
        #     pass

        # item1 = (OneLineListItem(text = f"Verifying", on_release = callback))
        # item2 = (OneLineListItem(text = f"Rectifying", on_release = callback))
        # item3 = (OneLineListItem(text = f"Complete", on_release = callback))

        # menu = MDDropdownMenu(
        #     caller = dropdown_button,
        #     items = (item1, item2, item3),
        #     )
        # print(menu)
        # menu.bind(on_release=self.set_item)


        ahm = self.root.get_screen("ahome")
        gtable = MDDataTable( 
            pos_hint = {"center_x": 0.5, "center_y": 0.5}, 
            size_hint = (0.9, 0.6),
            rows_num = 10,
            column_data = [
                ("Grievance", dp(100)),
                ("Status", dp(100)),
            ],
            row_data = glist
            # [
            #     (item[0], menu) 
            #             for item in glist
            # ]
        )

        ahm.add_widget(gtable)
        return ahm

    # def set_item(self, instance_menu, instance_menu_item):
    #     self.dropdown_button.set_item(instance_menu_item.text)
    #     instance_menu.dismiss()


        

Grievance2().run() 