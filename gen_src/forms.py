# -*- coding: utf-8 -*-
import os, sys, base64
sys.path.insert(0, os.path.dirname(__file__))
from registry import load, get, save
load()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def ensure(d):
    os.makedirs(d, exist_ok=True)

def write(rel, content):
    p = os.path.join(ROOT, rel)
    ensure(os.path.dirname(p))
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

# Form metadata XML wrapper
def form_meta_xml(name, uuid):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">\n'
        '  <Properties>\n'
        '    <Name>%s</Name>\n'
        '    <Synonym>%s</Synonym>\n'
        '    <Comment/>\n'
        '    <UUID>%s</UUID>\n'
        '    <FormType>Managed</FormType>\n'
        '    <IncludeHelpInContents>true</IncludeHelpInContents>\n'
        '    <ContextHelp/>\n'
        '  </Properties>\n'
        '  <ChildObjects/>\n'
        '</MetaDataObject>\n') % (name, name, uuid)

# Build object form content (managed form) for catalogs and documents.
# data_kind: "CatalogObject" / "DocumentObject"
# attr_list: list of (path, title, ctl) where ctl in {Input, CheckBox, ComboBox, Label}
def obj_form_content(objref_kind, obj_name, title, attr_list, tabular=None, module=""):
    type_obj = "cfg:%s.%s" % (objref_kind, obj_name)
    buf = []
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<Form xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:dcscom="http://v8.1c.ru/8.1/data-composition-system/composition" xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" xmlns:dcsse="http://v8.1c.ru/8.1/data-composition-system/settings-options" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <autoTitle>true</autoTitle>')
    buf.append('  <autoTitleSet>true</autoTitleSet>')
    buf.append('  <type>Managed</type>')
    buf.append('  <Extensions/>')
    buf.append('  <Attributes>')
    buf.append('    <Attribute name="Объект">')
    buf.append('      <Types><Type>%s</Type></Types>' % type_obj)
    buf.append('      <MainAttribute>true</MainAttribute>')
    buf.append('      <SavedData>true</SavedData>')
    buf.append('    </Attribute>')
    buf.append('  </Attributes>')
    buf.append('  <ChildItems>')
    for path, ttl, ctl in attr_list:
        buf.append('    <FormField name="%s" horizontalStretch="true">' % path)
        buf.append('      <DataPath>Объект.%s</DataPath>' % path)
        buf.append('      <Type>%s</Type>' % ctl)
        if ctl == "InputField":
            buf.append('      <Extension>Edit</Extension>')
        buf.append('      <Title>%s</Title>' % ttl)
        buf.append('      <TitleLocation>Top</TitleLocation>')
        buf.append('    </FormField>')
    if tabular:
        tname, cols = tabular
        buf.append('    <FormTable name="%s" horizontalStretch="true">' % tname)
        buf.append('      <DataPath>Объект.%s</DataPath>' % tname)
        buf.append('      <Type>Table</Type>')
        buf.append('      <Title>%s</Title>' % tname)
        buf.append('      <TitleLocation>Top</TitleLocation>')
        for cpath, cttl in cols:
            buf.append('      <ChildItems>')
            buf.append('        <FormField name="%s"><DataPath>%s</DataPath><Type>InputField</Type><Extension>Edit</Extension><Title>%s</Title></FormField>' % (cpath, cpath, cttl))
            buf.append('      </ChildItems>')
        buf.append('    </FormTable>')
    buf.append('  </ChildItems>')
    buf.append('  <Commands/>')
    buf.append('  <Parameters/>')
    buf.append('  <EventHandlers/>')
    buf.append('  <ExtendedAttributes/>')
    buf.append('  <FormAttributes/>')
    buf.append('  <CommandInterface/>')
    buf.append('  <FormDependencies/>')
    buf.append('  <FormExtensions>')
    buf.append('    <FormExtension>')
    buf.append('      <Module>%s</Module>' % base64.b64encode(module.encode("utf-8")).decode())
    buf.append('    </FormExtension>')
    buf.append('  </FormExtensions>')
    buf.append('</Form>')
    return "\n".join(buf)

