import atexit
import configparser
import os
import xml

import tkinter.filedialog
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import Label, Button, BooleanVar, Checkbutton, Tk, N, W, E, S, NW, NE

import xlsxwriter

import pandas as pd
import xml.etree.ElementTree as ETree


import constants
from storage import _ModelsDataStorage


class MyCheckBox:
    def __init__(self, tk: tkinter.Tk, row: int, column: int, check_id: str, text: str, value: bool):
        self.id = check_id
        self.text = text
        self.status = BooleanVar()
        self.check_box = Checkbutton(tk, text=self.text, variable=self.status)
        self.check_box.grid(row=row, column=column, sticky=NW, pady=4)
        self.set(value)

    def get(self) -> bool:
        return self.status.get()

    def set(self, value) -> None:
        self.status.set(value)


def object_parsing(object_xml: xml.etree.ElementTree.Element) -> tuple[str, str, str]:
    object_name = ''
    if 'name' in object_xml.attrib:
        object_name = object_xml.attrib['name']
    object_profile = ''
    if 'profiles' in object_xml.attrib:
        object_profile = settings.get_profile_name(object_xml.attrib['profiles'])
    doc_xml = object_xml.find('.//documentation')
    if doc_xml is None:
        documentation = ''
    else:
        documentation = doc_xml.text
    return object_name, object_profile, documentation


def get_models_recursion(
        model_xml: xml.etree.ElementTree.Element,
        path: str,
        object_list: dict,
        relation_list: dict,
        properties_list: dict,
        parent_iid: str
):
    for item_xml in model_xml:
        object_iid = settings.next_iid()
        if 'name' in item_xml.attrib:
            item_tree = tree_box.insert(parent=parent_iid, index=tkinter.END, iid=object_iid, text=item_xml.attrib['name'])
            new_path = path + '\\' + item_xml.attrib['name']
            if item_xml.tag == 'folder':
                tree_box.item(item_tree, image=FOLDER_IMAGE)
                get_models_recursion(
                    model_xml=item_xml,
                    path=new_path,
                    object_list=object_list,
                    relation_list=relation_list,
                    properties_list=properties_list,
                    parent_iid=str(object_iid)
                )
            elif item_xml.tag == 'element':
                tree_box.item(item_tree, image=DIAGRAM_IMAGE)
                # Тут надо разобрать на список элементов, которые содержатся на схеме
                item_list = []
                rel_list = []
                prop_list = []
                for element in item_xml.findall('child'):
                    if element.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == 'archimate:DiagramObject':
                        object_id = element.attrib['archimateElement']
                        item_list.append(object_list[object_id])
                        for attr in properties_list[object_id]:
                            attr_record = {
                                'ID': object_id,
                                'Key': attr,
                                'Value': properties_list[object_id][attr],
                                'Name': object_list[object_id]['Name'],
                                'Type': object_list[object_id]['Type']
                            }
                            prop_list.append(attr_record)
                    for relation in element.findall('sourceConnection'):
                        if 'archimateRelationship' in relation.attrib:
                            relation_id = relation.attrib['archimateRelationship']
                            rel_list.append(relation_list[relation_id])
                            for attr in properties_list[relation_id]:
                                attr_record = {
                                    'ID': relation_id,
                                    'Key': attr,
                                    'Value': properties_list[relation_id][attr],
                                    'Name': object_list[relation_id]['Name'],
                                    'Type': object_list[relation_id]['Type']
                                }
                                prop_list.append(attr_record)
                settings.new_model_content(
                    item_list=item_list,
                    relation_list=rel_list,
                    property_list=prop_list
                )


