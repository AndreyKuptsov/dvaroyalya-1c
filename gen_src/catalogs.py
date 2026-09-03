# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import load, get, save
from enums import syn

load()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CFG = ROOT

def ensure(d):
    os.makedirs(d, exist_ok=True)

def write(rel, content):
    p = os.path.join(CFG, rel)
    ensure(os.path.dirname(p))
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def uid_(key):
    return get(key)

HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">\n'

def type_string():
    return '<v8:Type>xs:string</v8:Type>'
def type_number(q=15,d=2):
    return '<v8:Type>xs:decimal</v8:Type><v8:Qualifiers><v8:Type>xs:decimal</v8:Type><v8:NumberQualifiers><v8:Precision>%d</v8:Precision><v8:Scale>%d</v8:Scale></v8:NumberQualifiers></v8:Qualifiers>' % (q,d)
def type_bool():
    return '<v8:Type>xs:boolean</v8:Type><v8:TypeQualifiers><v8:Type>xs:boolean</v8:Type></v8:TypeQualifiers>'
def type_date():
    return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>DateTime</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def type_dateonly():
    return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>Date</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def type_ref(cat):
    return '<v8:Type>cfg:CatalogRef.' + cat + '</v8:Type><v8:TypeQualifiers><v8:Type>cfg:CatalogRef.' + cat + '</v8:Type></v8:TypeQualifiers>'
def type_enum(en):
    return '<v8:Type>cfg:EnumRef.' + en + '</v8:Type><v8:TypeQualifiers><v8:Type>cfg:EnumRef.' + en + '</v8:Type></v8:TypeQualifiers>'
def type_string_wrap(v8type):
    return '<v8:Type>' + v8type + '</v8:Type>'

def attr(name, syn_name, typ, comment=None):
    s = '    <Attribute>\n'
    s += '      <Name>%s</Name>\n' % name
    s += '      <Synonym>%s</Synonym>\n' % syn_name
    s += '      <Comment>%s</Comment>\n' % (comment or "")
    s += '      <UUID>%s</UUID>\n' % uid_("cat.attr." + name)
    s += '      <ValueType>' + typ + '</ValueType>\n'
    s += '      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n'
    s += '      <FullTextSearch>Use</FullTextSearch>\n'
    s += '    </Attribute>\n'
    return s

def type_docref(doc):
    return '<v8:Type>cfg:DocumentRef.' + doc + '</v8:Type><v8:TypeQualifiers><v8:Type>cfg:DocumentRef.' + doc + '</v8:Type></v8:TypeQualifiers>'