def list_form_content(objref_kind, obj_name, module=""):
    buf = []
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<Form xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:dcscom="http://v8.1c.ru/8.1/data-composition-system/composition" xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" xmlns:dcsse="http://v8.1c.ru/8.1/data-composition-system/settings-options" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <autoTitle>true</autoTitle>')
    buf.append('  <autoTitleSet>true</autoTitleSet>')
    buf.append('  <type>Managed</type>')
    buf.append('  <Extensions/>')
    buf.append('  <Attributes>')
    buf.append('    <Attribute name="Список">')
    buf.append('      <Types><Type>cfg:List.%s</Type></Types>' % obj_name)
    buf.append('      <MainAttribute>true</MainAttribute>')
    buf.append('      <SavedData>true</SavedData>')
    buf.append('    </Attribute>')
    buf.append('  </Attributes>')
    buf.append('  <ChildItems>')
    buf.append('    <FormTable name="Список" horizontalStretch="true">')
    buf.append('      <DataPath>Список</DataPath>')
    buf.append('      <Type>Table</Type>')
    buf.append('      <Title>Список</Title>')
    buf.append('    </FormTable>')
    buf.append('  </ChildItems>')
    buf.append('  <Commands/>')
    buf.append('  <Parameters/>')
    buf.append('  <EventHandlers/>')
    buf.append('  <ExtendedAttributes/>')
    buf.append('  <FormAttributes/>')
    buf.append('  <CommandInterface/>')
    buf.append('  <FormDependencies/>')
    buf.append('  <FormExtensions>')
    buf.append('    <FormExtension><Module>%s</Module></FormExtension>' % base64.b64encode(module.encode("utf-8")).decode())
    buf.append('  </FormExtensions>')
    buf.append('</Form>')
    return "\n".join(buf)

# ---- Which object kinds ----
CATALOG_OBJECT = {}
CATALOG_OBJECT["Клиенты"] = [("ФИО","ФИО","InputField")]
CATALOG_OBJECT["Преподаватели"] = [("ФИО","ФИО","InputField")]
CATALOG_OBJECT["Направления"] = [("Наименование","Наименование","InputField")]
CATALOG_OBJECT["Аудитории"] = [("Наименование","Наименование","InputField")]
CATALOG_OBJECT["Абонементы"] = [("Наименование","Наименование","InputField")]
CATALOG_OBJECT["СпособыОплаты"] = [("Наименование","Наименование","InputField")]
CATALOG_OBJECT["Пользователи"] = [("Наименование","Наименование","InputField")]
CATALOG_OBJECT["АбонементыКлиента"] = [("Наименование","Наименование","InputField")]

# Catalog object forms: build full attribute fields from definitions in catalogs.py
import importlib.util
spec = importlib.util.spec_from_file_location("catalogs", os.path.join(os.path.dirname(__file__), "catalogs.py"))
# We don't import (would regenerate), we define attr lists here manually.

