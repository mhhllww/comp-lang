# generate_ontology.py
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal, URIRef
import random

# -----------------------------
# НАСТРОЙКИ (ПОМЕНЯЙ IRI ПОД СЕБЯ)
# -----------------------------
BASE_IRI = "http://mhlw-it-company#"
OUT_FILE = "it_company_ontology.ttl"
random.seed(42)

g = Graph()
NS = Namespace(BASE_IRI)

g.bind("", NS)
g.bind("owl", OWL)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

# Онтология (метаданные)
onto = NS["Онтология"]
g.add((onto, RDF.type, OWL.Ontology))
g.add((onto, RDFS.label, Literal("Онтология IT-компании (сгенерирована Python)", lang="ru")))

# -----------------------------
# УТИЛИТЫ
# -----------------------------
def iri(name: str) -> URIRef:
    # делаем безопасный IRI-фрагмент (пробелы -> _, лишнее убираем)
    safe = name.strip().replace(" ", "_").replace("/", "_").replace("\\", "_")
    return NS[safe]

def add_class(name: str, parent: str | None = None):
    c = iri(name)
    g.add((c, RDF.type, OWL.Class))
    g.add((c, RDFS.label, Literal(name, lang="ru")))
    if parent:
        g.add((c, RDFS.subClassOf, iri(parent)))
    return c

def add_obj_prop(name: str, domain: str | None = None, range_: str | None = None):
    p = iri(name)
    g.add((p, RDF.type, OWL.ObjectProperty))
    g.add((p, RDFS.label, Literal(name, lang="ru")))
    if domain:
        g.add((p, RDFS.domain, iri(domain)))
    if range_:
        g.add((p, RDFS.range, iri(range_)))
    return p

def add_data_prop(name: str, domain: str | None = None, range_xsd: URIRef | None = None):
    p = iri(name)
    g.add((p, RDF.type, OWL.DatatypeProperty))
    g.add((p, RDFS.label, Literal(name, lang="ru")))
    if domain:
        g.add((p, RDFS.domain, iri(domain)))
    if range_xsd:
        g.add((p, RDFS.range, range_xsd))
    return p

def add_individual(name: str, class_name: str):
    i = iri(name)
    g.add((i, RDF.type, iri(class_name)))
    g.add((i, RDFS.label, Literal(name, lang="ru")))
    return i

# -----------------------------
# 1) КЛАССЫ (55+), минимум 3 корневых
# -----------------------------
root_classes = [
    "Персона", "Организация", "Артефакт", "Процесс", "Технология"
]
for rc in root_classes:
    add_class(rc)  # корневые: под owl:Thing не указываем явно, это норм

# Иерархии
# Персона
add_class("Сотрудник", "Персона")
add_class("Разработчик", "Сотрудник")
add_class("ФронтендРазработчик", "Разработчик")
add_class("БэкендРазработчик", "Разработчик")
add_class("МобильныйРазработчик", "Разработчик")
add_class("DevOpsИнженер", "Сотрудник")
add_class("Тестировщик", "Сотрудник")
add_class("QAИнженер", "Тестировщик")
add_class("Автотестировщик", "Тестировщик")
add_class("Аналитик", "Сотрудник")
add_class("СистемныйАналитик", "Аналитик")
add_class("БизнесАналитик", "Аналитик")
add_class("Дизайнер", "Сотрудник")
add_class("UXДизайнер", "Дизайнер")
add_class("UIДизайнер", "Дизайнер")
add_class("Менеджер", "Сотрудник")
add_class("ПроектныйМенеджер", "Менеджер")
add_class("ПродуктовыйМенеджер", "Менеджер")
add_class("Тимлид", "Сотрудник")
add_class("Архитектор", "Сотрудник")
add_class("Клиент", "Персона")

# Организация
add_class("ITКомпания", "Организация")
add_class("Команда", "Организация")
add_class("Отдел", "Организация")
add_class("Проект", "Организация")
add_class("ПодразделениеРазработки", "Отдел")
add_class("ПодразделениеТестирования", "Отдел")
add_class("ПодразделениеDevOps", "Отдел")
add_class("ПодразделениеДизайна", "Отдел")
add_class("ПодразделениеАналитики", "Отдел")

# Артефакт
add_class("Продукт", "Артефакт")
add_class("Приложение", "Продукт")
add_class("ВебПриложение", "Приложение")
add_class("МобильноеПриложение", "Приложение")
add_class("Сервис", "Продукт")

add_class("Требование", "Артефакт")
add_class("UserStory", "Требование")
add_class("UseCase", "Требование")
add_class("ТехническоеЗадание", "Требование")

add_class("Задача", "Артефакт")
add_class("Баг", "Задача")
add_class("Фича", "Задача")
add_class("ТехническийДолг", "Задача")

