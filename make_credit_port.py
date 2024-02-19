import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta, date

start_time=datetime.now().strftime("%H:%M:%S")
fake = Faker('ru_RU')

### настройки кредитного портфеля
# путь к файлу сохранения реестра
filepath=r'c:\test777.xlsx'
# количество строк в реестре
reestr_raws_count=1000
# вероятность что есть созаемщик
FIO_SOZAEMSCHIKA_probability=0.1
# вероятность наличия просроченной задолженности по кредиту
ZADOLGEN_PROSROCHEN_POKURSU_probability=0.05
# дата на которую составляем реестр
date_of_reestr=datetime.strptime('01.12.2023', '%d.%m.%Y')
# дата с которой началась выдача кредитов
date_start_credit=date(2015,1,1)
# вероятность того, что ссуда в ПОС
POS_list_probability=0.9
# перечень ПОСов
POS_list_choice=[
    'Портфель прочих ипотечных ссуд',
    'Портфель ссуд заемщиков, имеющих счета в банке-кредиторе',
    'Портфель автокредитов',
    'Портфель иных потребительских ссуд'
]
# названия столбцов в соответствии с требованиями Банка России https://cbr.ru/Content/Document/File/156779/rktfl_01_03_2023.pdf
reestr_columns_list = [
    "DATE1", "ID_ZAEMSCHIKA", "SURNAME", "NAME", "MIDDLE_NAME", "INN", "REZIDENT", "POL", "DATA_ROG",
    "ADRES_REG", "ADRES", "DOCUMENT", "NOMER_DOCUMENTA", "KEM_VIDAN_DOCUMENT", "DATA_VIDACHI_DOCUMENTA",
    "SEMEINOE_POL", "KOL_IGDIVENCEV", "TIP_ZANYATOSTI", "BANK_CLEARK", "ZARPLATNIE_SCHETA", "DOLGENOST",
    "MESTO_RAB", "INN_RAB", "DOXOD_NA_DATU_VIDACHI", "DOXOD", "PDN_DATA_VIDACHI", "DOXOD_PDN_DATA_VIDACHI",
    "RASXOD_PDN_DATA_VIDACHI", "PDN_RESTRUKT_IZMENENIYA", "DOXOD_PDN_RESTRUKT_IZMENENIYA",
    "RASXOD_PDN_RESTRUKT_IZMENENIYA", "LAST_DATE_PDN", "ISTOCHNIK_DOXODA", "RASXOD_NA_DATU_VIDACHI", "RASXOD",
    "PLATEGSPOSB", "MAX_KREDIT", "SCORING_OCENKA", "FIO_SOZAEMSCHIKA", "FIN_POLOGENIE", "FIN_POLOGENIE_VIDACHA",
    "UID", "ID_DOGOVORA", "NOMER_DOGOVORA", "DATA_DOGOVORA", "DATA_VIDACHI", "DATA_KONCA_DOGOVORA",
    "DATA_ZAKR_DOGOVORA", "DATA_FACT_ZAKR_DOGOVORA", "SUMMA_KREDITA", "VALUT_KREDITA", "VID_KREDITA",
    "VID_KREDITA_115", "PROGRAMMA_KREDITA", "REGIM_KREDITA", "KATEGORY_KREDITA_PSK", "CEL_KREDITA",
    "USLOVIYA_IZMENENIY", "POLNAI_STOIMOST_KREDITA", "PROCENT_STAVKA_NA_DATU_VIDACHI", "PROCENT_STAVKA",
    "SUMMA_KREDIT_TREBOVAN", "VALUT_KREDIT_TREBOVAN", "SUMMA_KREDIT_TREBOVAN_POKURSU_ALL",
    "ZADOLGEN_PROSROCHEN_POKURSU", "NACH_PROCENT", "PROSROCHEN_PROCENT", "NEISPOLZOVAN_LIMIT",
    "VIKYPLEN_SUMMA_TREBOVAN_ALL", "VIKYPLEN_SUMMA_TREBOVAN_PROSROCH", "KOMISSII", "SUMMA_PENALTIES",
    "NOMINAL_VIKYPLEN_TREBOVAN", "DISCONT", "POS", "KATEGOR_KACHESTV", "PROCENT_REZERV", "KATEGOR_KACHESTV_PROCENT",
    "PROCENT_REZERV_PROCENT", "KATEGOR_KACHESTV_LIMIT", "PROCENT_REZERV_LIMIT", "LINE_STATUS", "BIOMETRIYA",
    "SSYD_SCHET", "SCHET_PROSROCHEN_ZADOLGEN", "SCHET_NACHISLEN_PROCENTOV", "SCHET_PROSROCHEN_PROCENTOV",
    "TEKUSCH_SCHET", "SCHET_PO_VIKYPLEN_SSYDAM", "SCHET_PROSROCH_VIKYPLEN_TREBOVAN", "SCHET_PENALTIES",
    "SCHET_KOMISSII", "KOL_VO_RESTRUKT", "IZMENENIE_DOGOVORA", "LAST_DATE_RESTRUKT", "PRIZNAK_NAPRAVLENIE_SSYD",
    "RESHENIYA_UO", "DATA_RESHENIYA_UO", "NEGATIV", "TIP_OPERACII", "DATA_OPERACII", "SUMMA_OPERACII",
    "REGIM_YPLAT_PROCENT", "REGIM_YPLAT_OSNOV", "DATA_YPLAT_PROCENT", "DATA_YPLAT_OSNOV", "DLINA_PROSROCHEN_PLATEG",
    "METOD_RASCHETA_PROSR", "OVERDUE_INTERVAL", "TIP_PLATEGA", "RAZMER_PLATEGA", "DATA_POSL_POGASH_PROC",
    "DATA_POSL_POGASH_SSUD", "LGOT_PERIOD_START", "LGOT_PERIOD_FINISH", "DLINA_PROSROCHEN_PLATEG_ZA_180_DNEY",
    "KACHESTVO_DOLGA", "SUMMA_REZERVA_PO_SROCH", "REZERV_PO_PROSROCH", "REZERV_NACHISLEN_PROCENT",
    "REZERV_PROSROCH_PROCENT", "REZERV_NEISPOLZOVAN_LIMIT", "REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_SROCH",
    "REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_PROSROCH", "YEAR_RESERV", "RAZMER_PERV_VZNOS", "VID_OBESPECH",
    "INFO_OBESPECH", "INFO_STRAXOVAN_OBESPECH", "SPRAVEDLIV_STOIMOST", "KATEGOR_KACHESTV_OBESPECH",
    "VNEBALANC_SCHET_OBESPECH", "STOIMOST_OBESPECH", "STRAXOV_SUM", "ZALOGODATEL_PORUCHITEL",
    "COD_PODRAZDELEN_KREDITNOI_ORG", "REZERV_MSFO", "PROCENT_REZERV_MSFO", "GOROD_TOCHKI_VYDACHI"
]