def get_models_list(file_name: str) -> str:
    if not os.path.exists(file_name):
        raise FileNotFoundError('Не найден файл с диаграммами в Archi!!!')
    with open(file_name, 'r', encoding='UTF-8') as model_file:
        model_xml = ETree.fromstring(model_file.read())
        if 'name' in model_xml.attrib:
            root_model_name = model_xml.attrib['name']
        else:
            root_model_name = 'ArchiMate Model'
        settings.clear()

        # Собираем данные по всем профилям в один словарь
        for profile_xml in model_xml.findall('.//profile'):
            settings.set_profile(
                profile_id=profile_xml.attrib['id'],
                profile_name=profile_xml.attrib['name']
            )

        # Получаем список всех объектов в модели и сразу формируем список значений атрибутов
        object_list = {}
        properties_list = {}
        for element_xml in model_xml.findall('.//element'):
            object_type = element_xml.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'][10:]
            object_name, object_profile, object_documentation = object_parsing(element_xml)
            object_list[element_xml.attrib['id']] = {
                'ID': element_xml.attrib['id'],
                'Type': object_type,
                'Name': object_name,
                'Documentation': object_documentation,
                'Specialization': object_profile
            }
            # Проверяем в части атрибутов
            properties_list[element_xml.attrib['id']] = {}
            for attr in element_xml.findall('.//property'):
                properties_list[element_xml.attrib['id']][attr.attrib['key']] = attr.attrib['value']

        # Получаем список всех взаимосвязей в модели
        relation_list = {}
        relations_xml = model_xml.find('.//folder[@type="relations"]')
        for relation_xml in relations_xml.findall('.//element'):
            # "ID","Type","Name","Documentation","Source","Target","Specialization"
            relation_id = relation_xml.attrib['id']
            relation_type = relation_xml.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'][10:]
            source_id = relation_xml.attrib['source']
            relation_source = object_list[source_id]
            target_id = relation_xml.attrib['target']
            relation_target = object_list[target_id]
            relation_name, relation_profile, relation_documentation = object_parsing(relation_xml)
            relation_list[relation_id] = {
                'ID': relation_id,
                'Type': relation_type,
                'Name': relation_name,
                'Documentation': relation_documentation,
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
        tree_box.insert(parent='', index=tkinter.END, iid=0, text=root_model_name, image=MODEL_IMAGE)
        tree_box.insert(parent='0', index=tkinter.END, iid=1, text='Views')
        get_models_recursion(
            model_xml=views_xml,
            path=f'\\{root_model_name}\\Views',
            object_list=object_list,
            relation_list=relation_list,
            properties_list=properties_list,
            parent_iid=str(settings.next_iid())
        )
    return root_model_name


def file_dialog():
    file_name = tkinter.filedialog.askopenfilename(filetypes=(('Arhi files', '*.archimate'), ('All files', '*.*')))
    if file_name != '':
        file_label.configure(text = file_name)
        for child in tree_box.get_children():
            tree_box.delete(child)
        get_models_list(file_name)


def save_dialog():
    selected_index = tree_box.selection()[0]
    element_attributes = next((x for x in elements_check if x.id == 'Attributes'), None)
    relation_attributes = next((x for x in relations_check if x.id == 'Attributes'), None)
    source_attributes = next((x for x in relations_check if x.id == 'SourceAttributes'), None)
    target_attributes = next((x for x in relations_check if x.id == 'TargetAttributes'), None)
    elements_df, relations_df, properties_df = settings.get_model_content(
        selected_index,
        element_attributes=element_attributes.get(),
        relation_attributes=relation_attributes.get(),
        source_attributes= source_attributes.get(),
        target_attributes= target_attributes.get()
    )


    for check_item in elements_check:
        if not check_item.get() and not check_item.id.find('attribute') == -1:
            print(check_item.id)
            elements_df.drop(check_item.id, axis=1, inplace=True)

    for check_item in relations_check:
        if not check_item.get() and not check_item.id.find('attribute') == -1:
            relations_df.drop(check_item.id, axis=1, inplace=True)

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
        properties_df.to_excel(writer, index=False, sheet_name='properties')
        writer.close()
        if autorun_check.get():
            os.system(f'start excel.exe "{file_name}"')


def item_selected(event):
    selected_index = tree_box.selection()[0]
    if selected_index in settings.get_model_keys():
        exel_btn['state'] = 'normal'
    else:
        exel_btn['state'] = 'disabled'


def exit_handler():
    for check_item in elements_check:
        config.set('Elements', check_item.id, str(check_item.get()))
    for check_item in relations_check:
        config.set('Relations', check_item.id, str(check_item.get()))
    config.set('Excel', autorun_check.id, str(autorun_check.get()))
    with open('settings.ini', 'w') as f:
        config.write(f)


if __name__ == '__main__':
    # Выполняем инициализацию программы:
    # - регистрация события закрытия программы
    atexit.register(exit_handler)
    # - загрузка настроек
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # - инициализация переменных
    settings = _ModelsDataStorage()
    elements_check = []
    relations_check = []


    # Формируем окно и интерфейс программы
    # - создаем окно, регистрируем необходимые картинки и устанавливаем наименование и логотип
    window = Tk()
    MODEL_IMAGE = tkinter.PhotoImage(file='model-icon.png')
    FOLDER_IMAGE = tkinter.PhotoImage(file='folder-icon.png')
    DIAGRAM_IMAGE = tkinter.PhotoImage(file='diagram-icon.png')
    APP_ICON = tkinter.PhotoImage(file="archiexport-icon.png")
    window.title('Импорт данных о модели из Archi')
    window.iconphoto(False, APP_ICON)
    # - наименование рабочего файла и кнопка выбора рабочего файла
    file_label = Label(window, text='Выберите archimate-файл', anchor='w', font=constants.WINDOW_FONT, width=40)
    file_label.grid(column=0, row=0, sticky=W)
    file_btn = Button(window, text="...", command=file_dialog, font=constants.WINDOW_FONT)
    file_btn.grid(column=1, row=0, sticky=NE)
    # - настраиваем стили, вычисляем размер и создаём элемент для просмотра дерева
    # (высота зависит от размеров списков настроек)
    buttons_len = len(constants.ELEMENT_BUTTONS) + len(constants.RELATION_BUTTONS)
    style = ttk.Style()
    style.configure('Treeview', rowheight=22, foreground='black')
    style.map('Treeview', background=[('selected', 'lightgrey')], foreground=[('selected', 'black')])
    tree_box = Treeview(window, show='tree', selectmode='browse')
    tree_box.grid(column=0, row=1, sticky=E+W+S+N, columnspan=2, rowspan=buttons_len+1)
    tree_box.column('#0')
    tree_box.bind('<<TreeviewSelect>>', item_selected)
    # - кнопка запуска обработки
    exel_btn = Button(window, text='Обработать', command=save_dialog, font=constants.WINDOW_FONT)
    exel_btn['state'] = 'disabled'
    exel_btn.grid(column=0, row=buttons_len+2)
    # Чек-бокс автозапуска
    autorun_check = MyCheckBox(
        window,
        row=buttons_len+2,
        column=1,
        check_id='autorun',
        text='открыть файл после обработки',
        value=eval(config['Excel']['autorun'])
    )
    # - блок настроек
    # (формируется на основе двух констант - для объектов и для взаимосвязей)
    element_label = Label(window, text='Объекты', font=constants.WINDOW_FONT)
    element_label.grid(row=0, column=3)
    i = 1
    for item in constants.ELEMENT_BUTTONS:
        elements_check.append(MyCheckBox(
            window,
            row = i,
            column=3,
            check_id=item[0],
            text=item[1],
            value=eval(config['Elements'][item[0]])
        ))
        i+=1

    element_label = Label(window, text='Взаимосвязи', font=constants.WINDOW_FONT)
    element_label.grid(row=i, column=3)
    i+=1
    for item in constants.RELATION_BUTTONS:
        relations_check.append(MyCheckBox(
            window,
            row = i,
            column=3,
            check_id=item[0],
            text=item[1],
            value=eval(config['Relations'][item[0]])
        ))
        i+=1
    # Запускаем созданное окно
    window.mainloop()