def cat_form_fields(cat):
    # returns list of (path,title,ctl) using standard catalog attribute set
    if cat == "Клиенты":
        return [("Наименование","ФИО","InputField"),("ДатаРождения","Дата рождения","InputField"),
                ("Телефон","Телефон","InputField"),("Email","Email","InputField"),
                ("Telegram","Telegram","InputField"),("TelegramID","Telegram ID","InputField"),
                ("ДатаРегистрации","Дата регистрации","InputField"),("СтатусКлиента","Статус клиента","ComboBox"),
                ("ИсточникПривлечения","Источник привлечения","ComboBox"),("ОтветственныйМенеджер","Ответственный менеджер","InputField"),
                ("СогласиеНаУведомления","Согласие на уведомления","CheckBox"),("СогласиеНаОбработкуДанных","Согласие на обработку ПД","CheckBox"),
                ("Комментарий","Комментарий","InputField")]
    if cat == "Преподаватели":
        return [("Наименование","ФИО","InputField"),("Телефон","Телефон","InputField"),
                ("Email","Email","InputField"),("Специализация","Специализация","InputField"),
                ("ДатаНачалаРаботы","Дата начала работы","InputField"),("Статус","Статус","ComboBox"),
                ("Ставка","Ставка","InputField"),("Филиал","Филиал","ComboBox"),
                ("Сотрудник","Сотрудник","InputField"),
                ("Комментарий","Комментарий","InputField")]
    if cat == "Направления":
        return [("Наименование","Наименование","InputField"),("ДлительностьЗанятия","Длительность занятия","InputField"),
                ("БазоваяСтоимость","Базовая стоимость","InputField"),("ТипЗанятия","Тип занятия","ComboBox"),
                ("Филиал","Филиал","ComboBox"),
                ("Описание","Описание","InputField"),("Активность","Активность","CheckBox")]
    if cat == "Аудитории":
        return [("Наименование","Наименование","InputField"),("Номер","Номер","InputField"),
                ("Вместимость","Вместимость","InputField"),("Тип","Тип","ComboBox"),
                ("Филиал","Филиал","ComboBox"),
                ("НаличиеОборудования","Наличие оборудования","CheckBox"),("Статус","Статус","CheckBox")]
    if cat == "Инструменты":
        return [("Наименование","Наименование","InputField"),("ТипИнструмента","Тип инструмента","ComboBox"),
                ("Филиал","Филиал","ComboBox"),("ИнвентарныйНомер","Инвентарный номер","InputField"),
                ("НаличиеАкустическое","Акустический","CheckBox"),("Статус","Статус","ComboBox"),
                ("СтоимостьАрендыВЧас","Стоимость аренды (час)","InputField"),("Комментарий","Комментарий","InputField")]
    if cat == "Абонементы":
        return [("Наименование","Наименование","InputField"),("КоличествоЗанятий","Количество занятий","InputField"),
                ("СрокДействия","Срок действия (дней)","InputField"),("Стоимость","Стоимость","InputField"),
                ("Направление","Направление","InputField"),("ДлительностьЗанятия","Длительность занятия (мин)","InputField"),
                ("ВозможностьЗаморозки","Возможность заморозки","CheckBox"),("МаксимальныйСрокЗаморозки","Макс. срок заморозки (дней)","InputField"),
                ("КоличествоПереносов","Количество переносов","InputField"),("Филиал","Филиал","ComboBox"),("Активность","Активность","CheckBox")]
    if cat == "СпособыОплаты":
        return [("Наименование","Наименование","InputField")]
    if cat == "Пользователи":
        return [("Наименование","Наименование","InputField"),("ФИО","ФИО","InputField"),
                ("Телефон","Телефон","InputField"),("Email","Email","InputField"),("Роль","Роль","InputField")]
    if cat == "АбонементыКлиента":
        return [("Наименование","Наименование","InputField"),("Клиент","Клиент","InputField"),
                ("ВидАбонемента","Вид абонемента","InputField"),("ДатаПокупки","Дата покупки","InputField"),
                ("ДатаНачалаДействия","Дата начала действия","InputField"),("ДатаОкончания","Дата окончания","InputField"),
                ("КоличествоЗанятий","Количество занятий","InputField"),("Использовано","Использовано","InputField"),
                ("Заморожено","Заморожено (дней)","InputField"),("Статус","Статус","ComboBox")]
    return [("Наименование","Наименование","InputField")]

CATALOGS = ["Клиенты","Преподаватели","Направления","Аудитории","Абонементы","СпособыОплаты","Пользователи","АбонементыКлиента","Инструменты"]