def coapplicants():
    # добавляем созаемщика
    coapplicants_list=[fake.name() for _ in range(random.randint(1, 3))]
    return ';'.join(coapplicants_list)

def date_diff_month (end_date, start_date):
    #расчет количества полных месяцев между датами
    months_difference = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    if end_date.day < start_date.day:
        months_difference -= 1
    return months_difference

def ostatok_po_kreditu (principal, annual_interest_rate, end_date, start_date, cur_date,pay_type):
    #расчет остатка по кредиту
    number_of_payments = date_diff_month (end_date, start_date)
    months_passed = date_diff_month (cur_date, start_date)
    if pay_type=='Аннуитетный':
        monthly_interest_rate = annual_interest_rate / 12 / 100
        remaining_balance = principal * (1 - ((1 + monthly_interest_rate) ** months_passed - 1) / ((1 + monthly_interest_rate) ** number_of_payments - 1))
        return remaining_balance
    elif pay_type=='Дифференцированный':
        return principal-(principal/number_of_payments*months_passed)
    else:
        return principal

def fn_calc_RAZMER_PLATEGA(loan_amount, annual_interest_rate, end_date, start_date, cur_date,pay_type):
    # расчет размере платежа
    number_of_payments = date_diff_month (end_date, start_date)
    months_passed = date_diff_month (cur_date, start_date)
    if months_passed<1:
        return None
    if pay_type=='Аннуитетный':
        monthly_interest_rate = (annual_interest_rate / 12) / 100
        annuity_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-number_of_payments))
        return round(annuity_payment,2)
    elif pay_type=='Дифференцированный':
        principal_monthly=loan_amount/number_of_payments
        principal=loan_amount-(principal_monthly*(months_passed-1))
        if cur_date.month <3:
            days_interval=31
        else:
            days_interval=days_in_month[cur_date.month-2]
        intrest=principal*annual_interest_rate/100*days_interval/365
        return principal_monthly+intrest
    else:
        return None

def DATA_YPLAT_PROCENT_func (date_of_credit, date_of_reestr):
    # определяем дату уплаты процентов
    if date_of_reestr.month>1:
        f_year=date_of_reestr.year
        f_month=date_of_reestr.month-1
        days_in_prev_month=days_in_month[date_of_reestr.month-1]
        if days_in_prev_month<date_of_credit.day:
            f_day=days_in_prev_month
        else:
            f_day=date_of_credit.day
    else:
        f_year=date_of_reestr.year-1
        f_month=12
        f_day=date_of_credit.day
    prom_date=date(f_year, f_month, f_day)
    if prom_date<=date_of_credit:
        return None
    return prom_date

def fn_from_DLINA_PROSROCHEN_to_OVERDUE(DLINA_PROSROCHEN):
    if DLINA_PROSROCHEN==0:
        return '0'
    elif DLINA_PROSROCHEN<31:
        return '1-30'
    elif DLINA_PROSROCHEN<91:
        return '31-90'
    elif DLINA_PROSROCHEN<181:
        return '91-180'
    elif DLINA_PROSROCHEN<361:
        return '181-360'
    elif DLINA_PROSROCHEN<721:
        return '360-720'
    else:
        return '720+'

def fn_KACHESTVO_DOLGA(DLINA_PROSROCHEN):
    if DLINA_PROSROCHEN<31:
        return 'Хорошее'
    elif DLINA_PROSROCHEN<61:
        return 'Среднее'
    else:
        return 'Неудовлетворительное'

def fn_VID_OBESPECH(tip_kredita):
    if tip_kredita=="Жилищные ссуды":
        return 'Залог имущественных прав (требований) на недвижимое имущество'
    elif tip_kredita in ["Ипотечные ссуды", "Ипотечные ссуды с пониженным уровнем риска","Прочая ипотека", "Военная ипотека"]:
        return 'Залог недвижимого имущества'
    elif tip_kredita=="Автокредиты":
        return 'Залог движимого имущества'
    return 'Нет'

def get_random_variant_from_Excel(field_name, df_choices):
    # Фильтрация строк по заданному "названию поля"
    filtered_df = df_choices[df_choices['название поля'] == field_name]
    if filtered_df.empty:
        return None  # Если нет строк с заданным "названием поля"
    # Создание списка кортежей из столбцов "вариант" и "вероятность"
    data = list(zip(filtered_df['вариант'], filtered_df['вероятность']))
    # Выбор случайного варианта с учетом вероятности
    random_variant = random.choices(data, weights=[item[1] for item in data], k=1)[0][0]
    return random_variant 

days_in_month = {
    1: 31,   # Январь
    2: 28,   # Февраль
    3: 31,   # Март
    4: 30,   # Апрель
    5: 31,   # Май
    6: 30,   # Июнь
    7: 31,   # Июль
    8: 31,   # Август
    9: 30,   # Сентябрь
    10: 31,  # Октябрь
    11: 30,  # Ноябрь
    12: 31   # Декабрь
}

