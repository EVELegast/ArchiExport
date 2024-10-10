import atexit
import configparser
import os
import tkinter
import tkinter.filedialog
import xml
from tkinter import ttk
from tkinter.ttk import Treeview
import xlsxwriter

import pandas as pd
import xml.etree.ElementTree as ET

from tkinter import *

class MyCheckBox:
    def __init__(self, tk: tkinter.Tk, row: int, column: int, id: str, text: str, value: bool):
        self.id = id
        self.text = text
        self.status = BooleanVar()
        self.check_box = Checkbutton(tk, text=self.text, variable=self.status)
        self.check_box.grid(row=row, column=column, sticky=NW, pady=4)
        self.set(value)

    def get(self) -> bool:
        return self.status.get()

    def set(self, value) -> None:
        self.status.set(value)



def get_models_recursion(
        model_xml: xml.etree.ElementTree.Element,
        path: str,
        object_list: dict,
        relation_list: dict,
        parent_iid: str
):
    global full_model_list
    global object_iid
    for item in model_xml:
        object_iid += 1
        if 'name' in item.attrib:
            item_tree = tree_box.insert(parent=parent_iid, index=tkinter.END, iid=object_iid, text=item.attrib['name'])
            new_path = path + '\\' + item.attrib['name']
            if item.tag == 'folder':
                tree_box.item(item_tree, image=folder_image)
                get_models_recursion(
                    model_xml=item,
                    path=new_path,
                    object_list=object_list,
                    relation_list=relation_list,
                    parent_iid=str(object_iid)
                )
            elif item.tag == 'element':
                tree_box.item(item_tree, image=diagram_image)
                # Тут надо разобрать на список элементов, которые содержатся на схеме
                item_list = []
                rel_list = []
                for element in item.findall('child'):
                    if element.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == 'archimate:DiagramObject':
                        item_list.append(object_list[element.attrib['archimateElement']])
                    for relation in element.findall('sourceConnection'):
                        relation_id = relation.attrib['archimateRelationship']
                        rel_list.append(relation_list[relation_id])
                full_model_list[str(object_iid)] = {
                    'elements': item_list,
                    'relations': rel_list
                }


def get_models_list(file_name: str) -> str:
    global object_iid
    global profiles
    if not os.path.exists(file_name):
        raise FileNotFoundError('Не найден файл с диаграммами в Archi!!!')
    with open(file_name, 'r', encoding='UTF-8') as model_file:
        print('Начинаем обработку...')
        model_xml = ET.fromstring(model_file.read())
        if 'name' in model_xml.attrib:
            root_model_name = model_xml.attrib['name']
        else:
            root_model_name = 'ArchiMate Model'
        full_model_list.clear()
        profiles.clear()
        # Собираем данные по всем профилям в один словарь
        object_list = {}
        for item in model_xml.findall('.//profile'):
            profiles[item.attrib['id']] = item.attrib['name']
        # Получаем список всех объектов в модели
        for item in model_xml.findall('.//element'):
            object_type = item.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'][10:]
            object_name = ''
            if 'name' in item.attrib:
                object_name = item.attrib['name']
            object_profile = ''
            if 'profiles' in item.attrib:
                object_profile = profiles[item.attrib['profiles']]
            doc_xml = item.find('.//documentation')
            if doc_xml is None:
                documentation = ''
            else:
                documentation = doc_xml.text
            object_list[item.attrib['id']] = {
                'ID': item.attrib['id'],
                'Type': object_type,
                'Name':object_name,
                'Documentation': documentation,
                'Specialization': object_profile
            }
        # Получаем список всех взаимосвязей в модели
        relation_list = {}
        relations_xml = model_xml.find('.//folder[@name="Relations"]')
        for item in relations_xml.findall('.//element'):
            # "ID","Type","Name","Documentation","Source","Target","Specialization"
            relation_id = item.attrib['id']
            relation_type = item.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'][10:]
            source_id = item.attrib['source']
            relation_source = object_list[source_id]
            target_id = item.attrib['target']
            relation_target = object_list[target_id]
            relation_name = ''
            if 'name' in item.attrib:
                relation_name = item.attrib['name']
            relation_profile = ''
            if 'profiles' in item.attrib:
                relation_profile = profiles[item.attrib['profiles']]
            doc_xml = item.find('.//documentation')
            if doc_xml is None:
                documentation = ''
            else:
                documentation = doc_xml.text
            relation_list[relation_id] = {
                'ID': relation_id,
                'Type': relation_type,
                'Name': relation_name,
                'Documentation': documentation,
                'Source': source_id,
                'Target': target_id,
                'Specialization': relation_profile,
                'SourceName': relation_source['Name'],
                'SourceType': relation_source['Type'],
                'TargetName': relation_target['Name'],
                'TargetType': relation_target['Type']
            }
        # Находим узел, в котором расположено определение моделей
        views_xml = model_xml.find('.//folder[@name="Views"]')
        tree_box.insert(parent='', index=tkinter.END, iid=0, text=root_model_name, image=model_image)
        tree_box.insert(parent='0', index=tkinter.END, iid=1, text='Views')
        object_iid = 1
        get_models_recursion(
            model_xml=views_xml,
            path=f'\\{root_model_name}\\Views',
            object_list=object_list,
            relation_list=relation_list,
            parent_iid='1'
        )
    return root_model_name

