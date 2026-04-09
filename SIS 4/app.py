# =============================================================================
# ProposalAI — Technical Proposal Generator
# SIS Week 12 — Integrated Agentic Mini-Project
#
# UI/UX revision: professional B2B SaaS aesthetic
#   - Light theme: white cards on soft #F5F5F3 background
#   - DM Sans typography (clean, neutral, modern)
#   - Consistent card-based sectioning with subtle borders
#   - Logical left/right two-column layout
#   - All business logic is UNCHANGED from v1
# =============================================================================

import streamlit as st
import time
import random
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------- #
#  PAGE CONFIG — must be the very first Streamlit call                        #
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="ProposalAI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
#  DATA MODELS  (unchanged)
# =============================================================================

@dataclass
class ProposalRequest:
    client_name: str
    solution_type: str
    space_description: str
    area_sqm: int
    floors: int
    users_or_cashiers: int
    budget_usd: int
    retention_days: int
    risk_tolerance: str
    preferred_brand: str
    currency: str
    language: str
    contingency_pct: int
    include_installation: bool
    model_id: str


@dataclass
class BOMLine:
    category: str
    item: str
    qty: int
    unit_price: float
    notes: str = ""

    @property
    def total(self) -> float:
        return self.qty * self.unit_price


@dataclass
class ProposalScore:
    cost: int
    risk: int
    scalability: int

    @property
    def composite(self) -> int:
        return round((self.cost * 0.35) + (self.risk * 0.35) + (self.scalability * 0.30))


@dataclass
class Insight:
    level: str
    title: str
    detail: str


@dataclass
class MonitoringSnapshot:
    api_calls: int
    input_tokens: int
    output_tokens: int
    latency_ms: int
    hallucination_flags: int
    confidence_pct: int
    errors: list = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def estimated_cost_usd(self) -> float:
        return round(
            (self.input_tokens / 1_000_000) * 3.0
            + (self.output_tokens / 1_000_000) * 15.0,
            4,
        )


@dataclass
class ProposalResult:
    request: ProposalRequest
    bom: list
    score: ProposalScore
    executive_summary: str
    insights: list
    monitoring: MonitoringSnapshot
    generated_at: str = field(
        default_factory=lambda: datetime.now().strftime("%d %b %Y, %H:%M")
    )


# =============================================================================
#  DOMAIN KNOWLEDGE BASE  (unchanged)
# =============================================================================

BRANDS = {
    "cctv":       ["Hikvision", "Dahua", "Uniview", "Axis", "Bosch"],
    "networking": ["Cisco", "MikroTik", "TP-Link", "Ubiquiti", "HPE Aruba"],
    "pos":        ["Elo Touch", "Epson", "Zebra", "Star Micronics", "Honeywell"],
    "it":         ["Dell", "HPE", "Lenovo", "APC", "Synology"],
}

KZT_RATE = 450.0
TRANSLATIONS = {
    "Russian": {
        "This proposal covers": "Данное предложение охватывает",
        "Total estimated cost is": "Общая стоимость составляет",
        "within": "в пределах",
        "exceeding": "превышает",
        "budget": "бюджет",
        "The proposal scores": "Оценка предложения",
        "strong result": "высокий результат",
    },
    "Kazakh": {
        "This proposal covers": "Бұл ұсыныс қамтиды",
        "Total estimated cost is": "Жалпы құны",
        "within": "шегінде",
        "exceeding": "асып кетеді",
        "budget": "бюджет",
        "The proposal scores": "Ұсыныс бағасы",
        "strong result": "жақсы нәтиже",
    }
}
TYPE_LABELS = {
    "cctv":       "IP Surveillance",
    "networking": "Network Infrastructure",
    "pos":        "Point-of-Sale System",
    "it":         "IT Infrastructure",
}
# Wrap in t() during access