bank_branches = {
    "101": "Центральный филиал",
    "202": "Северо-Западный филиал",
    "303": "Южный филиал",
    "404": "Приволжский филиал",
    "505": "Дальневосточный филиал"
}

def fn_define_credit_start_date(date_of_reestr,number_of_payments, date_start_credit):
    
    delta_back=random.randint(1,number_of_payments)
    total_months_back = date_of_reestr.month + date_of_reestr.year * 12 - delta_back-1
    years_start = total_months_back// 12
    month_start = (total_months_back%  12)+1
    day_start=random.randint(1,days_in_month[month_start])
    date_start=date(years_start,month_start,day_start)
    if date_start<date_start_credit:
        date_start=fake.date_between_dates(date_start=date_start_credit,date_end=date_of_reestr) 
    return date_start

def fn_define_credit_end_date(DATA_DOGOVORA,number_of_payments):
    total_months_end = DATA_DOGOVORA.month + DATA_DOGOVORA.year * 12 + number_of_payments-1
    years_end = total_months_end// 12
    month_end = total_months_end% 12+1
    day_end=DATA_DOGOVORA.day
    if day_end>days_in_month[month_end]:
        day_end=days_in_month[month_end]
    return date(years_end,month_end,day_end)

def fn_KATEGOR_KACHESTV_reserv(pos, fin_pol, ka4_dol,overdue,cred_type):
    ## переделать Оценка не проводилась не менее 50%
    kk=[]
    ios_kk={'Хорошее':1,'Среднее':2,'Плохое':3,'Неудовлетворительное':3,'Оценка не проводилась':3}
    ios_proc=[0,1,21,51,100]
    pos_kk=[2,2,2,3,4,5,5]

    overdue_tabl=['0','1-30','31-90','91-180','181-360','360-720','720+']
    pos_proc_v1={
        'Жилищные ссуды': [3,8,20,50,75,100,100],
        'Ипотечные ссуды': [0.35,1.5,10,35,75,100,100],
        'Ипотечные ссуды с пониженным уровнем риска': [0.35,1.5,10,35,75,100,100],
        'Прочая ипотека': [0.35,1.5,10,35,75,100,100],
        'Военная ипотека': [0.35,1.5,10,35,75,100,100],
        'Автокредиты':  [0.5,1.5,10,35,75,100,100],
        'Иные потребительские ссуды': [3,8,20,50,75,100,100]
    }
    if pos=='0':
        kk.append (str(ios_kk[fin_pol]+ios_kk[ka4_dol]-1))
        kk.append(ios_proc[ios_kk[fin_pol]+ios_kk[ka4_dol]-2])
    else:
        kk.append (str(pos_kk[overdue_tabl.index(overdue)]))
        kk.append(pos_proc_v1[cred_type][overdue_tabl.index(overdue)])
    return kk

# открываем файл с вариантами для полей
file_path_to_Excel_choices=r'c:\Pet_project\cbr\reestr\reestr_choices.xlsx'
df_choices = pd.read_excel(file_path_to_Excel_choices)

