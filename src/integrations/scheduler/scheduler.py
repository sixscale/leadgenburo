from ..models import IntegrationsData, FieldIds, ScenarioIds, FormFieldIds, UsersIds
from ..api.serializers import (
    IntegrationsDataSerializer,
    FieldIdsSerializer,
    ScenarioIdsSerializer,
    FormFieldIdsSerializer,
    UsersIdsSerializer,
)
from ..service.google_sheet_integration import get_sheet_config_data, get_funnel_info_from_integration_table
from ..service.skorozvon_integration import skorozvon_api

from apscheduler.schedulers.background import BackgroundScheduler


def get_spreadsheet_id_from_url(url: str):
    if url:
        return url.split("https://docs.google.com/spreadsheets/d/")[1].split("/")[0]
    return url


def get_tg_chat_id(chat_text: str):
    if ":" in chat_text and "\n" in chat_text:
        return chat_text.split("\n")[0].split(":")[1].strip()
    return chat_text


def check_for_null(value: str):
    if not value:
        return ""
    return value


def create_object(model_serializer, data: dict):
    serializer = model_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def sync_integrations_data(integrations_data: dict):
    for i in range(len(integrations_data["Проекты"])):
        if not integrations_data["Проекты"][i]:
            break
        if integrations_data["Статус"][i] != "Подключить":
            continue
        current_integration = {
            "project_name": integrations_data["Проекты"][i].strip(),
            "stage_id": integrations_data["ID Стадии"][i].strip(),
            "tg_bot_id": get_tg_chat_id(integrations_data["Телеграм бот:"][i]),
            "google_spreadsheet_id": get_spreadsheet_id_from_url(
                integrations_data["Ссылка на таблицу лидов [предыдущие]"][i]),
            "sheet_name": integrations_data["Название листа"][i].strip(),
            "previous_sheet_names": check_for_null(integrations_data["Названия прошлых листов"][i]).strip(),
            "skorozvon_scenario_name": check_for_null(integrations_data["Имя сценария в скорозвоне"][i]).strip(),
        }
        if IntegrationsData.objects.filter(project_name=current_integration["project_name"]).exists():
            instance = IntegrationsData.objects.get(project_name=current_integration["project_name"])
            serializer = IntegrationsDataSerializer(instance)
            for field in current_integration.keys():
                if current_integration[field] != serializer[field]:
                    serializer.update(instance, current_integration)
                    break
        else:
            create_object(IntegrationsDataSerializer, current_integration)


def sync_field_ids(bitrix_field_name, config_data: dict):
    for field_id, field_value in config_data.items():
        data = {
            "bitrix_field_name": bitrix_field_name,
            "bitrix_field_id": field_id,
            "bitrix_field_value": field_value
        }
        if FieldIds.objects.filter(bitrix_field_name=bitrix_field_name).filter(bitrix_field_id=field_id).exists():
            instance = FieldIds.objects.get(bitrix_field_name=bitrix_field_name, bitrix_field_id=field_id)
            serializer = FieldIdsSerializer(instance)
            for key in data.keys():
                if data[key] != serializer[key]:
                    serializer.update(instance, data)
        else:
            create_object(FieldIdsSerializer, data)


def sync_google_sheets_data_to_db():
    sync_integrations_data(get_funnel_info_from_integration_table())
    sheet_config_data = get_sheet_config_data()
    sync_form_data(sheet_config_data["Анкета"])
    for name, data in sheet_config_data.items():
        if name not in ["Соответстиве имен сценариев и воронок", "Анкета"]:
            sync_field_ids(name, data)


def sync_id_to_name_data(sync_data: dict, model, serializer_class, field_id_title: str, field_name_title: str):
    for field_id, field_name in sync_data.items():
        data = {
            field_id_title: field_id,
            field_name_title: field_name,
        }
        if model.objects.filter(**{field_id_title: field_id}).exists():
            instance = model.objects.get(**{field_id_title: field_id})
            serializer = serializer_class(instance)
            if serializer[field_id_title] != data[field_id_title]:
                serializer.update(instance, data)
        else:
            create_object(serializer_class, data)


def sync_form_data(form_data: dict):
    sync_id_to_name_data(
        form_data,
        FormFieldIds,
        FormFieldIdsSerializer,
        "field_id",
        "field_name"
    )


def sync_skorozvon_scenarios():
    scenarios = skorozvon_api.get_scenarios()
    sync_id_to_name_data(
        scenarios,
        ScenarioIds,
        ScenarioIdsSerializer,
        "scenario_id",
        "scenario_name"
    )


def sync_skorozvon_users():
    scenarios = skorozvon_api.get_users()
    sync_id_to_name_data(
        scenarios,
        UsersIds,
        UsersIdsSerializer,
        "user_id",
        "user_name"
    )

# def sync_skorozvon_call_report():
#     reports = skorozvon_api.get_call_report()



def sync_skorozvon_data():
    sync_skorozvon_scenarios()
    sync_skorozvon_users()


def sync_data():
    sync_google_sheets_data_to_db()
    sync_skorozvon_data()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_data, 'interval', minutes=1)
    scheduler.start()