add_class("Код", "Артефакт")
add_class("Репозиторий", "Артефакт")
add_class("Коммит", "Артефакт")
add_class("ПуллРеквест", "Артефакт")
add_class("Документация", "Артефакт")

add_class("Тест", "Артефакт")
add_class("ЮнитТест", "Тест")
add_class("ИнтеграционныйТест", "Тест")
add_class("E2EТест", "Тест")

add_class("Сборка", "Артефакт")
add_class("Релиз", "Артефакт")
add_class("АртефактСборки", "Артефакт")

# Процесс
add_class("Методология", "Процесс")
add_class("Scrum", "Методология")
add_class("Kanban", "Методология")

add_class("Спринт", "Процесс")
add_class("Митинг", "Процесс")
add_class("Планирование", "Митинг")
add_class("Дейли", "Митинг")
add_class("Ретро", "Митинг")
add_class("Демо", "Митинг")

add_class("CI_CD", "Процесс")
add_class("Деплой", "Процесс")
add_class("РевьюКода", "Процесс")

# Технология
add_class("ЯзыкПрограммирования", "Технология")
add_class("Python", "ЯзыкПрограммирования")
add_class("Java", "ЯзыкПрограммирования")
add_class("JavaScript", "ЯзыкПрограммирования")
add_class("TypeScript", "ЯзыкПрограммирования")
add_class("Kotlin", "ЯзыкПрограммирования")

add_class("Фреймворк", "Технология")
add_class("Django", "Фреймворк")
add_class("Spring", "Фреймворк")
add_class("React", "Фреймворк")
add_class("FastAPI", "Фреймворк")

add_class("БазаДанных", "Технология")
add_class("PostgreSQL", "БазаДанных")
add_class("MongoDB", "БазаДанных")
add_class("Redis", "БазаДанных")

add_class("Инструмент", "Технология")
add_class("Git", "Инструмент")
add_class("Docker", "Инструмент")
add_class("Kubernetes", "Инструмент")
add_class("Jira", "Инструмент")

# -----------------------------
# 2) СВОЙСТВА (Object + Data)
# -----------------------------
# Object properties
p_работаетВ = add_obj_prop("работаетВ", "Сотрудник", "ITКомпания")
p_состоитВ = add_obj_prop("состоитВ", "Сотрудник", "Команда")
p_входитВОтдел = add_obj_prop("входитВОтдел", "Сотрудник", "Отдел")
p_участвуетВ = add_obj_prop("участвуетВ", "Сотрудник", "Проект")
p_ведетПроект = add_obj_prop("ведетПроект", "Менеджер", "Проект")
p_разрабатывает = add_obj_prop("разрабатывает", "Разработчик", "Продукт")
p_тестирует = add_obj_prop("тестирует", "Тестировщик", "Продукт")
p_пишетКод = add_obj_prop("пишетКод", "Разработчик", "Код")
p_делаетКоммит = add_obj_prop("делаетКоммит", "Сотрудник", "Коммит")
p_создаетPR = add_obj_prop("создаетПуллРеквест", "Сотрудник", "ПуллРеквест")
p_PRв = add_obj_prop("пуллРеквестВ", "ПуллРеквест", "Репозиторий")
p_репоДля = add_obj_prop("репозиторийДля", "Репозиторий", "Продукт")
p_задачаВПроекте = add_obj_prop("задачаВПроекте", "Задача", "Проект")
p_назначенаНа = add_obj_prop("назначенаНа", "Задача", "Сотрудник")
p_требованиеДля = add_obj_prop("требованиеДля", "Требование", "Продукт")
p_реализует = add_obj_prop("реализует", "Задача", "Требование")
p_содержитЗадачу = add_obj_prop("содержитЗадачу", "Спринт", "Задача")
p_релизДля = add_obj_prop("релизДля", "Релиз", "Продукт")
p_используетТех = add_obj_prop("используетТехнологию", "Продукт", "Технология")
p_связанС = add_obj_prop("связанС", None, None)  # универсальная связь

# Data properties
d_имя = add_data_prop("имя", None, XSD.string)
d_email = add_data_prop("email", "Персона", XSD.string)
d_id = add_data_prop("идентификатор", None, XSD.string)
d_роль = add_data_prop("роль", "Сотрудник", XSD.string)
d_приоритет = add_data_prop("приоритет", "Задача", XSD.string)
d_статус = add_data_prop("статус", "Задача", XSD.string)
d_сложность = add_data_prop("сложностьSP", "Задача", XSD.integer)
d_версия = add_data_prop("версия", "Релиз", XSD.string)

