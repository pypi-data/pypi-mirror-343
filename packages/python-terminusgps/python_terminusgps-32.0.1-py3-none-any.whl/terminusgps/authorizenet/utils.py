from authorizenet import apicontractsv1, apicontrollers
from authorizenet.apicontrollersbase import APIOperationBase
from django import forms

from .auth import get_environment, get_merchant_auth
from .errors import ControllerExecutionError


class ControllerExecutionMixin:
    @staticmethod
    def execute_controller(controller: APIOperationBase) -> dict | None:
        """
        Executes an Authorizenet controller and returns its response.

        :param controller: An Authorizenet API controller.
        :type controller: :py:obj:`~authorizenet.apicontrollersbase.APIOperationBase`
        :raises ControllerExecutionError: If the API call fails.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        controller.setenvironment(get_environment())
        controller.execute()
        response = controller.getresponse()

        if response is not None and response.messages.resultCode != "Ok":
            raise ControllerExecutionError(
                message=response.messages.message[0]["text"].text,
                code=response.messages.message[0]["code"].text,
            )
        return response


def get_customer_profile_ids() -> list[int]:
    """
    Returns a list of all customer profile ids in Authorizenet.

    :raises ControllerExecutionError: If the API call fails.
    :returns: A list of all customer profile ids in Authorizenet.
    :rtype: :py:obj:`list`

    """
    request = apicontractsv1.getCustomerProfileIdsRequest(
        merchantAuthentication=get_merchant_auth()
    )
    controller = apicontrollers.getCustomerProfileIdsController(request)
    response = ControllerExecutionMixin.execute_controller(controller)
    if response is None or "ids" not in response.getchildren():
        return []
    return [int(id) for id in response.ids.getchildren()]


def generate_customer_address(form: forms.Form) -> apicontractsv1.customerAddressType:
    """
    Takes a form and returns a :py:obj:`~authorizenet.apicontractsv1.customerAddressType`.

    :param form: A Django form.
    :type form: :py:obj:`~django.forms.Form`
    :raises ValueError: If ``address`` wasn't in the form.
    :raises ValueError: If ``first_name`` wasn't in the form.
    :raises ValueError: If ``last_name`` wasn't in the form.
    :returns: A customer address object.
    :rtype: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`

    """
    required_fields: list[str] = ["address", "first_name", "last_name"]
    for field in required_fields:
        if field not in form.cleaned_data or form.cleaned_data.get(field) is None:
            raise ValueError(
                f"'{field}' was not provided by the form, got '{form.cleaned_data.get(field)}'."
            )

    address: apicontractsv1.customerAddressType = form.cleaned_data["address"]
    address.firstName = form.cleaned_data["first_name"]
    address.lastName = form.cleaned_data["last_name"]
    if form.cleaned_data.get("phone"):
        address.phone = form.cleaned_data["phone"]
    return address


def generate_customer_payment(form: forms.Form) -> apicontractsv1.paymentType:
    """
    Takes a form and returns a :py:obj:`~authorizenet.apicontractsv1.paymentType`.

    :param form: A Django form.
    :type form: :py:obj:`~django.forms.Form`
    :raises ValueError: If ``credit_card`` wasn't in the form.
    :returns: A payment object.
    :rtype: :py:obj:`~authorizenet.apicontractsv1.paymentType`

    """
    required_fields: list[str] = ["credit_card"]
    for field in required_fields:
        if field not in form.cleaned_data or form.cleaned_data.get(field) is None:
            raise ValueError(
                f"'{field}' was not provided by the form, got '{form.cleaned_data.get(field)}'."
            )

    credit_card: apicontractsv1.creditCardType = form.cleaned_data["credit_card"]
    return apicontractsv1.paymentType(creditCard=credit_card)