for c in CATALOGS:
    base = "Catalogs/%s" % c
    fields = cat_form_fields(c)
    # ObjectForm
    oname = "ObjectForm"
    write("%s/Forms/%s.xml" % (base, oname), form_meta_xml(oname, get("form."+c+".object")))
    mod = ""
    write("%s/Forms/%s/Ext/Form.xml" % (base, oname),
          obj_form_content("CatalogObject", c, c, fields, module=mod))
    # ListForm
    lname = "ListForm"
    write("%s/Forms/%s.xml" % (base, lname), form_meta_xml(lname, get("form."+c+".list")))
    write("%s/Forms/%s/Ext/Form.xml" % (base, lname), list_form_content("List", c, module=""))
    # ChoiceForm
    chname = "ChoiceForm"
    write("%s/Forms/%s.xml" % (base, chname), form_meta_xml(chname, get("form."+c+".choice")))
    write("%s/Forms/%s/Ext/Form.xml" % (base, chname), list_form_content("List", c, module=""))

print("catalog forms written:", len(CATALOGS))

# ============ DOCUMENT FORMS ============
def doc_form_fields(doc):
    D = {
     "Занятие": [("ДатаЗанятия","Дата","InputField"),("ВремяНачала","Время начала","InputField"),
                 ("ВремяОкончания","Время окончания","InputField"),("Преподаватель","Преподаватель","InputField"),
                 ("Аудитория","Аудитория","InputField"),("Направление","Направление","InputField"),
                 ("ТипЗанятия","Тип занятия","ComboBox"),("Статус","Статус","ComboBox"),
                 ("Комментарий","Комментарий","InputField")],
     "ЗаписьНаЗанятие": [("Клиент","Клиент","InputField"),("Занятие","Занятие","InputField"),
                 ("ДатаЗаписи","Дата записи","InputField"),("ИсточникЗаписи","Источник записи","InputField"),
                 ("Абонемент","Абонемент","InputField"),("Статус","Статус","ComboBox")],
     "ПродажаАбонемента": [("Клиент","Клиент","InputField"),("Абонемент","Абонемент","InputField"),
                 ("ДатаПродажи","Дата продажи","InputField"),("Стоимость","Стоимость","InputField"),
                 ("СпособОплаты","Способ оплаты","InputField"),("ДатаНачала","Дата начала","InputField"),
                 ("ДатаОкончания","Дата окончания","InputField")],
     "Оплата": [("Клиент","Клиент","InputField"),("ДатаОплаты","Дата","InputField"),
                 ("Сумма","Сумма","InputField"),("СпособОплаты","Способ оплаты","InputField"),
                 ("Назначение","Назначение","ComboBox"),("Абонемент","Абонемент","InputField"),
                 ("Комментарий","Комментарий","InputField")],
     "Посещение": [("Занятие","Занятие","InputField"),("Преподаватель","Преподаватель","InputField"),
                 ("ДатаПосещения","Дата","InputField"),("Комментарий","Комментарий","InputField")],
     "ОтменаЗанятия": [("Занятие","Занятие","InputField"),("Причина","Причина","ComboBox"),
                 ("ДатаОтмены","Дата отмены","InputField"),("СписыватьЗанятие","Списывать занятие","CheckBox"),
                 ("ВозвращатьЗанятие","Возвращать на баланс","CheckBox"),("ВозвращатьОплату","Возвращать оплату","CheckBox"),
                 ("Комментарий","Комментарий","InputField")],
     "ПереносЗанятия": [("ПервоначальноеЗанятие","Первоначальное занятие","InputField"),("НовоеЗанятие","Новое занятие","InputField"),
                 ("ПричинаПереноса","Причина переноса","InputField"),("ДатаПереноса","Дата переноса","InputField"),
                 ("Исполнитель","Исполнитель","InputField"),("НоваяДата","Новая дата","InputField"),
                 ("НовоеВремяНачала","Новое время начала","InputField"),("НовоеВремяОкончания","Новое время окончания","InputField")],
     "ЗаморозкаАбонемента": [("Клиент","Клиент","InputField"),("Абонемент","Абонемент","InputField"),
                 ("ДатаНачала","Дата начала","InputField"),("ДатаОкончания","Дата окончания","InputField"),
                 ("Причина","Причина","InputField")],
     "Возврат": [("Клиент","Клиент","InputField"),("Сумма","Сумма","InputField"),
                 ("СпособОплаты","Способ оплаты","InputField"),("Абонемент","Абонемент","InputField"),
                 ("Комментарий","Комментарий","InputField")],
     "АрендаИнструмента": [("Клиент","Клиент","InputField"),("Инструмент","Инструмент","InputField"),
                 ("ДатаНачала","Дата аренды","InputField"),("ВремяНачала","Время начала","InputField"),
                 ("ВремяОкончания","Время окончания","InputField"),("Стоимость","Стоимость","InputField"),
                 ("Статус","Статус","ComboBox"),("Комментарий","Комментарий","InputField")],
    }
    return D[doc]

