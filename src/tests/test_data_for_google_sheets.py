import pytest

from integrations.service.validation import BitrixDeal
from pydantic import BaseModel, Field


class BitrixDealTest(BaseModel):
    deal_id: int = Field(default=-1)
    stage_id: str = Field(default="")
    lead_name: str = Field(default="")
    phone: str = Field(default="")
    lead_type: str = Field(default="")
    lead_qualification: str = Field(default="")
    lead_comment: str = Field(default="")
    link_to_audio: str = Field(default="")
    date: str = Field(default="")
    city: str = Field(default="")
    country: str = Field(default="")
    car_mark: str = Field(default="")
    car_model: str = Field(default="")
    project_name: str = Field(default="")
    link_to_lead: str = Field(default="")
    is_valid_lead: bool = Field(default=True)
    working_stage: str = Field(default="")


test_base_model = BitrixDealTest(
    deal_id=1184880,
    stage_id='C94:UC_NIMO45',
    lead_name='евгений',
    phone='79126805926',
    lead_type='1',
    lead_qualification='11',
    lead_comment='21',
    link_to_audio='https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
    date='2024-05-24',
    city='Mscw',
    country='Russia',
    car_mark='car_mark',
    car_model='car_model',
    project_name='project_name',
    link_to_lead='https://leadrecord.bitrix24.ru/crm/deal/details/1184880/',
    is_valid_lead=True,
    working_stage='C94:EXECUTING',
)

test_base_model_invalid = test_base_model.model_copy(update={"is_valid_lead": False})
test_base_model_for_P5 = test_base_model.model_copy(update={"stage_id": "C21:EXECUTING"})
test_base_model_for_P15 = test_base_model.model_copy(update={"stage_id": "C17:EXECUTING"})
test_base_model_for_P17 = test_base_model.model_copy(update={"stage_id": "C13:EXECUTING"})
test_base_model_empty = test_base_model.model_copy(update={
    "stage_id": "lead_name",
    "lead_name": "",
    "phone": "",
    "lead_type": "",
    "lead_qualification": "",
    "lead_comment": "",
    "link_to_audio": "",
    "date": "",
    "city": "",
    "country": "",
    "car_mark": "",
    "car_model": "",
    "project_name": "",
    "link_to_lead": "",
    "is_valid_lead": True,
    "working_stage": "",
})

test_base_model_empty_invalid = test_base_model_empty.model_copy(update={"is_valid_lead": False})

expected_output_invalid_lead = [
    '2024-05-24',
    '',
    'project_name',
    'https://leadrecord.bitrix24.ru/crm/deal/details/1184880/',
    'евгений',
    '79126805926',
    "Имя: евгений. Комментарий: 21",
    "1 | 11",
    'https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
]

expected_output_for_P5 = [
    '2024-05-24',
    '',
    '79126805926',
    'Mscw',
    "Имя: евгений. Комментарий: 21",
    'https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
]

expected_output_for_P15 = [
    '2024-05-24',
    '',
    '79126805926',
    "Имя: евгений. Комментарий: 21",
    'https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
    'Russia',
]

expected_output_for_P17 = [
    '2024-05-24',
    '',
    '79126805926',
    'car_mark',
    'car_model',
    "Имя: евгений. Комментарий: 21",
    'https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
]

expected_output_for_other = [
    '2024-05-24',
    '',
    'евгений',
    '79126805926',
    '21',
    "1 | 11",
    'https://downloader.disk.yandex.ru/disk/a1ed4b04670fde475873830c86fb11c4bfd7d1beba125dc96ee0aeae34e20adb/664f3efc/b3zqie5wyETRkDfLlyNe7NBXHyMxA0Kczy_aYp_Wu8oREepkgaPzxJl-J-ZKISbraZS-9_WpAMRMMqTJAsCtuw%3D%3D?uid=1925056298&filename=call_audio_953662862_23052024_120459.mp3&disposition=attachment&hash=&limit=0&content_type=audio%2Fmpeg&owner_uid=1925056298&fsize=648477&hid=a9a4faf4a6f5e45296ecdbc002c60683&media_type=audio&tknv=v2&etag=800acd5e7ba423e1c81ec1d1b8270893',
]

test_base_model_empty_output = [
    '',
    '',
    '',
    '',
    '',
    " | ",
    '',
]

test_base_model_empty_invalid_output = [
    '',
    '',
    '',
    '',
    '',
    '',
    "Имя: . Комментарий: ",
    " | ",
    '',
]