def file_dialog():
    file_name = tkinter.filedialog.askopenfilename(filetypes=(('Arhi files', '*.archimate'), ('All files', '*.*')))
    if file_name != '':
        file_label.configure(text = file_name)
        for i in tree_box.get_children():
            tree_box.delete(i)
        get_models_list(file_name)

def save_dialog():
    selected_index = tree_box.selection()[0]
    elements_df = pd.DataFrame.from_dict(full_model_list[selected_index]['elements'])
    relations_df = pd.DataFrame.from_dict(full_model_list[selected_index]['relations'])

    for item in elements_check:
        if not item.get():
            elements_df.drop(item.id, axis=1, inplace=True)

    for item in relations_check:
        if not item.get():
            relations_df.drop(item.id, axis=1, inplace=True)

    file_name = tkinter.filedialog.asksaveasfilename(
        initialfile=tree_box.item(selected_index)['text'],
        confirmoverwrite=True,
        filetypes=(('Excel file', '*.xlsx'), ('All files', '*.*')),
        defaultextension='.xlsx',
    )
    if file_name != '':
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        elements_df.to_excel(writer, index=False, sheet_name='elements')
        relations_df.to_excel(writer, index=False, sheet_name='relations')
        writer.close()

def item_selected(event):
    selected_index = tree_box.selection()[0]
    if selected_index in full_model_list:
        exel_btn['state'] = 'normal'
    else:
        exel_btn['state'] = 'disabled'

def exit_handler():
    for item in elements_check:
        config.set('Elements', item.id, str(item.get()))
    for item in relations_check:
        config.set('Relations', item.id, str(item.get()))
    with open('settings.ini', 'w') as f:
        config.write(f)

atexit.register(exit_handler)

config = configparser.ConfigParser()
config.read('settings.ini')

full_model_list = {}
profiles = {}

element_buttons = [
    ('ID', 'идентификатор'),
    ('Type', 'тип'),
    ('Name', 'имя'),
    ('Documentation','описание'),
    ('Specialization','специализация'),
]
relation_buttons = [
    ('ID', 'идентификатор'),
    ('Type', 'тип'),
    ('Name', 'имя'),
    ('Documentation', 'описание'),
    ('Source', 'идентификатор источника'),
    ('Target', 'идентификатор приёмника'),
    ('Specialization', 'специализация'),
    ('SourceName', 'имя источника'),
    ('SourceType', 'тип источника'),
    ('TargetName', 'имя приёмника'),
    ('TargetType', 'тип приёмника')
]

buttons_len = len(element_buttons) + len(relation_buttons)

elements_check = []
relations_check = []

window_font = ('Arial', 14)

window = Tk()
window.title('Импорт данных о модели из Archi')

model_image = tkinter.PhotoImage(file='model-icon.png')
folder_image = tkinter.PhotoImage(file='folder-icon.png')
diagram_image = tkinter.PhotoImage(file='diagram-icon.png')

icon = PhotoImage(file ="archiexport-icon.png")
window.iconphoto(False, icon)

file_label = Label(window, text='Выберите archimate-файл', anchor='w', font=window_font, width=40)
file_label.grid(column=0, row=0, sticky=W)
file_btn = Button(window, text="...", command=file_dialog, font=window_font)
file_btn.grid(column=1, row=0, sticky=NE)
style = ttk.Style()
# style.theme_use('default')
style.configure('Treeview', rowheight=22, foreground='black')
style.map('Treeview', background=[('selected', 'lightgrey')], foreground=[('selected', 'black')])

tree_box = Treeview(window, show='tree', selectmode='browse')
tree_box.grid(column=0, row=1, sticky=E+W+S+N, columnspan=2, rowspan=buttons_len+1)
tree_box.column('#0')
tree_box.bind('<<TreeviewSelect>>', item_selected)
exel_btn = Button(window, text='Обработать', command=save_dialog, font=window_font)
exel_btn['state'] = 'disabled'
exel_btn.grid(column=0, row=buttons_len+2, columnspan=2)


element_label = Label(window, text='Объекты', font=window_font)
element_label.grid(row=0, column=3)

i = 1

for item in element_buttons:
    elements_check.append(MyCheckBox(
        window,
        row = i,
        column=3,
        id=item[0],
        text=item[1],
        value=eval(config['Elements'][item[0]])
    ))
    i+=1

element_label = Label(window, text='Взаимосвязи', font=window_font)
element_label.grid(row=i, column=3)
i+=1

for item in relation_buttons:
    relations_check.append(MyCheckBox(
        window,
        row = i,
        column=3,
        id=item[0],
        text=item[1],
        value=eval(config['Relations'][item[0]])
    ))
    i+=1

window.mainloop()