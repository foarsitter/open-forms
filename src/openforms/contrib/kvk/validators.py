from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from requests import RequestException
from zds_client import ClientError

from openforms.contrib.kvk.client import KVKClientError, KVKSearchClient
from openforms.utils.validators import validate_digits, validate_rsin
from openforms.validations.registry import register


@deconstructible
class NumericBaseValidator:
    value_size: int
    value_label: int
    error_messages = {
        "too_short": _("%(type)s should have %(size)i characters."),
    }

    def __call__(self, value):
        validate_digits(value)

        if len(value) != self.value_size:
            raise ValidationError(
                self.error_messages["too_short"],
                params={"size": self.value_size, "type": self.value_label},
                code="invalid",
            )


@deconstructible
class KVKNumberValidator(NumericBaseValidator):
    value_size = 8
    value_label = _("KvK number")


@deconstructible
class KVKBranchNumberValidator(NumericBaseValidator):
    value_size = 12
    value_label = _("Branch number")


validate_kvk = KVKNumberValidator()
validate_branchNumber = KVKBranchNumberValidator()


class KVKRemoteBaseValidator:
    query_param: str
    value_label: str

    error_messages = {
        "not_found": _("%(type)s does not exist."),
        "too_short": _("%(type)s should have %(size)i characters."),
    }

    def __call__(self, value):
        assert self.query_param

        client = KVKSearchClient()
        try:
            result = client.query(**{self.query_param: value})
        except (RequestException, ClientError, KVKClientError):
            raise ValidationError(
                self.error_messages["not_found"],
                params={"type": self.value_label},
                code="invalid",
            )
        else:
            if not len(result.get("resultaten", [])):
                raise ValidationError(
                    self.error_messages["not_found"],
                    params={"type": self.value_label},
                    code="invalid",
                )
            else:
                return True


@register("kvk-kvkNumber", verbose_name=_("KvK number"), for_components=("textfield",))
@deconstructible
class KVKNumberRemoteValidator(KVKRemoteBaseValidator):
    query_param = "kvkNummer"
    value_label = _("KvK number")

    def __call__(self, value):
        validate_kvk(value)
        super().__call__(value)


@register("kvk-rsin", verbose_name=_("KvK RSIN"), for_components=("textfield",))
@deconstructible
class KVKRSINRemoteValidator(KVKRemoteBaseValidator):
    query_param = "rsin"
    value_label = _("RSIN")

    def __call__(self, value):
        validate_rsin(value)
        super().__call__(value)


@register(
    "kvk-branchNumber",
    verbose_name=_("KvK branch number"),
    for_components=("textfield",),
)
@deconstructible
class KVKBranchNumberRemoteValidator(KVKRemoteBaseValidator):
    query_param = "vestigingsnummer"
    value_label = _("Branch number")

    def __call__(self, value):
        validate_branchNumber(value)
        super().__call__(value)