def doc_tabular(doc):
    if doc == "Занятие":
        return ("Участники", [("Клиент","Клиент"),("Абонемент","Абонемент"),("СтатусПосещения","Статус посещения"),("Стоимость","Стоимость"),("Комментарий","Комментарий")])
    if doc == "Посещение":
        return ("Участники", [("Клиент","Клиент"),("СтатусПосещения","Статус посещения"),("СписатьЗанятие","Списать занятие"),("Комментарий","Комментарий")])
    return None

DOCS = ["Занятие","ЗаписьНаЗанятие","ПродажаАбонемента","Оплата","Посещение","ОтменаЗанятия","ПереносЗанятия","ЗаморозкаАбонемента","Возврат","АрендаИнструмента"]

for d in DOCS:
    base = "Documents/%s" % d
    fields = doc_form_fields(d)
    oname = "ObjectForm"
    write("%s/Forms/%s.xml" % (base, oname), form_meta_xml(oname, get("form."+d+".object")))
    write("%s/Forms/%s/Ext/Form.xml" % (base, oname),
          obj_form_content("DocumentObject", d, d, fields, tabular=doc_tabular(d), module=""))
    lname = "ListForm"
    write("%s/Forms/%s.xml" % (base, lname), form_meta_xml(lname, get("form."+d+".list")))
    write("%s/Forms/%s/Ext/Form.xml" % (base, lname), list_form_content("List", d, module=""))
    chname = "ChoiceForm"
    write("%s/Forms/%s.xml" % (base, chname), form_meta_xml(chname, get("form."+d+".choice")))
    write("%s/Forms/%s/Ext/Form.xml" % (base, chname), list_form_content("List", d, module=""))

print("document forms written:", len(DOCS))