# -----------------------------
# 3) ИНДИВИДЫ (120+), у каждого хотя бы 1 слот
# -----------------------------
# Компания + отделы + команды
company = add_individual("Компания_АльфаСофт", "ITКомпания")
g.add((company, d_имя, Literal("АльфаСофт", lang="ru")))
g.add((company, d_id, Literal("COMP-001")))

departments = []
dept_names = [
    ("Отдел_Разработки", "ПодразделениеРазработки"),
    ("Отдел_QA", "ПодразделениеТестирования"),
    ("Отдел_DevOps", "ПодразделениеDevOps"),
    ("Отдел_Дизайна", "ПодразделениеДизайна"),
    ("Отдел_Аналитики", "ПодразделениеАналитики"),
]
for idx, (n, cls) in enumerate(dept_names, 1):
    d = add_individual(n, cls)
    g.add((d, d_id, Literal(f"DEPT-{idx:02d}")))
    departments.append(d)
    g.add((d, p_связанС, company))

teams = []
for i in range(1, 11):  # 10 команд
    t = add_individual(f"Команда_{i}", "Команда")
    g.add((t, d_id, Literal(f"TEAM-{i:02d}")))
    teams.append(t)
    g.add((t, p_связанС, company))

# Проекты (10)
projects = []
for i in range(1, 11):
    pr = add_individual(f"Проект_{i}", "Проект")
    g.add((pr, d_имя, Literal(f"Проект {i}", lang="ru")))
    g.add((pr, d_id, Literal(f"PRJ-{i:03d}")))
    projects.append(pr)
    g.add((pr, p_связанС, company))

# Продукты (12)
product_classes = ["ВебПриложение", "МобильноеПриложение", "Сервис"]
products = []
for i in range(1, 13):
    cls = random.choice(product_classes)
    prod = add_individual(f"Продукт_{i}", cls)
    g.add((prod, d_имя, Literal(f"Продукт {i}", lang="ru")))
    g.add((prod, d_id, Literal(f"PROD-{i:03d}")))
    products.append(prod)
    g.add((prod, p_связанС, random.choice(projects)))

# Технологии (индивиды технологий можно тоже создать)
tech_individuals = [
    ("Тех_Python", "Python"),
    ("Тех_Java", "Java"),
    ("Тех_JavaScript", "JavaScript"),
    ("Тех_TypeScript", "TypeScript"),
    ("Тех_Kotlin", "Kotlin"),
    ("Тех_Django", "Django"),
    ("Тех_FastAPI", "FastAPI"),
    ("Тех_Spring", "Spring"),
    ("Тех_React", "React"),
    ("Тех_PostgreSQL", "PostgreSQL"),
    ("Тех_MongoDB", "MongoDB"),
    ("Тех_Redis", "Redis"),
    ("Тех_Git", "Git"),
    ("Тех_Docker", "Docker"),
    ("Тех_Kubernetes", "Kubernetes"),
    ("Тех_Jira", "Jira"),
]
techs = []
for i, (n, cls) in enumerate(tech_individuals, 1):
    te = add_individual(n, cls)
    g.add((te, d_id, Literal(f"TECH-{i:03d}")))
    techs.append(te)

# Привяжем продукты к технологиям
for prod in products:
    for _ in range(3):
        g.add((prod, p_используетТех, random.choice(techs)))

# Сотрудники (60): разработчики, QA, DevOps, аналитики, дизайнеры, менеджеры
roles = [
    ("ФронтендРазработчик", "Frontend"),
    ("БэкендРазработчик", "Backend"),
    ("МобильныйРазработчик", "Mobile"),
    ("DevOpsИнженер", "DevOps"),
    ("QAИнженер", "QA"),
    ("Автотестировщик", "QA-Auto"),
    ("СистемныйАналитик", "SA"),
    ("БизнесАналитик", "BA"),
    ("UXДизайнер", "UX"),
    ("UIДизайнер", "UI"),
    ("ПроектныйМенеджер", "PM"),
    ("ПродуктовыйМенеджер", "PO"),
    ("Тимлид", "Lead"),
    ("Архитектор", "Arch"),
]
employees = []
for i in range(1, 61):
    cls, role = random.choice(roles)
    emp = add_individual(f"Сотрудник_{i}", cls)
    g.add((emp, d_имя, Literal(f"Сотрудник {i}", lang="ru")))
    g.add((emp, d_email, Literal(f"employee{i}@alfasoft.example")))
    g.add((emp, d_id, Literal(f"EMP-{i:04d}")))
    g.add((emp, d_роль, Literal(role)))
    employees.append(emp)

    # связи сотрудника
    g.add((emp, p_работаетВ, company))
    g.add((emp, p_состоитВ, random.choice(teams)))
    g.add((emp, p_входитВОтдел, random.choice(departments)))
    g.add((emp, p_участвуетВ, random.choice(projects)))