employers_list=[fake.company() for _ in range(reestr_raws_count // 10)]
employers_INN_list=[fake.bothify(text='##########') for _ in range(len(employers_list))]

random_number_string = [fake.bothify(text='##########') for _ in range(reestr_raws_count)]
REZIDENT_list = [get_random_variant_from_Excel("REZIDENT", df_choices)for _ in range(reestr_raws_count)]
POL_list=[get_random_variant_from_Excel("POL", df_choices)for _ in range(reestr_raws_count)]
first_names_list=[fake.first_name_male() if pol == "М" else fake.first_name_female() for pol in POL_list]
last_names_list=[fake.last_name_male() if pol == "М" else fake.last_name_female() for pol in POL_list]
middle_names_list=[fake.middle_name_male() if pol == "М" else fake.middle_name_female() for pol in POL_list]
birth_date_list=[fake.date_of_birth(minimum_age=21,  maximum_age=65) for _ in range(reestr_raws_count)]
address_list=[fake.address() for _ in range(reestr_raws_count)]
passport_list=[fake.bothify(text='##########') for _ in range(reestr_raws_count)]
kem_vidan_list=[fake.administrative_unit() for _ in range(reestr_raws_count)]
data_vidachi_pass_list=[fake.date_between_dates(date_start=birth_date,date_end=date_of_reestr) for birth_date in birth_date_list ]
SEM_POL_list = [get_random_variant_from_Excel("SEM_POL", df_choices) for _ in range(reestr_raws_count)]
KOL_IGDIVENCEV_list = [random.randint(0, 5) for _ in range(reestr_raws_count)]
TIP_ZANYATOSTI_list= [get_random_variant_from_Excel("TIP_ZANYATOSTI", df_choices) for _ in range(reestr_raws_count)]
BANK_CLEARK_list = [get_random_variant_from_Excel("BANK_CLEARK", df_choices) for _ in range(reestr_raws_count)]
ZARPLATNIE_SCHETA_list= [get_random_variant_from_Excel("ZARPLATNIE_SCHETA", df_choices) for _ in range(reestr_raws_count)]
DOLGENOST_list=[fake.job() for _ in range(reestr_raws_count)]
MESTO_RAB_list=[fake.random_element(elements=employers_list) for _ in range(reestr_raws_count)]
employer_inn_mapping = dict(zip(employers_list, employers_INN_list))
INN_RAB_list=[employer_inn_mapping.get(employer, None) for employer in MESTO_RAB_list]
### сделать источники дохода в соответствии с типом занятости
ISTOCHNIK_DOXODA_list= [str(random.randint(1, 13)) for _ in range(reestr_raws_count)]
FIO_SOZAEMSCHIKA_list= [coapplicants() if random.random() < FIO_SOZAEMSCHIKA_probability else None for _ in range(reestr_raws_count)]

# NB! фин положение с течением срока кредита не изменяется и соответствует значению на дату выдачи
FIN_POLOGENIE_list=[get_random_variant_from_Excel("FIN_POLOGENIE", df_choices)for _ in range(reestr_raws_count)]
FIN_POLOGENIE_VIDACHA_list=[FIN_POLOGENIE_list[i] for i in range(reestr_raws_count) ]

UID_list= [fake.bothify(text="########-####-####-####-############-#",letters='0123456789ABCDEF') for _ in range(reestr_raws_count)]
ID_DOGOVORA_list=[fake.bothify(text='##########') for _ in range(reestr_raws_count)]
NOMER_DOGOVORA_list=[fake.bothify(text='КД№ ########-??')for _ in range(reestr_raws_count)]

VID_KREDITA_list=[get_random_variant_from_Excel("VID_KREDITA", df_choices) for i in range(reestr_raws_count)]

number_of_payments_shadow_list=[
    get_random_variant_from_Excel("number_of_payments_shadow"+'_'+VID_KREDITA_list[i], df_choices)
    for i in range(reestr_raws_count)
]

DATA_DOGOVORA_list=[
    fn_define_credit_start_date(date_of_reestr,number_of_payments_shadow_list[i],date_start_credit)
    for i in range(reestr_raws_count)
]
DATA_VIDACHI_list=[element + timedelta(days=random.randint(0, 5))  for element in DATA_DOGOVORA_list]
DATA_KONCA_DOGOVORA_list=[
    fn_define_credit_end_date(DATA_DOGOVORA_list[i],number_of_payments_shadow_list[i])
    for i in range(reestr_raws_count)
]

SUMMA_KREDITA_list=[get_random_variant_from_Excel("SUMMA_KREDITA"+'_'+VID_KREDITA_list[i], df_choices)for i in range(reestr_raws_count)]
VID_KREDITA_115_list=[get_random_variant_from_Excel("VID_KREDITA_115"+'_'+VID_KREDITA_list[i], df_choices)for i in range(reestr_raws_count)]
REGIM_KREDITA_list=[get_random_variant_from_Excel("REGIM_KREDITA"+'_'+VID_KREDITA_list[i], df_choices)for i in range(reestr_raws_count)]
PROCENT_STAVKA_NA_DATU_VIDACHI_list=[round(random.randint(1150, 2500)/100,2) for  _ in range(reestr_raws_count)]
TIP_PLATEGA_list=[get_random_variant_from_Excel("TIP_PLATEGA"+'_'+VID_KREDITA_list[i], df_choices)for i in range(reestr_raws_count)]
SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list = [
    round(
    ostatok_po_kreditu(
        SUMMA_KREDITA_list[i],
        PROCENT_STAVKA_NA_DATU_VIDACHI_list[i],
        DATA_KONCA_DOGOVORA_list[i],
        DATA_DOGOVORA_list[i],
        date_of_reestr,
        TIP_PLATEGA_list[i]
    ),2) for i in range(reestr_raws_count)
]
ZADOLGEN_PROSROCHEN_POKURSU_list = [    
    round(
    random.randint(
        0,int(
            SUMMA_KREDITA_list[i]-
            SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i]
            ) ),2) 
    if random.random() < ZADOLGEN_PROSROCHEN_POKURSU_probability else 0
    for i in range(reestr_raws_count)
]
# добавляем просроченную задолженность к общей сумме задолженности, т.к. ранее мы рассчитали остаток срочного основного долга для случая своевременной уплаты.
# всё, что не было уплачено своевременно должно увеличивать эту сумму. 

SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list=[SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i]+ZADOLGEN_PROSROCHEN_POKURSU_list[i] for i in range(reestr_raws_count)]

## доработать с учетом того что в ноябре не 31 день
NACH_PROCENT_list = [
    abs(
    round(
    SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i] * 
    PROCENT_STAVKA_NA_DATU_VIDACHI_list[i] *
    (30-DATA_DOGOVORA_list[i].day)/365/100,2))
    for i in range(reestr_raws_count)
]
## просроченные проценты отражаем только для тех кредитов, у которых есть просроченный основной долг,
## вероятность просроченных процентов в два раза меньше основного долга (оценочное мнение), так как в первую очередь списываются просроченные проценты

PROSROCHEN_PROCENT_list = [
    round(
    SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i] * PROCENT_STAVKA_NA_DATU_VIDACHI_list[i]/12/100 * random.randint(1, 3),2)
    if random.random() < 0.5 and ZADOLGEN_PROSROCHEN_POKURSU_list[i] > 0
    else 0  
    for i in range(reestr_raws_count)
]

# рассчитывается для лимитных продуктов как разница между суммой кредита и остатком основного долга
NEISPOLZOVAN_LIMIT_list=[
    SUMMA_KREDITA_list[i]-
    SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i] if REGIM_KREDITA_list[i]!='Единоразовая выдача' else 0
    for i in range(reestr_raws_count)
]

POS_list=[random.choice(POS_list_choice) if random.random() < POS_list_probability else '0' for _ in range(reestr_raws_count)]

LINE_STATUS_list=[get_random_variant_from_Excel(
    "LINE_STATUS", df_choices)
    if REGIM_KREDITA_list[i]!='Единоразовая выдача' else None
    for i in range(reestr_raws_count)]

# переделать пятая цифра в зависимости от срока кредита
SSYD_SCHET_list=[fake.bothify(text='4550################') for _ in range(reestr_raws_count)]
# переделать счет просрочки только для ссуд, у которых есть текущая просрочка? нужно ли это. могла быть просрочка, счет открыли, просрочку погасили
SCHET_PROSROCHEN_ZADOLGEN_list=[fake.bothify(text='45815###############') for _ in range(reestr_raws_count)]
SCHET_NACHISLEN_PROCENTOV_list=[fake.bothify(text='47427###############') for _ in range(reestr_raws_count)]
SCHET_PROSROCHEN_PROCENTOV_list=[fake.bothify(text='45915###############') for _ in range(reestr_raws_count)]
## сделать, чтобы если зарплатный клиент, то еще один счет через точку запятую ставил
TEKUSCH_SCHET_list=[fake.bothify(text='40817###############') for _ in range(reestr_raws_count)]