# Catalogs definition: name, syn, hierarchy, attrs [(name, syn, typ), ...]
CATS = {
 "Клиенты": {
   "syn":"Клиенты","hier":False,
   "attrs":[
     ("ДатаРождения","Дата рождения",type_dateonly()),
     ("Телефон","Телефон",type_string()),
     ("Email","Email",type_string()),
     ("Telegram","Telegram",type_string()),
     ("TelegramID","Telegram ID",type_string()),
     ("Комментарий","Комментарий",type_string()),
     ("ДатаРегистрации","Дата регистрации",type_dateonly()),
     ("СтатусКлиента","Статус клиента",type_enum("СтатусыКлиентов")),
     ("ИсточникПривлечения","Источник привлечения",type_enum("ИсточникиПривлечения")),
     ("ОтветственныйМенеджер","Ответственный менеджер",type_ref("Пользователи")),
     ("СогласиеНаУведомления","Согласие на получение уведомлений",type_bool()),
     ("СогласиеНаОбработкуДанных","Согласие на обработку персональных данных",type_bool()),
   ]},
 "Преподаватели": {
   "syn":"Преподаватели","hier":False,
   "attrs":[
     ("Телефон","Телефон",type_string()),
     ("Email","Email",type_string()),
     ("Специализация","Специализация",type_ref("Направления")),
     ("ДатаНачалаРаботы","Дата начала работы",type_dateonly()),
     ("Статус","Статус",type_enum("СтатусыПреподавателей")),
     ("Ставка","Ставка",type_number(15,2)),
     ("Филиал","Филиал",type_enum("Филиалы")),
     ("Комментарий","Комментарий",type_string()),
     ("Сотрудник","Сотрудник",type_ref("Пользователи")),
   ]},
  "Направления": {
    "syn":"Направления","hier":False,
    "attrs":[
      ("ДлительностьЗанятия","Длительность занятия",type_number(3,0)),
      ("БазоваяСтоимость","Базовая стоимость",type_number(15,2)),
      ("ТипЗанятия","Индивидуальное/групповое",type_enum("ТипыЗанятий")),
      ("Филиал","Филиал",type_enum("Филиалы")),
      ("Описание","Описание",type_string()),
      ("Активность","Активность",type_bool()),
    ]},
  "Аудитории": {
    "syn":"Аудитории","hier":False,
    "attrs":[
      ("Номер","Номер",type_string()),
      ("Вместимость","Вместимость",type_number(3,0)),
      ("Тип","Тип",type_enum("ТипыАудиторий")),
      ("Филиал","Филиал",type_enum("Филиалы")),
      ("НаличиеОборудования","Наличие оборудования",type_bool()),
      ("Статус","Статус",type_bool()),
    ]},
 "Абонементы": {
   "syn":"Абонементы","hier":False,
   "attrs":[
     ("КоличествоЗанятий","Количество занятий",type_number(15,0)),
     ("СрокДействия","Срок действия (дней)",type_number(10,0)),
     ("Стоимость","Стоимость",type_number(15,2)),
     ("Направление","Направление",type_ref("Направления")),
     ("ДлительностьЗанятия","Длительность занятия (мин)",type_number(3,0)),
     ("ВозможностьЗаморозки","Возможность заморозки",type_bool()),
     ("МаксимальныйСрокЗаморозки","Максимальный срок заморозки (дней)",type_number(10,0)),
      ("КоличествоПереносов","Количество переносов",type_number(3,0)),
      ("Филиал","Филиал",type_enum("Филиалы")),
      ("Активность","Активность",type_bool()),
    ]},
  "Инструменты": {
    "syn":"Инструменты","hier":False,
    "attrs":[
      ("ТипИнструмента","Тип инструмента",type_enum("ТипыИнструментов")),
      ("Филиал","Филиал",type_enum("Филиалы")),
      ("ИнвентарныйНомер","Инвентарный номер",type_string()),
      ("НаличиеАкустическое","Акустический",type_bool()),
      ("Статус","Статус",type_enum("СтатусыИнструмента")),
      ("СтоимостьАрендыВЧас","Стоимость аренды (час)",type_number(15,2)),
      ("Комментарий","Комментарий",type_string()),
    ]},
  "СпособыОплаты": {
   "syn":"Способы оплаты","hier":False,
   "attrs":[],
 },
 "Пользователи": {
   "syn":"Пользователи/Сотрудники","hier":False,
   "attrs":[
     ("ФИО","ФИО",type_string()),
     ("Телефон","Телефон",type_string()),
     ("Email","Email",type_string()),
     ("Роль","Роль",type_string()),
   ]},
 "АбонементыКлиента": {
   "syn":"Абонементы клиента","hier":False,
   "attrs":[
     ("Клиент","Клиент",type_ref("Клиенты")),
     ("ВидАбонемента","Вид абонемента",type_ref("Абонементы")),
     ("ДатаПокупки","Дата покупки",type_date()),
     ("ДатаНачалаДействия","Дата начала действия",type_dateonly()),
     ("ДатаОкончания","Дата окончания",type_dateonly()),
     ("КоличествоЗанятий","Количество занятий",type_number(15,0)),
     ("Использовано","Использовано",type_number(15,0)),
     ("Заморожено","Заморожено (дней)",type_number(10,0)),
     ("Статус","Статус",type_enum("СтатусыАбонементаКлиента")),
     ("ПроданоПоДокументу","Продажа абонемента",type_docref("ПродажаАбонемента")),
   ]},
}

def type_docref(doc):
    return '<v8:Type>cfg:DocumentRef.' + doc + '</v8:Type><v8:TypeQualifiers><v8:Type>cfg:DocumentRef.' + doc + '</v8:Type></v8:TypeQualifiers>'