LABELS = {
    "English": {
        "New proposal": "New Proposal",
        "Client requirements": "Client Requirements",
        "System parameters": "System Parameters",
        "Client name": "Client Name",
        "Solution type": "Solution Type",
        "Space description": "Space Description",
        "Area (m²)": "Area (m²)",
        "Floors": "Floors",
        "Budget (USD)": "Budget (USD)",
        "Language": "Language",
        "AI model": "AI Model",
        "Currency": "Currency",
        "Risk tolerance": "Risk Tolerance",
        "Retention (days)": "Retention (days)",
        "Preferred brand": "Preferred Brand",
        "Contingency %": "Contingency %",
        "Include installation": "Include Installation",
        "Generate proposal": "Generate Proposal",
        "Dash Overview": "Dashboard Overview",
        "Summary": "Summary",
        "Total cost": "Total Cost",
        "Components": "Components",
        "Budget headroom": "Budget Headroom",
        "Composite score": "Composite Score",
        "BoM": "Bill of Materials",
        "Proposal Scores": "Proposal Scores",
        "Budget Breakdown": "Budget Breakdown",
        "Executive Summary": "Executive Summary",
        "Insights": "Insights",
        "AI Monitoring": "AI Monitoring",
        "Metric": "Metric",
        "Value": "Value",
        "Subtotal": "Subtotal",
        "Total Cost": "Total Cost",
        "Category": "Category",
        "Item": "Item",
        "Qty": "Qty",
        "Unit": "Unit",
        "Total": "Total",
        "BoM subtotal": "BoM Subtotal",
        "Contingency": "Contingency",
        "Client budget": "Client Budget",
        "Headroom": "Headroom",
        "Over budget": "Over Budget",
        "Fitness": "Fitness",
        "Risk": "Risk",
        "Scalability": "Scalability",
        "Composite Score": "Composite Score",
        "No gen": "No proposal generated yet",
        "Ready": "Ready to generate magic?",
        "Configure": "Configure your project requirements in the sidebar on the left and hit the button to see your proposal.",
        "Navigation": "Navigation",
        "Staff headcount": "Staff Headcount",
        "Concurrent users": "Concurrent Users",
        "Cashier stations": "Cashier Stations",
        "Workstations needed": "Workstations Needed",
        "Live": "Live",
        "On budget": "On Budget",
        "Clean": "Clean",
        "Review": "Review",
        "High": "High",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "within": "within",
        "exceeding": "exceeding",
        "incl.": "incl.",
        "contingency": "contingency",
        "total units": "total units",
        "flags": "flags",
        "flag": "flag",
        "No flags": "No flags",
        "Ready to deploy": "Ready to deploy",
        "Score": "Score",
        "Generated Proposal": "Generated Proposal",
        "Generated": "Generated",
        "review needed": "review needed",
        "below threshold": "below threshold",
        "IP Surveillance": "IP Surveillance",
        "Network Infrastructure": "Network Infrastructure",
        "Point-of-Sale System": "Point-of-Sale System",
        "IT Infrastructure": "IT Infrastructure",
        "Access Control System": "Access Control System",
        "Smart Office Automation": "Smart Office Automation",
        "Video Analytics (AI CCTV)": "Video Analytics (AI CCTV)",
        "Data Center Setup": "Data Center Setup",
        "Cloud Infrastructure Setup": "Cloud Infrastructure Setup",
        "Cybersecurity Solution": "Cybersecurity Solution",
        "VoIP / IP Telephony": "VoIP / IP Telephony",
        "Wi-Fi Optimization / Upgrade": "Wi-Fi Optimization / Upgrade",
        "Retail Analytics System": "Retail Analytics System",
        "Queue Management System": "Queue Management System",
        "Smart Retail (IoT Sensors)": "Smart Retail (IoT Sensors)",
        "Industrial Monitoring (IoT)": "Industrial Monitoring (IoT)",
        "Backup & Disaster Recovery": "Backup & Disaster Recovery",
        "Server Infrastructure Setup": "Server Infrastructure Setup",
        "Hybrid Cloud Solution": "Hybrid Cloud Solution",
        "Select the type of solution you want to generate": "Select the type of solution you want to generate",
    },
    "Russian": {
        "New proposal": "Новое предложение",
        "Client requirements": "Требования клиента",
        "System parameters": "Параметры системы",
        "Client name": "Название клиента",
        "Solution type": "Тип решения",
        "Space description": "Описание объекта",
        "Area (m²)": "Площадь (м²)",
        "Floors": "Этажи",
        "Budget (USD)": "Бюджет (USD)",
        "Language": "Язык",
        "AI model": "AI-модель",
        "Currency": "Валюта",
        "Risk tolerance": "Риск-толерантность",
        "Retention (days)": "Хранение (дней)",
        "Preferred brand": "Предпочт. бренд",
        "Contingency %": "Резерв %",
        "Include installation": "Включить монтаж",
        "Generate proposal": "Сформировать предложение",
        "Dash Overview": "Обзор дашборда",
        "Summary": "Сводка",
        "Total cost": "Общая стоимость",
        "Components": "Компоненты",
        "Budget headroom": "Бюджетный запас",
        "Composite score": "Итоговая оценка",
        "BoM": "Спецификация оборудования (BoM)",
        "Proposal Scores": "Оценки предложения",
        "Budget Breakdown": "Расшифровка бюджета",
        "Executive Summary": "Исполнительное резюме",
        "Insights": "Аналитика",
        "AI Monitoring": "AI мониторинг",
        "Metric": "Метрика",
        "Value": "Значение",
        "Subtotal": "Подитог",
        "Total Cost": "Итоговая цена",
        "Category": "Категория",
        "Item": "Товар",
        "Qty": "Кол-во",
        "Unit": "Цена ед.",
        "Total": "Всего",
        "BoM subtotal": "BoM подитог",
        "Contingency": "Резерв",
        "Client budget": "Бюджет клиента",
        "Headroom": "Запас",
        "Over budget": "Превышение бюджета",
        "Fitness": "Соответствие",
        "Risk": "Риски",
        "Scalability": "Масштабируемость",
        "Composite Score": "Общий балл",
        "No gen": "У вас пока нет предложений",
        "Ready": "Готовы создать магию?",
        "Configure": "Настройте требования к проекту в боковой панели слева и нажмите кнопку, чтобы увидеть результат.",
        "Navigation": "Навигация",
        "Staff headcount": "Кол-во сотрудников",
        "Concurrent users": "Одновременных польз.",
        "Cashier stations": "Кассовые места",
        "Workstations needed": "Рабочих мест",
        "Live": "В прямом эфире",
        "On budget": "В бюджете",
        "Clean": "Чисто",
        "Review": "Проверка",
        "High": "Высокий",
        "low": "низкий",
        "medium": "средний",
        "high": "высокий",
        "within": "в пределах",
        "exceeding": "превышает",
        "incl.": "вкл.",
        "contingency": "резерв",
        "total units": "всего ед.",
        "flags": "ошибки",
        "flag": "ошибка",
        "No flags": "Ошибок нет",
        "Ready to deploy": "Готово к внедрению",
        "Score": "Балл",
        "Generated Proposal": "Сформированное предложение",
        "Generated": "Сформировано",
        "review needed": "нужна проверка",
        "below threshold": "ниже порога",
        "IP Surveillance": "IP-Видеонаблюдение",
        "Network Infrastructure": "Сетевая инфраструктура",
        "Point-of-Sale System": "POS-система",
        "IT Infrastructure": "ИТ-инфраструктура",
        "Access Control System": "Система контроля доступа",
        "Smart Office Automation": "Автоматизация умного офиса",
        "Video Analytics (AI CCTV)": "Видеоаналитика (AI Видеонаблюдение)",
        "Data Center Setup": "Организация ЦОД",
        "Cloud Infrastructure Setup": "Настройка облачной инфраструктуры",
        "Cybersecurity Solution": "Решение по кибербезопасности",
        "VoIP / IP Telephony": "VoIP / IP-телефония",
        "Wi-Fi Optimization / Upgrade": "Оптимизация / Модернизация Wi-Fi",
        "Retail Analytics System": "Система аналитики ритейла",
        "Queue Management System": "Система управления очередью",
        "Smart Retail (IoT Sensors)": "Smart Retail (IoT-сенсоры)",
        "Industrial Monitoring (IoT)": "Промышленный мониторинг (IoT)",
        "Backup & Disaster Recovery": "Резервное копирование и восстановление",
        "Server Infrastructure Setup": "Настройка серверной инфраструктуры",
        "Hybrid Cloud Solution": "Гибридное облачное решение",
        "Select the type of solution you want to generate": "Выберите тип решения, который вы хотите сгенерировать",
    },
    "Kazakh": {
        "New proposal": "Жаңа ұсыныс",
        "Client requirements": "Клиент талаптары",
        "System parameters": "Жүйе параметрлері",
        "Client name": "Клиент атауы",
        "Solution type": "Шешім түрі",
        "Space description": "Нысан сипаттамасы",
        "Area (m²)": "Аумағы (м²)",
        "Floors": "Қабаттар",
        "Budget (USD)": "Бюджет (USD)",
        "Language": "Тіл",
        "AI model": "AI-модель",
        "Currency": "Валюта",
        "Risk tolerance": "Тәуекел деңгейі",
        "Retention (days)": "Сақтау (күн)",
        "Preferred brand": "Қалаулы бренд",
        "Contingency %": "Резерв %",
        "Include installation": "Орнатуды қосу",
        "Generate proposal": "Ұсынысты жасау",
        "Dash Overview": "Дашбордқа шолу",
        "Summary": "Жиынтық",
        "Total cost": "Жалпы құны",
        "Components": "Компоненттер",
        "Budget headroom": "Бюджет қоры",
        "Composite score": "Қорытынды баға",
        "BoM": "Жабдықтар тізімі (BoM)",
        "Proposal Scores": "Ұсыныс бағалары",
        "Budget Breakdown": "Бюджеттің егжей-тегжейі",
        "Executive Summary": "Қысқаша шолу",
        "Insights": "Инсайттар",
        "AI Monitoring": "AI мониторингі",
        "Metric": "Метрика",
        "Value": "Мән",
        "Subtotal": "Аралық сома",
        "Total Cost": "Жалпы сома",
        "Category": "Санат",
        "Item": "Тауар",
        "Qty": "Саны",
        "Unit": "Бірлік баға",
        "Total": "Барлығы",
        "BoM subtotal": "BoM аралық сомасы",
        "Contingency": "Резерв",
        "Client budget": "Клиент бюджеті",
        "Headroom": "Қор",
        "Over budget": "Бюджеттен асып кету",
        "Fitness": "Сәйкестік",
        "Risk": "Тәуекел",
        "Scalability": "Масштабталуы",
        "Composite Score": "Жалпы балл",
        "No gen": "Әзірге ұсыныстар жоқ",
        "Ready": "Сиқыр жасауға дайынсыз ба?",
        "Configure": "Сол жақтағы бүйірлік панельде жоба талаптарын реттеп, ұсынысты көру үшін түймені басыңыз.",
        "Navigation": "Навигация",
        "Staff headcount": "Қызметкер саны",
        "Concurrent users": "Бір мезгілдегі қолданушылар",
        "Cashier stations": "Кассалық орындар",
        "Workstations needed": "Жұмыс орны",
        "Live": "Тікелей",
        "On budget": "Бюджетте",
        "Clean": "Таза",
        "Review": "Тексеру",
        "High": "Жоғары",
        "low": "төмен",
        "medium": "орташа",
        "high": "жоғары",
        "within": "шегінде",
        "exceeding": "асып кетеді",
        "incl.": "қоса алғанда",
        "contingency": "резерв",
        "total units": "жалпы бірлік",
        "flags": "қателер",
        "flag": "қате",
        "No flags": "Қателер жоқ",
        "Ready to deploy": "Енгізуге дайын",
        "Score": "Балл",
        "Generated Proposal": "Жасалған ұсыныс",
        "Generated": "Жасалған",
        "review needed": "тексеру керек",
        "below threshold": "шектеуден төмен",
        "IP Surveillance": "IP-Бейнебақылау",
        "Network Infrastructure": "Желілік инфрақұрылым",
        "Point-of-Sale System": "POS-жүйесі",
        "IT Infrastructure": "АКТ-инфрақұрылым",
        "Access Control System": "Кіруді басқару жүйесі",
        "Smart Office Automation": "Ақылды кеңсені автоматтандыру",
        "Video Analytics (AI CCTV)": "Бейнеаналитика (AI Бейнебақылау)",
        "Data Center Setup": "Деректер орталығын (ЦОД) ұйымдастыру",
        "Cloud Infrastructure Setup": "Бұлтты инфрақұрылымды баптау",
        "Cybersecurity Solution": "Киберқауіпсіздік шешімі",
        "VoIP / IP Telephony": "VoIP / IP-телефония",
        "Wi-Fi Optimization / Upgrade": "Wi-Fi оңтайландыру / жаңарту",
        "Retail Analytics System": "Ритейл аналитика жүйесі",
        "Queue Management System": "Кезек басқару жүйесі",
        "Smart Retail (IoT Sensors)": "Smart Retail (IoT-сенсорлар)",
        "Industrial Monitoring (IoT)": "Өнеркәсіптік мониторинг (IoT)",
        "Backup & Disaster Recovery": "Резервтік көшіру және қалпына келтіру",
        "Server Infrastructure Setup": "Серверлік инфрақұрылымды баптау",
        "Hybrid Cloud Solution": "Гибридті бұлтты шешім",
        "Select the type of solution you want to generate": "Генерациялағыңыз келетін шешім түрін таңдаңыз",
    }
}

