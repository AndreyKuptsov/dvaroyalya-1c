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

# ---------- Session parameters ----------
SESSIONS = {
 "ТекущийПользователь": ("СправочникСсылка.Пользователи", "Текущий пользователь"),
 "ТекущаяРоль": ("Строка", "Текущая роль"),
 "ДатаЗапретаКомментариев": ("Дата", "Дата запрета"),
}

def sess_xml(name, vt, syn):
    sid = get("session." + name)
    buf=[HEADER]
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>'%name)
    buf.append('    <Synonym>%s</Synonym>'%syn)
    buf.append('    <Comment/>')
    buf.append('    <UUID>%s</UUID>'%sid)
    if vt == "Строка":
        buf.append('    <ValueType><v8:Type>xs:string</v8:Type></ValueType>')
    elif vt == "Дата":
        buf.append('    <ValueType><v8:Type>xs:dateTime</v8:Type><v8:TypeQualifiers><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers><v8:DateFractions>DateTime</v8:DateFractions></v8:DateQualifiers></v8:TypeQualifiers></ValueType>')
    else:
        buf.append('    <ValueType><v8:Type>cfg:'+vt+'</v8:Type><v8:TypeQualifiers><v8:Type>cfg:'+vt+'</v8:Type></v8:TypeQualifiers></ValueType>')
    buf.append('  </Properties>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for n,(vt,syn) in SESSIONS.items():
    write("SessionParameters/"+n+".xml", sess_xml(n,vt,syn))

# ---------- Roles ----------
ROLES = {
 "Администратор": dict(syn="Администратор", full=True, dataprocessors=["ИмпортДанных","Уведомления","РезервноеКопирование"],
   docs=["Занятие","ЗаписьНаЗанятие","ПродажаАбонемента","Оплата","Посещение","ОтменаЗанятия","ПереносЗанятия","ЗаморозкаАбонемента","Возврат"],
   cats=["Клиенты","Преподаватели","Направления","Аудитории","Абонементы","СпособыОплаты","АбонементыКлиента","Пользователи"],
   inforegs=["РасписаниеПреподавателей","ДоступностьАудиторий","НастройкиУведомлений","ИсторияИзменений"],
   accregs=["ОстаткиАбонементов","Посещения","Оплаты","ЗагрузкаПреподавателей","ЗагрузкаАудиторий"],
   enums=list(__import__("enums", fromlist=["ENUMS"]).ENUMS.keys()),
   reports=["Расписание","Посещаемость","ЗагрузкаПреподавателей","ЗагрузкаАудиторий","Продажи","Клиенты","Абонементы","Задолженность"]),
 "Руководитель": dict(syn="Руководитель", full=False, dataprocessors=["ИмпортДанных","Уведомления"],
   docs=["Занятие","ЗаписьНаЗанятие","ПродажаАбонемента","Оплата","Посещение","ОтменаЗанятия","ПереносЗанятия","ЗаморозкаАбонемента","Возврат"],
   cats=["Клиенты","Преподаватели","Направления","Аудитории","Абонементы","СпособыОплаты","АбонементыКлиента"],
   inforegs=["РасписаниеПреподавателей","ДоступностьАудиторий","НастройкиУведомлений","ИсторияИзменений"],
   accregs=["ОстаткиАбонементов","Посещения","Оплаты","ЗагрузкаПреподавателей","ЗагрузкаАудиторий"],
   enums=list(__import__("enums", fromlist=["ENUMS"]).ENUMS.keys()),
   reports=["Расписание","Посещаемость","ЗагрузкаПреподавателей","ЗагрузкаАудиторий","Продажи","Клиенты","Абонементы","Задолженность"]),
 "Преподаватель": dict(syn="Преподаватель", full=False,
   docs=["Занятие","Посещение"],
   cats=["Клиенты","Направления","АбонементыКлиента"],
   inforegs=["РасписаниеПреподавателей"],
   accregs=["Посещения","ОстаткиАбонементов"],
   enums=[],
   reports=["Расписание"]),
 "Бухгалтер": dict(syn="Бухгалтер", full=False, dataprocessors=["Уведомления"],
   docs=["Оплата","Возврат","ПродажаАбонемента"],
   cats=["Клиенты","Абонементы","СпособыОплаты","АбонементыКлиента"],
   inforegs=["НастройкиУведомлений"],
   accregs=["Оплаты","ОстаткиАбонементов"],
   enums=[],
   reports=["Продажи","Абонементы","Задолженность"]),
 "Наблюдатель": dict(syn="Наблюдатель", full=False,
   docs=[], cats=["Клиенты","Преподаватели","Направления","Аудитории","Абонементы","АбонементыКлиента"],
   inforegs=["РасписаниеПреподавателей","ДоступностьАудиторий"],
   accregs=["Посещения","Оплаты","ОстаткиАбонементов"],
   enums=[],
   reports=["Расписание","Посещаемость","Продажи","ЗагрузкаПреподавателей","ЗагрузкаАудиторий"]),
}

def right(s, access="Read", data="Allowed"):
    return '    <Right><Name>%s</Name><Value><Access>%s</Access>%s</Value></Right>\n' % (s, access, data_due(data) if data else "")

def data_due(mode):
    return ""

def role_xml(name, md):
    rid = get("role."+name)
    buf=[HEADER]
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>'%name)
    buf.append('    <Synonym>%s</Synonym>'%md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <UUID>%s</UUID>'%rid)
    buf.append('    <DataHistory>DontUse</DataHistory>')
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    # Enum rights
    for en in md["enums"]:
        buf.append('    <Enum>')
        buf.append('      <EnumRef><Name>%s</Name></EnumRef>'%en)
        buf.append('      <EnumRights>')
        buf.append(right("Read"))
        if md["full"]:
            buf.append(right("Extend"))
        buf.append('      </EnumRights>')
        buf.append('    </Enum>')
    # Catalog rights
    for c in md["cats"]:
        buf.append('    <Catalog>')
        buf.append('      <CatalogRef><Name>%s</Name></CatalogRef>'%c)
        buf.append('      <CatalogRights>')
        buf.append(right("Read"))
        if md["full"]:
            buf.append(right("Insert"))
            buf.append(right("Update"))
            buf.append(right("Delete"))
        buf.append('      </CatalogRights>')
        buf.append('    </Catalog>')
    # Document rights
    for d in md["docs"]:
        buf.append('    <Document>')
        buf.append('      <DocumentRef><Name>%s</Name></DocumentRef>'%d)
        buf.append('      <DocumentRights>')
        buf.append(right("View"))
        if md["full"]:
            buf.append(right("Input"))
            buf.append(right("Edit"))
            buf.append(right("Posting"))
            buf.append(right("Unposting"))
            buf.append(right("Delete"))
            buf.append(right("InteractiveDelete"))
            buf.append(right("UndoPosting"))
            buf.append(right("InteractiveInput"))
            buf.append(right("InteractiveMarkDelete"))
        buf.append('      </DocumentRights>')
        buf.append('    </Document>')
    # inforeg rights (view)
    for r in md["inforegs"]:
        buf.append('    <InformationRegister>')
        buf.append('      <InformationRegisterRef><Name>%s</Name></InformationRegisterRef>'%r)
        buf.append('      <InformationRegisterRights>')
        buf.append(right("Read"))
        if md["full"]:
            buf.append(right("Input"))
            buf.append(right("Update"))
            buf.append(right("Delete"))
        buf.append('      </InformationRegisterRights>')
        buf.append('    </InformationRegister>')
    # accregister rights
    for r in md["accregs"]:
        buf.append('    <AccumulationRegister>')
        buf.append('      <AccumulationRegisterRef><Name>%s</Name></AccumulationRegisterRef>'%r)
        buf.append('      <AccumulationRegisterRights>')
        buf.append(right("Read"))
        buf.append('      </AccumulationRegisterRights>')
        buf.append('    </AccumulationRegister>')
    # Report rights
    for r in md["reports"]:
        buf.append('    <Report>')
        buf.append('      <ReportRef><Name>%s</Name></ReportRef>'%r)
        buf.append('      <ReportRights>')
        buf.append(right("View"))
        buf.append('      </ReportRights>')
        buf.append('    </Report>')
    # DataProcessor rights
    dprocs = md.get("dataprocessors", [])
    for d in dprocs:
        buf.append('    <DataProcessor>')
        buf.append('      <DataProcessorRef><Name>%s</Name></DataProcessorRef>'%d)
        buf.append('      <DataProcessorRights>')
        buf.append(right("View"))
        if md["full"]:
            buf.append(right("Input"))
            buf.append(right("Edit"))
        buf.append('      </DataProcessorRights>')
        buf.append('    </DataProcessor>')
    # CommonModule rights (usage)
    buf.append('    <CommonModule>')
    buf.append('      <CommonModuleRef><Name>ПараметрыСеанса</Name></CommonModuleRef>')
    buf.append('      <CommonModuleRights>')
    buf.append(right("Client"))
    buf.append(right("Server"))
    buf.append('      </CommonModuleRights>')
    buf.append('    </CommonModule>')
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

KEY = ("DataHistory","Read","View","Input","Edit","Posting","Unposting","Delete",
       "InteractiveDelete","UndoPosting","InteractiveInput","InteractiveMarkDelete","Extend","Client","Server")

for n,md in ROLES.items():
    write("Roles/"+n+".xml", role_xml(n,md))

save()
print("roles:", len(ROLES), "sessions:", len(SESSIONS))