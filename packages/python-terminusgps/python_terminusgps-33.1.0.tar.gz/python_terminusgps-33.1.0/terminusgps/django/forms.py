from collections.abc import Sequence

from authorizenet import apicontractsv1
from django import forms


class CreditCardWidget(forms.widgets.MultiWidget):
    def __init__(self, widgets=(), attrs: dict | None = None) -> None:
        if not widgets:
            widgets = [
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
            ]
        super().__init__(widgets=widgets, attrs=attrs)

    def decompress(
        self, value: apicontractsv1.creditCardType | None
    ) -> list[str | None]:
        """Decompresses a :py:attr:`~authorizenet.apicontractsv1.creditCardType` into a list of strings."""
        if value is None:
            return [None, None, None, None]

        expiry_parts = value.expirationDate.split("-")
        return [value.cardNumber, expiry_parts[0], expiry_parts[1], value.cardCode]


class AddressWidget(forms.widgets.MultiWidget):
    def __init__(self, widgets=(), attrs: dict | None = None) -> None:
        if not widgets:
            widgets = [
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
            ]
        super().__init__(widgets=widgets, attrs=attrs)

    def decompress(
        self, value: apicontractsv1.customerAddressType | None
    ) -> list[str | None]:
        """Decompresses a :py:attr:`~authorizenet.apicontractsv1.customerAddressType` into a list of strings."""
        if value is None:
            return [None, None, None, None, None]

        return [value.address, value.city, value.state, value.country, value.zip]


class CreditCardField(forms.MultiValueField):
    require_all_fields = True

    def __init__(self, fields=(), widget=CreditCardWidget(), *args, **kwargs) -> None:
        if not fields:
            fields = (
                forms.CharField(label="Card #"),
                forms.IntegerField(label="Expiry Month", min_value=1, max_value=12),
                forms.IntegerField(label="Expiry Year"),
                forms.CharField(label="CCV #"),
            )
        super().__init__(fields=fields, widget=widget, *args, **kwargs)

    def compress(self, data_list: Sequence[str]) -> apicontractsv1.creditCardType:
        """Compresses ``data_list`` into a :py:obj:`~authorizenet.apicontractsv1.creditCardType`."""
        return apicontractsv1.creditCardType(
            **{
                "cardNumber": data_list[0],
                "expirationDate": f"{data_list[1]}-{data_list[2]}",
                "cardCode": data_list[3],
            }
        )


class AddressField(forms.MultiValueField):
    require_all_fields = True

    def __init__(self, fields=(), widget=AddressWidget(), *args, **kwargs) -> None:
        if not fields:
            fields = (
                forms.CharField(label="Street", max_length=128),
                forms.CharField(label="City", max_length=128),
                forms.CharField(label="State", max_length=64),
                forms.CharField(label="Zip #", min_length=5, max_length=10),
                forms.CharField(label="Country", max_length=2),
            )
        super().__init__(fields=fields, widget=widget, *args, **kwargs)

    def compress(self, data_list: Sequence[str]) -> apicontractsv1.customerAddressType:
        """Compresses ``data_list`` into a :py:obj:`~authorizenet.apicontractsv1.customerAddressType`."""
        return apicontractsv1.customerAddressType(
            **{
                "address": data_list[0],
                "city": data_list[1],
                "state": data_list[2],
                "zip": data_list[3],
                "country": data_list[4],
            }
        )


def main() -> None:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "terminusgps.django.settings")
    django.setup()

    class TestForm(forms.Form):
        first_name = forms.CharField(label="First Name")
        last_name = forms.CharField(label="Last Name")
        phone = forms.CharField(label="Phone #")
        address = AddressField(label="Address")
        credit_card = CreditCardField(label="Credit Card")

    form_data = {
        "first_name": "TestFirst",
        "last_name": "TestLast",
        "phone": "555-555-5555",
        "address_0": "123 Main St.",
        "address_1": "Houston",
        "address_2": "Texas",
        "address_3": "77065",
        "address_4": "US",
        "credit_card_0": "4111111111111111",
        "credit_card_1": "1",
        "credit_card_2": "41",
        "credit_card_3": "444",
    }
    form = TestForm(form_data)
    print(f"{form.is_valid() = }")
    print(f"{form.errors = }")
    print(f"{type(form.clean()["address"]) = }")
    print(f"{type(form.clean()["credit_card"]) = }")


if __name__ == "__main__":
    main()
