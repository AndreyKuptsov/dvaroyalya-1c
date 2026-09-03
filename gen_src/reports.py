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

REPORTS = {
 "Расписание": dict(syn="Расписание",
   query="""ВЫБРАТЬ
	Занятия.ДатаЗанятия КАК Дата,
	Занятия.ВремяНачала КАК ВремяНачала,
	Занятия.ВремяОкончания КАК ВремяОкончания,
	Занятия.Преподаватель КАК Преподаватель,
	Занятия.Аудитория КАК Аудитория,
	Занятия.Направление КАК Направление,
	Занятия.Статус КАК Статус,
	Занятия.ТипЗанятия КАК ТипЗанятия
ИЗ
	Документ.Занятие КАК Занятия
ГДЕ
	Занятия.ДатаЗанятия МЕЖДУ &НачалоПериода И &КонецПериода""",
   fields=["Дата","ВремяНачала","ВремяОкончания","Преподаватель","Аудитория","Направление","Статус","ТипЗанятия"],
   grouppath=["Преподаватель"],
   params=[("НачалоПериода","Дата","ДатаНачала"),("КонецПериода","Дата","ДатаОкончания")]),
 "Посещаемость": dict(syn="Посещаемость",
   query="""ВЫБРАТЬ
	Посещения.Клиент КАК Клиент,
	СУММА(Посещения.Присутствовал) КАК Присутствовал,
	СУММА(Посещения.Отсутствовал) КАК Отсутствовал,
	СУММА(Посещения.Списано) КАК Списано
ИЗ
	РегистрНакопления.Посещения КАК Посещения
ГДЕ
	Посещения.Период МЕЖДУ &НачалоПериода И &КонецПериода
СГРУППИРОВАТЬ ПО
	Посещения.Клиент""",
   fields=["Клиент","Присутствовал","Отсутствовал","Списано"],
   grouppath=["Клиент"],
   params=[("НачалоПериода","Дата","ДатаНачала"),("КонецПериода","Дата","ДатаОкончания")]),
 "ЗагрузкаПреподавателей": dict(syn="Загрузка преподавателей",
   query="""ВЫБРАТЬ
	Загрузка.Преподаватель КАК Преподаватель,
	СУММА(Загрузка.Часы) КАК Часы
ИЗ
	РегистрНакопления.ЗагрузкаПреподавателей КАК Загрузка
ГДЕ
	Загрузка.Период МЕЖДУ &НачалоПериода И &КонецПериода
СГРУППИРОВАТЬ ПО
	Загрузка.Преподаватель""",
   fields=["Преподаватель","Часы"],
   grouppath=["Преподаватель"],
   params=[("НачалоПериода","Дата","ДатаНачала"),("КонецПериода","Дата","ДатаОкончания")]),
 "ЗагрузкаАудиторий": dict(syn="Загрузка аудиторий",
   query="""ВЫБРАТЬ
	Загрузка.Аудитория КАК Аудитория,
	СУММА(Загрузка.Часы) КАК Часы
ИЗ
	РегистрНакопления.ЗагрузкаАудиторий КАК Загрузка
ГДЕ
	Загрузка.Период МЕЖДУ &НачалоПериода И &КонецПериода
СГРУППИРОВАТЬ ПО
	Загрузка.Аудитория""",
   fields=["Аудитория","Часы"],
   grouppath=["Аудитория"],
   params=[("НачалоПериода","Дата","ДатаНачала"),("КонецПериода","Дата","ДатаОкончания")]),
 "Продажи": dict(syn="Продажи",
   query="""ВЫБРАТЬ
	Оплаты.Клиент КАК Клиент,
	Оплаты.Назначение КАК Назначение,
	СУММА(Оплаты.Сумма) КАК Выручка,
	СУММА(Оплаты.КоличествоОплат) КАК КоличествоОплат
ИЗ
	РегистрНакопления.Оплаты КАК Оплаты
ГДЕ
	Оплаты.Период МЕЖДУ &НачалоПериода И &КонецПериода
	И Оплаты.Назначение <> ЗНАЧЕНИЕ(Перечисление.ВидыОперацийОплат.Возврат)
СГРУППИРОВАТЬ ПО
	Оплаты.Клиент,
	Оплаты.Назначение""",
   fields=["Клиент","Назначение","Выручка","КоличествоОплат"],
   grouppath=["Клиент"],
   params=[("НачалоПериода","Дата","ДатаНачала"),("КонецПериода","Дата","ДатаОкончания")]),
 "Клиенты": dict(syn="Клиенты",
   query="""ВЫБРАТЬ
	Клиенты.Ссылка КАК Клиент,
	Клиенты.ДатаРегистрации КАК ДатаРегистрации,
	Клиенты.СтатусКлиента КАК Статус
ИЗ
	Справочник.Клиенты КАК Клиенты
ГДЕ
	НЕ Клиенты.ПометкаУдаления""",
   fields=["Клиент","ДатаРегистрации","Статус"],
   grouppath=["Статус"],
   params=[]),
 "Абонементы": dict(syn="Абонементы",
   query="""ВЫБРАТЬ
	АбонементыКлиента.ВидАбонемента КАК ВидАбонемента,
	АбонементыКлиента.Статус КАК Статус,
	СУММА(АбонементыКлиента.КоличествоЗанятий - АбонементыКлиента.Использовано) КАК Остаток
ИЗ
	Справочник.АбонементыКлиента КАК АбонементыКлиента
ГДЕ
	НЕ АбонементыКлиента.ПометкаУдаления
СГРУППИРОВАТЬ ПО
	АбонементыКлиента.ВидАбонемента,
	АбонементыКлиента.Статус""",
   fields=["ВидАбонемента","Статус","Остаток"],
   grouppath=["Статус"],
   params=[]),
 "Задолженность": dict(syn="Задолженность",
   query="""ВЫБРАТЬ
	Оплаты.Клиент КАК Клиент,
	СУММА(ВЫБОР КОГДА Оплаты.Назначение = ЗНАЧЕНИЕ(Перечисление.ВидыОперацийОплат.Возврат)
		ТОГДА -Оплаты.Сумма ИНАЧЕ Оплаты.Сумма КОНЕЦ) КАК Оплачено
ИЗ
	РегистрНакопления.Оплаты КАК Оплаты
СГРУППИРОВАТЬ ПО
	Оплаты.Клиент
ИМЕЮЩИЕ
	СУММА(ВЫБОР КОГДА Оплаты.Назначение = ЗНАЧЕНИЕ(Перечисление.ВидыОперацийОплат.Возврат)
		ТОГДА -Оплаты.Сумма ИНАЧЕ Оплаты.Сумма КОНЕЦ) < 0""",
   fields=["Клиент","Оплачено"],
   grouppath=["Клиент"],
   params=[]),
}