# ежемесячные платежи по процентам у всех типов кредитов
REGIM_YPLAT_PROCENT_monthly=['Дифференцированный','Аннуитетный','Минимальный', 'Иной']
REGIM_YPLAT_PROCENT_list=['ежемесячно' if TIP_PLATEGA_list[i] in REGIM_YPLAT_PROCENT_monthly else None for i in range(reestr_raws_count)]
REGIM_YPLAT_OSNOV_monthly=['Дифференцированный','Аннуитетный','Минимальный']
REGIM_YPLAT_OSNOV_list=['ежемесячно' if TIP_PLATEGA_list[i] in REGIM_YPLAT_PROCENT_monthly else 'по графику' for i in range(reestr_raws_count)]

# NB! проценты уплачиваются по всем видов кредитов ежемесячно
DATA_YPLAT_PROCENT_list=[
    DATA_YPLAT_PROCENT_func (DATA_DOGOVORA_list[i], date_of_reestr) for i in range(reestr_raws_count)
]

DATA_YPLAT_OSNOV_list=[
    DATA_YPLAT_PROCENT_func (DATA_DOGOVORA_list[i], date_of_reestr)
    if REGIM_YPLAT_OSNOV_list[i] in REGIM_YPLAT_OSNOV_monthly else None
    for i in range(reestr_raws_count)
]
# сделать, чтобы длина просроченных платежей соответствовала сумме просроченного основного долга
DLINA_PROSROCHEN_PLATEG_list=[
    random.randint(0, 1000) if ZADOLGEN_PROSROCHEN_POKURSU_list[i]>0 else 0
    for i in range(reestr_raws_count)
]
# NB! выбран вариант без просроченных платежей+просроченные платежи от 1 до 30 дней 
# (т.е. не учтен вариант ссуды без просроченных платежей и с просрочкой до 30 дней)
# а также не учтен вариант 360+: используется  "360-720" и "720+""

OVERDUE_INTERVAL_list=[fn_from_DLINA_PROSROCHEN_to_OVERDUE(DLINA_PROSROCHEN_PLATEG_list[i] ) for i in range(reestr_raws_count)]

RAZMER_PLATEGA_list=[
    fn_calc_RAZMER_PLATEGA(
               SUMMA_KREDITA_list[i],
               PROCENT_STAVKA_NA_DATU_VIDACHI_list[i],
               DATA_KONCA_DOGOVORA_list[i],
               DATA_DOGOVORA_list[i],
               date_of_reestr,
               TIP_PLATEGA_list[i]
    )
    for i in range(reestr_raws_count)
]

DLINA_PROSROCHEN_PLATEG_ZA_180_DNEY_list=[
    DLINA_PROSROCHEN_PLATEG_list[i]
    if POS_list[i]=='0' else None
    for i in range(reestr_raws_count)
]

KACHESTVO_DOLGA_list=[
    fn_KACHESTVO_DOLGA(DLINA_PROSROCHEN_PLATEG_ZA_180_DNEY_list[i])
    if POS_list[i]=='0' else None
    for i in range(reestr_raws_count)
]

#=======================//////////////////////////////////////////===================
KATEGOR_KACHESTV_list=[fn_KATEGOR_KACHESTV_reserv(
    POS_list[i],
    FIN_POLOGENIE_list[i],
    KACHESTVO_DOLGA_list[i],
    OVERDUE_INTERVAL_list[i],
    VID_KREDITA_115_list[i]
    )[0] for i in range(reestr_raws_count)]

PROCENT_REZERV_list=[fn_KATEGOR_KACHESTV_reserv(
    POS_list[i],
    FIN_POLOGENIE_list[i],
    KACHESTVO_DOLGA_list[i],
    OVERDUE_INTERVAL_list[i],
    VID_KREDITA_115_list[i]
    )[1] for i in range(reestr_raws_count)]

# NB! рассчитано без учета обеспечения
SUMMA_REZERVA_PO_SROCH_list= [
    
    round(
    (SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list[i]-
    ZADOLGEN_PROSROCHEN_POKURSU_list[i])*
    PROCENT_REZERV_list[i]/100,2)
    for i in range(reestr_raws_count)
]

REZERV_PO_PROSROCH_list=[
    
    round(
    (ZADOLGEN_PROSROCHEN_POKURSU_list[i])*
    PROCENT_REZERV_list[i]/100,2)
    for i in range(reestr_raws_count)
]

REZERV_NACHISLEN_PROCENT_list=[
    
    round(
    (NACH_PROCENT_list[i])*
    PROCENT_REZERV_list[i]/100,2)
    for i in range(reestr_raws_count)
]

REZERV_PROSROCH_PROCENT_list=[
    round(
    (PROSROCHEN_PROCENT_list[i])*
    PROCENT_REZERV_list[i]/100,2)
    for i in range(reestr_raws_count)
]

REZERV_NEISPOLZOVAN_LIMIT_list=[
    round(
    (NEISPOLZOVAN_LIMIT_list[i])*
    PROCENT_REZERV_list[i]/100,2)
    for i in range(reestr_raws_count)
]

RAZMER_PERV_VZNOS_list=[
    round(
    random.randint(0,80)/100*SUMMA_KREDITA_list[i]
    ,2)
    if VID_KREDITA_115_list[i] in ["Жилищные ссуды", "Ипотечные ссуды", "Ипотечные ссуды с пониженным уровнем риска","Прочая ипотека", "Военная ипотека", "Автокредиты"] 
    else 0
    for i in range(reestr_raws_count)
]

VID_OBESPECH_choice=[
    'Гарантийный депозит (вклад)',
    'Залог имущественных прав (требований) на недвижимое имущество',
    'Залог ценных бумаг',
    'Поручительства (гарантии)',
    'Залог движимого имущества',
    'Залог недвижимого имущества',
    'Нет'
]
## переделать ипотека залог недвижимость, автокредит - автомобиль
VID_OBESPECH_list=[
    fn_VID_OBESPECH(VID_KREDITA_115_list[i])
    for i in range(reestr_raws_count)
]

