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

def type_string(): return '<v8:Type>xs:string</v8:Type>'
def type_number(q=15,d=2): return '<v8:Type>xs:decimal</v8:Type><v8:Qualifiers><v8:Type>xs:decimal</v8:Type><v8:NumberQualifiers><v8:Precision>%d</v8:Precision><v8:Scale>%d</v8:Scale></v8:NumberQualifiers></v8:Qualifiers>'%(q,d)
def type_bool(): return '<v8:Type>xs:boolean</v8:Type><v8:TypeQualifiers><v8:Type>xs:boolean</v8:Type></v8:TypeQualifiers>'
def type_datetime(): return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>DateTime</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def type_time(): return '<v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>Time</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers>'
def c_ref(cat): return '<v8:Type>cfg:CatalogRef.'+cat+'</v8:Type><v8:TypeQualifiers><v8:Type>cfg:CatalogRef.'+cat+'</v8:Type></v8:TypeQualifiers>'
def d_ref(doc): return '<v8:Type>cfg:DocumentRef.'+doc+'</v8:Type><v8:TypeQualifiers><v8:Type>cfg:DocumentRef.'+doc+'</v8:Type></v8:TypeQualifiers>'
def e_ref(en): return '<v8:Type>cfg:EnumRef.'+en+'</v8:Type><v8:TypeQualifiers><v8:Type>cfg:EnumRef.'+en+'</v8:Type></v8:TypeQualifiers>'

def dimension(name, syn, typ, index=True):
    s = '    <Dimension>\n      <Name>%s</Name>\n      <Synonym>%s</Synonym>\n      <Comment/>\n      <UUID>%s</UUID>\n      <ValueType>%s</ValueType>\n      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n      <FullTextSearch>Use</FullTextSearch>\n      <Indexing>%s</Indexing>\n      <DataLockFields>Use</DataLockFields>\n    </Dimension>\n' % (name, syn, get("reg.dim."+name), typ, "Index" if index else "DoNotIndex")
    return s

def resource(name, syn, typ):
    return '    <Resource>\n      <Name>%s</Name>\n      <Synonym>%s</Synonym>\n      <Comment/>\n      <UUID>%s</UUID>\n      <ValueType>%s</ValueType>\n      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n      <FullTextSearch>Use</FullTextSearch>\n      <DataLockFields>Use</DataLockFields>\n    </Resource>\n' % (name, syn, get("reg.res."+name), typ)

def attribute(name, syn, typ):
    return '    <Attribute>\n      <Name>%s</Name>\n      <Synonym>%s</Synonym>\n      <Comment/>\n      <UUID>%s</UUID>\n      <ValueType>%s</ValueType>\n      <FillFromFillingValue>UseWhenFillingValueFilled</FillFromFillingValue>\n      <FullTextSearch>Use</FullTextSearch>\n      <DataLockFields>DoNotLoad</DataLockFields>\n    </Attribute>\n' % (name, syn, get("reg.attr."+name), typ)

# ============ INFORMATION REGISTERS ============
INFOREGS = {}

INFOREGS["РасписаниеПреподавателей"] = dict(
  syn="Расписание преподавателей", periodic={"Type":"Day","Frequency":"","ShiftByDays":0},
  dims=[("Преподаватель","Преподаватель",c_ref("Преподаватели")),
        ("ДеньНедели","День недели",type_number(1,0))],
  res=[("ВремяНачала","Время начала",type_time()),
       ("ВремяОкончания","Время окончания",type_time()),
       ("Доступность","Доступность",type_bool())],
  attrs=[("ТипЗанятия","Тип занятия",e_ref("ТипыЗанятий")),
         ("АудиторияПоУмолчанию","Аудитория по умолчанию",c_ref("Аудитории")),
         ("Исключение","Исключение (отпуск/болезнь)",type_bool())],
)

INFOREGS["ДоступностьАудиторий"] = dict(
  syn="Доступность аудиторий", periodic={"Type":"Day","Frequency":"","ShiftByDays":0},
  dims=[("Аудитория","Аудитория",c_ref("Аудитории")),("ДеньНедели","День недели",type_number(1,0))],
  res=[("ВремяНачала","Время начала",type_time()),
       ("ВремяОкончания","Время окончания",type_time()),
       ("Доступна","Доступна",type_bool())],
)

INFOREGS["НастройкиУведомлений"] = dict(
  syn="Настройки уведомлений",
  dims=[("Клиент","Клиент",c_ref("Клиенты"))],
  res=[("Telegram","Telegram",type_bool()),
       ("Email","Email",type_bool()),
       ("SMS","SMS",type_bool())],
  attrs=[("Канал","Канал",type_string())],
)

INFOREGS["ИсторияИзменений"] = dict(
  syn="История изменений",
  dims=[("Пользователь","Пользователь",c_ref("Пользователи"))],
  res=[],
  attrs=[("ДатаВремя","Дата/время",type_datetime()),
         ("Объект","Объект",type_string()),
         ("Действие","Действие",type_string()),
         ("СтароеЗначение","Старое значение",type_string()),
         ("НовоеЗначение","Новое значение",type_string())],
)