# Менеджеры ведут проекты
managers = [e for e in employees if (e, RDF.type, iri("ПроектныйМенеджер")) in g or (e, RDF.type, iri("ПродуктовыйМенеджер")) in g]
if not managers:
    managers = employees[:5]
for pr in projects:
    g.add((random.choice(managers), p_ведетПроект, pr))

# Репозитории (20)
repos = []
for i in range(1, 21):
    r = add_individual(f"Репозиторий_{i}", "Репозиторий")
    g.add((r, d_id, Literal(f"REPO-{i:03d}")))
    repos.append(r)
    g.add((r, p_репоДля, random.choice(products)))

# Коммиты (30) + PR (20) + код (30)
commits = []
for i in range(1, 31):
    c = add_individual(f"Коммит_{i}", "Коммит")
    g.add((c, d_id, Literal(f"CMT-{i:04d}")))
    commits.append(c)
    author = random.choice(employees)
    g.add((author, p_делаетКоммит, c))
    g.add((c, p_связанС, random.choice(repos)))

prs = []
for i in range(1, 21):
    pr = add_individual(f"ПуллРеквест_{i}", "ПуллРеквест")
    g.add((pr, d_id, Literal(f"PR-{i:04d}")))
    prs.append(pr)
    author = random.choice(employees)
    g.add((author, p_создаетPR, pr))
    g.add((pr, p_PRв, random.choice(repos)))

codes = []
for i in range(1, 31):
    cd = add_individual(f"КодовыйМодуль_{i}", "Код")
    g.add((cd, d_id, Literal(f"CODE-{i:03d}")))
    codes.append(cd)
    dev = random.choice(employees)
    g.add((dev, p_пишетКод, cd))
    g.add((cd, p_связанС, random.choice(repos)))

# Требования (20)
req_classes = ["UserStory", "UseCase", "ТехническоеЗадание"]
requirements = []
for i in range(1, 21):
    cls = random.choice(req_classes)
    rq = add_individual(f"Требование_{i}", cls)
    g.add((rq, d_id, Literal(f"REQ-{i:04d}")))
    requirements.append(rq)
    g.add((rq, p_требованиеДля, random.choice(products)))

# Задачи (40) + баги/фичи/долг
task_classes = ["Баг", "Фича", "ТехническийДолг"]
priorities = ["низкий", "средний", "высокий", "критический"]
statuses = ["создана", "в работе", "на ревью", "тестируется", "готово"]

tasks = []
for i in range(1, 41):
    cls = random.choice(task_classes)
    t = add_individual(f"Задача_{i}", cls)
    g.add((t, d_id, Literal(f"TASK-{i:04d}")))
    g.add((t, d_приоритет, Literal(random.choice(priorities), lang="ru")))
    g.add((t, d_статус, Literal(random.choice(statuses), lang="ru")))
    g.add((t, d_сложность, Literal(random.randint(1, 13), datatype=XSD.integer)))
    tasks.append(t)

    g.add((t, p_задачаВПроекте, random.choice(projects)))
    g.add((t, p_назначенаНа, random.choice(employees)))
    g.add((t, p_реализует, random.choice(requirements)))

# Спринты (10) и распределение задач
sprints = []
for i in range(1, 11):
    sp = add_individual(f"Спринт_{i}", "Спринт")
    g.add((sp, d_id, Literal(f"SPR-{i:03d}")))
    sprints.append(sp)
    for t in random.sample(tasks, k=4):
        g.add((sp, p_содержитЗадачу, t))

# Релизы (10)
releases = []
for i in range(1, 11):
    rl = add_individual(f"Релиз_{i}", "Релиз")
    g.add((rl, d_id, Literal(f"REL-{i:03d}")))
    g.add((rl, d_версия, Literal(f"1.{i}.0")))
    releases.append(rl)
    g.add((rl, p_релизДля, random.choice(products)))

# Клиенты (10)
clients = []
for i in range(1, 11):
    cl = add_individual(f"Клиент_{i}", "Клиент")
    g.add((cl, d_имя, Literal(f"Клиент {i}", lang="ru")))
    g.add((cl, d_id, Literal(f"CL-{i:03d}")))
    clients.append(cl)
    g.add((cl, p_связанС, random.choice(products)))

# -----------------------------
# СОХРАНЕНИЕ
# -----------------------------
g.serialize(destination=OUT_FILE, format="turtle")
print(f"Готово! Сгенерирован файл: {OUT_FILE}")
print(f"Base IRI: {BASE_IRI}")
print("Импортируй файл в Protégé / WebProtégé (Create project -> Import ontology).")
