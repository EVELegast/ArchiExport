"""
TODO: Нужно сделать запись в новый XML формат
TODO: Нужно подать на вход объекты из Archi
TODO: Нужно сделать подписи к стрелкам
"""
import pandas as pd

strategyColor = "#F5DEAA"
motivationColor = "#CCCCFF"
businessColor = "#FFFF99"
applicationColor = "#99FFFF"
technologyColor = "#AFFFAF"
physicalColor = "#AFFFAF"
implementationColor = "#FFE0E0"
groupingColor = ""
locationColor = "#FFB973"
junctionAndColor = "#000000"
junctionOrColor = "#FFFFFF"

"""

"""
archiElemMap = {
    # Motivation Layer
    "Stakeholder":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=role;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.role;"],
    "Driver":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=driver;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.driver;"],
    "Assessment":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=assess;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.assess;"],
    "Goal":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=goal;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.goal;"],
    "Outcome":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=outcome;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.outcome;strokeWidth=2;"],
    "Principle":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=principle;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.principle;strokeWidth=2;"],
    "Requirement":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=requirement;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.requirement;"],
    "Constraint":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=constraint;archiType=oct;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.constraint;"],
    "Meaning":
        ["html=1;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=meaning;archiType=oct;",
         "shape=mxgraph.basic.cloud_callout;html=1;whiteSpace=wrap;fillColor=" + motivationColor + ";"],
    "Value":
        ["html=1;whiteSpace=wrap;fillColor=" + motivationColor + ";shape=mxgraph.archimate3.application;appType=amValue;archiType=oct;",
         "shape=ellipse;html=1;whiteSpace=wrap;fillColor=" + motivationColor + ";"],
    # Strategy Layer
    "Resource":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.application;appType=resource;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.resource;"],
    "Capability":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.application;appType=capability;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.capability;"],
    "CourseOfAction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.application;appType=course;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.valueStream;"],
    "ValueStream":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.application;appType=valueStream;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + strategyColor + ";shape=mxgraph.archimate3.course;"],
    # Business Layer
    "BusinessActor":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=actor;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";verticalLabelPosition=bottom;verticalAlign=top;align=center;shape=mxgraph.archimate3.actor;"],
    "BusinessRole":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=role;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.role;"],
    "BusinessCollaboration":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=collab;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.collaboration;"],
    "BusinessInterface":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=interface;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.interface;"],
    "BusinessProcess":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=proc;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.process;"],
    "BusinessFunction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=func;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.function;"],
    "BusinessInteraction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=interaction;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.interaction;"],
    "BusinessEvent":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=event;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.event;"],
    "BusinessService":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=serv;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.service;"],
    "BusinessObject":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=passive;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.businessObject;overflow=fill;"],
    "Contract":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=contract;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.contract;"],
    "Representation":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=representation;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.representation;"],
    "Product":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.application;appType=product;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + businessColor + ";shape=mxgraph.archimate3.product;"],
    # Application Layer
    "ApplicationComponent":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=comp;archiType=square",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.component;"],
    "ApplicationCollaboration":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=collab;archiType=square",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.collaboration;"],
    "ApplicationInterface":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=interface;archiType=square",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.interface;"],
    "ApplicationFunction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=func;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.function;"],
    "ApplicationInteraction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=interaction;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.interaction;"],
    "ApplicationProcess":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=proc;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.process;"],
    "ApplicationEvent":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=event;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.event;"],
    "ApplicationService":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=serv;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.service;"],
    "DataObject":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.application;appType=passive;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + applicationColor + ";shape=mxgraph.archimate3.businessObject;overflow=fill;"],
    # Technology Layer
    "Node":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=node;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.node;"],
    "Device":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=device;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.device;"],
    "SystemSoftware":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=sysSw;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.sysSw;"],
    "TechnologyCollaboration":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=collab;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.collaboration;"],
    "TechnologyInterface":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=interface;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.interface;"],
    "Path":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=path;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.path;strokeWidth=6;"],
    "CommunicationNetwork":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=netw;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.network;"],
    "TechnologyFunction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=func;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.function;"],
    "TechnologyProcess":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=proc;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.process;"],
    "TechnologyInteraction":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=interaction;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.interaction;"],
    "TechnologyEvent":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=event;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.event;"],
    "TechnologyService":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=serv;archiType=rounded",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.service;"],
    "Artifact":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=mxgraph.archimate3.application;appType=artifact;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + technologyColor + ";shape=note;size=14;"],
    # Physical Layer
    "Equipment":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.application;appType=equipment;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.equipment;"],
    "Facility":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.application;appType=facility;archiType=square",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.facility;"],
    "DistributionNetwork":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.application;appType=distribution;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.distribution;strokeWidth=4;"],
    "Material":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.application;appType=material;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + physicalColor + ";shape=mxgraph.archimate3.material;"],

    # Implementation Layer
    "WorkPackage":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.application;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.workPackage;strokeWidth=5;"],
    "Deliverable":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.application;appType=deliverable;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.deliverable;"],
    "ImplementationEvent":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.application;appType=event;archiType=rounded;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.event;"],
    "Plateau":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.application;appType=plateau;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.plateau;"],
    "Gap":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.application;appType=gap;",
         "html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + implementationColor + ";shape=mxgraph.archimate3.gapIcon;"],
    # Composite Elements
    "Location":
        ["html=1;outlineConnect=0;whiteSpace=wrap;fillColor=" + locationColor + ";shape=mxgraph.archimate3.application;appType=location;archiType=square;",
         "html=1;outlineConnect=0;whiteSpace=wrap;shape=mxgraph.archimate3.locationIcon;fillColor=#efd1e4;aspect=fixed;"],
    "Grouping":
        ["shape=folder;spacingTop=10;tabWidth=100;tabHeight=25;tabPosition=left;html=1;dashed=1;",
         ""],
    # Junction
    "JunctionAnd":
        ["ellipse;html=1;verticalLabelPosition=bottom;labelBackgroundColor=none;verticalAlign=top;fillColor=strokeColor",
         ""],
    "JunctionOr":
        ["ellipse;html=1;verticalLabelPosition=bottom;labelBackgroundColor=none;verticalAlign=top;fillColor=" + junctionOrColor,
         ""]
}