def inforeg_xml(name, md):
    rid = get("inforeg."+name)
    buf = [HEADER]
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>'%name)
    buf.append('    <Synonym>%s</Synonym>'%md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <UUID>%s</UUID>'%rid)
    buf.append('    <InformationRegisterPeriodicity>')
    if "periodic" in md:
        buf.append('      <Type>%s</Type>'%md["periodic"]["Type"])
        buf.append('      <Frequency>%s</Frequency>'%md["periodic"]["Frequency"])
        buf.append('      <ShiftByDays>%s</ShiftByDays>'%md["periodic"]["ShiftByDays"])
    else:
        buf.append('      <Type>Nonperiodical</Type>')
        buf.append('      <Frequency/>')
        buf.append('      <ShiftByDays>0</ShiftByDays>')
    buf.append('    </InformationRegisterPeriodicity>')
    buf.append('    <UseStandardCommands>true</UseStandardCommands>')
    buf.append('    <DataLockControlMode>Managed</DataLockControlMode>')
    buf.append('    <RegisterRecords>')
    buf.append('    </RegisterRecords>')
    buf.append('    <WriteMode>Exchange</WriteMode>')
    buf.append('    <DataVersioning>DontUse</DataVersioning>')
    buf.append('    <MainPresentation>Auto</MainPresentation>')
    buf.append('    <DefaultListForm>InformationRegister.%s.ListForm</DefaultListForm>'%name)
    buf.append('    <DefaultChoiceForm>InformationRegister.%s.ChoiceForm</DefaultChoiceForm>'%name)
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    for dn, ds, dt in md["dims"]:
        buf.append(dimension(dn,ds,dt))
    for rn, rs, rt in md["res"]:
        buf.append(resource(rn,rs,rt))
    for an, as_, at in md.get("attrs",[]):
        buf.append(attribute(an,as_,at))
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for n,m in INFOREGS.items():
    write("InformationRegisters/"+n+".xml", inforeg_xml(n,m))

# ============ ACCUMULATION REGISTERS ============
ACCREGS = {}

ACCREGS["ОстаткиАбонементов"] = dict(
  syn="Остатки абонементов", type="Balance",
  dims=[("АбонементКлиента","Абонемент клиента",c_ref("АбонементыКлиента")),
        ("Клиент","Клиент",c_ref("Клиенты"))],
  res=[("КоличествоЗанятий","Количество занятий",type_number(15,0))],
)

ACCREGS["Посещения"] = dict(
  syn="Посещения", type="Turnover",
  dims=[("Клиент","Клиент",c_ref("Клиенты")),
        ("Преподаватель","Преподаватель",c_ref("Преподаватели")),
        ("Направление","Направление",c_ref("Направления"))],
  res=[("Присутствовал","Присутствовал",type_number(15,0)),
       ("Отсутствовал","Отсутствовал",type_number(15,0)),
       ("Списано","Списано",type_number(15,0))],
)

ACCREGS["Оплаты"] = dict(
  syn="Оплаты", type="Turnover",
  dims=[("Клиент","Клиент",c_ref("Клиенты")),
        ("Абонемент","Абонемент",c_ref("АбонементыКлиента")),
        ("Назначение","Назначение",e_ref("ВидыОперацийОплат"))],
  res=[("Сумма","Сумма",type_number(15,2)),
       ("КоличествоОплат","Количество оплат",type_number(15,0))],
)

ACCREGS["ЗагрузкаПреподавателей"] = dict(
  syn="Загрузка преподавателей", type="Turnover",
  dims=[("Преподаватель","Преподаватель",c_ref("Преподаватели"))],
  res=[("Часы","Часы (минуты)",type_number(15,0))],
)

ACCREGS["ЗагрузкаАудиторий"] = dict(
  syn="Загрузка аудиторий", type="Turnover",
  dims=[("Аудитория","Аудитория",c_ref("Аудитории"))],
  res=[("Часы","Часы (минуты)",type_number(15,0))],
)

ACCREGS["АрендыИнструментов"] = dict(
  syn="Аренда инструментов", type="Turnover",
  dims=[("Инструмент","Инструмент",c_ref("Инструменты")),
        ("Клиент","Клиент",c_ref("Клиенты")),
        ("Филиал","Филиал",e_ref("Филиалы"))],
  res=[("Стоимость","Стоимость",type_number(15,2)),
       ("КоличествоЧасов","Количество часов",type_number(15,0))],
)

def accreg_xml(name, md):
    rid = get("accreg."+name)
    buf=[HEADER]
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>'%name)
    buf.append('    <Synonym>%s</Synonym>'%md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <UUID>%s</UUID>'%rid)
    buf.append('    <RegisterType>%s</RegisterType>'%(md["type"]))
    buf.append('    <UseStandardCommands>true</UseStandardCommands>')
    buf.append('    <DataLockControlMode>Managed</DataLockControlMode>')
    buf.append('    <RegisterRecords>')
    buf.append('    </RegisterRecords>')
    buf.append('    <WriteMode>Exchange</WriteMode>')
    buf.append('    <DefaultListForm>AccumulationRegister.%s.ListForm</DefaultListForm>'%name)
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    for dn,ds,dt in md["dims"]:
        buf.append(dimension(dn,ds,dt))
    for rn,rs,rt in md["res"]:
        buf.append(resource(rn,rs,rt))
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for n,m in ACCREGS.items():
    write("AccumulationRegisters/"+n+".xml", accreg_xml(n,m))

save()
print("inforegs:", len(INFOREGS), "accregs:", len(ACCREGS))