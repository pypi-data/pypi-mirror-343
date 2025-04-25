from authorizenet import apicontractsv1, apicontrollers
from authorizenet.apicontractsv1 import customerProfileType

from terminusgps.authorizenet.profiles.base import AuthorizenetProfileBase


class CustomerProfile(AuthorizenetProfileBase):
    """An Authorizenet customer profile."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        response = self._authorizenet_get_customer_profile()
        self._id = (
            int(response.profile.customerProfileId)
            if response is not None
            else self.create(*args, **kwargs)
        )

    def create(self, email: str, desc: str = "") -> int:
        """
        Creates a customer profile and returns its id.

        :param email: An email address.
        :type email: :py:obj:`str`
        :param desc: An optional description.
        :type desc: :py:obj:`str`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :raises ValueError: If the Authorizenet API response was not retrieved.
        :returns: The new customer profile id.
        :rtype: :py:obj:`int`

        """
        response = self._authorizenet_create_customer_profile(email=email, desc=desc)
        if response is None:
            raise ValueError("Failed to retrieve Authorizenet API response.")
        self._email = email
        self._desc = desc
        return int(response.customerProfileId)

    def update(
        self,
        merchant_id: int | str | None = None,
        email: str | None = None,
        desc: str | None = None,
    ) -> None:
        """
        Updates the customer profile.

        :param email: An email address.
        :type email: :py:obj:`str`
        :param desc: An optional description.
        :type desc: :py:obj:`str`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if any([merchant_id, email, desc]):
            self._authorizenet_update_customer_profile(merchant_id, email, desc)
            self._email = email
            self._desc = desc
            self._merchantCustomerId = merchant_id

    def delete(self) -> None:
        """
        Deletes the customer profile.

        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._authorizenet_delete_customer_profile()

    @property
    def payment_profile_ids(self) -> list[int]:
        """A list of the customer's payment profile ids, if any."""
        response = self._authorizenet_get_customer_profile(issuer_info=False)
        return [
            int(profile.customerPaymentProfileId)
            for profile in response.profile.paymentProfiles
        ]

    @property
    def address_profile_ids(self) -> list[int]:
        """A list of the customer's address profile ids, if any."""
        response = self._authorizenet_get_customer_profile(issuer_info=False)
        return [
            int(profile.customerAddressId) for profile in response.profile.shipToList
        ]

    @property
    def email(self) -> str | None:
        """A customer email address."""
        if self._email is None:
            response = self._authorizenet_get_customer_profile(issuer_info=False)
            self._email = response.profile.email if response is not None else None
        return self._email

    @email.setter
    def email(self, other: str) -> None:
        """Sets :py:attr:`email` and updates the customer profile email in Authorizenet."""
        self._email = other
        self._authorizenet_update_customer_profile(email=other)

    @property
    def desc(self) -> str | None:
        """A customer description."""
        if self._desc is None:
            response = self._authorizenet_get_customer_profile(issuer_info=False)
            self._desc = response.profile.description if response is not None else None
        return self._desc

    @desc.setter
    def desc(self, other: str) -> None:
        """Sets :py:attr:`desc` and updates the customer profile description in Authorizenet."""
        self._desc = other
        self._authorizenet_update_customer_profile(desc=other)

    @property
    def exists(self) -> bool:
        return bool(self._authorizenet_get_customer_profile())

    def _authorizenet_create_customer_profile(
        self, email: str, desc: str = ""
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.createCustomerProfileRequest` using the Authorizenet API.

        `createCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-create-customer-profile>`_

        :param email: An email address.
        :type email: :py:obj:`str`
        :param desc: An optional description.
        :type desc: :py:obj:`str`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.createCustomerProfileRequest(
            merchantAuthentication=self.merchantAuthentication,
            profile=customerProfileType(
                merchantCustomerId=self.merchantCustomerId,
                email=email,
                description=desc,
            ),
        )
        controller = apicontrollers.createCustomerProfileController(request)
        return self.execute_controller(controller)

    def _authorizenet_get_customer_profile(
        self, issuer_info: bool = True
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.getCustomerProfileRequest` using the Authorizenet API.

        `getCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-get-customer-profile>`_

        :param merchant_id: An optional customer merchant id.
        :type merchant_id: :py:obj:`int` | :py:obj:`None`
        :param issuer_info: Whether or not to include issuer info in the response.
        :type issuer_info: :py:obj:`bool`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.getCustomerProfileRequest(
            merchantAuthentication=self.merchantAuthentication,
            includeIssuerInfo=str(issuer_info).lower(),
        )
        if self.id is not None:
            request.customerProfileId = str(self.id)
        elif self.id is None and self.merchantCustomerId is not None:
            request.merchantCustomerId = str(self.merchantCustomerId)
        else:
            return

        controller = apicontrollers.getCustomerProfileController(request)
        return self.execute_controller(controller)

    def _authorizenet_update_customer_profile(
        self, email: str | None = None, desc: str | None = None
    ) -> dict | None:
        """
        Executes an :py:obj:`~authorizenet.apicontractsv1.updateCustomerProfileRequest` using the Authorizenet API.

        `updateCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-update-customer-profile>`_

        :param email: A customer email address.
        :type email: :py:obj:`str` | :py:obj:`None`
        :param desc: A customer description.
        :type desc: :py:obj:`str` | :py:obj:`None`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :raises AssertionError: If :py:attr:`id` wasn't set.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        new_profile: customerProfileType = customerProfileType(
            merchantCustomerId=self.merchantCustomerId, customerProfileId=self.id
        )
        if email is not None:
            new_profile.email = email
        if desc is not None:
            new_profile.desc = desc

        request = apicontractsv1.updateCustomerProfileRequest(
            merchantAuthentication=self.merchantAuthentication, profile=new_profile
        )
        controller = apicontrollers.updateCustomerProfileController(request)
        return self.execute_controller(controller)

    def _authorizenet_delete_customer_profile(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.deleteCustomerProfileRequest` using the Authorizenet API.

        `deleteCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-delete-customer-profile>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.deleteCustomerProfileRequest(
            merchantAuthentication=self.merchantAuthentication,
            customerProfileId=self.id,
        )
        controller = apicontrollers.deleteCustomerProfileController(request)
        return self.execute_controller(controller)
