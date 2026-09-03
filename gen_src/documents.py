# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import load, get, save
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

HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">\n'

def type_string():
    return '<v8:Type>xs:string</v8:Type>'
def type_number(q=15,d=2):
    return '<v8:Type>xs:decimal</v8:Type><v8:Qualifiers><v8:Type>xs:decimal</v8:Type><v8:NumberQualifiers><v8:Precision>%d</v8:Precision><v8:Scale>%d</v8:Scale></v8:NumberQualifiers></v8:Qualifiers>' % (q,d)
def type_bool():
    return '<v8:Type>xs:boolean</v8:Type><v8:TypeQualifiers><v8:Type>xs:boolean</v8:Type></v8:TypeQualifiers>'
def type_datetime():
    return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>DateTime</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def type_dateonly():
    return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>Date</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def type_ref(cat_type, cat):
    return '<v8:Type>cfg:' + cat_type + '.' + cat + '</v8:Type><v8:TypeQualifiers><v8:Type>cfg:' + cat_type + '.' + cat + '</v8:Type></v8:TypeQualifiers>'
def c_ref(cat): return type_ref("CatalogRef", cat)
def d_ref(doc): return type_ref("DocumentRef", doc)
def e_ref(en): return type_ref("EnumRef", ren(en))

def ren(en):
    return en

def attr(name, syn_name, typ):
    s = '    <Attribute>\n'
    s += '      <Name>%s</Name>\n' % name
    s += '      <Synonym>%s</Synonym>\n' % syn_name
    s += '      <Comment/>\n'
    s += '      <UUID>%s</UUID>\n' % get("doc.attr." + name)
    s += '      <ValueType>' + typ + '</ValueType>\n'
    s += '      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n'
    s += '      <FullTextSearch>Use</FullTextSearch>\n'
    s += '    </Attribute>\n'
    return s

def tabsec(name, syn_name, cols):
    s = '    <TabularSection>\n'
    s += '      <Name>%s</Name>\n' % name
    s += '      <Synonym>%s</Synonym>\n' % syn_name
    s += '      <Comment/>\n'
    s += '      <UUID>%s</UUID>\n' % get("doc.ts." + name)
    s += '      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n'
    s += '      <FullTextSearch>Use</FullTextSearch>\n'
    s += '      <Attributes>\n'
    for cname, csyn, ctyp in cols:
        s += '        <Attribute>\n'
        s += '          <Name>%s</Name>\n' % cname
        s += '          <Synonym>%s</Synonym>\n' % csyn
        s += '          <Comment/>\n'
        s += '          <UUID>%s</UUID>\n' % get("doc.ts.col." + cname)
        s += '          <ValueType>' + ctyp + '</ValueType>\n'
        s += '          <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n'
        s += '          <FullTextSearch>Use</FullTextSearch>\n'
        s += '          <Indexing>DoNotIndex</Indexing>\n'
        s += '          <DataLockFields>DoNotLoad</DataLockFields>\n'
        s += '        </Attribute>\n'
    s += '      </Attributes>\n'
    s += '    </TabularSection>\n'
    return s

DOCS = {}

DOCS["Занятие"] = dict(
  syn="Занятие",
  attrs=[
    ("ДатаЗанятия","Дата",type_dateonly()),
    ("ВремяНачала","Время начала",type_datetime()),
    ("ВремяОкончания","Время окончания",type_datetime()),
    ("Преподаватель","Преподаватель",c_ref("Преподаватели")),
    ("Аудитория","Аудитория",c_ref("Аудитории")),
    ("Направление","Направление",c_ref("Направления")),
    ("ТипЗанятия","Тип занятия",e_ref("ТипыЗанятий")),
    ("Статус","Статус",e_ref("СтатусыЗанятия")),
    ("Комментарий","Комментарий",type_string()),
  ],
  tabs={
    "Участники":[
      ("Клиент","Клиент",c_ref("Клиенты")),
      ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
      ("СтатусПосещения","Статус посещения",e_ref("СтатусыПосещения")),
      ("Стоимость","Стоимость",type_number()),
      ("Комментарий","Комментарий",type_string()),
    ],
  },
)

