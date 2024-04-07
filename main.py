import flet as ft
import sqlite3
import random

class BD:
    def __init__(self):
        self.conn = sqlite3.connect('Students.db')
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS Students;")
        self.cur.execute("DROP TABLE IF EXISTS Competencies;")

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Students(
                        id INTEGER PRIMARY KEY,
                        system_id INTEGER,
                        name1 TEXT,
                        name2 TEXT,
                        name3 TEXT,
                        university TEXT, 
                        tel INTEGER,
                        email TEXT,
                        password TEXT,
                        mode TEXT);
                    ''')
        self.conn.commit()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Competencies(
                                id INTEGER PRIMARY KEY,
                                competencies1 INTEGER,
                                competencies2 INTEGER,
                                competencies3 INTEGER,
                                competencies4 INTEGER,
                                competencies5 INTEGER,
                                competencies6 INTEGER,
                                competencies7 INTEGER,
                                competencies8 INTEGER,
                                competencies9 INTEGER);
                              ''')
        self.conn.commit()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Events(
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                type TEXT,
                                date TEXT,
                                description TEXT);''')
        self.conn.commit()

    def addEvent(self, id, name, type, date, description):
        self.cur.execute(
            f"INSERT INTO Events (id, name, type, date, description) VALUES (?, ?, ?, ?, ?)",
            (id, name, type, date, description))
        self.conn.commit()
        self.cur.execute(
            f"INSERT INTO Competencies (id, competencies1, competencies2, competencies3, competencies4, competencies5, competencies6, competencies7, competencies8, competencies9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.conn.commit()

    def showAllEvents(self):
        sqlite_select_query = """SELECT id from Events"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        return records
    def studentAdd(self,id, name, university, tel, email, password, mode):
        self.cur.execute(f"INSERT INTO Students (id, name1, name2, name3, university, tel, email, password, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (id, name[0], name[1], name[2], university, tel, email, password, mode))
        self.conn.commit()
        self.cur.execute(
            f"INSERT INTO Competencies (id, competencies1, competencies2, competencies3, competencies4, competencies5, competencies6, competencies7, competencies8, competencies9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.conn.commit()

    def changeLvlComp(self, id, a, b, c, d, e, w, q, t, y):
        self.cur.execute(f"UPDATE Competencies SET competencies1 = ?, competencies2 = ?, competencies3 = ?, competencies4=?, competencies5=?, competencies6=?, competencies7=?, competencies8=?, competencies9=? WHERE id = {id}",
                         (a, b, c, d, e, w, q, t, y))

    def studentDel(self, id):
        self.cur.execute(f"SELECT id FROM Students WHERE id = {id}")
        iid = self.cur.fetchone()[0]
        self.cur.execute(f"DELETE FROM Students WHERE id = {id}")
        self.cur.execute(f"DELETE FROM Competencies WHERE id = {id}")
        self.conn.commit()

    def showStudent(self, id):
        self.cur.execute(f"SELECT id, name1, email, password FROM Students WHERE id = {id}")
        print(self.cur.fetchone())
        self.conn.commit()
        self.cur.execute(f"SELECT id, competencies1, competencies2, competencies3, competencies4, competencies5, competencies6, competencies7, competencies8, competencies9 FROM Competencies WHERE id = {id}")
        print(self.cur.fetchone())
        self.conn.commit()

    def compeShow(self, id):
        self.cur.execute(
            f"SELECT id, competencies1, competencies2, competencies3, competencies4, competencies5, competencies6, competencies7, competencies8, competencies9 FROM Competencies WHERE id = {id}")
        return self.cur.fetchone()

    def idFromEmail(self, eMail):
        self.cur.execute(f"SELECT id FROM Students WHERE email = {eMail}")
        return self.cur.fetchone()[0]
    def isFindStudent(self, eMail, password):
        self.cur.execute(f"SELECT id FROM Students WHERE email = ? and password = ?", (eMail, password))
        if self.cur.fetchone():
            return True
        else:
            return False

    def query(self, query):
        self.cur.execute(query)
        mas = self.cur.fetchone()
        return mas

    def allId(self):
        sqlite_select_query = """SELECT id, name1, name2, name3 from Students"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        return records


def appendCompMas(mas):
    mass = []
    for i in range(1, 10):
        if mas[i] != 0:
            mass.append(
                ft.Card(
                    ft.Container(
                        ft.Text(f"Компитенция{i}" if mas[i] != 0 else None, color="#000000", weight=ft.FontWeight.W_500,
                                size=15),
                        padding=6 if mas[i] != 0 else 0
                    ),
                    color=None if mas[i] == 0 else (ft.colors.YELLOW if mas[i] == 1 else ft.colors.GREEN)
                )
            )
    return mass

def main(page: ft.Page):
    page.title = "Tyumen campus"
    page.padding = 0
    page.window_maximized = True

    bd = BD()
    tid = ""
    for i in range(0, 9):
        tid += str(random.randint(0, 9))
    bd.studentAdd(tid, ("Assesor", "1", "2"), "lol", 123123, "12", "12", "assesor")
    bd.changeLvlComp(bd.allId()[0][0], 0, 2, 0, 1, 1, 0, 0, 0, 2)
    bd.showStudent(bd.allId()[0][0])
    events = bd.showAllEvents()
    students = bd.allId()
    for i in events:
        bd.changeLvlComp(i[0], 1, 2, 0, 0, 0, 2, 1, 0, 5)

    compRow = ft.Row([], width=564, wrap=True)

    rName1 = ft.TextField(label="ФАМИЛИЯ", text_size=30)
    rName2 = ft.TextField(label="ИМЯ", text_size=30)
    rName3 = ft.TextField(label="ОТЧЕСТВО", text_size=30)
    rEmail = ft.TextField(label="EMAIL", text_size=30)
    rPass = ft.TextField(label="ПАРОЛЬ", text_size=30)
    rPassCheck = ft.TextField(label="ПОВТОРИТЕ ПОРОЛЬ", text_size=30)
    rNum = ft.TextField(label="НОМЕР ТЕЛЕФОНА", text_size=30)
    rUnivers = ft.Dropdown(options=[
                                ft.dropdown.Option("ТИУ"),
                                ft.dropdown.Option("ТюмГУ"),
                                ft.dropdown.Option("ТюмГМУ"),
                                ft.dropdown.Option("ГАУ Северного Зауралья"),
                                ft.dropdown.Option("ТГИК"),
                            ],
                                width=400,
                                text_size=30,
                                label="ВУЗ")
    error = ft.Text("", color=ft.colors.RED, size=20)
    infID = ft.Text("", color="#627254", weight=ft.FontWeight.W_500, size=15)
    infNAME1 = ft.Text(f"", color="#627254", weight=ft.FontWeight.W_500, size=15)
    infNAME2 = ft.Text(f"", color="#627254", weight=ft.FontWeight.W_500, size=15)
    infNAME3 = ft.Text(f"", color="#627254", weight=ft.FontWeight.W_500, size=15)

    topEvent = ft.Card(
                content=ft.Column
                    (
                [
                            ft.Container(
                                ft.Text("МЕРОПРИЯТИЯ ПО ВАШИМ НАПРВЛЕНИЯМ", color="#FFFFFF",
                                        weight=ft.FontWeight.W_500, size=19),
                                padding=10
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.Card(
                                        ft.Container(
                                            ft.Text("Компетенция", color="#000000", weight=ft.FontWeight.W_500, size=15),
                                            padding=10
                                        ),
                                        color="#90D26D"
                                    )
                                ], width=431, wrap=True),
                                padding=10,
                            )
                        ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                color="#B8D4FF",
                width=431,
                height=258,
            )

    contentColumn1 = ft.Column([
                ft.Row([
                    ft.Container (
                        ft.Text("ГЛАВНАЯ", color="#000000", weight=ft.FontWeight.W_500, size=40),
                        padding=50
                    ),
                ]),
                ft.Row([
                    ft.Container(
                        ft.Text("ДОСТУПНЫЕ МЕРОПРИЯТИЯ", color="#000000", weight=ft.FontWeight.W_500, size=20),
                        padding=ft.padding.only(left=50),

                    ),
                ]),
                ft.Row([
                    ft.Container(
                        topEvent,
                        padding=ft.padding.only(left=50)
                    ),
                    ft.Container(
                        ft.Card(
                            ft.Column([
                                ft.Container(
                                    ft.Text("МЕРОПРИЯТИЯ, КОТОРЫЕ МОГУТ ВАМ ПОНРАВИТСЯ", color="#FFFFFF",
                                            weight=ft.FontWeight.W_500, size=19),
                                    padding=10
                                ),
                                ft.Container(
                                    ft.Row([
                                        ft.Card(
                                            ft.Container(
                                                ft.Text("Компетенция", color="#000000", weight=ft.FontWeight.W_500, size=15),
                                                padding=10
                                            ),
                                            color="#90D26D"
                                        )
                                    ], width=431, wrap=True),
                                    padding=10,

                                )

                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                            color="#B8D4FF",
                            width=431,
                            height=258,
                        ),
                        padding=ft.padding.only(left=50)
                    )
                ]),
                ft.Row([
                    ft.Container(
                        ft.Text("РАЗВЛЕКАТЕЛЬНЫЕ МЕРОПРИЯТИЯ", color="#000000", weight=ft.FontWeight.W_500, size=20),
                        padding=ft.padding.only(left=50, top=50),
                    ),
                ]),
                ft.ListView([
                    ft.Card(
                        ft.Container(
                            ft.Row([
                                ft.Container(
                                    ft.Image(
                                        src="venv/content/road.jpg",
                                        height=290,
                                        width=290
                                    ),
                                    padding=ft.padding.only(left=20)
                                ),
                                ft.Container(
                                    ft.Column([
                                        ft.Container(
                                            ft.Column([
                                                ft.Text(f"{bd.query(f"SELECT name FROM Events WHERE id = {i[0]}")[0]}",
                                                        color="#FFFFFF",
                                                        weight=ft.FontWeight.W_500, size=19),
                                                ft.Text(f"{bd.query(f"SELECT description FROM Events WHERE id = {i[0]}")[0]}",
                                                        color="#FFFFFF",
                                                        weight=ft.FontWeight.W_200, size=15),
                                            ])
                                        ),
                                        ft.Row([], #appendCompMas(bd.compeShow(i[0]))
                                        run_spacing=2,
                                        spacing=2,
                                        width=431,
                                        wrap=True),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    margin=15

                                ),

                            ], vertical_alignment=ft.CrossAxisAlignment.START),
                            height=258,
                        ),

                        color="#B8D4FF",
                    ) for i in events

                ],padding=ft.padding.only(left=50),width=969,height=460,),
            ])


    lEmail = ft.TextField(label="Электронная почта", width=500)
    lPassword = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=500)

    def registr(e):
        if rName1.value and rName2.value and rName3.value and rEmail.value and rPass.value and rPassCheck.value and rNum.value and rUnivers.value:
            if rPass.value == rPassCheck.value:
                id = ""
                for i in range(0, 9):
                    id += str(random.randint(0, 9))
                bd.studentAdd(id, (rName1.value, rName2.value, rName3.value), rUnivers.value, rNum.value, f"{rEmail.value}", rPass.value, "student")
                content.controls = login
                page.update()
            else:
                error.value = "Пароли не совпадают!"
                page.update()
        else:
            error.value = "Не все поля заполнены!"
            page.update()

    def login(e):
        if bd.isFindStudent(lEmail.value, lPassword.value):
            mas = bd.query(f"SELECT name1, name2, name3, mode FROM Students WHERE email = {f"{lEmail.value}"} and password = {lPassword.value}")
            infID.value = f"ID: {bd.idFromEmail(lEmail.value)}"
            infNAME1.value = mas[0]
            infNAME2.value = mas[1]
            infNAME3.value = mas[2]
            print(bd.showAllEvents()[0])
            students = bd.allId()
            topEvent.content = ft.Column(
                [
                            ft.Container(
                                ft.Text("МЕРОПРИЯТИЕ ПО ВАШИМ НАПРВЛЕНИЯМ", color="#FFFFFF",
                                        weight=ft.FontWeight.W_500, size=19),
                                padding=10
                            ),
                            ft.Container(
                                # ft.Text(bd.query(f"SELECT name FROM Events WHERE id = {bd.showAllEvents()[0]}")[0], color="#FFFFFF",
                                #         weight=ft.FontWeight.W_500, size=19),
                                padding=10
                            ),
                            ft.Container(
                                ft.Row([
                                    ft.Card(
                                        ft.Container(
                                            ft.Text("Компетенция", color="#000000", weight=ft.FontWeight.W_500, size=15),
                                            padding=10
                                        ),
                                        color="#90D26D"
                                    )
                                ], width=431, wrap=True),
                                padding=10,
                            )
                        ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            if mas[3] == "assesor":
                contentColumn1.controls = [
                    ft.Row([
                        ft.Container(
                            ft.Text("ГЛАВНАЯ", color="#000000", weight=ft.FontWeight.W_500, size=40),
                            padding=50
                        ),
                    ]),
                    ft.Row([
                        ft.Container(
                            ft.Text("СПИСОК СТУДЕНТОВ", color="#000000", weight=ft.FontWeight.W_500, size=20),
                            padding=ft.padding.only(left=50),

                        ),
                    ]),
                    ft.ListView([
                        ft.Card(
                            ft.Container(
                                ft.Row([
                                    ft.Container(
                                        ft.Image(
                                            src="venv/content/road.jpg",
                                            height=120,
                                            width=120
                                        ),
                                        padding=ft.padding.only(left=20)
                                    ),
                                    ft.Container(
                                        ft.Column([
                                            ft.Container(
                                                ft.Column([
                                                    ft.Text(
                                                        f"{bd.query(f"SELECT name1 FROM Students WHERE id = {i[0]}")[0]}",
                                                        color="#FFFFFF",
                                                        weight=ft.FontWeight.W_500, size=14),
                                                ])
                                            )
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        margin=15

                                    ),

                                ], vertical_alignment=ft.CrossAxisAlignment.START),
                                height=160,
                            ),

                            color="#B8D4FF",
                        ) for i in students

                    ], padding=ft.padding.only(left=50), width=969, height=660, divider_thickness=2)
                ]
            mas = bd.compeShow(bd.idFromEmail(lEmail.value))
            compRow.controls = appendCompMas(mas)


            content.controls = lk
            page.update()
        else:
            error.value = "Неверный логин или пароль!"
            page.update()

    def registrMenu(e):
        error.value = ""
        content.controls = [
                ft.Row(
                    [
                        ft.Image(src="venv/content/logo.png", height=168, width=168),
                        ft.Text("РЕГИСТРАЦИЯ", size=50),
                        ft.Container(height=100, width=100),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    rName1,
                                    rName2,
                                    rName3
                                ],
                                spacing=30
                            ),
                            margin=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    rEmail,
                                    rPass,
                                    rPassCheck,
                                ],
                                spacing=30
                            ),
                            margin=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    ft.Row(
                        [
                            rNum,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    margin=10
                ),
                ft.Container(
                    ft.Row(
                        [
                            rUnivers,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    margin=10
                ),
                ft.Container(ft.Row([error], alignment=ft.MainAxisAlignment.CENTER), height=60),
                ft.TextButton("РЕГИСТРАЦИЯ", scale=2, on_click=registr),
                ft.Container(height=140),
                ft.Text("Нажимая на кнопку, я даю согласиена обработку и подтверждаю, что ознакомлен \nс условиями политики обработки персональных данных", text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [
                        ft.Text("Есть аккаунт?"),
                        ft.TextButton("ВХОД")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.update()

    lk = [ft.Row([
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.Image(
                            src="venv/content/logo.png",
                            width=168,
                            height=168
                        ),
                    ]),

                    ft.Row([
                        ft.Card(
                            ft.Container(
                                infID,
                                padding=10
                            ),
                            color="#FFFFFF",
                            width=564,
                            height=45
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER
                    ),

                    ft.Container(
                        ft.Row([
                            ft.Image(
                                src="venv/content/avatar.png",
                                width=168,
                                height=168,
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ),
                    ft.Column([
                        ft.Card(
                            ft.Container(
                                infNAME1,
                                padding=7
                            ),
                            color="#FFFFFF",
                            width=283,
                            height=45
                        )
                    ]),
                    ft.Column([
                        ft.Card(
                            ft.Container(
                                infNAME2,
                                padding=7
                            ),
                            color="#FFFFFF",
                            width=283,
                            height=45
                        )
                    ]),
                    ft.Column([
                        ft.Card(
                            ft.Container(
                                infNAME3,
                                padding=7
                            ),
                            color="#FFFFFF",
                            width=283,
                            height=45
                        )
                    ]),
                    ft.Row([
                        ft.Card(
                            ft.Container(
                                ft.Column([
                                    ft.Text("Компетенции", color="#627254", weight=ft.FontWeight.W_500, size=15),
                                    compRow,
                                ]),
                                padding=7
                            ),


                            color="#FFFFFF",
                            width=564,
                            height=168
                        ),

                    ],alignment=ft.MainAxisAlignment.CENTER),

                    ft.Row([
                        ft.Card(
                            ft.Container(
                                ft.TextButton(text="ПРОЙДЕННЫЕ МЕРОПРИЯТИЯ")
                            ),
                            color="#FFFFFF",
                            width=564,
                            height=45

                        ),

                    ], alignment=ft.MainAxisAlignment.CENTER)




                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#B8D4FF",
                width=658,
                height=1080,
            ),
            contentColumn1
        ], vertical_alignment=ft.CrossAxisAlignment.START)]

    login = [ft.Row(
                [
                    ft.Image(src="venv/content/logo.png", width=168,
                             height=168),
                    ft.Text("ВХОД", size=30, font_family="Comic Sans MS", text_align=ft.TextAlign.CENTER),
                    ft.Container(width=168)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Container(height=100),
            ft.Column(
                [
                    ft.Row(
                        [
                            lEmail,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            lPassword,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [error],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            ft.TextButton("ВОЙТИ", width=200, scale=1.5, on_click=login)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=30

            ),
            ft.Column(
                [
                    ft.Container(width=100, height=100),
                    ft.Row(
                        [
                            ft.Container(width=500,
                                         height=40,
                                         content=ft.Text(
                                             "Нажимая на кнопку я даю согласие на обработку персональных данных и согласен с условиями политики обработки персональных данных.",
                                             text_align=ft.TextAlign.CENTER))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=50

            ),
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Нет аккаунта?",
                                text_align=ft.TextAlign.CENTER, size=20),
                            ft.TextButton("Зарегистрируйся!", scale=1, on_click=registrMenu)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=50
            )]

    content = ft.Column(login)

    page.add(
        content
    )

ft.app(target=main)