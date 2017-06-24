import random
from datetime import date, datetime
from enum import Enum
from os.path import dirname


from openpyxl_templates.style import DefaultStyleSet, _Colors
from openpyxl_templates.table_sheet.columns import TableColumn, ChoiceColumn, DateColumn, CharColumn, TextColumn, \
    BoolColumn, IntColumn, FloatColumn, DatetimeColumn, TimeColumn, FormulaColumn
from openpyxl_templates.table_sheet.table_sheet import TableSheet
from openpyxl_templates.templated_workbook import TemplatedWorkbook

DIR = dirname(__file__)


class Sexes(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Person:
    def __init__(self, first_name, last_name, date_of_birth, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)


persons = (
    Person(
        "Jane",
        "Doe",
        date(year=1983, month=3, day=10),
        Sexes.FEMALE
    ),
    Person(
        "John",
        "Doe",
        date(year=1992, month=9, day=3),
        Sexes.MALE
    ),
    Person(
        "Mickey",
        "Mouse",
        date(year=1972, month=3, day=10),
        Sexes.MALE
    ),
    Person(
        "Goofy",
        "",
        date(year=1972, month=3, day=10),
        Sexes.MALE
    ),
    Person(
        "Minnie",
        "Mouse",
        date(year=1975, month=6, day=17),
        Sexes.FEMALE
    )
)

class SexColumn(ChoiceColumn):
    hidden = False
    choices = (
        ("Male", Sexes.MALE),
        ("Female", Sexes.FEMALE),
        ("Other", Sexes.OTHER)
    )
    add_list_validation = True


class TemplatedPersonsSheet(TableSheet):
    first_name = TableColumn(header="First name", width=15)
    last_name = TableColumn(header="Last name", width=15)
    sex = SexColumn(header="Sex")
    date_of_birth = DateColumn(header="Date of birth")

    hide_excess_columns = False



# class ElementsSheet(TableSheet):
#     title = "Title"
#     description = "This is the description. It can be a couple of sentences long."
#
#     columns = [
#         CharColumn(object_attr="char", header="CharColumn", width=15),
#         # TextColumn(object_attr="text", header="TextColumn",  width=20, hidden=True),
#         BooleanColumn(object_attr="boolean", header="BooleanColumn", width=18),
#         IntegerColumn(object_attr="i", header="IntegerColumn", width=18),
#         FloatColumn(object_attr="f", header="FloatColumn", width=15, group=True),
#         ChoiceColumn(object_attr="choice", header="ChoiceColumn", width=15,
#                      choices=(("Choice 1", 1), ("Choice 2", 2), ("Choice 3", 3))),
#         TimeColumn(object_attr="time", header="TimeColumn", width=18),
#         DateColumn(object_attr="date", header="DateColumn", width=20, group=True, hidden=False),
#         DateTimeColumn(object_attr="datetime", header="DateTimeColumn", width=20, hidden=False)
#     ]

class DemoObject:
    def __init__(self, char, text, boolean, i, f, choice, time, date, datetime):
        self.char = char
        self.text = text
        self.boolean = boolean
        self.integer = i
        self.float = f
        self.choice = choice
        self.time = time
        self.date = date
        self.datetime = datetime


def demo_objects(count=100):
    from_date = datetime(year=1990, month=1, day=1).timestamp()
    to_date = datetime(year=2020, month=12, day=31).timestamp()

    dates = list(datetime.fromtimestamp(random.uniform(from_date, to_date)) for i in range(0, count))
    dates.sort()

    for i in range(0, count):
        float = random.random() * 1000
        date = dates[i]

        yield DemoObject(
            "Object %d" % (i + 1),
            "This is a text which\n will wrap by default",
            random.choice((True, False)),
            float,
            float,
            random.randint(1, 3),
            date,
            date,
            date
        )


class ColumnDemoSheet(TableSheet):
    table_name = "ColumnDemo"

    char = CharColumn(header="CharColumn")
    text = TextColumn(header="TextColumn")
    boolean = BoolColumn(header="BoolColumn")
    integer = IntColumn(header="IntColumn")
    float = FloatColumn(header="FloatColumn")
    datetime = DatetimeColumn(header="DatetimeColumn")
    date = DateColumn(header="DateColumn")
    time = TimeColumn(header="TimeColumn")
    formula = FormulaColumn(header="FormulaColumn", formula="=SUM(ColumnDemo[IntColumn])")


class DemoWorkbook(TemplatedWorkbook):
    timestamp = True
    persons = TemplatedPersonsSheet(sheetname="Persons", active=True)
    column_demo = ColumnDemoSheet(sheetname="Column demo")


if __name__ == "__main__":
    workbook = DemoWorkbook(template_styles=DefaultStyleSet(accent_color=_Colors.DARK_RED))
    workbook.column_demo.write(objects=list(demo_objects(100)), title="Column demo")
    workbook.persons.write(objects=persons, title="Persons")

    workbook.save("demo.xlsx")