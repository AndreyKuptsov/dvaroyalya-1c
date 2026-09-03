# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import load, get, save
from enums import ENUMS
load()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CFG = ROOT

def ensure(d):
    os.makedirs(d, exist_ok=True)

def write(path, content):
    p = path
    if not os.path.isabs(p):
        p = os.path.join(CFG, p)
    ensure(os.path.dirname(p))
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

save()

LANG_COMP = get("lang.ru")
CFG_COMP = get("config")

def child(kind, entryname, refkey):
    return '    <%s><Name>%s</Name></%s>\n' % (kind, entryname, kind)

def config_xml():
    buf=[]
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <InternalInfo>')
    buf.append('    <xen:generator>')
    buf.append('      <xen:packageName>ДваРояля</xen:packageName>')
    buf.append('    </xen:generator>')
    buf.append('    <xen:platformVersion>8.3.20</xen:platformVersion>')
    buf.append('  </InternalInfo>')
    buf.append('  <Properties>')
    buf.append('    <Name>ДваРояля</Name>')
    buf.append('    <Synonym>')
    buf.append('      <v8:item><v8:lang>' + LANG_COMP + '</v8:lang><v8:content>ИС "Два Рояля"</v8:content></v8:item>')
    buf.append('    </Synonym>')
    buf.append('    <Comment>')
    buf.append('      <v8:item><v8:lang>' + LANG_COMP + '</v8:lang><v8:content>Информационная система управления записью и учётом занятий музыкальной студии</v8:content></v8:item>')
    buf.append('    </Comment>')
    buf.append('    <UUID>' + CFG_COMP + '</UUID>')
    buf.append('    <DefaultLanguage>' + LANG_COMP + '</DefaultLanguage>')
    buf.append('    <RuntimeUpdateMode>AutoUpdate</RuntimeUpdateMode>')
    buf.append('    <UpdateCatalogVersion>0</UpdateCatalogVersion>')
    buf.append('    <ConfigurationExtensionCompatibilityMode>Version8_3_20</ConfigurationExtensionCompatibilityMode>')
    buf.append('    <DefaultRunMode>ManagedApplication</DefaultRunMode>')
    buf.append('    <UsePurposes>PersonalComputer</UsePurposes>')
    buf.append('    <ScriptVariant>Russian</ScriptVariant>')
    buf.append('    <DefaultScriptVariant>Russian</DefaultScriptVariant>')
    buf.append('    <ObjectModel>Strict</ObjectModel>')
    buf.append('    <ModalityUseMode>DontUse</ModalityUseMode>')
    buf.append('    <SynchronousPlatformExtensionAndAddInCallUseMode>NotUse</SynchronousPlatformExtensionAndAddInCallUseMode>')
    buf.append('    <MethodsUseMode>DontUse</MethodsUseMode>')
    buf.append('    <NetworkDataExchangeUseMode>DontUse</NetworkDataExchangeUseMode>')
    buf.append('    <ControlOfUnsupportedMethodUse>Error</ControlOfUnsupportedMethodUse>')
    buf.append('    <CompatibilityMode>Version8_3_20</CompatibilityMode>')
    buf.append('    <Options>')
    buf.append('      <Option><Name>LoadPrintFormLengthLimit</Name><Value>false</Value></Option>')
    buf.append('    </Options>')
    buf.append('    <InterfaceCompatibilityMode>Taxi</InterfaceCompatibilityMode>')
    buf.append('    <MobileApplicationCompatibilityMode>NotUse</MobileApplicationCompatibilityMode>')
    buf.append('    <Version>1.0.0.1</Version>')
    buf.append('  </Properties>')
    buf.append('  <ChildObjects>')
    # Languages
    for lang in [("ru","Русский")]:
        pass
    buf.append('    <Language><Name>ru</Name></Language>')
    # Roles
    for r in ["Администратор","Руководитель","Преподаватель","Бухгалтер","Наблюдатель"]:
        buf.append('    <Role><Name>%s</Name></Role>'%r)
    # Catalogs
    for c in ["Клиенты","Преподаватели","Направления","Аудитории","Абонементы","СпособыОплаты","Пользователи","АбонементыКлиента","Инструменты"]:
        buf.append('    <Catalog><Name>%s</Name></Catalog>'%c)
    # Documents
    for d in ["Занятие","ЗаписьНаЗанятие","ПродажаАбонемента","Оплата","Посещение","ОтменаЗанятия","ПереносЗанятия","ЗаморозкаАбонемента","Возврат","АрендаИнструмента"]:
        buf.append('    <Document><Name>%s</Name></Document>'%d)
    # Enums
    for e in ENUMS:
        buf.append('    <Enum><Name>%s</Name></Enum>'%e)
    # Registers
    for ir in ["РасписаниеПреподавателей","ДоступностьАудиторий","НастройкиУведомлений","ИсторияИзменений"]:
        buf.append('    <InformationRegister><Name>%s</Name></InformationRegister>'%ir)
    for ar in ["ОстаткиАбонементов","Посещения","Оплаты","ЗагрузкаПреподавателей","ЗагрузкаАудиторий","АрендыИнструментов"]:
        buf.append('    <AccumulationRegister><Name>%s</Name></AccumulationRegister>'%ar)
    # Common modules
    for cm in ["РаботаСДатами","ПараметрыСеанса","УправлениеДоступом","КонтрольКонфликтовРасписания","РаботаСОстаткамиАбонементов","УведомленияСервер","АудитДействий","ОбщегоНазначения"]:
        buf.append('    <CommonModule><Name>%s</Name></CommonModule>'%cm)
    # Session parameters
    for s in ["ТекущийПользователь","ТекущаяРоль","ДатаЗапретаКомментариев"]:
        buf.append('    <SessionParameter><Name>%s</Name></SessionParameter>'%s)
    # Reports
    for r in ["Расписание","Посещаемость","ЗагрузкаПреподавателей","ЗагрузкаАудиторий","Продажи","Клиенты","Абонементы","Задолженность"]:
        buf.append('    <Report><Name>%s</Name></Report>'%r)
    # DataProcessors
    for d in ["ИмпортДанных","Уведомления","РезервноеКопирование"]:
        buf.append('    <DataProcessor><Name>%s</Name></DataProcessor>'%d)
    buf.append('  </ChildObjects>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

write("Configuration.xml", config_xml())
save()
print("Configuration.xml written")