# ============ DATA PROCESSOR FORMS ============
def dp_form_content(dp_name, attrs, module=""):
    buf = []
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<Form xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <autoTitle>true</autoTitle>')
    buf.append('  <autoTitleSet>true</autoTitleSet>')
    buf.append('  <type>Managed</type>')
    buf.append('  <Extensions/>')
    buf.append('  <Attributes>')
    buf.append('    <Attribute name="ОбработкаОбъект">')
    buf.append('      <Types><Type>cfg:DataProcessorObject.%s</Type></Types>' % dp_name)
    buf.append('      <MainAttribute>true</MainAttribute>')
    buf.append('      <SavedData>true</SavedData>')
    buf.append('    </Attribute>')
    buf.append('  </Attributes>')
    buf.append('  <ChildItems>')
    for path, ttl, ctl in attrs:
        buf.append('    <FormField name="%s" horizontalStretch="true"><DataPath>ОбработкаОбъект.%s</DataPath><Type>%s</Type><Title>%s</Title><TitleLocation>Top</TitleLocation></FormField>' % (path, path, ctl, ttl))
    buf.append('    <Button name="Выполнить" type="CommandBar">')
    buf.append('      <CommandName>Form.Command.Выполнить</CommandName>')
    buf.append('      <Type>Button</Type><Title>Выполнить</Title>')
    buf.append('    </Button>')
    buf.append('  </ChildItems>')
    buf.append('  <Commands>')
    buf.append('    <Command name="Выполнить"><Title>Выполнить</Title><Action>Выполнить</Action></Command>')
    buf.append('  </Commands>')
    buf.append('  <Parameters/>')
    buf.append('  <EventHandlers><EventHandler event="Выполнить" name="Выполнить"><Action>Выполнить</Action></EventHandler></EventHandlers>')
    buf.append('  <ExtendedAttributes/>')
    buf.append('  <FormAttributes/>')
    buf.append('  <CommandInterface/>')
    buf.append('  <FormDependencies/>')
    buf.append('  <FormExtensions>')
    buf.append('    <FormExtension><Module>%s</Module></FormExtension>' % base64.b64encode(module.encode("utf-8")).decode())
    buf.append('  </FormExtensions>')
    buf.append('</Form>')
    return "\n".join(buf)

def report_form_content(report_name, module=""):
    buf = []
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<Form xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <autoTitle>true</autoTitle>')
    buf.append('  <autoTitleSet>true</autoTitleSet>')
    buf.append('  <type>Managed</type>')
    buf.append('  <Extensions/>')
    buf.append('  <Attributes>')
    buf.append('    <Attribute name="Отчет">')
    buf.append('      <Types><Type>cfg:Report.%s</Type></Types>' % report_name)
    buf.append('      <MainAttribute>true</MainAttribute>')
    buf.append('      <SavedData>true</SavedData>')
    buf.append('    </Attribute>')
    buf.append('  </Attributes>')
    buf.append('  <ChildItems>')
    buf.append('    <FormField name="СхемаКомпоновкиДанных" horizontalStretch="true">')
    buf.append('      <DataPath>Отчет.СхемаКомпоновкиДанных</DataPath>')
    buf.append('      <Type>InputField</Type><Extension>Edit</Extension>')
    buf.append('      <Title>Настройки отчёта</Title><TitleLocation>Top</TitleLocation>')
    buf.append('    </FormField>')
    buf.append('  </ChildItems>')
    buf.append('  <Commands/>')
    buf.append('  <Parameters/>')
    buf.append('  <EventHandlers/>')
    buf.append('  <ExtendedAttributes/>')
    buf.append('  <FormAttributes/>')
    buf.append('  <CommandInterface/>')
    buf.append('  <FormDependencies/>')
    buf.append('  <FormExtensions>')
    buf.append('    <FormExtension><Module>%s</Module></FormExtension>' % base64.b64encode(module.encode("utf-8")).decode())
    buf.append('  </FormExtensions>')
    buf.append('</Form>')
    return "\n".join(buf)

DP_FORMS = {
    "ИмпортДанных": [("ВидОбъекта","Вид объекта","ComboBox"),("ФайлДанных","Файл данных","InputField"),("Статус","Статус","Label")],
    "РезервноеКопирование": [("КаталогХранения","Каталог хранения","InputField"),("ПутьКФайлу","Путь к файлу","InputField"),("Статус","Статус","Label")],
    "Уведомления": [("Сообщение","Сообщение","InputField"),("ПользователиПолучатели","Получатели","InputField"),("ОтправлятьВTelegram","Отправлять в Telegram","CheckBox")],
}
for dp, attrs in DP_FORMS.items():
    base = "DataProcessors/%s" % dp
    write("%s/Forms/Form.xml" % base, form_meta_xml("Form", get("form."+dp+".form")))
    write("%s/Forms/Form/Ext/Form.xml" % base, dp_form_content(dp, attrs, module=""))
print("data processor forms written:", len(DP_FORMS))

