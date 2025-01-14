import logging
from typing import List

import xmltodict
from glom import glom

from openforms.logging.logevent import stuf_bg_request, stuf_bg_response
from stuf.constants import EndpointType
from stuf.models import StufService

from ..client import BaseClient
from .constants import NAMESPACE_REPLACEMENTS, STUF_BG_EXPIRY_MINUTES

logger = logging.getLogger(__name__)


class StufBGClient(BaseClient):
    sector_alias = "bg"
    soap_security_expires_minutes = STUF_BG_EXPIRY_MINUTES

    def __init__(self, service: StufService):
        super().__init__(
            service,
            request_log_hook=stuf_bg_request,
            response_log_hook=stuf_bg_response,
        )

    def get_values_for_attributes(self, bsn: str, attributes) -> bytes:
        context = {
            **dict(zip(attributes, attributes)),
            "bsn": bsn,
        }
        response = self.templated_request(
            "npsLv01",
            template="stuf_bg/StufBgRequest.xml",
            context=context,
            endpoint_type=EndpointType.vrije_berichten,
        )
        return response.content

    def get_values(self, bsn: str, attributes: List[str]) -> dict:

        response_data = self.get_values_for_attributes(bsn, attributes)

        dict_response = xmltodict.parse(
            response_data,
            process_namespaces=True,
            namespaces=NAMESPACE_REPLACEMENTS,
        )

        # handle missing keys/empty data graciously, see #1842
        # some include a fault response, others use an empty <antwoord /> XML element
        antwoord_object = glom(
            dict_response, "Envelope.Body.npsLa01.antwoord.object", default=None
        )
        fault = glom(dict_response, "Envelope.Body.Fault", default=None)

        # success case - we did receive a meaningful response
        if antwoord_object is not None:
            return antwoord_object

        # no fault, but also empty antwoord data -> treat this as empty response
        if fault is None:
            return {}

        # we have a fault -> log it appropriately and raise an exception
        logger.error(
            "Response data has an unexpected shape",
            extra={"response": dict_response, "fault": fault},
        )
        raise ValueError("Problem processing StUF-BG response")