archiRelMap = {
    "AccessRelationship": "html=1;endArrow=none;elbow=vertical;dashed=1;startFill=0;dashPattern=1 4;rounded=0;",
	"access-relationship_read": "html=1;startArrow=open;endArrow=none;elbow=vertical;startFill=0;dashed=1;dashPattern=1 4;rounded=0;",
	"access-relationship_write": "html=1;endArrow=open;elbow=vertical;endFill=0;dashed=1;dashPattern=1 4;rounded=0;",
	"access-relationship_readwrite": "html=1;endArrow=open;elbow=vertical;endFill=0;dashed=1;startArrow=open;startFill=0;dashPattern=1 4;rounded=0;",
    "AggregationRelationship": "html=1;startArrow=diamondThin;startFill=0;elbow=vertical;startSize=10;endArrow=none;rounded=0;",
    "AssignmentRelationship": "endArrow=block;html=1;endFill=1;startArrow=oval;startFill=1;elbow=vertical;rounded=0;",
    "AssociationRelationship": "html=1;endArrow=none;elbow=vertical;rounded=0;",
	"CompositionRelationship": "html=1;startArrow=diamondThin;startFill=1;elbow=vertical;startSize=10;endArrow=none;rounded=0;",
	"FlowRelationship": "html=1;endArrow=block;dashed=1;elbow=vertical;endFill=1;dashPattern=6 4;rounded=0;",
	"InfluenceRelationship": "",
	"RealizationRelationship": "html=1;endArrow=block;elbow=vertical;endFill=0;dashed=1;rounded=0;",
	"ServingRelationship": "html=1;endArrow=open;elbow=vertical;endFill=1;rounded=0;entryPerimeter=0;",
	"SpecializationRelationship": "endArrow=block;html=1;endFill=0;elbow=vertical;rounded=0;",
	"TriggeringRelationship": "html=1;endArrow=block;dashed=0;elbow=vertical;endFill=1;rounded=0;"

    # edgeStyle=elbowEdgeStyle; - изогнутая линия?
}

