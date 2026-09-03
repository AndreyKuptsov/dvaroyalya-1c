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

OBJMOD = '''<?xml version="1.0" encoding="UTF-8"?>
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logfrm" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enct">
  <Properties>
    <Name>ObjectModule</Name>
    <Synonym/>
    <Comment/>
  </Properties>
</MetaDataObject>
'''

def objmod(name, code):
    write("Catalogs/%s/Ext/ObjectModule.bsl"%name, code)
    write("Catalogs/%s/Ext/ObjectModule.xml"%name, OBJMOD)

# Клиенты object module
objmod("Клиенты", '''// Модуль справочника Клиенты

Процедура ОбработкаУдаления(Отказ)
	// Аудит удаления/архивирования клиента
	АудитДействий.ЗарегистрироватьИзменение(ЭтотОбъект, "Архивирование клиента", "", Строка(СтатусКлиента));
КонецПроцедуры

Процедура ОбработкаЗаписиНового(Отказ)
	Если ПустоеЗначение(ДатаРегистрации) Тогда
		ДатаРегистрации = ТекущаяДата();
	КонецЕсли;
	Если ПустоеЗначение(СтатусКлиента) Тогда
		СтатусКлиента = Перечисления.СтатусыКлиентов.Потенциальный;
	КонецЕсли;
КонецПроцедуры
''')

# АбонементыКлиента object module
objmod("АбонементыКлиента", '''// Модуль справочника Абонементы клиента

// Вычисление остатка занятий: Количество - Использовано
Функция ОстатокЗанятий() Экспорт
	Возврат КоличествоЗанятий - Использовано;
КонецФункции

Процедура ОбработкаЗаписи(Отказ)
	// Автоматический контроль статуса по остатку
	Если Не ПустоеЗначение(ДатаОкончания) И ДатаОкончания < ТекущаяДата() Тогда
		Если Статус <> Перечисления.СтатусыАбонементаКлиента.Заморожен Тогда
			Статус = Перечисления.СтатусыАбонементаКлиента.Истёк;
		КонецЕсли;
	ИначеЕсли Использовано >= КоличествоЗанятий Тогда
		Статус = Перечисления.СтатусыАбонементаКлиента.Закончился;
	КонецЕсли;
КонецПроцедуры
''')

save()
print("catalog object modules added")