REPORTS = ["Абонементы","ЗагрузкаАудиторий","ЗагрузкаПреподавателей","Задолженность","Клиенты","Посещаемость","Продажи","Расписание"]
for r in REPORTS:
    base = "Reports/%s" % r
    write("%s/Forms/Form.xml" % base, form_meta_xml("Form", get("form."+r+".form")))
    write("%s/Forms/Form/Ext/Form.xml" % base, report_form_content(r, module=""))
    # settings form reference
    write("%s/Forms/Настройки.xml" % base, form_meta_xml("Настройки", get("form."+r+".settings")))
    write("%s/Forms/Настройки/Ext/Form.xml" % base, report_form_content(r, module=""))
print("report forms written:", len(REPORTS))

# ============ REGISTER FORMS (list/choice) ============
def register_list_form_content(reg_name, type_kind, module=""):
    buf = []
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<Form xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">')
    buf.append('  <autoTitle>true</autoTitle>')
    buf.append('  <autoTitleSet>true</autoTitleSet>')
    buf.append('  <type>Managed</type>')
    buf.append('  <Extensions/>')
    buf.append('  <Attributes>')
    buf.append('    <Attribute name="Список">')
    buf.append('      <Types><Type>cfg:%s.%s</Type></Types>' % (type_kind, reg_name))
    buf.append('      <MainAttribute>true</MainAttribute>')
    buf.append('      <SavedData>true</SavedData>')
    buf.append('    </Attribute>')
    buf.append('  </Attributes>')
    buf.append('  <ChildItems>')
    buf.append('    <FormTable name="Список" horizontalStretch="true">')
    buf.append('      <DataPath>Список</DataPath>')
    buf.append('      <Type>Table</Type>')
    buf.append('      <Title>Список</Title>')
    buf.append('    </FormTable>')
    buf.append('  </ChildItems>')
    buf.append('  <Commands/>')
    buf.append('  <Parameters/>')
    buf.append('  <EventHandlers/>')
    buf.append('  <ExtendedAttributes/>')
    buf.append('  <FormAttributes/>')
    buf.append('  <CommandInterface/>')
    buf.append('  <FormDependencies/>')
    buf.append('  <FormExtensions>')
    buf.append('    <FormExtension><Module>%s</Module></FormExtension>' % base64.b64encode(module.encode("utf-8")).decode())
    buf.append('  </FormExtensions>')
    buf.append('</Form>')
    return "\n".join(buf)

INFOREG_NAME = ["РасписаниеПреподавателей","ДоступностьАудиторий","НастройкиУведомлений","ИсторияИзменений"]
for rg in INFOREG_NAME:
    base = "InformationRegisters/%s" % rg
    write("%s/Forms/ListForm.xml" % base, form_meta_xml("ListForm", get("form.ir.list."+rg)))
    write("%s/Forms/ListForm/Ext/Form.xml" % base, register_list_form_content(rg, "RegisterList", module=""))
    write("%s/Forms/ChoiceForm.xml" % base, form_meta_xml("ChoiceForm", get("form.ir.choice."+rg)))
    write("%s/Forms/ChoiceForm/Ext/Form.xml" % base, register_list_form_content(rg, "RegisterList", module=""))
print("inforeg forms written:", len(INFOREG_NAME))

ACCREG_NAME = ["ОстаткиАбонементов","Посещения","Оплаты","ЗагрузкаПреподавателей","ЗагрузкаАудиторий","АрендыИнструментов"]
for rg in ACCREG_NAME:
    base = "AccumulationRegisters/%s" % rg
    write("%s/Forms/ListForm.xml" % base, form_meta_xml("ListForm", get("form.ar.list."+rg)))
    write("%s/Forms/ListForm/Ext/Form.xml" % base, register_list_form_content(rg, "RegisterList", module=""))
print("accreg forms written:", len(ACCREG_NAME))
save()