def report_xml(name, md):
    rid = get("report."+name)
    buf=[HEADER]
    buf.append('  <Properties>')
    buf.append('    <Name>%s</Name>'%name)
    buf.append('    <Synonym>%s</Synonym>'%md["syn"])
    buf.append('    <Comment/>')
    buf.append('    <UUID>%s</UUID>'%rid)
    buf.append('    <DefaultForm>Report.%s.Form</DefaultForm>'%name)
    buf.append('    <StandardSettingsForm>Report.%s.Настройки</StandardSettingsForm>'%name)
    buf.append('    <ExtendedConfigurationDataCompositionSchema>')
    buf.append('      <DataCompositionSchema>%s</DataCompositionSchema>'%get("report.dcs."+name))
    buf.append('    </ExtendedConfigurationDataCompositionSchema>')
    buf.append('  </Properties>')
    buf.append('</MetaDataObject>')
    return "\n".join(buf)

for n,md in REPORTS.items():
    write("Reports/"+n+".xml", report_xml(n,md))

# DataCompositionSchema files
import html
def dcs_xml(name, md):
    did = get("report.dcs."+name)
    from html import escape as he
    fields = md["fields"]
    buf=[]
    buf.append('<?xml version="1.0" encoding="UTF-8"?>')
    buf.append('<DataCompositionSchema xmlns="http://v8.1c.ru/8.3/sk" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" xmlns:dcscom="http://v8.1c.ru/8.1/data-composition-system/composition" xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" xmlns:dcsse="http://v8.1c.ru/8.1/data-composition-system/settings-options" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
    buf.append('  <dataSource>')
    buf.append('    <DataSource>')
    buf.append('      <Name>DataSet</Name>')
    buf.append('      <Query>'+he(md["query"], quote=False)+'</Query>')
    buf.append('      <Field>')
    for fpath in fields:
        buf.append('        <Field><FieldPath>'+he(fpath)+'</FieldPath><Title>'+he(fpath)+'</Title></Field>')
    buf.append('      </Field>')
    buf.append('    </DataSource>')
    if md["params"]:
        buf.append('    <Parameters>')
        for pname,ptype,pdefault in md["params"]:
            buf.append('      <Parameter>')
            buf.append('        <Name>%s</Name>'%pname)
            buf.append('        <Title>%s</Title>'%pdefault)
            buf.append('        <ValueType><v8:Type>xs:%s</v8:Type></ValueType>'%("dateTime" if ptype=="Дата" else ptype))
            buf.append('      </Parameter>')
        buf.append('    </Parameters>')
    buf.append('  </dataSource>')
    buf.append('  <dataCompositionSchema>')
    buf.append('    <dataCompositionSchemas>')
    buf.append('      <dataCompositionSchema>')
    buf.append('        <Name>ОсновнаяСхема</Name>')
    buf.append('        <dataSet>')
    buf.append('          <dataSet>')
    buf.append('            <Name>DataSet</Name>')
    buf.append('            <Fields>')
    for fpath in md["grouppath"]:
        buf.append('              <Field><FieldPath>%s</FieldPath></Field>'%he(fpath))
    buf.append('            </Fields>')
    buf.append('          </dataSet>')
    buf.append('        </dataSet>')
    buf.append('        <dataParameters>')
    if md["params"]:
        for pname,ptype,pdefault in md["params"]:
            buf.append('          <dataParameter><Name>%s</Name><Title>%s</Title><Value xsi:type="xs:string">%s</Value></dataParameter>'%(he(pname),he(pdefault),he("%s, %s"%(pdefault,pdefault))))
    buf.append('        </dataParameters>')
    buf.append('        <template/>')
    buf.append('        <structure><structure xsi:type="structureStructure">')
    for gpath in md["grouppath"]:
        buf.append('          <group xsi:type="structureGroup"><Name>%s</Name><Fields><Field><FieldPath>%s</FieldPath></Field></Fields><structure><structure xsi:type="structureStructure"><group xsi:type="structureGroup"><Name>ДетальныеЗаписи</Name></group></structure></structure></group>'%(he(gpath),he(gpath)))
    buf.append('          <group xsi:type="structureGroup"><Name>ДетальныеЗаписи</Name></group>')
    buf.append('        </structure>')
    buf.append('        </structure>')
    buf.append('        <settings>')
    buf.append('          <settings xsi:type="settingsSettings">')
    buf.append('            <selectionItems/>')
    buf.append('            <parametersValues><parametersValues><parametersValue><parameter>НачалоПериода</parameter><value xsi:type="xs:string">НачалоПериода</value></parametersValue></parametersValues></parametersValues>')
    buf.append('          </settings>')
    buf.append('        </settings>')
    buf.append('        <options/>')
    buf.append('      </dataCompositionSchema>')
    buf.append('    </dataCompositionSchemas>')
    buf.append('    <dataCompositionOptions><dataCompositionOptions><item><item><Name>ПараметрыДанных</Name></item><Value xsi:type="xs:string">Доступны</Value></item><item><item><Name>ОбычноеПредставление</Name></item><Value xsi:type="xs:string">Авто</Value></item></dataCompositionOptions></dataCompositionOptions>')
    buf.append('    <dataCompositionTemplates/>')
    buf.append('  </dataCompositionSchema>')
    buf.append('</DataCompositionSchema>')
    return "\n".join(buf)

for n,md in REPORTS.items():
    write("Reports/"+n+"/Ext/DataCompositionSchema.xml", dcs_xml(n,md))

save()
print("reports:", len(REPORTS))