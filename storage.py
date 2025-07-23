from sys import prefix

import pandas as pd

class _ModelsDataStorage:
    def __init__(self):
        self.__object_iid = 0
        self.__model_list = {}
        self.__profiles = {}

    def next_iid(self) -> int:
        self.__object_iid += 1
        return self.__object_iid

    def new_model_content(
            self, item_list: list,
            relation_list: list,
            property_list: list,
            item_graph_list: list,
            relation_graph_list) -> None:
        # Просто собираем все полученные списки в словарь и добавляем в список для моделей
        self.__model_list[str(self.__object_iid)] = {
            'elements': item_list,
            'relations': relation_list,
            'properties': property_list,
            'elements_graph': item_graph_list,
            'relations_graph': relation_graph_list
        }

    def get_full_model_list(self) -> dict:
        return self.__model_list

    def get_model_keys(self) -> list:
        return list(self.__model_list.keys())

    def get_model_content_excel(
            self,
            iid: str,
            element_attributes: bool = True,
            relation_attributes: bool = True,
            source_attributes: bool = True,
            target_attributes: bool = True
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        model_content = self.__model_list[iid]
        elements_df = pd.DataFrame.from_dict(model_content['elements'])
        relations_df = pd.DataFrame.from_dict(model_content['relations'])
        property_df = pd.DataFrame.from_dict(model_content['properties'])

        property_df.rename(columns={'Value': 'Property'}, inplace=True)

        if not property_df.empty:
            df = property_df[['ID', 'Key', 'Property']].set_index(['ID', 'Key']).unstack()
            df.columns = [':'.join(col) for col in df.columns]
            df = df.reset_index()

            if element_attributes:
                elements_df = elements_df.merge(df, left_on='ID', right_on='ID').dropna(axis=1)
            if relation_attributes:
                relations_df = relations_df.merge(df, left_on='ID', right_on='ID').dropna(axis=1)

            objects_list = []
            if source_attributes:
                objects_list.append('Source')
            if target_attributes:
                objects_list.append('Target')

            for object_type in objects_list:
                df.columns = [object_type if col.find(':') == -1 else object_type + col[col.find(':'):] for col in
                              df.columns]
                relations_df = relations_df.merge(df, left_on=object_type, right_on=object_type).dropna(axis=1)

        return elements_df, relations_df, property_df

    def get_model_content_drawio(
            self,
            iid: str
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        model_content = self.__model_list[iid]
        # Заберем для начала все объекты на диаграмме
        elements_df = pd.DataFrame.from_dict(model_content['elements_graph'])
        # А теперь добавим информацию об объектах, соединяя по идентификатору
        df = pd.DataFrame.from_dict(model_content['elements']).drop_duplicates()
        elements_df = elements_df.merge(df, left_on='object_ID', right_on='ID', suffixes=('', '_object')).dropna(axis=1)
        elements_df.drop('ID_object', axis=1, inplace=True)
        elements_df.set_index('ID', inplace=True)
        # Заберем для начала все взаимосвязи на диаграмме
        relations_df = pd.DataFrame.from_dict(model_content['relations_graph'])
        # А теперь добавим информацию о связанных объектах
        if not relations_df.empty:
            df = pd.DataFrame.from_dict(model_content['relations']).drop_duplicates()
            relations_df = relations_df.merge(df, left_on='relation_ID', right_on='ID', suffixes=('', '_relation')).dropna(axis=1)
            relations_df.drop('ID_relation', axis=1, inplace=True)
            relations_df.set_index('ID', inplace=True)

        return elements_df, relations_df

    def set_profile(self, profile_id: str, profile_name: str) -> None:
        self.__profiles[profile_id] = profile_name

    def get_profile_name(self, profile_id: str) -> str:
        return self.__profiles[profile_id]

    def clear(self):
        self.__model_list.clear()
        self.__profiles.clear()

    def get_object_iid(self) -> int:
        return self.__object_iid