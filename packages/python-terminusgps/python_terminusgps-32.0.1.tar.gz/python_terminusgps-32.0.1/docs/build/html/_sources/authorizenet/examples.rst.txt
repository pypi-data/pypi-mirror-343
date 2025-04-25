Usage Examples
==============

=========================================
Retrieve an Authorizenet customer profile
=========================================

--------------------------------------------------------------------------------
1. Import :py:obj:`~terminusgps.authorizenet.profiles.customers.CustomerProfile`
--------------------------------------------------------------------------------

.. code:: python

    from terminusgps.authorizenet.profiles import CustomerProfile

----------------------------------------------------------------------------
2. Initialize a profile with a merchant id (must be present in Authorizenet)
----------------------------------------------------------------------------

.. code:: python

    ...
    cprofile = CustomerProfile(merchant_id=1) # Must pass merchant id

------------------------------------------------
3. Perform operations using the customer profile
------------------------------------------------

.. code:: python

    ...
    cprofile.update(email="support@terminusgps.com", desc="Support User")

-----------------
Full code example
-----------------

.. code:: python

    from terminusgps.authorizenet.profiles import CustomerProfile

    cprofile = CustomerProfile(merchant_id=1)
    cprofile.update(email="support@terminusgps.com", desc="Support User")
