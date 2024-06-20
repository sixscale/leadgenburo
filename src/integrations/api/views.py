import json
import logging
from datetime import datetime

from django.conf import settings
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .permissions import AppTokenIsCorrect
from .serializers import CallDataInfoSerializer, FormResponseSerializer
from ..service.bitrix_integration import (
    create_bitrix_deal_by_call,
    create_bitrix_deal_by_form,
    handle_deal, get_deal_info,
)
from ..service.exceptions import (
    ScenarioNotFoundError,
    UnsuccessfulLeadCreationError,
    CategoryNotFoundError,
    SkorozvonAPIError,
)
from ..service.validation import SkorozvonCall, SkorozvonForm, flatten_data

logger = logging.getLogger(__name__)


class FormResponseAPI(CreateAPIView):
    serializer_class = FormResponseSerializer

    @staticmethod
    def get_str_form_response(form_response: list):
        return settings.FORM_SPLIT_QUESTION_SYMBOL.join([
            f"{question.get('question_name', '').replace(settings.FORM_SPLIT_ANSWER_SYMBOL, '')}"
            f"{settings.FORM_SPLIT_ANSWER_SYMBOL}"
            f"{question.get('answer_values', [''])[0]}"
            for question in form_response
        ])

    def post(self, request, *args, **kwargs):
        logger.info(f"lead type: FORM\n"
                    f"request time: {datetime.now()}\n"
                    f"request data: {json.dumps(request.data)}\n")
        data = flatten_data(request.data)
        data["form_scenario_id"] = request.data.get("form_response", dict()).get("scenario_id", "")
        data["form_response"] = self.get_str_form_response(request.data.get("form_response", dict()).get("answers", ""))
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            lead_info = SkorozvonForm.model_validate(data)
            try:
                create_bitrix_deal_by_form(lead_info)
            except (ScenarioNotFoundError, UnsuccessfulLeadCreationError, CategoryNotFoundError, SkorozvonAPIError):
                pass
            except Exception:
                pass
        return Response(status=status.HTTP_201_CREATED)


class PhoneCallInfoAPI(CreateAPIView):
    serializer_class = CallDataInfoSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"lead type: CALL\n"
                    f"request time: {datetime.now()}\n"
                    f"request data: {json.dumps(request.data)}\n")
        serializer = self.serializer_class(data=flatten_data(request.data))
        if serializer.is_valid():
            serializer.save()
            lead_info = SkorozvonCall.model_validate(serializer.data)
            try:
                create_bitrix_deal_by_call(lead_info)
            except (ScenarioNotFoundError, UnsuccessfulLeadCreationError, CategoryNotFoundError, SkorozvonAPIError):
                pass
            except Exception:
                pass
        return Response(status=status.HTTP_201_CREATED)


class DealCreationHandlerAPI(APIView):
    permission_classes = [AppTokenIsCorrect]

    def post(self, request):
        deal_id = request.data["data[FIELDS][ID]"]
        info = get_deal_info(deal_id)
        print(info)
        print(type(info))


        cached_deal_id = cache.get(deal_id)
        if cached_deal_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cache.set(deal_id, True, timeout=30)
        handle_deal(deal_id)
        cache.delete(deal_id)
        return Response(status=status.HTTP_200_OK)


class TestAPI(APIView):
    def post(self, request):
        return Response(status=status.HTTP_200_OK)