def catalog_xml(name, md):
    cid = uid_("catalog." + name)
    buf = []
    buf.append(HEADER)
    buf.append('  <InternalInfo>')
    buf.append('    <xen:generator><xen:packageName>ДваРояля</xen:packageName></xen:generator>')
    buf.append('  </InternalInfo>')
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>' % name)
    buf.append('    <Synonym>%s</Synonym>' % md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <SynonymCode>Код</SynonymCode>')
    buf.append('    <CommentCode/>')
    buf.append('    <DefaultCodeLength>9</DefaultCodeLength>')
    buf.append('    <CodeType>Number</CodeType>')
    buf.append('    <CodeAllowedLength>Variable</CodeAllowedLength>')
    buf.append('    <CodeSeries>WholeCatalog</CodeSeries>')
    buf.append('    <CheckUnique>DontCheck</CheckUnique>')
    buf.append('    <Autonumbering>Auto</Autonumbering>')
    buf.append('    <DefaultPresentation>AsSynonyms</DefaultPresentation>')
    buf.append('    <Explanation/>')
    buf.append('    <CreateOnInput>Use</CreateOnInput>')
    buf.append('    <Hierarchical>false</Hierarchical>')
    buf.append('    <Predefined>false</Predefined>')
    buf.append('    <Owner>None</Owner>')
    buf.append('    <IncludeHelpInContents>true</IncludeHelpInContents>')
    buf.append('    <FoldersOnTop>true</FoldersOnTop>')
    buf.append('    <UseStandardCommands>true</UseStandardCommands>')
    buf.append('    <ChoiceMode>BothWays</ChoiceMode>')
    buf.append('    <DescriptionLength>0</DescriptionLength>')
    buf.append('    <CodeLength>9</CodeLength>')
    buf.append('    <DefaultObjectForm>Catalog.%s.ObjectForm</DefaultObjectForm>' % name)
    buf.append('    <DefaultListForm>Catalog.%s.ListForm</DefaultListForm>' % name)
    buf.append('    <DefaultChoiceForm>Catalog.%s.ChoiceForm</DefaultChoiceForm>' % name)
    buf.append('    <DefaultListPresentation>%s</DefaultListPresentation>' % md["syn"])
    buf.append('    <DefaultFolderPresentation>Папка</DefaultFolderPresentation>')
    buf.append('    <UseStandardCommandsInList>true</UseStandardCommandsInList>')
    buf.append('    <NamePrefixes/>')
    buf.append('    <DataLockControlMode>Managed</DataLockControlMode>')
    buf.append('    <FullTextSearch>Use</FullTextSearch>')
    buf.append('    <ObjectPresentation>%s</ObjectPresentation>' % md["syn"])
    buf.append('    <ExtendedObjectPresentation/>')
    buf.append('    <ListPresentation>%s</ListPresentation>' % md["syn"])
    buf.append('    <ExtendedListPresentation/>')
    buf.append('    <ExplanationList/>')
    buf.append('    <CreateOnInputChoice>Auto</CreateOnInputChoice>')
    buf.append('    <DataHistory>DontUse</DataHistory>')
    buf.append('    <EditType>InDialog</EditType>')
    buf.append('    <ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>')
    buf.append('    <VersioningData>DoNotUse</VersioningData>')
    buf.append('    <Characteristics>false</Characteristics>')
    buf.append('    <StandardAttributes>')
    buf.append('      <StandardAttribute>')
    buf.append('        <Name>Code</Name>')
    buf.append('        <Synonym>Код</Synonym>')
    buf.append('        <Comment/>')
    buf.append('        <UUID>%s</UUID>' % uid_("cat.attr." + name + ".Code"))
    buf.append('        <IsEnabled>true</IsEnabled>')
    buf.append('        <DataHistory>DontUse</DataHistory>')
    buf.append('        <FullTextSearch>Use</FullTextSearch>')
    buf.append('      </StandardAttribute>')
    buf.append('    </StandardAttributes>')
    buf.append('    <Templates>')
    buf.append('      <Template>')
    buf.append('        <Name>ПечатьПреподавателей</Name>')
    buf.append('        <Comment/>')
    buf.append('        <UUID>%s</UUID>' % uid_("tmpl." + name))
    buf.append('        <Type>SpreadsheetDocument</Type>')
    buf.append('        <FileName>ПечатьПреподавателей</FileName>')
    buf.append('      </Template>')
    buf.append('    </Templates>')
    buf.append('    <WriteMode>Exchange</WriteMode>')
    buf.append('    <SubordinationUse>NotUse</SubordinationUse>')
    buf.append('    <DataLockFields>')
    buf.append('    </DataLockFields>')
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    for aname, asyn, atyp in md.get("attrs", []):
        buf.append(attr(aname, asyn, atyp))
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for name, md in CATS.items():
    if md.get("enum"):
        continue
    write("Catalogs/" + name + ".xml", catalog_xml(name, md))

# Predefined elements for catalogs with fixed lists
PREDEFINED = {
 "СпособыОплаты": ["Наличные", "БанковскаяКарта", "Перевод", "ОнлайнОплата", "Другое"],
}

def predef_xml(cat, items):
    cid = get("catalog."+cat)
    buf = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<Predefined xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:v8="http://v8.1c.ru/8.1/data/core">',
           '  <Properties>',
           '    <Name>' + cat + '.Predefined</Name>',
           '    <Synonym/>',
           '    <Comment/>',
           '  </Properties>',
           '  <ChildObjects>']
    for i, item in enumerate(items):
        buf.append('    <PredefinedElement>')
        buf.append('      <Name>' + item + '</Name>')
        buf.append('      <Synonym>' + item + '</Synonym>')
        buf.append('      <Comment/>')
        buf.append('      <UUID>' + get("predef."+cat+"."+item) + '</UUID>')
        buf.append('      <Code>%d</Code>' % (i+1))
        buf.append('      <Description>' + item + '</Description>')
        buf.append('    </PredefinedElement>')
    buf.append('  </ChildObjects>')
    buf.append('</Predefined>')
    return "\n".join(buf)

for cat, items in PREDEFINED.items():
    write("Catalogs/" + cat + "/Ext/Predefined.xml", predef_xml(cat, items))

save()
print("catalogs written:", sum(1 for x in CATS.values() if not x.get("enum")))

def cat_form(name, attrs):
    elems = []
    elems.append('<Items xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Form">')
    elems.append('<ChildItems>')
    elems.append('<FormField Name="Code"><Type>InputField</Type><DataPath>Code</DataPath><ReadOnly>false</ReadOnly><Extension>Edit</Extension></FormField>')
    elems.append('</ChildItems>')
    elems.append('</Items>')
    return "\n".join(elems)

save()
print("catalogs written:", sum(1 for x in CATS.values() if not x.get("enum")))