def t(label: str) -> str:
    lang = st.session_state.get("language", "English")
    return LABELS.get(lang, {}).get(label, label)

# =============================================================================
#  BUSINESS LOGIC — DOMAIN CALCULATORS  (unchanged)
# =============================================================================

def calculate_cctv_bom(req: ProposalRequest):
    indoor = max(1, round(req.area_sqm / 80))
    outdoor = req.floors * 2 + 2
    total_cams = indoor + outdoor
    nvr_channels = next(c for c in [8, 16, 32, 64] if c >= total_cams)
    bitrate_mbps = 2.0
    storage_tb = round(
        (total_cams * bitrate_mbps * 86_400 * req.retention_days) / 8 / 1_000_000, 1
    )
    storage_units = max(2, round(storage_tb / 8))
    poe_switches = max(1, round(total_cams / 12))
    brand = req.preferred_brand if req.preferred_brand != "Auto" else "Hikvision/Dahua"
    bom = [
        BOMLine("Camera",      f"IP Camera 4MP indoor — {brand}",  indoor,        85,  "H.265+, IR 30m"),
        BOMLine("Camera",      f"IP Camera 8MP outdoor — {brand}", outdoor,       140, "Weatherproof IP67"),
        BOMLine("Recorder",    f"{nvr_channels}-ch NVR — {brand}", 1,             420, f"Supports {nvr_channels} channels"),
        BOMLine("Switch",      "PoE switch 24-port gigabit",        poe_switches,  210, "802.3af/at"),
        BOMLine("Storage",     "HDD 8TB surveillance-grade",        storage_units, 95,  f"~{storage_tb} TB needed"),
        BOMLine("Power",       "UPS 1500VA rack",                   1,             180, "Runtime ~40 min"),
        BOMLine("Accessories", "Conduit, mounts, cabling",          total_cams,    12,  "Per camera estimate"),
    ]
    if req.include_installation:
        bom.append(BOMLine("Labor", "Installation & commissioning", total_cams, 18, "Per camera, incl. config"))
    return bom


def calculate_networking_bom(req: ProposalRequest):
    ap_by_area  = round(req.area_sqm / 150)
    ap_by_users = round(req.users_or_cashiers / 25)
    ap_count    = max(ap_by_area, ap_by_users, 1)
    raw_ports   = req.users_or_cashiers + ap_count
    switch_24   = max(1, round(raw_ports * 1.2 / 24))
    brand = req.preferred_brand if req.preferred_brand != "Auto" else "Cisco/MikroTik"
    bom = [
        BOMLine("Wireless",  f"Wi-Fi 6 AP — {brand}",          ap_count,                        190, "802.11ax, dual-band"),
        BOMLine("Switching", "24-port gigabit PoE switch",       switch_24,                      320, "PoE budget 380W"),
        BOMLine("Routing",   f"Firewall/router — {brand}",       1,                              480, "UTM, up to 1 Gbps"),
        BOMLine("Cabling",   "Cat6 UTP patch cables 3m",         req.users_or_cashiers+ap_count, 8,   ""),
        BOMLine("Power",     "UPS 2000VA",                        1,                              220, "Protects core stack"),
        BOMLine("Rack",      '19" open rack 12U',                 1,                              150, "With patch panel"),
    ]
    if req.include_installation:
        bom.append(BOMLine("Labor", "Network setup & SSID config", 1, 800, "Flat rate"))
    return bom