DOCS["ЗаписьНаЗанятие"] = dict(
  syn="Запись на занятие",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("Занятие","Занятие",d_ref("Занятие")),
    ("ДатаЗаписи","Дата записи",type_datetime()),
    ("ИсточникЗаписи","Источник записи",type_string()),
    ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
    ("Статус","Статус",e_ref("СтатусыЗаписи")),
  ],
)

DOCS["ПродажаАбонемента"] = dict(
  syn="Продажа абонемента",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("Абонемент","Абонемент",c_ref("Абонементы")),
    ("ДатаПродажи","Дата продажи",type_datetime()),
    ("Стоимость","Стоимость",type_number()),
    ("СпособОплаты","Способ оплаты",c_ref("СпособыОплаты")),
    ("ДатаНачала","Дата начала",type_dateonly()),
    ("ДатаОкончания","Дата окончания",type_dateonly()),
  ],
)

DOCS["Оплата"] = dict(
  syn="Оплата",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("ДатаОплаты","Дата",type_datetime()),
    ("Сумма","Сумма",type_number()),
    ("СпособОплаты","Способ оплаты",c_ref("СпособыОплаты")),
    ("Назначение","Назначение",e_ref("ВидыОперацийОплат")),
    ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
    ("Комментарий","Комментарий",type_string()),
  ],
)

DOCS["Посещение"] = dict(
  syn="Посещение",
  attrs=[
    ("Занятие","Занятие",d_ref("Занятие")),
    ("Преподаватель","Преподаватель",c_ref("Преподаватели")),
    ("ДатаПосещения","Дата",type_datetime()),
    ("Комментарий","Комментарий",type_string()),
  ],
  tabs={
    "Участники":[
      ("Клиент","Клиент",c_ref("Клиенты")),
      ("СтатусПосещения","Статус посещения",e_ref("СтатусыПосещения")),
      ("СписатьЗанятие","Списать занятие",type_bool()),
      ("Комментарий","Комментарий",type_string()),
      ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
    ],
  },
)

DOCS["ОтменаЗанятия"] = dict(
  syn="Отмена занятия",
  attrs=[
    ("Занятие","Занятие",d_ref("Занятие")),
    ("Причина","Причина",e_ref("ПричиныОтмены")),
    ("ДатаОтмены","Дата отмены",type_datetime()),
    ("СписыватьЗанятие","Списывать занятие",type_bool()),
    ("ВозвращатьЗанятие","Возвращать занятие на баланс",type_bool()),
    ("ВозвращатьОплату","Возвращать оплату",type_bool()),
    ("Комментарий","Комментарий",type_string()),
  ],
)

DOCS["ПереносЗанятия"] = dict(
  syn="Перенос занятия",
  attrs=[
    ("ПервоначальноеЗанятие","Первоначальное занятие",d_ref("Занятие")),
    ("НовоеЗанятие","Новое занятие",d_ref("Занятие")),
    ("ПричинаПереноса","Причина переноса",type_string()),
    ("ДатаПереноса","Дата переноса",type_datetime()),
    ("Исполнитель","Исполнитель",c_ref("Пользователи")),
    ("НоваяДата","Новая дата",type_dateonly()),
    ("НовоеВремяНачала","Новое время начала",type_datetime()),
    ("НовоеВремяОкончания","Новое время окончания",type_datetime()),
  ],
)

DOCS["ЗаморозкаАбонемента"] = dict(
  syn="Заморозка абонемента",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
    ("ДатаНачала","Дата начала",type_dateonly()),
    ("ДатаОкончания","Дата окончания",type_dateonly()),
    ("Причина","Причина",type_string()),
  ],
)

DOCS["Возврат"] = dict(
  syn="Возврат",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("Сумма","Сумма",type_number()),
    ("СпособОплаты","Способ оплаты",c_ref("СпособыОплаты")),
    ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
    ("Комментарий","Комментарий",type_string()),
  ],
)