styleAlign = {
		1: 'left',
		2: 'center',
		4: 'right'
}

stylePosition = {
    0: 'top',
    1: 'middle',
    2: 'bottom'
}

styleFontStyle = {
    "normal", 0,
    "bold", 1,
    "italic", 2,
    "bolditalic", 3
}

header = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="" modified="${timeISOString}" agent="Archi" etag="${model.name}" type="device">
	<diagram id="${theView.id}" name="${escX(theView.name)}">
		<mxGraphModel dx="2302" dy="697" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
			<root>
				<mxCell id="0" />
				<mxCell id="1" parent="0" />
"""


footer= """
			</root>
		</mxGraphModel>
	</diagram>
</mxfile>\n
"""

# TODO: На основе стиля заполнить цвет и другие возможные параметры, либо подставить стандартные значения
def get_style(element: pd.Series) -> str:
    if element['Icon']:
        return archiElemMap[element['Type']][1]
    else:
        return archiElemMap[element['Type']][0]

def map_elements(elements_df: pd.DataFrame, relations_df: pd.DataFrame):
    elements_xml = ''
    # Перебираем полученные объекты
    for key, element in elements_df.iterrows():
        # Делаем замены для символов, которые могут быть использованы как теги
        pass
        # Генерируем строку с параметрами объекта
        pass
        # Уточняем тип объекта (нужно для связи типа Access и объекта типа Junction)
        pass
        # TODO: Нужно сформировать стили, если они заданы
        style = get_style(element)
        parent = '1'
        element_width = element['Width']
        element_height = element['Height']
        element_xml = "<mxCell id=\"{0}\" value=\"{1}\" style=\"{2}\" vertex=\"1\" parent=\"{3}\">\n".format(key, element['Name'], style, parent)
        element_xml += "<mxGeometry x=\"{0}\" y=\"{1}\" width=\"{2}\" height=\"{3}\" as=\"geometry\" />\n".format(element['X'], element['Y'], element_width, element_height)
        element_xml += "</mxCell>\n"
        elements_xml += element_xml

        # Тут ещё дополнительно даётся рекурсия для вложенных объектов
        # TODO Проверить необходимость обработки вложенных объектов
        pass
    # Перебираем полученные взаимосвязи
    for key, relation in relations_df.iterrows():
        style = archiRelMap[relation['Type']]
        if len(relation['bendpoints']) > 0:
            style = "edgeStyle=orthogonalEdgeStyle;"+style
        source = relation['source_id']
        target = relation['target_id']
        relation_xml = "<mxCell style=\"{0}\" edge=\"1\" parent=\"1\" source=\"{1}\" target=\"{2}\">".format(style, source, target)
        relation_xml += "<mxGeometry width=\"160\" relative=\"1\" as=\"geometry\">\n"
        # relation_xml += "< mxPoint x = \"{0}\" y = \"{1}\" as =\"sourcePoint\" / >\n".format(relation['startX'], relation['startY'])"
        # relation_xml += "< mxPoint x = \"{0}\" y = \"{1}\" as =\"targetPoint\" / >\n".format(relation['endX'], relation['endY'])"
        # Перебираем промежуточные точки
        if len(relation['bendpoints']) > 0:
            relation_xml += "<Array as=\"points\">\n"
            for bendpoint in relation['bendpoints']:
                relation_xml += "<mxPoint x=\"{}\" y=\"{}\" />\n".format(bendpoint['X'], bendpoint['Y'])
            relation_xml += "</Array>\n"
        relation_xml += "</mxGeometry>\n</mxCell>\n"
        elements_xml += relation_xml

    return elements_xml

def save_draw_io(file_name: str, elements_df: pd.DataFrame, relations_df: pd.DataFrame):
    with open(file_name, 'w', encoding='utf-8') as f:
        # Записываем начальную часть
        f.write(header)
        # Записываем содержание
        f.write(map_elements(elements_df, relations_df))
        # Записываем финальную часть
        f.write(footer)