def calculate_pos_bom(req: ProposalRequest):
    cashiers = max(1, req.users_or_cashiers)
    brand = req.preferred_brand if req.preferred_brand != "Auto" else "Elo Touch / Epson"
    bom = [
        BOMLine("Terminal",   f'Touch POS terminal 15" — {brand}', cashiers,              580, "i5, 8GB RAM, SSD"),
        BOMLine("Peripheral", "Thermal receipt printer 80mm",        cashiers,              95,  "USB + LAN"),
        BOMLine("Peripheral", "Barcode scanner 2D",                  cashiers,              55,  "USB, omnidirectional"),
        BOMLine("Peripheral", "Cash drawer 24V",                     cashiers,              40,  "RJ11 trigger"),
        BOMLine("Peripheral", "Card reader (contactless)",           cashiers,              70,  "EMV, NFC"),
        BOMLine("Network",    "8-port unmanaged switch",             max(1,cashiers//8),    45,  "For terminal segment"),
        BOMLine("Software",   "POS licence — annual",                cashiers,              120, "Per terminal/year"),
    ]
    if cashiers > 4:
        bom.append(BOMLine("Server", "Local POS server Mini-PC", 1, 680, "i7, 16GB, 512 SSD"))
    if req.include_installation:
        bom.append(BOMLine("Labor", "POS setup, config & training", cashiers, 60, "Per terminal"))
    return bom


def calculate_it_bom(req: ProposalRequest):
    users     = max(1, req.users_or_cashiers)
    cpu_cores = max(4, round(users / 5) * 2)
    ram_gb    = max(16, round(users * 4 / 16) * 16)
    brand = req.preferred_brand if req.preferred_brand != "Auto" else "Dell / HPE"
    bom = [
        BOMLine("Workstation", f"Business desktop — {brand}", users, 620, "i5, 16GB, 512 SSD"),
        BOMLine("Monitor",     '24" IPS monitor',              users, 180, "Full HD, HDMI"),
        BOMLine("Server",      f"Tower server — {brand}",      1,     1800, f"{cpu_cores}-core, {ram_gb}GB RAM"),
        BOMLine("Storage",     "NAS 4-bay — Synology",         1,     560,  "Backup + file share"),
        BOMLine("Storage",     "HDD 4TB NAS-grade",            4,     75,   "For NAS"),
        BOMLine("Network",     "24-port managed switch",        1,     300,  "VLAN-ready"),
        BOMLine("Power",       "UPS 3000VA rack — APC",         1,     480,  "Protects server + network"),
        BOMLine("Software",    "Windows Server 2022 Std",       1,     850,  "Incl. 5 CALs"),
    ]
    if req.include_installation:
        bom.append(BOMLine("Labor", "Server setup, AD, domain join", 1, 1200, "Flat rate"))
    return bom


# =============================================================================
#  SCORING ENGINE  (unchanged)
# =============================================================================

def score_proposal(req: ProposalRequest, bom: list) -> ProposalScore:
    total_bom       = sum(l.total for l in bom)
    total_with_cont = total_bom * (1 + req.contingency_pct / 100)
    ratio           = total_with_cont / req.budget_usd

    if ratio <= 0.80:   cost_score = 78
    elif ratio <= 0.95: cost_score = 95
    elif ratio <= 1.00: cost_score = 88
    elif ratio <= 1.10: cost_score = 72
    else:               cost_score = max(30, round(100 - (ratio - 1) * 200))

    risk_base = 90
    if len(req.space_description) < 20:                              risk_base -= 15
    if req.users_or_cashiers == 0:                                   risk_base -= 10
    if req.solution_type == "cctv" and req.retention_days < 14:     risk_base -= 8
    if req.risk_tolerance == "high":                                 risk_base += 5
    elif req.risk_tolerance == "low":                                risk_base -= 5
    risk_score = max(30, min(100, risk_base))

    scale_base = 80
    if req.solution_type == "cctv":
        total_cams   = round(req.area_sqm / 80) + req.floors * 2 + 2
        nvr_channels = next(c for c in [8, 16, 32, 64] if c >= total_cams)
        if nvr_channels - total_cams >= 4: scale_base += 10
    if req.include_installation: scale_base += 5
    scale_score = min(100, scale_base)

    return ProposalScore(cost=cost_score, risk=risk_score, scalability=scale_score)


# =============================================================================
#  EXECUTIVE SUMMARY GENERATOR  (unchanged)
# =============================================================================

def generate_executive_summary(req: ProposalRequest, bom: list, score: ProposalScore) -> str:
    total        = sum(l.total for l in bom)
    grand_total  = total * (1 + req.contingency_pct / 100)
    headroom     = req.budget_usd - grand_total
    headroom_pct = round(abs(headroom / req.budget_usd) * 100, 1)
    label        = TYPE_LABELS.get(req.solution_type, req.solution_type)
    sym          = "$" if req.currency == "USD" else "₸"
    rate         = 1 if req.currency == "USD" else KZT_RATE
    fmt          = lambda v: f"{sym}{v * rate:,.0f}"

    lines = [
        f"This proposal covers a full {label.lower()} solution for **{req.client_name}**, "
        f"designed for a {req.area_sqm}\u00a0m\u00b2 facility across {req.floors} floor(s)."
    ]

    if req.solution_type == "cctv":
        cameras = round(req.area_sqm / 80) + req.floors * 2 + 2
        lines.append(
            f"The recommended architecture deploys **{cameras}\u00a0cameras** — a mix of indoor 4MP "
            f"and outdoor 8MP units — supported by an NVR with {req.retention_days}-day recording retention."
        )
    elif req.solution_type == "networking":
        aps = max(round(req.area_sqm / 150), round(req.users_or_cashiers / 25), 1)
        lines.append(
            f"The design provides **{aps}\u00a0Wi-Fi 6 access points** and managed switching "
            f"infrastructure supporting up to {req.users_or_cashiers} concurrent users."
        )
    elif req.solution_type == "pos":
        lines.append(
            f"The solution covers **{req.users_or_cashiers}\u00a0full POS terminal sets** (touch screen, "
            f"printer, scanner, cash drawer, card reader) with software licensing."
        )
    elif req.solution_type == "it":
        lines.append(
            f"The solution provisions **{req.users_or_cashiers}\u00a0workstations**, a central server, "
            f"NAS backup, and supporting infrastructure."
        )

    lines.append(
        f"Total estimated cost is **{fmt(grand_total)}** (incl. {req.contingency_pct}% contingency), "
        f"{'within' if headroom >= 0 else 'exceeding'} the {fmt(req.budget_usd)} budget "
        f"{'with a ' + str(headroom_pct) + '% margin' if headroom >= 0 else 'by ' + str(headroom_pct) + '%'}."
    )

    if score.composite >= 85:
        lines.append(
            f"The proposal scores **{score.composite}/100** — a strong result reflecting "
            f"good budget fit, low risk, and room to scale."
        )
    elif score.composite >= 70:
        lines.append(
            f"The proposal scores **{score.composite}/100**. One or more dimensions require "
            f"review before client submission — see the Insights panel."
        )
    else:
        lines.append(
            f"The proposal scores **{score.composite}/100**, which is below threshold. "
            f"Review flagged risks and re-scope before submitting."
        )

    return " ".join(lines)

def translate_text(text: str, lang: str) -> str:
    if lang == "English":
        return text

    dictionary = TRANSLATIONS.get(lang, {})

    for en, translated in dictionary.items():
        text = text.replace(en, translated)

    return text

# =============================================================================
#  INSIGHTS ENGINE  (unchanged)
# =============================================================================

def generate_insights(req: ProposalRequest, bom: list, score: ProposalScore) -> list:
    total       = sum(l.total for l in bom)
    grand_total = total * (1 + req.contingency_pct / 100)
    headroom    = req.budget_usd - grand_total
    insights    = []

    if headroom < 0:
        insights.append(Insight("error", "Over budget",
            f"BoM + contingency exceeds budget by ${abs(headroom):,.0f}. "
            "Consider reducing scope or negotiating pricing."))
    elif headroom < req.budget_usd * 0.05:
        insights.append(Insight("warning", "Thin budget margin",
            f"Only ${headroom:,.0f} ({round(headroom/req.budget_usd*100,1)}%) remains. "
            "Any scope addition will breach budget."))
    else:
        insights.append(Insight("success", "Budget well-fitted",
            f"${headroom:,.0f} headroom remaining. Proposal is financially sound."))

    if req.solution_type == "cctv":
        total_cams   = round(req.area_sqm / 80) + req.floors * 2 + 2
        nvr_channels = next(c for c in [8, 16, 32, 64] if c >= total_cams)
        spare = nvr_channels - total_cams
        if spare >= 4:
            insights.append(Insight("success", f"{spare} spare NVR channels",
                "Client can add cameras later without replacing the recorder."))
        if req.retention_days < 14:
            insights.append(Insight("warning", "Short retention period",
                f"{req.retention_days} days may not meet insurance or compliance requirements. "
                "Recommend minimum 14–30 days for retail."))
        if any("UPS" in l.item for l in bom):
            insights.append(Insight("info", "UPS runtime not verified",
                "Estimated load is based on camera count. "
                "Verify actual site wattage with electrician."))

    if req.solution_type == "networking" and req.users_or_cashiers > 100:
        insights.append(Insight("warning", "High user density",
            "Consider redundant uplinks and managed QoS to maintain performance."))

    if req.solution_type == "it":
        insights.append(Insight("info", "Backup strategy",
            "NAS-based backup is included. Recommend off-site or cloud replication "
            "for D2C resilience."))

    if len(req.space_description) < 25:
        insights.append(Insight("warning", "Vague space description",
            "Short description increases estimation uncertainty. "
            "Ask client for floor plan."))

    if score.scalability >= 85:
        insights.append(Insight("success", "Good scalability headroom",
            "Solution architecture supports future expansion without full redesign."))
    elif score.scalability < 70:
        insights.append(Insight("warning", "Limited scalability",
            "Current spec leaves little room to grow. "
            "Consider upsizing key components."))

    return insights


# =============================================================================
#  MONITORING MOCK  (unchanged)
# =============================================================================

def generate_monitoring(req: ProposalRequest) -> MonitoringSnapshot:
    base_in  = {"cctv": 820, "networking": 760, "pos": 680, "it": 940}
    base_out = {"cctv": 1100, "networking": 980, "pos": 890, "it": 1340}
    in_tok  = base_in.get(req.solution_type, 800)  + random.randint(-50, 80)
    out_tok = base_out.get(req.solution_type, 1000) + random.randint(-80, 120)
    errors  = []
    if len(req.space_description) < 15:
        errors.append("Low-confidence input: space description too short")
    confidence = min(97, max(72, 100 - len(errors) * 12 + random.randint(-3, 3)))
    return MonitoringSnapshot(
        api_calls=1,
        input_tokens=in_tok,
        output_tokens=out_tok,
        latency_ms=random.randint(1800, 3400),
        hallucination_flags=0,
        confidence_pct=confidence,
        errors=errors,
    )


# =============================================================================
#  PROPOSAL ORCHESTRATOR  (unchanged)
# =============================================================================

def generate_proposal(req: ProposalRequest) -> ProposalResult:
    router = {
        "cctv":       calculate_cctv_bom,
        "networking": calculate_networking_bom,
        "pos":        calculate_pos_bom,
        "it":         calculate_it_bom,
    }
    bom = router[req.solution_type](req)
    score = score_proposal(req, bom)
    summary = generate_executive_summary(req, bom, score)
    summary = translate_text(summary, req.language)
    insights = generate_insights(req, bom, score)
    monitoring = generate_monitoring(req)
    return ProposalResult(
        request=req, bom=bom, score=score,
        executive_summary=summary, insights=insights, monitoring=monitoring,
    )


# =============================================================================
#  DESIGN SYSTEM — CSS
#
#  Decisions:
#    • Page background: #F5F5F3 (warm off-white, not pure white — reduces glare)
#    • Card background: #FFFFFF with 1px solid #E8E7E3 border
#    • Metric tiles: #FAFAF8 — slightly warmer than cards to create hierarchy
#    • Typography: DM Sans (clean, narrow, professional — not Inter/Roboto)
#    • Two weights: 400 body, 500 for labels and values
#    • Status colours: semantic only (green/amber/red) — never decorative
#    • No shadows, no gradients, no glow effects
# =============================================================================

CSS = """
<style>
/* ── Global Styles ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f8fafc !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}

[data-testid="stHeader"] {
    background-color: rgba(248, 250, 252, 0) !important;
}

/* ── Sidebar Design (SaaS Modern) ──────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #e0f2fe 100%) !important;
    box-shadow: 4px 0 15px rgba(0,0,0,0.03) !important;
    border: none !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #1f2937 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #1e293b !important;
}

/* Container for sidebar grouping */
.sidebar-container {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(226, 232, 240, 0.8);
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 0 2rem 0;
}

.sidebar-logo-text {
    font-size: 1.5rem;
    font-weight: 800;
    color: #4f46e5;
    letter-spacing: -0.02em;
}

/* ── Cards ──────────────────────────────────────────────────────────── */
.ai-card {
    background: #ffffff;
    border: none;
    border-radius: 24px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.1);
}

.ai-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px -4px rgba(0, 0, 0, 0.08);
}

.ai-card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1e293b;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* ── Metrics & KPIs ─────────────────────────────────────────────────── */
.ai-metric {
    background: #ffffff;
    border: 1px solid #f1f5f9;
    border-radius: 24px;
    padding: 1.5rem;
    text-align: left;
    transition: all 0.3s ease;
}

.ai-metric:hover {
    border-color: #e2e8f0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.ai-metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.ai-metric-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: #1e293b;
    line-height: 1.2;
}

.ai-metric-sub {
    font-size: 0.85rem;
    margin-top: 0.5rem;
    color: #94a3b8;
}

/* ── Modern Table ───────────────────────────────────────────────────── */
.bom-table {
    width: 100%;
    border-spacing: 0 12px;
    border-collapse: separate;
}

.bom-table th {
    font-size: 0.75rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    padding: 0 1rem;
    text-align: left;
}

.bom-table td {
    background: #f8fafc;
    padding: 1.25rem 1rem;
    font-size: 0.9rem;
    color: #334155;
}

.bom-table tr td:first-child { border-radius: 16px 0 0 16px; }
.bom-table tr td:last-child { border-radius: 0 16px 16px 0; }

.subtotal-container {
    margin-top: 1rem;
    padding: 1.5rem;
    background: #f8fafc;
    border-radius: 20px;
}

.subtotal-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
}

.subtotal-row.total {
    border-top: 1px solid #e2e8f0;
    margin-top: 0.5rem;
    padding-top: 1rem;
    font-weight: 800;
    font-size: 1.1rem;
    color: #1e293b;
}

/* ── Buttons ─────────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 16px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    height: auto !important;
}

.stButton > button[kind="primary"] {
    background: #4f46e5 !important;
    border: none !important;
    box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.3) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.4) !important;
    background: #4338ca !important;
}

/* ── Inputs (Fixed Visibility) ───────────────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    border-radius: 14px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
    background-color: #ffffff !important;
    color: #111111 !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #94a3b8 !important;
}

.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid #e2e8f0 !important;
    background-color: #ffffff !important;
    color: #111111 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #1f2937 !important;
}

/* ── Score Bars ─────────────────────────────────────────────────────── */
.score-track {
    height: 10px;
    background: #f1f5f9;
    border-radius: 10px;
    margin: 8px 0;
}

.score-fill {
    height: 100%;
    border-radius: 10px;
}

/* ── Sidebar Redesign & Soften ──────────────────────────────────────── */
[data-testid="stSidebar"] label {
    color: #475569 !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    margin-bottom: 0.4rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Fix sidebar slider */
[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"] {
    background: #4f46e5 !important;
}

/* ── Generic Table Style ───────────────────────────────────────────── */
.modern-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
}
.modern-table td, .modern-table th {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.9rem;
}
.modern-table th {
    background: #f8fafc;
    text-align: left;
    color: #64748b;
    font-weight: 700;
}
.modern-table tr:last-child td {
    border-bottom: none;
}

/* ── Animations ─────────────────────────────────────────────────────── */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.ai-card, .ai-metric {
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
"""


# =============================================================================
#  UI HELPER FUNCTIONS
# =============================================================================

def H(content: str):
    """Shorthand: render raw HTML markup."""
    st.markdown(content, unsafe_allow_html=True)


def section(label: str):
    """Renders a small all-caps section label above a card group."""
    H(f'<div class="ai-section">{label}</div>')


def badge(text: str, kind: str = "neutral") -> str:
    """Returns an inline badge HTML string (used inside larger HTML blocks)."""
    return f'<span class="ai-badge {kind}">{text}</span>'


def score_color(v: int) -> str:
    """Maps a score value to a semantic colour."""
    if v >= 80: return "#10B981" # Emerald-500
    if v >= 65: return "#F59E0B" # Amber-500
    return "#EF4444" # Red-500


def score_bar_html(label: str, value: int, is_composite: bool = False) -> str:
    """Returns HTML string for a labelled score bar."""
    color = score_color(value)
    cls   = "score-row score-composite" if is_composite else "score-row"
    return f"""
    <div class="{cls}">
      <div class="score-meta">
        <span class="lbl">{label}</span>
        <span class="val">{value}</span>
      </div>
      <div class="score-track">
        <div class="score-fill" style="width:{value}%;background:{color}"></div>
      </div>
    </div>"""

def render_score_bar(label: str, value: int, is_composite: bool = False):
    """Renders a labelled score bar (thin wrapper kept for compatibility)."""
    H(score_bar_html(label, value, is_composite))


def bom_table_html(bom: list, currency: str) -> str:
    """
    Returns HTML string for the Bill of Materials table.
    Using a pure HTML table gives us precise column-width and typography control.
    """
    rate = KZT_RATE if currency == "KZT" else 1.0
    sym  = "₸" if currency == "KZT" else "$"
    fmt  = lambda v: f"{sym}{v * rate:,.0f}"

    rows = ""
    for line in bom:
        note_html = (
            f"<br><span style='font-size:10px;color:#C4C3BF'>{line.notes}</span>"
            if line.notes else ""
        )
        rows += f"""
        <tr>
          <td class="cat">{line.category}</td>
          <td>{line.item}{note_html}</td>
          <td class="r mono muted">&times;{line.qty}</td>
          <td class="r mono muted">{fmt(line.unit_price)}</td>
          <td class="r mono">{fmt(line.total)}</td>
        </tr>"""

    subtotal = sum(l.total for l in bom)
    return f"""
    <table class="bom-table">
      <thead>
        <tr>
          <th>{t("Category")}</th><th>{t("Item")}</th>
          <th class="r">{t("Qty")}</th><th class="r">{t("Unit")}</th><th class="r">{t("Total")}</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="subtotal-container">
      <div class="subtotal-row">
        <span>{t("Subtotal")}</span>
        <span>{fmt(subtotal)}</span>
      </div>
      <div class="subtotal-row total">
        <span>{t("Total Cost")}</span>
        <span>{fmt(subtotal)}</span>
      </div>
    </div>"""

def render_bom_table(bom: list, currency: str):
    """Renders the BoM table (thin wrapper kept for compatibility)."""
    H(bom_table_html(bom, currency))


def budget_breakdown_html(total: float, contingency_v: float, grand_total: float,
                          budget: float, contingency_pct: int, currency: str) -> str:
    """Returns HTML string for the budget breakdown table."""
    rate     = KZT_RATE if currency == "KZT" else 1.0
    sym      = "₸" if currency == "KZT" else "$"
    fmt      = lambda v: f"{sym}{v * rate:,.0f}"
    headroom = budget - grand_total
    sign     = "+" if headroom >= 0 else "–"
    color    = "#10B981" if headroom >= 0 else "#EF4444"
    label    = t("Headroom") if headroom >= 0 else t("Over budget")
    return f"""
    <table class="budget-table">
      <tr><td>{t("BoM subtotal")}</td><td class="r">{fmt(total)}</td></tr>
      <tr><td>{t("Contingency")} ({contingency_pct}%)</td><td class="r">{fmt(contingency_v)}</td></tr>
      <tr class="total"><td>{t("Total Cost")}</td><td class="r">{fmt(grand_total)}</td></tr>
      <tr><td>{t("Client budget")}</td><td class="r">{fmt(budget)}</td></tr>
      <tr>
        <td style="color:{color};font-weight:500">{label}</td>
        <td class="r" style="color:{color};font-weight:500;font-family:'Plus Jakarta Sans',monospace">
          {sign}{fmt(abs(headroom))}
        </td>
      </tr>
    </table>"""

def render_budget_breakdown(total: float, contingency_v: float, grand_total: float,
                             budget: float, contingency_pct: int, currency: str):
    """Renders budget breakdown (thin wrapper kept for compatibility)."""
    H(budget_breakdown_html(total, contingency_v, grand_total, budget, contingency_pct, currency))


def insight_html(insight: Insight) -> str:
    """Returns HTML string for a single insight row."""
    dot_map = {"success": "#10B981", "warning": "#F59E0B", "error": "#EF4444", "info": "#6366F1"}
    dot = dot_map.get(insight.level, "#94A3B8")
    return f"""
    <div class="insight-row">
      <div class="insight-dot" style="background:{dot}"></div>
      <div>
        <div class="insight-title">{insight.title}</div>
        <div class="insight-detail">{insight.detail}</div>
      </div>
    </div>"""

def render_insight(insight: Insight):
    """Renders an insight row (thin wrapper kept for compatibility)."""
    H(insight_html(insight))


def monitoring_html(mon: MonitoringSnapshot) -> str:
    """Returns HTML string for all monitoring rows."""
    out = f"""
    <table class="modern-table">
      <thead>
        <tr><th>{t("Metric")}</th><th>{t("Value")}</th></tr>
      </thead>
      <tbody>
        <tr><td>{t("API Calls")}</td><td>{mon.api_calls} {badge(t("Live"), "info")}</td></tr>
        <tr><td>{t("Input Tokens")}</td><td>{mon.input_tokens:,}</td></tr>
        <tr><td>{t("Output Tokens")}</td><td>{mon.output_tokens:,}</td></tr>
        <tr><td>{t("Total Tokens")}</td><td>{mon.total_tokens:,}</td></tr>
        <tr><td>{t("Est. API Cost")}</td><td>${mon.estimated_cost_usd:.4f} {badge(t("On budget"), "ok")}</td></tr>
        <tr><td>{t("Response Latency")}</td><td>{mon.latency_ms} ms</td></tr>
        <tr><td>{t("AI Confidence")}</td><td>{mon.confidence_pct}% {badge(t("High"), "ok") if mon.confidence_pct >= 80 else badge(t("Review"), "warn")}</td></tr>
      </tbody>
    </table>"""

    if mon.errors:
        err_html = "".join(
            f'<div class="ai-badge warn" style="display:block;margin-top:5px;'
            f'border-radius:6px;font-size:11px">&#9651; {e}</div>'
            for e in mon.errors
        )
        out += f"<div style='margin-top:10px'>{err_html}</div>"
    return out

def render_monitoring(mon: MonitoringSnapshot):
    """Renders monitoring rows (thin wrapper kept for compatibility)."""
    H(monitoring_html(mon))


# =============================================================================
#  INPUT PANEL
# =============================================================================

def render_input_panel() -> Optional[ProposalRequest]:

    # ── Init session state defaults (only on first run) ──────────────── #
    defaults = {
        "client_name": "TechRetail LLP",
        "solution_type": "cctv",
        "space_description": "3-floor retail store, ~1800 m² total, outdoor parking, 2 entrances",
        "area_sqm": 1800,
        "floors": 3,
        "users": 12,
        "budget": 12000,
        "model": "claude-sonnet-4-6",
        "language": "English",
        "currency": "USD",
        "risk": "medium",
        "retention": 30,
        "brand": "Auto",
        "contingency": 15,
        "installation": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Read language once at the top so all labels on THIS run are correct.
    # (Streamlit will rerun after language selectbox changes, updating everything.)
    lang = st.session_state.get("language", "English")

    # ── Sidebar Container: New Proposal ────────────────────────────────── #
    H('<div class="sidebar-container">')
    H(f'<div style="color:#1e293b; font-size:1.1rem; font-weight:700; margin-bottom:1.5rem; display:flex; align-items:center; gap:10px;">'
      f'<span>✨</span> {t("New proposal")}</div>')

    # ── Group 1: Client Requirements ───────────────────────────────────── #
    H(f'<div style="color:#64748b; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;">'
      f'{t("Client requirements")}</div>')

    st.text_input(
        t("Client name"),
        key="client_name",
    )

    # Define grouped options
    options_map = {
        "📹 Surveillance": [
            "IP Surveillance",
            "Video Analytics (AI CCTV)",
            "Access Control System"
        ],
        "🌐 Networking": [
            "Network Infrastructure",
            "Wi-Fi Optimization / Upgrade",
            "VoIP / IP Telephony"
        ],
        "💼 Business Systems": [
            "Point-of-Sale System",
            "Queue Management System",
            "Retail Analytics System",
            "Smart Retail (IoT Sensors)"
        ],
        "☁️ Cloud & IT": [
            "IT Infrastructure",
            "Data Center Setup",
            "Cloud Infrastructure Setup",
            "Industrial Monitoring (IoT)",
            "Backup & Disaster Recovery",
            "Server Infrastructure Setup",
            "Hybrid Cloud Solution",
            "Smart Office Automation"
        ],
        "🔐 Security": [
            "Cybersecurity Solution"
        ]
    }
    
    # Flatten for selectbox with emojis
    all_options = []
    logic_mapping = {}
    for group, items in options_map.items():
        emoji = group.split()[0]
        for item in items:
            prefixed = f"{emoji} {item}"
            all_options.append(prefixed)
            # Internal mapping
            logic_key = "cctv"
            if group == "🌐 Networking": logic_key = "networking"
            elif group == "💼 Business Systems": logic_key = "pos"
            elif group == "☁️ Cloud & IT" or group == "🔐 Security": logic_key = "it"
            logic_mapping[prefixed] = logic_key

    # Find current selection index
    current_human = next((k for k, v in logic_mapping.items() if v == st.session_state.solution_type), all_options[0])

    selected_human = st.selectbox(
        t("Solution type"),
        options=all_options,
        index=all_options.index(current_human),
        format_func=lambda x: f"{x.split(' ', 1)[0]} {t(x.split(' ', 1)[1])}",
        key="selected_human_type",
    )
    
    # Map back to internal logic key
    st.session_state.solution_type = logic_mapping[selected_human]

    H(f'<div style="font-size: 0.75rem; color: #64748b; margin-top: -0.8rem; margin-bottom: 1.5rem; padding-left: 0.2rem;">'
      f'{t("Select the type of solution you want to generate")}</div>')

    st.text_area(
        t("Space description"),
        key="space_description",
        height=80,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.number_input(t("Area (m²)"), 20, 50000, key="area_sqm")
    with c2:
        st.number_input(t("Floors"), 1, 30, key="floors")

    # Dynamic label driven by current solution type (already stored in session_state)
    user_label_key = {
        "cctv":       "Staff headcount",
        "networking": "Concurrent users",
        "pos":        "Cashier stations",
        "it":         "Workstations needed",
    }[st.session_state.solution_type]
    st.number_input(t(user_label_key), 1, 500, key="users")

    st.slider(t("Budget (USD)"), 1000, 100000, key="budget")

    # ── Group 2: System Parameters ─────────────────────────────────────── #
    H(f'<div style="color:#64748b; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1.5rem; margin-top:1.5rem;">'
      f'{t("System parameters")}</div>')

    c3, c4 = st.columns(2)
    with c3:
        st.selectbox(
            t("AI model"),
            options=["claude-sonnet-4-6", "claude-opus-4-6"],
            index=["claude-sonnet-4-6", "claude-opus-4-6"].index(st.session_state.model),
            key="model",
        )
    with c4:
        st.selectbox(
            t("Language"),
            options=["English", "Russian", "Kazakh"],
            index=["English", "Russian", "Kazakh"].index(st.session_state.language),
            key="language",
        )

    c5, c6 = st.columns(2)
    with c5:
        st.selectbox(
            t("Currency"),
            options=["USD", "KZT"],
            index=["USD", "KZT"].index(st.session_state.currency),
            key="currency",
        )
    with c6:
        st.selectbox(
            t("Risk tolerance"),
            options=["low", "medium", "high"],
            index=["low", "medium", "high"].index(st.session_state.risk),
            format_func=lambda x: t(x),
            key="risk",
        )

    c7, c8 = st.columns(2)
    with c7:
        st.number_input(t("Retention (days)"), 7, 365, key="retention")
    with c8:
        # Compute safe brand index locally — never mutate session_state during render
        brand_opts = ["Auto"] + BRANDS.get(st.session_state.solution_type, [])
        brand_safe = st.session_state.brand if st.session_state.brand in brand_opts else "Auto"
        st.selectbox(
            t("Preferred brand"),
            options=brand_opts,
            index=brand_opts.index(brand_safe),
            key="brand",
        )

    c9, c10 = st.columns(2)
    with c9:
        st.slider(t("Contingency %"), 5, 30, key="contingency")
    with c10:
        # Label-above pattern keeps vertical rhythm without spacer hacks
        st.write("")
        st.checkbox(t("Include installation"), key="installation")

    generate = st.button(
        t("Generate proposal"),
        type="primary",
        use_container_width=True,
    )

    H("</div>")  # close sidebar-container

    # ── Build ProposalRequest on generate click ────────────────────────── #
    if generate:
        if not st.session_state.client_name.strip():
            st.error("Client name is required.")
            return None

        return ProposalRequest(
            client_name=st.session_state.client_name,
            solution_type=st.session_state.solution_type,
            space_description=st.session_state.space_description,
            area_sqm=st.session_state.area_sqm,
            floors=st.session_state.floors,
            users_or_cashiers=st.session_state.users,
            budget_usd=st.session_state.budget,
            retention_days=st.session_state.retention,
            risk_tolerance=st.session_state.risk,
            preferred_brand=st.session_state.brand,
            currency=st.session_state.currency,
            language=st.session_state.language,
            contingency_pct=st.session_state.contingency,
            include_installation=st.session_state.installation,
            model_id=st.session_state.model,
        )

    return None

# =============================================================================
#  RESULTS DASHBOARD
# =============================================================================

def render_results(result: ProposalResult):
    """
    Right column — six clearly separated sections:

      Header bar        client + timestamp + status badges
      1. Summary        4 metric tiles (cost, items, headroom, score)
      2. BoM + Scores   2-col: table (60%) | score bars + budget (40%)
      3. Executive summary  full-width narrative card
      4. Insights       left 50%
      5. Monitoring     right 50%
      6. Footer

    Design decisions:
      - Section titles are INSIDE cards as .ai-card-title — no floating labels
      - White cards provide clear visual grouping
      - Metric tiles use a distinct #FAFAF8 background to create hierarchy
      - Executive summary card has more padding + larger line-height
      - Score bars use semantic colour only (green/amber/red by value)
      - Budget breakdown table lives under the score card (same column)
      - Footer is separated by a top border, not just margin
    """
    req   = result.request
    bom   = result.bom
    score = result.score
    mon   = result.monitoring

    total         = sum(l.total for l in bom)
    contingency_v = total * (req.contingency_pct / 100)
    grand_total   = total + contingency_v
    headroom      = req.budget_usd - grand_total
    rate          = KZT_RATE if req.currency == "KZT" else 1.0
    sym           = "₸" if req.currency == "KZT" else "$"
    fmt           = lambda v: f"{sym}{v * rate:,.0f}"
    type_label    = t(TYPE_LABELS.get(req.solution_type, req.solution_type))
    flag_ct       = sum(1 for i in result.insights if i.level in ("warning", "error"))

    # ── Header bar ────────────────────────────────────────────────────── #
    score_kind = "ok" if score.composite >= 80 else "warn" if score.composite >= 65 else "error"
    flag_badge = (
        badge(f"{flag_ct} {t('flags') if flag_ct != 1 else t('flag')}", "warn")
        if flag_ct else badge(t("No flags"), "ok")
    )
    H(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                padding: 1.5rem 2rem; background: white; border-bottom: 1px solid #f1f5f9; 
                margin-bottom: 2rem; border-radius: 0 0 24px 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
      <div>
        <div style="font-size:1.25rem;font-weight:800;color:#1e293b;letter-spacing:-0.02em">
          {req.client_name}
          <span style="color:#6366f1;font-weight:600;font-size:1rem"> &middot; {type_label}</span>
        </div>
        <div style="font-size:0.8rem;color:#94a3b8;margin-top:4px; font-weight:500;">
          {t("Generated")} {result.generated_at} &middot; {req.model_id}
        </div>
      </div>
      <div style="display:flex;gap:10px;align-items:center">
        {badge(f"{t('Score')} {score.composite}/100", score_kind)}
        {flag_badge}
        {badge(t("Ready to deploy"), "info")}
      </div>
    </div>""")

    # ── 1. Summary metrics ────────────────────────────────────────────── #
    # Section title lives inside the metric group — no floating label
    H(f'<div style="padding: 0 2rem;"><div class="ai-section" style="margin-bottom:1rem; color: #64748b; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;">{t("Dash Overview")}</div>')
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        H(f"""<div class="ai-metric">
                <div class="ai-metric-label">💰 {t("Total cost")}</div>
                <div class="ai-metric-value">{fmt(grand_total)}</div>
                <div class="ai-metric-sub">{t("incl.")} {req.contingency_pct}% {t("contingency")}</div>
              </div>""")
    with m2:
        units = sum(l.qty for l in bom)
        H(f"""<div class="ai-metric">
                <div class="ai-metric-label">📦 {t("Components")}</div>
                <div class="ai-metric-value">{len(bom)}</div>
                <div class="ai-metric-sub">{units} {t("total units")}</div>
              </div>""")
    with m3:
        sub_cls = "ok" if headroom >= 0 else "over"
        sub_txt = t("within") if headroom >= 0 else t("exceeding")
        H(f"""<div class="ai-metric">
                <div class="ai-metric-label">🏦 {t("Budget headroom")}</div>
                <div class="ai-metric-value">{fmt(abs(headroom))}</div>
                <div class="ai-metric-sub {sub_cls}">{sub_txt}</div>
              </div>""")
    with m4:
        q_sub = (
            t("strong result") if score.composite >= 80
            else t("review needed") if score.composite >= 65
            else t("below threshold")
        )
        H(f"""<div class="ai-metric">
                <div class="ai-metric-label">🎯 {t("Composite score")}</div>
                <div class="ai-metric-value">{score.composite}/100</div>
                <div class="ai-metric-sub">{q_sub}</div>
              </div>""")
    H('</div>') # Close padding div

    # ── 2. BoM table + Score card ─────────────────────────────────────── #
    H('<div style="padding: 1.5rem 2rem 0 2rem;">')
    bom_col, score_col = st.columns([1.8, 1.2], gap="large")

    with bom_col:
        H(f"""
        <div class="ai-card">
          <div class="ai-card-title"><span>📋</span> {t("BoM")}</div>
          {bom_table_html(bom, req.currency)}
        </div>""")

    with score_col:
        scores_html = (
            score_bar_html(t("Fitness"),  score.cost)
            + score_bar_html(t("Risk"), score.risk)
            + score_bar_html(t("Scalability"),   score.scalability)
            + "<hr style='border:none;border-top:1px solid #f1f5f9;margin:1.5rem 0'>"
            + score_bar_html(t("Composite Score"), score.composite, is_composite=True)
        )
        H(f"""
        <div class="ai-card">
          <div class="ai-card-title"><span>📈</span> {t("Proposal Scores")}</div>
          {scores_html}
        </div>""")

        H(f"""
        <div class="ai-card">
          <div class="ai-card-title"><span>💸</span> {t("Budget Breakdown")}</div>
          {budget_breakdown_html(total, contingency_v, grand_total,
                                 req.budget_usd, req.contingency_pct, req.currency)}
        </div>""")
    H('</div>') # Close padding div

    # ── 3. Executive summary ──────────────────────────────────────────── #
    H('<div style="padding: 0 2rem;">')
    import re
    summary_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", result.executive_summary)
    
    H(f"""
    <div class="ai-card">
      <div class="ai-card-title"><span>📝</span> {t("Executive Summary")}</div>
      <div style="font-size:1rem;line-height:1.8;color:#334155; font-weight: 500;">
        {summary_html}
      </div>
    </div>""")

    # ── 4+5. Insights + Monitoring ────────────────────────────────────── #
    ins_col, mon_col = st.columns(2, gap="large")

    with ins_col:
        ins_html = "".join(insight_html(i) for i in result.insights)
        H(f"""
        <div class="ai-card">
          <div class="ai-card-title"><span>💡</span> {t("Insights")}</div>
          <div style="margin-top: 0.5rem;">{ins_html}</div>
        </div>""")

    with mon_col:
        H(f"""
        <div class="ai-card">
          <div class="ai-card-title"><span>⚡</span> {t("AI Monitoring")}</div>
          <div style="margin-top: 0.5rem;">{monitoring_html(mon)}</div>
        </div>""")
    H('</div>') # Close padding div

    # ── 6. Footer ─────────────────────────────────────────────────────── #
    H("""
    <div style="text-align:center;margin-top:2.5rem;padding-top:1.25rem;
                border-top:1px solid #EEEEE9;font-size:11px;color:#D0CFC9">
      ProposalAI &middot; AI-assisted, architect-directed &middot;
      Export: File &rarr; Print &rarr; Save as PDF
    </div>""")


# =============================================================================
#  MAIN ENTRY POINT
# =============================================================================

def main():
    H(CSS)  # inject design system

    # ── Sidebar Content ────────────────────────────────────────────────── #
    with st.sidebar:
        H("""
        <div class="sidebar-logo">
            <div style="background: #4f46e5; color: white; width: 40px; height: 40px; 
                        border-radius: 12px; display: flex; align-items: center; 
                        justify-content: center; font-weight: 800; font-size: 20px;">
                ◈
            </div>
            <div class="sidebar-logo-text">ProposalAI</div>
        </div>
        """)

        # Render input panel inside sidebar
        req = render_input_panel()
        if req:
            with st.spinner("Generating proposal…"):
                time.sleep(0.9)
                result = generate_proposal(req)
            st.session_state["last_result"] = result

    # ── Main Content Area ─────────────────────────────────────────────── #
    if "last_result" in st.session_state:
        render_results(st.session_state["last_result"])
    else:
        H(f"""
        <div class="empty-state">
          <div style="font-size: 64px; margin-bottom: 1.5rem;">✨</div>
          <div style="font-size: 2rem; font-weight: 800; color: #1e293b; margin-bottom: 1rem;">
            {t("Ready")}
          </div>
          <div style="color: #64748b; font-size: 1.1rem; max-width: 400px; margin: 0 auto;">
            {t("Configure")}
          </div>
        </div>""")


if __name__ == "__main__":
    main()