INFO_OBESPECH_list=[
    fake.bothify(text='ДЗ№ ########-??')
    if VID_OBESPECH_list[i]!='Нет' else None
    for i in range(reestr_raws_count)
]
INFO_STRAXOVAN_OBESPECH_choice=['застраховано','не застраховано']
INFO_STRAXOVAN_OBESPECH_list=[
    random.choice(INFO_STRAXOVAN_OBESPECH_choice)
    if VID_OBESPECH_list[i]!='Нет' else None
    for i in range(reestr_raws_count)
]

VNEBALANC_SCHET_OBESPECH_list=[
    fake.bothify(text='91312###############')
    if VID_OBESPECH_list[i]!='Нет' else None
    for i in range(reestr_raws_count)
]

STOIMOST_OBESPECH_list=[
    SUMMA_KREDITA_list[i]
    if VID_OBESPECH_list[i]!='Нет' else None
    for i in range(reestr_raws_count)
]

STRAXOV_SUM_list=[
    SUMMA_KREDITA_list[i]
    if INFO_STRAXOVAN_OBESPECH_list[i]=='застраховано' else None
    for i in range(reestr_raws_count)
]
## NB! если отчество пустое, то в конце будет лишний пробел
ZALOGODATEL_PORUCHITEL_list=[
    first_names_list[i]+' '+last_names_list[i]+' '+middle_names_list[i]    
    if VID_OBESPECH_list[i]!='Нет' else None
    for i in range(reestr_raws_count)
]


COD_PODRAZDELEN_KREDITNOI_ORG_list=[
    random.choice(list(bank_branches.keys()))
    for i in range(reestr_raws_count)
]

GOROD_TOCHKI_VYDACHI_list=[
    bank_branches[COD_PODRAZDELEN_KREDITNOI_ORG_list[i]]
    for i in range(reestr_raws_count)
]