DOCS["АрендаИнструмента"] = dict(
  syn="Аренда инструмента",
  attrs=[
    ("Клиент","Клиент",c_ref("Клиенты")),
    ("Инструмент","Инструмент",c_ref("Инструменты")),
    ("ДатаНачала","Дата аренды",type_dateonly()),
    ("ВремяНачала","Время начала",type_datetime()),
    ("ВремяОкончания","Время окончания",type_datetime()),
    ("Стоимость","Стоимость",type_number()),
    ("Статус","Статус",e_ref("СтатусыАренды")),
    ("Комментарий","Комментарий",type_string()),
  ],
)

def doc_xml(name, md):
    did = get("document." + name)
    buf = []
    buf.append(HEADER)
    buf.append('  <InternalInfo>')
    buf.append('    <xen:generator><xen:packageName>ДваРояля</xen:packageName></xen:generator>')
    buf.append('  </InternalInfo>')
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>' % name)
    buf.append('    <Synonym>%s</Synonym>' % md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <UseStandardCommands>true</UseStandardCommands>')
    buf.append('    <NumberType>Number</NumberType>')
    buf.append('    <NumberLength>11</NumberLength>')
    buf.append('    <NumberAllowedLength>Variable</NumberAllowedLength>')
    buf.append('    <NumberPeriodicity>Nonperiodical</NumberPeriodicity>')
    buf.append('    <DefaultNumberingType>Auto</DefaultNumberingType>')
    buf.append('    <CheckUnique>DontCheck</CheckUnique>')
    buf.append('    <Autonumbering>Auto</Autonumbering>')
    buf.append('    <Posting>Allow</Posting>')
    buf.append('    <RealTimePosting>Disallow</RealTimePosting>')
    buf.append('    <DefaultPostingMode>Operation</DefaultPostingMode>')
    buf.append('    <PostingModeForUnposted>Operation</PostingModeForUnposted>')
    buf.append('    <PostingInPrivilegedMode>false</PostingInPrivilegedMode>')
    buf.append('    <CreateOnInput>Use</CreateOnInput>')
    buf.append('    <FullTextSearch>Use</FullTextSearch>')
    buf.append('    <IncludeHelpInContents>true</IncludeHelpInContents>')
    buf.append('    <UseStandardCommandsInList>true</UseStandardCommandsInList>')
    buf.append('    <NumberPrefix>true</NumberPrefix>')
    buf.append('    <NumberPeriodicity>Nonperiodical</NumberPeriodicity>')
    buf.append('    <ObjectPresentation>%s</ObjectPresentation>' % md["syn"])
    buf.append('    <ExtendedObjectPresentation/>')
    buf.append('    <ListPresentation>%s</ListPresentation>' % md["syn"])
    buf.append('    <ExtendedListPresentation/>')
    buf.append('    <Explanation/>')
    buf.append('    <DefaultObjectForm>Document.%s.ObjectForm</DefaultObjectForm>' % name)
    buf.append('    <DefaultListForm>Document.%s.ListForm</DefaultListForm>' % name)
    buf.append('    <DefaultChoiceForm>Document.%s.ChoiceForm</DefaultChoiceForm>' % name)
    buf.append('    <DefaultListPresentation>%s</DefaultListPresentation>' % md["syn"])
    buf.append('    <WriteMode>Exchange</WriteMode>')
    buf.append('    <LengthLimitOnEnter>false</LengthLimitOnEnter>')
    buf.append('    <RegisterRecords>')
    buf.append('    </RegisterRecords>')
    buf.append('    <Post>false</Post>')
    buf.append('    <DataLockFields>')
    buf.append('    </DataLockFields>')
    buf.append('    <NumberAuto>true</NumberAuto>')
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    for aname, asyn, atyp in md.get("attrs", []):
        buf.append(attr(aname, asyn, atyp))
    for tname, tcols in md.get("tabs", {}).items():
        buf.append(tabsec(tname, tname, tcols))
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for name, md in DOCS.items():
    write("Documents/" + name + ".xml", doc_xml(name, md))

save()
print("documents written:", len(DOCS))