#==================================================== загружаем полученные столбцы в датафрейм ========================================
reestr= pd.DataFrame(columns=reestr_columns_list)
reestr["ID_ZAEMSCHIKA"]=random_number_string
#дату задаем после того как задали размерность датафрейма
reestr["DATE1"]=date_of_reestr
reestr["SURNAME"]=last_names_list
reestr["NAME"]=first_names_list
reestr["MIDDLE_NAME"]=middle_names_list
reestr["INN"]=random_number_string
reestr["REZIDENT"]=REZIDENT_list
reestr["POL"]=POL_list
reestr["DATA_ROG"]=birth_date_list
reestr["ADRES_REG"]=address_list
reestr["ADRES"]=address_list
reestr["DOCUMENT"]="21"
reestr["NOMER_DOCUMENTA"]=passport_list
reestr["KEM_VIDAN_DOCUMENT"]=kem_vidan_list
reestr["DATA_VIDACHI_DOCUMENTA"]=data_vidachi_pass_list
reestr["SEMEINOE_POL"]=SEM_POL_list
reestr["KOL_IGDIVENCEV"]=KOL_IGDIVENCEV_list
reestr["TIP_ZANYATOSTI"]=TIP_ZANYATOSTI_list
reestr["BANK_CLEARK"]=BANK_CLEARK_list
reestr["ZARPLATNIE_SCHETA"]=ZARPLATNIE_SCHETA_list
reestr["DOLGENOST"]=DOLGENOST_list
reestr["MESTO_RAB"]=MESTO_RAB_list
reestr["INN_RAB"]=INN_RAB_list
### reestr["DOXOD_NA_DATU_VIDACHI"]=DOXOD_NA_DATU_VIDACHI_list
### reestr["DOXOD"]=DOXOD_list
### reestr["PDN_DATA_VIDACHI"]=PDN_DATA_VIDACHI_list
### reestr["DOXOD_PDN_DATA_VIDACHI"]=DOXOD_PDN_DATA_VIDACHI_list
### reestr["RASXOD_PDN_DATA_VIDACHI"]=RASXOD_PDN_DATA_VIDACHI_list
### reestr["PDN_RESTRUKT_IZMENENIYA"]=PDN_RESTRUKT_IZMENENIYA_list
### reestr["DOXOD_PDN_RESTRUKT_IZMENENIYA"]=DOXOD_PDN_RESTRUKT_IZMENENIYA_list
### reestr["RASXOD_PDN_RESTRUKT_IZMENENIYA"]=RASXOD_PDN_RESTRUKT_IZMENENIYA_list
### reestr["LAST_DATE_PDN"]=LAST_DATE_PDN_list
# переделать источник подтверждения дохода для пенсионеров, в соответствии с программой
reestr["ISTOCHNIK_DOXODA"]=ISTOCHNIK_DOXODA_list
### reestr["RASXOD_NA_DATU_VIDACHI"]=RASXOD_NA_DATU_VIDACHI_list
### reestr["RASXOD"]=RASXOD_list
### reestr["PLATEGSPOSB"]=PLATEGSPOSB_list
### reestr["MAX_KREDIT"]=MAX_KREDIT_list
### reestr["SCORING_OCENKA"]=SCORING_OCENKA_list
reestr["FIO_SOZAEMSCHIKA"]=FIO_SOZAEMSCHIKA_list
reestr["FIN_POLOGENIE"]=FIN_POLOGENIE_list
reestr["FIN_POLOGENIE_VIDACHA"]=FIN_POLOGENIE_VIDACHA_list
reestr["UID"]=UID_list
reestr["ID_DOGOVORA"]=ID_DOGOVORA_list
reestr["NOMER_DOGOVORA"]=NOMER_DOGOVORA_list
reestr["DATA_DOGOVORA"]=DATA_DOGOVORA_list
reestr["DATA_VIDACHI"]=DATA_VIDACHI_list
reestr["DATA_KONCA_DOGOVORA"]=DATA_KONCA_DOGOVORA_list
reestr["DATA_ZAKR_DOGOVORA"]=DATA_KONCA_DOGOVORA_list
# данный показатель используется для РЕЕСТРов на предыдущие отчетные даты
#reestr["DATA_FACT_ZAKR_DOGOVORA"]=DATA_FACT_ZAKR_DOGOVORA_list
reestr["SUMMA_KREDITA"]=SUMMA_KREDITA_list
reestr["VALUT_KREDITA"]='643'
reestr["VID_KREDITA"]=VID_KREDITA_list
reestr["VID_KREDITA_115"]=VID_KREDITA_115_list
# сделать тестовые программы кредитования в экселе
# reestr["PROGRAMMA_KREDITA"]=PROGRAMMA_KREDITA_list
reestr["REGIM_KREDITA"]=REGIM_KREDITA_list
### reestr["KATEGORY_KREDITA_PSK"]=KATEGORY_KREDITA_PSK_list
# в зависимости от программы кредитования
# reestr["CEL_KREDITA"]=CEL_KREDITA_list
# reestr["USLOVIYA_IZMENENIY"]=USLOVIYA_IZMENENIY_list
# reestr["POLNAI_STOIMOST_KREDITA"]=POLNAI_STOIMOST_KREDITA_list
reestr["PROCENT_STAVKA_NA_DATU_VIDACHI"]=PROCENT_STAVKA_NA_DATU_VIDACHI_list
reestr["PROCENT_STAVKA"]=PROCENT_STAVKA_NA_DATU_VIDACHI_list
# так как все кредиты в рублях, то ["SUMMA_KREDIT_TREBOVAN"]=["SUMMA_KREDIT_TREBOVAN_POKURSU_ALL"]
reestr["SUMMA_KREDIT_TREBOVAN"]=SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list
reestr["VALUT_KREDIT_TREBOVAN"]='643'
reestr["SUMMA_KREDIT_TREBOVAN_POKURSU_ALL"]=SUMMA_KREDIT_TREBOVAN_POKURSU_ALL_list
## сделать размер просрочки в зависимости от количества дней
reestr["ZADOLGEN_PROSROCHEN_POKURSU"]=0
##!##reestr["ZADOLGEN_PROSROCHEN_POKURSU"]=ZADOLGEN_PROSROCHEN_POKURSU_list
reestr["NACH_PROCENT"]=NACH_PROCENT_list
reestr["PROSROCHEN_PROCENT"]=PROSROCHEN_PROCENT_list
reestr["NEISPOLZOVAN_LIMIT"]=NEISPOLZOVAN_LIMIT_list
##### генерация выкупа ссуд в ближайшее время не планируется
##### reestr["VIKYPLEN_SUMMA_TREBOVAN_ALL"]=VIKYPLEN_SUMMA_TREBOVAN_ALL_list
##### reestr["VIKYPLEN_SUMMA_TREBOVAN_PROSROCH"]=VIKYPLEN_SUMMA_TREBOVAN_PROSROCH_list
## подумать, какие комиссии можно добавить, чтобы потом можно было ПСК посчитать
## reestr["KOMISSII"]=KOMISSII_list
## рассчитать сумму штрафов в соответствии с ФЗ-353
## reestr["SUMMA_PENALTIES"]=SUMMA_PENALTIES_list
##### генерация выкупа ссуд в ближайшее время не планируется
##### reestr["NOMINAL_VIKYPLEN_TREBOVAN"]=NOMINAL_VIKYPLEN_TREBOVAN_list
##### reestr["DISCONT"]=DISCONT_list
reestr["POS"]=POS_list
reestr["KATEGOR_KACHESTV"]=KATEGOR_KACHESTV_list
reestr["PROCENT_REZERV"]=PROCENT_REZERV_list
# !NB в жизни по инд ссудам может быть разный процент резерва для основного долга и процентов/лимита. У нас для простоты будет один и тот же.
reestr["KATEGOR_KACHESTV_PROCENT"]=KATEGOR_KACHESTV_list
reestr["PROCENT_REZERV_PROCENT"]=PROCENT_REZERV_list
reestr["KATEGOR_KACHESTV_LIMIT"]=KATEGOR_KACHESTV_list
reestr["PROCENT_REZERV_LIMIT"]=PROCENT_REZERV_list
reestr["LINE_STATUS"]=LINE_STATUS_list
reestr["BIOMETRIYA"]='Нет'
reestr["SSYD_SCHET"]=SSYD_SCHET_list
reestr["SCHET_PROSROCHEN_ZADOLGEN"]=SCHET_PROSROCHEN_ZADOLGEN_list
reestr["SCHET_NACHISLEN_PROCENTOV"]=SCHET_NACHISLEN_PROCENTOV_list
reestr["SCHET_PROSROCHEN_PROCENTOV"]=SCHET_PROSROCHEN_PROCENTOV_list
reestr["TEKUSCH_SCHET"]=TEKUSCH_SCHET_list
##### на текущий момент выкупленные ссуды не генерируются
##### reestr["SCHET_PO_VIKYPLEN_SSYDAM"]=SCHET_PO_VIKYPLEN_SSYDAM_list
##### reestr["SCHET_PROSROCH_VIKYPLEN_TREBOVAN"]=SCHET_PROSROCH_VIKYPLEN_TREBOVAN_list
## на текущий момент штрафы, пени и комиссии не начисляются
## счет штрафов может быть сводный
## reestr["SCHET_PENALTIES"]=SCHET_PENALTIES_list
## счет комиссии может быть сводный
## reestr["SCHET_KOMISSII"]=SCHET_KOMISSII_list
# на текущий момент ссуды не реструктурируются
# reestr["KOL_VO_RESTRUKT"]=KOL_VO_RESTRUKT_list
# reestr["IZMENENIE_DOGOVORA"]=IZMENENIE_DOGOVORA_list
# reestr["LAST_DATE_RESTRUKT"]=LAST_DATE_RESTRUKT_list
# reestr["PRIZNAK_NAPRAVLENIE_SSYD"]=PRIZNAK_NAPRAVLENIE_SSYD_list
# reestr["RESHENIYA_UO"]=RESHENIYA_UO_list
# reestr["DATA_RESHENIYA_UO"]=DATA_RESHENIYA_UO_list
# reestr["NEGATIV"]=NEGATIV_list
##### этот раздел генерировать не планируется
##### reestr["TIP_OPERACII"]=TIP_OPERACII_list
##### reestr["DATA_OPERACII"]=DATA_OPERACII_list
##### reestr["SUMMA_OPERACII"]=SUMMA_OPERACII_list
reestr["REGIM_YPLAT_PROCENT"]=REGIM_YPLAT_PROCENT_list
reestr["REGIM_YPLAT_OSNOV"]=REGIM_YPLAT_OSNOV_list
reestr["DATA_YPLAT_PROCENT"]=DATA_YPLAT_PROCENT_list
reestr["DATA_YPLAT_OSNOV"]=DATA_YPLAT_OSNOV_list
reestr["DLINA_PROSROCHEN_PLATEG"]=DLINA_PROSROCHEN_PLATEG_list
# обычно используется метод FIFO
reestr["METOD_RASCHETA_PROSR"]='FIFO'
reestr["OVERDUE_INTERVAL"]=OVERDUE_INTERVAL_list
reestr["TIP_PLATEGA"]=TIP_PLATEGA_list
reestr["RAZMER_PLATEGA"]=RAZMER_PLATEGA_list
## подумать как сделать с учетом просрочки
# reestr["DATA_POSL_POGASH_PROC"]=DATA_POSL_POGASH_PROC_list
# reestr["DATA_POSL_POGASH_SSUD"]=DATA_POSL_POGASH_SSUD_list
##### льготные периоды в настоящий момент не генерируются
# reestr["LGOT_PERIOD_START"]=LGOT_PERIOD_START_list
# reestr["LGOT_PERIOD_FINISH"]=LGOT_PERIOD_FINISH_list
# заполняется только по ИОС. должно быть не меньше непрерывной просрочки, но не более 180 дней
# при этом по ссудам без просрочки может быть больше ноля. Влияет на качество обслуживания долга
reestr["DLINA_PROSROCHEN_PLATEG_ZA_180_DNEY"]=DLINA_PROSROCHEN_PLATEG_ZA_180_DNEY_list
reestr["KACHESTVO_DOLGA"]=KACHESTVO_DOLGA_list
reestr["SUMMA_REZERVA_PO_SROCH"]=SUMMA_REZERVA_PO_SROCH_list
reestr["REZERV_PO_PROSROCH"]=REZERV_PO_PROSROCH_list
reestr["REZERV_NACHISLEN_PROCENT"]=REZERV_NACHISLEN_PROCENT_list
reestr["REZERV_PROSROCH_PROCENT"]=REZERV_PROSROCH_PROCENT_list
reestr["REZERV_NEISPOLZOVAN_LIMIT"]=REZERV_NEISPOLZOVAN_LIMIT_list
##### reestr["REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_SROCH"]=REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_SROCH_list
##### reestr["REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_PROSROCH"]=REZERV_VIKYPLEN_SUMMA_TREBOVAN_PO_PROSROCH_list
reestr["YEAR_RESERV"]='С 2014'
reestr["RAZMER_PERV_VZNOS"]=RAZMER_PERV_VZNOS_list
reestr["VID_OBESPECH"]=VID_OBESPECH_list
reestr["INFO_OBESPECH"]=INFO_OBESPECH_list
reestr["INFO_STRAXOVAN_OBESPECH"]=INFO_STRAXOVAN_OBESPECH_list
## на текущий момент резерв на обеспечение не корректируется
## reestr["SPRAVEDLIV_STOIMOST"]=SPRAVEDLIV_STOIMOST_list
#№ reestr["KATEGOR_KACHESTV_OBESPECH"]=KATEGOR_KACHESTV_OBESPECH_list
reestr["VNEBALANC_SCHET_OBESPECH"]=VNEBALANC_SCHET_OBESPECH_list
reestr["STOIMOST_OBESPECH"]=STOIMOST_OBESPECH_list
reestr["STRAXOV_SUM"]=STRAXOV_SUM_list
reestr["ZALOGODATEL_PORUCHITEL"]=ZALOGODATEL_PORUCHITEL_list
reestr["COD_PODRAZDELEN_KREDITNOI_ORG"]=COD_PODRAZDELEN_KREDITNOI_ORG_list
##### резерв МСФО делать не планируется
# reestr["REZERV_MSFO"]=REZERV_MSFO_list
# reestr["PROCENT_REZERV_MSFO"]=PROCENT_REZERV_MSFO_list
reestr["GOROD_TOCHKI_VYDACHI"]=GOROD_TOCHKI_VYDACHI_list

# задаем типы данных
date_columns = ['DATE1',
                'DATA_ROG',
                'DATA_VIDACHI_DOCUMENTA',
                'LAST_DATE_PDN',
                'DATA_DOGOVORA',
                'DATA_VIDACHI',
                'DATA_KONCA_DOGOVORA',
                'DATA_ZAKR_DOGOVORA',
                'DATA_FACT_ZAKR_DOGOVORA',
                'LAST_DATE_RESTRUKT',
                'DATA_YPLAT_PROCENT',
                'DATA_YPLAT_OSNOV',
                'DATA_POSL_POGASH_PROC',
                'DATA_POSL_POGASH_SSUD',
                'LGOT_PERIOD_START',
                'LGOT_PERIOD_FINISH'
                ]
reestr[date_columns] = reestr[date_columns].apply(lambda x: pd.to_datetime(x).dt.date)
reestr.to_excel(filepath, index=False)
print (f'Start at {start_time} END at {datetime.now().strftime("%H:%M:%S")}' )