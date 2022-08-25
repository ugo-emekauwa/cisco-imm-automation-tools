"""
UCS FI Claim Handler for Cisco Intersight, v2.2
Author: Ugo Emekauwa
Contact: uemekauw@cisco.com, uemekauwa@gmail.com
Summary: The UCS FI Claim Handler for Cisco Intersight automates the
         claiming of UCS Fabric Interconnect clusters in Intersight Managed
         Mode.
Credits: Brian Morrissey and David Soper for providing the UCS FI Device
         Console URLs.
GitHub Repository: https://github.com/ugo-emekauwa/cisco-imm-automation-tools
"""


########################
# MODULE REQUIREMENT 1 #
########################
"""
For the following variable below named key_id, please fill in between
the quotes your Intersight API Key ID.

Here is an example:
key_id = "5c89885075646127773ec143/5c82fc477577712d3088eb2f/5c8987b17577712d302eaaff"

"""
key_id = ""


########################
# MODULE REQUIREMENT 2 #
########################
"""
For the following variable below named key, please fill in between
the quotes your system's file path to your Intersight API key "SecretKey.txt"
file.

Here is an example:
key = "C:\\Users\\demouser\\Documents\\SecretKey.txt"

"""
key = ""


########################
# MODULE REQUIREMENT 3 #
########################
"""
Provide the required configuration settings to claim the
device on Cisco Intersight. Remove the sample
values and replace them with your own, where applicable.
"""

####### Start Configuration Settings - Provide values for the variables listed below. #######

# General Settings
## Provide a list of IP addresses for all UCS IMM FI clusters that need to be claimed. Provide only one IP address for each UCS IMM FI cluster.
ucs_fi_device_console_ip_list = ["192.168.0.11",]

## Provide the authentication credentials for the UCS IMM FI clusters that need to be claimed.
## If claiming more than one UCS IMM FI cluster, the credentials must be the same.
ucs_fi_device_console_username = "admin"
ucs_fi_device_console_password = "C1sco12345"

# Intersight Base URL Setting (Change only if using the Intersight Virtual Appliance)
intersight_base_url = "https://www.intersight.com/api/v1"
url_certificate_verification = True

####### Finish Configuration Settings - The required value entries are complete. #######


#############################################################################################################################
#############################################################################################################################


import sys
import traceback
import json
import copy
import intersight
import re
import requests
import urllib3
import time

# Suppress InsecureRequestWarning error messages
urllib3.disable_warnings()

# Function to get Intersight API client as specified in the Intersight Python SDK documentation for OpenAPI 3.x
## Modified to align with overall formatting, try/except blocks added for additional error handling, certificate verification option added
def get_api_client(api_key_id,
                   api_secret_file,
                   endpoint="https://intersight.com",
                   url_certificate_verification=True
                   ):
    try:
        with open(api_secret_file, 'r') as f:
            api_key = f.read()
        
        if re.search('BEGIN RSA PRIVATE KEY', api_key):
            # API Key v2 format
            signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
            signing_scheme = intersight.signing.SCHEME_RSA_SHA256
            hash_algorithm = intersight.signing.HASH_SHA256

        elif re.search('BEGIN EC PRIVATE KEY', api_key):
            # API Key v3 format
            signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_DETERMINISTIC_RFC6979
            signing_scheme = intersight.signing.SCHEME_HS2019
            hash_algorithm = intersight.signing.HASH_SHA256

        configuration = intersight.Configuration(
            host=endpoint,
            signing_info=intersight.signing.HttpSigningConfiguration(
                key_id=api_key_id,
                private_key_path=api_secret_file,
                signing_scheme=signing_scheme,
                signing_algorithm=signing_algorithm,
                hash_algorithm=hash_algorithm,
                signed_headers=[
                    intersight.signing.HEADER_REQUEST_TARGET,
                    intersight.signing.HEADER_HOST,
                    intersight.signing.HEADER_DATE,
                    intersight.signing.HEADER_DIGEST,
                    ]
                )
            )

        if not url_certificate_verification:
            configuration.verify_ssl = False
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to access the Intersight API Key.")
        print("Exiting due to the Intersight API Key being unavailable.\n")
        print("Please verify that the correct API Key ID and API Key have "
              "been entered, then re-attempt execution.\n")
        print("Exception Message: ")
        traceback.print_exc()
        sys.exit(0)
        
    return intersight.ApiClient(configuration)


# Establish function to test for the availability of the Intersight API and Intersight account
def test_intersight_api_service(intersight_api_key_id,
                                intersight_api_key,
                                intersight_base_url="https://www.intersight.com/api/v1",
                                preconfigured_api_client=None
                                ):
    """This is a function to test the availability of the Intersight API and
    Intersight account. The tested Intersight account contains the user who is
    the owner of the provided Intersight API Key and Key ID.

    Args:
        intersight_api_key_id (str):
            The ID of the Intersight API key.
        intersight_api_key (str):
            The system file path of the Intersight API key.
        intersight_base_url (str):
            Optional; The base URL for Intersight API paths. The default value
            is "https://www.intersight.com/api/v1". This value typically only
            needs to be changed if using the Intersight Virtual Appliance. The
            default value is "https://www.intersight.com/api/v1".
        preconfigured_api_client ("ApiClient"):
            Optional; An ApiClient class instance which handles
            Intersight client-server communication through the use of API keys.
            The default value is None. If a preconfigured_api_client argument
            is provided, empty strings ("") or None can be provided for the
            intersight_api_key_id, intersight_api_key, and intersight_base_url
            arguments.

    Returns:
        A string of the name for the Intersight account tested, verifying the
        Intersight API service is up and the Intersight account is accessible.
        
    Raises:
        Exception:
            An exception occurred due to an issue with the provided API Key
            and/or API Key ID.
    """
    # Define Intersight SDK ApiClient variable
    if preconfigured_api_client is None:
        api_client = get_api_client(api_key_id=intersight_api_key_id,
                                    api_secret_file=intersight_api_key,
                                    endpoint=intersight_base_url
                                    )
    else:
        api_client = preconfigured_api_client
    try:
        # Check that Intersight Account is accessible
        print("Testing access to the Intersight API by verifying the "
              "Intersight account information...")
        api_client.call_api(resource_path="/iam/Accounts",
                            method="GET",
                            auth_settings=['cookieAuth', 'http_signature', 'oAuth2', 'oAuth2']
                            )
        response = api_client.last_response.data
        iam_account = json.loads(response)
        if api_client.last_response.status != 200:
            print("\nThe Intersight API and Account Availability Test did not "
                  "pass.")
            print("The Intersight account information could not be verified.")
            print("Exiting due to the Intersight account being unavailable.\n")
            print("Please verify that the correct API Key ID and API Key have "
                  "been entered, then re-attempt execution.\n")
            sys.exit(0)
        else:
            intersight_account_name = iam_account["Results"][0]["Name"]
            print("The Intersight API and Account Availability Test has "
                  "passed.\n")
            print(f"The Intersight account named '{intersight_account_name}' "
                  "has been found.")
            return intersight_account_name
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to access the Intersight API.")
        print("Exiting due to the Intersight API being unavailable.\n")
        print("Please verify that the correct API Key ID and API Key have "
              "been entered, then re-attempt execution.\n")
        print("Exception Message: ")
        traceback.print_exc()
        sys.exit(0)


# Establish function to retrieve the MOID of a specific Intersight API object by name
def intersight_object_moid_retriever(intersight_api_key_id,
                                     intersight_api_key,
                                     object_name,
                                     intersight_api_path,
                                     object_type="object",
                                     organization="default",
                                     intersight_base_url="https://www.intersight.com/api/v1",
                                     preconfigured_api_client=None
                                     ):
    """This is a function to retrieve the MOID of Intersight objects
    using the Intersight API.

    Args:
        intersight_api_key_id (str):
            The ID of the Intersight API key.
        intersight_api_key (str):
            The system file path of the Intersight API key.
        object_name (str):
            The name of the Intersight object.
        intersight_api_path (str):
            The Intersight API path of the Intersight object.
        object_type (str):
            Optional; The type of Intersight object. The default value is
            "object".
        organization (str):
            Optional; The Intersight organization of the Intersight object.
            The default value is "default".
        intersight_base_url (str):
            Optional; The base URL for Intersight API paths. The default value
            is "https://www.intersight.com/api/v1". This value typically only
            needs to be changed if using the Intersight Virtual Appliance.
        preconfigured_api_client ("ApiClient"):
            Optional; An ApiClient class instance which handles
            Intersight client-server communication through the use of API keys.
            The default value is None. If a preconfigured_api_client argument
            is provided, empty strings ("") or None can be provided for the
            intersight_api_key_id, intersight_api_key, and intersight_base_url
            arguments.

    Returns:
        A string of the MOID for the provided Intersight object.
        
    Raises:
        Exception:
            An exception occurred due to an issue accessing the Intersight API
            path. The status code or error message will be specified.
    """
    # Define Intersight SDK ApiClient variable
    if preconfigured_api_client is None:
        api_client = get_api_client(api_key_id=intersight_api_key_id,
                                    api_secret_file=intersight_api_key,
                                    endpoint=intersight_base_url
                                    )
    else:
        api_client = preconfigured_api_client
    try:
        # Retrieve the Intersight Account name
        api_client.call_api(resource_path="/iam/Accounts",
                            method="GET",
                            auth_settings=['cookieAuth', 'http_signature', 'oAuth2', 'oAuth2']
                            )
        response = api_client.last_response.data
        iam_account = json.loads(response)
        if api_client.last_response.status != 200:
            print("The provided Intersight account information could not be "
                  "accessed.")
            print("Exiting due to the Intersight account being unavailable.\n")
            print("Please verify that the correct API Key ID and API Key have "
                  "been entered, then re-attempt execution.\n")
            sys.exit(0)
        else:
            intersight_account_name = iam_account["Results"][0]["Name"]
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to access the Intersight API.")
        print("Exiting due to the Intersight API being unavailable.\n")
        print("Please verify that the correct API Key ID and API Key have "
              "been entered, then re-attempt execution.\n")
        sys.exit(0)
    # Retrieving the provided object from Intersight...
    full_intersight_api_path = f"/{intersight_api_path}"
    try:
        api_client.call_api(resource_path=full_intersight_api_path,
                            method="GET",
                            auth_settings=['cookieAuth', 'http_signature', 'oAuth2', 'oAuth2']
                            )
        response = api_client.last_response.data
        intersight_objects = json.loads(response)
        # The Intersight API resource path has been accessed successfully.
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("There was an issue retrieving the "
              f"{object_type} from Intersight.")
        print("Unable to access the provided Intersight API resource path "
              f"'{intersight_api_path}'.")
        print("Please review and resolve any error messages, then re-attempt "
              "execution.\n")
        print("Exception Message: ")
        traceback.print_exc()
        sys.exit(0)

    if intersight_objects.get("Results"):
        for intersight_object in intersight_objects.get("Results"):
            if intersight_object.get("Organization"):
                provided_organization_moid = intersight_object_moid_retriever(intersight_api_key_id=None,
                                                                              intersight_api_key=None,
                                                                              object_name=organization,
                                                                              intersight_api_path="organization/Organizations",
                                                                              object_type="Organization",
                                                                              preconfigured_api_client=api_client
                                                                              )
                if intersight_object.get("Organization", {}).get("Moid") == provided_organization_moid:
                    if intersight_object.get("Name") == object_name:
                        intersight_object_moid = intersight_object.get("Moid")
                        # The provided object and MOID has been identified and retrieved.
                        return intersight_object_moid
            else:
                if intersight_object.get("Name") == object_name:
                    intersight_object_moid = intersight_object.get("Moid")
                    # The provided object and MOID has been identified and retrieved.
                    return intersight_object_moid
        else:
            print("\nA configuration error has occurred!\n")
            print(f"The provided {object_type} named '{object_name}' was not "
                  "found.")
            print("Please check the Intersight Account named "
                  f"{intersight_account_name}.")
            print("Verify through the API or GUI that the needed "
                  f"{object_type} is present.")
            print(f"If the needed {object_type} is missing, please create it.")
            print("Once the issue has been resolved, re-attempt execution.\n")
            sys.exit(0)
    else:
        print("\nA configuration error has occurred!\n")
        print(f"The provided {object_type} named '{object_name}' was not "
              "found.")
        print(f"No requested {object_type} instance is currently available in "
              f"the Intersight account named {intersight_account_name}.")
        print("Please check the Intersight Account named "
              f"{intersight_account_name}.")
        print(f"Verify through the API or GUI that the needed {object_type} "
              "is present.")
        print(f"If the needed {object_type} is missing, please create it.")
        print("Once the issue has been resolved, re-attempt execution.\n")
        sys.exit(0)


# Establish function to request login to UCS FI Device Console
def _request_ucs_fi_device_console_login(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_username,
    ucs_fi_device_console_password
    ):
    """This is a function to request an HTTP response for a login to a UCS
    Fabric Interconnect Device Console under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_username (str):
            The admin username of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_password (str):
            The admin password of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).

    Returns:
        A Response class instance for the UCS Fabric Interconnect Device
        Console login HTTP request.

    Raises:
        Exception:
            An exception occurred due to an issue with the UCS Fabric
            Interconnect login HTTP request.
    """
    # Login to UCS FI Device Console
    ucs_fi_device_console_headers = {
        "Content-Type": "application/json"
        }
    ucs_fi_device_console_url = f"https://{ucs_fi_device_console_ip}/Login"
    ucs_fi_device_console_post_body = {
        "User": ucs_fi_device_console_username,
        "Password": ucs_fi_device_console_password
        }
    try:
        ucs_fi_device_console_login_request = requests.post(
            ucs_fi_device_console_url,
            headers=ucs_fi_device_console_headers,
            data=json.dumps(ucs_fi_device_console_post_body),
            verify=False
            )
        return ucs_fi_device_console_login_request
    except Exception as exception_message:
        print("\nA configuration error has occurred!\n")
        print(f"Unable to login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        print(exception_message)
         

# Establish function to request the UCS IMM FI Device Connector Claim Code
def _request_ucs_fi_device_connector_claim_code(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_login
    ):
    """"This is a function to request an HTTP response for a Claim Code to a
    UCS Fabric Interconnect under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_login (Response):
            A Response class instance of a UCS Fabric Interconnect Device
            Console login HTTP request.

    Returns:
        A Response class instance for the UCS Fabric Interconnect Claim Code
        HTTP request.

    Raises:
        Exception:
            An exception occurred due to an issue with the UCS Fabric
            Interconnect Claim Code HTTP request.
    """
    # Obtain Claim Code
    ucs_fi_device_connector_headers = {
        "Accept-Language": "application/json"
        }
    ucs_fi_device_connector_claim_code_url = f"https://{ucs_fi_device_console_ip}/connector/SecurityTokens"
    try:
        ucs_fi_device_connector_claim_code_request = requests.get(
            ucs_fi_device_connector_claim_code_url,
            cookies=ucs_fi_device_console_login.cookies,
            headers=ucs_fi_device_connector_headers,
            verify=False
            ) 
        return ucs_fi_device_connector_claim_code_request
    except Exception as exception_message:
        print("\nA configuration error has occurred!\n")
        print("Unable to request the Device Connector Claim Code "
              f"of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        print(exception_message)


# Establish function to request a refresh of the UCS IMM FI Device Connector
def _request_ucs_fi_device_connector_refresh(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_login
    ):
    """"This is a function to request an HTTP response for refreshing the
    Device Connector of a UCS Fabric Interconnect under Intersight Managed
    Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_login (Response):
            A Response class instance of a UCS Fabric Interconnect Device
            Console login HTTP request.

    Returns:
        A Response class instance for the UCS Fabric Interconnect Device
        Connector refresh HTTP request.

    Raises:
        Exception:
            An exception occurred due to an issue with the UCS Fabric
            Interconnect Device Connector refresh HTTP request.
    """
    # Refresh the Device Connector
    ucs_fi_device_connector_headers = {
        "Content-Type": "application/json"
        }
    ucs_fi_device_connector_refresh_url = f"https://{ucs_fi_device_console_ip}/connector/Connect"
    ucs_fi_device_connector_post_body = {}
    try:
        ucs_fi_device_connector_refresh_request = requests.post(
            ucs_fi_device_connector_refresh_url,
            cookies=ucs_fi_device_console_login.cookies,
            headers=ucs_fi_device_connector_headers,
            data=json.dumps(ucs_fi_device_connector_post_body),
            verify=False
            ) 
        return ucs_fi_device_connector_refresh_request
    except Exception as exception_message:
        print("\nA configuration error has occurred!\n")
        print("Unable to request the Device Connector refresh "
              f"of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        print(exception_message)


# Establish function to request UCS IMM FI Device Connector Device ID
def _request_ucs_fi_device_connector_device_id(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_login
    ):
    """"This is a function to request an HTTP response for the Device ID
    of a UCS Fabric Interconnect under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_login (Response):
            A Response class instance of a UCS Fabric Interconnect Device
            Console login HTTP request.

    Returns:
        A Response class instance for the UCS Fabric Interconnect Device ID
        HTTP request.

    Raises:
        Exception:
            An exception occurred due to an issue with the UCS Fabric
            Interconnect Device ID HTTP request.
    """
    # Obtain Device ID
    ucs_fi_device_connector_headers = {
        "Accept-Language": "application/json"
        }
    ucs_fi_device_connector_device_id_url = f"https://{ucs_fi_device_console_ip}/connector/DeviceIdentifiers"
    try:
        ucs_fi_device_connector_device_id_request = requests.get(
            ucs_fi_device_connector_device_id_url,
            cookies=ucs_fi_device_console_login.cookies,
            headers=ucs_fi_device_connector_headers,
            verify=False
            ) 
        return ucs_fi_device_connector_device_id_request
    except Exception as exception_message:
        print("\nA configuration error has occurred!\n")
        print("Unable to obtain the Device ID for the Device Connector "
              f"of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        print(exception_message)            


# Establish function to request UCS IMM FI Device Connector system information
def _request_ucs_fi_device_connector_system_info(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_login
    ):
    """"This is a function to request an HTTP response for the system
    information of a UCS Fabric Interconnect under Intersight Managed Mode
    (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_login (Response):
            A Response class instance of a UCS Fabric Interconnect Device
            Console login HTTP request.

    Returns:
        A Response class instance for the UCS Fabric Interconnect system
        information HTTP request.

    Raises:
        Exception:
            An exception occurred due to an issue with the UCS Fabric
            Interconnect system information HTTP request.
    """
    # Obtain system information
    ucs_fi_device_connector_headers = {
        "Accept-Language": "application/json"
        }
    ucs_fi_device_connector_system_info_url = f"https://{ucs_fi_device_console_ip}/connector/Systems"
    try:
        ucs_fi_device_connector_system_info_request = requests.get(
            ucs_fi_device_connector_system_info_url,
            cookies=ucs_fi_device_console_login.cookies,
            headers=ucs_fi_device_connector_headers,
            verify=False
            ) 
        return ucs_fi_device_connector_system_info_request
    except Exception as exception_message:
        print("\nA configuration error has occurred!\n")
        print("Unable to obtain the system information for the Device "
              f"Connector of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        print(exception_message)            


# Establish function to login to UCS FI Device Console
def obtain_ucs_fi_device_console_login_cookie(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_username,
    ucs_fi_device_console_password
    ):
    """This is a function to login to the Device Console of a UCS Fabric
    Interconnect under Intersight Managed Mode (IMM) and obtain the cookies for
    the login session.

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_username (str):
            The admin username of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_password (str):
            The admin password of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).

    Returns:
        A CookieJar containing cookies for the established login session to the
        provided UCS Fabric Interconnect. The login cookies are valid for 30
        minutes.

    Raises:
        Exception:
            An exception occurred due to an issue with accessing the provided
            UCS Fabric Interconnect.
    """
    try:
        # Login to UCS FI Device Console
        print("\nAttempting login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}...")
        ucs_fi_device_console_login = _request_ucs_fi_device_console_login(
            ucs_fi_device_console_ip,
            ucs_fi_device_console_username,
            ucs_fi_device_console_password
            )
        if ucs_fi_device_console_login.status_code == 200:
            print("Login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip} was successful.\n")
            print("The login cookie for the Device Console of "
                  f"{ucs_fi_device_console_ip} has been retrieved.")
            return ucs_fi_device_console_login.cookies
        else:
            print("\nA configuration error has occurred!\n")
            print("Unable to login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip}.\n")
            print("Exception Message: ")
            print(ucs_fi_device_console_login.json())
    except Exception:
        print("\nA configuration error has occurred!\n")
        print(f"Unable to login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        traceback.print_exc()
         

# Establish function to obtain UCS IMM FI Device Connector Device ID
def obtain_ucs_fi_device_connector_device_id(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_username,
    ucs_fi_device_console_password
    ):
    """This is a function to obtain the Device Connector Device ID for a UCS
    Fabric Interconnect under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_username (str):
            The admin username of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_password (str):
            The admin password of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).

    Returns:
        A string of the Device Connector Device ID for the UCS Fabric
        Interconnect.

    Raises:
        Exception:
            An exception occurred due to an issue with accessing the provided
            UCS Fabric Interconnect.
    """
    try:
        # Login to UCS FI Device Console
        print("\nAttempting login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}...")
        ucs_fi_device_console_login = _request_ucs_fi_device_console_login(
            ucs_fi_device_console_ip,
            ucs_fi_device_console_username,
            ucs_fi_device_console_password
            )
        if ucs_fi_device_console_login.status_code == 200:
            print("Login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip} was successful.\n")
            # Obtain Device ID
            print("Attempting to obtain the UCS FI Device Connector Device "
                  "ID...")
            get_ucs_fi_device_connector_device_id = _request_ucs_fi_device_connector_device_id(
                ucs_fi_device_console_ip,
                ucs_fi_device_console_login
                ) 
            if get_ucs_fi_device_connector_device_id.status_code == 200:
                ucs_fi_device_connector_device_id_list = get_ucs_fi_device_connector_device_id.json()
                ucs_fi_device_connector_device_id = ucs_fi_device_connector_device_id_list[0]["Id"]
                print("The Device ID for the Device Connector of "
                      f"{ucs_fi_device_console_ip} has been retrieved.")
                return ucs_fi_device_connector_device_id
            else:
                print("\nA configuration error has occurred!\n")
                print("Unable to obtain the Device ID for the Device "
                      f"Connector of {ucs_fi_device_console_ip}.\n")
                print("Exception Message: ")
                print(get_ucs_fi_device_connector_device_id.json())            
        else:
            print("\nA configuration error has occurred!\n")
            print("Unable to login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip}.\n")
            print("Exception Message: ")
            print(ucs_fi_device_console_login.json())
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to obtain the Device ID for the Device Connector "
              f"of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        traceback.print_exc()


# Establish function to obtain UCS IMM FI Device Connector Claim Code
def obtain_ucs_fi_device_connector_claim_code(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_username,
    ucs_fi_device_console_password
    ):
    """This is a function to obtain the Device Connector Claim Code for an
    unclaimed UCS Fabric Interconnect under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_username (str):
            The admin username of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_password (str):
            The admin password of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).

    Returns:
        A string of the Device Connector Claim Code for an unclaimed UCS Fabric
        Interconnect.

    Raises:
        Exception:
            An exception occurred due to an issue with accessing the provided
            UCS Fabric Interconnect.
    """
    try:
        # Login to UCS FI Device Console
        print("\nAttempting login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}...")
        ucs_fi_device_console_login = _request_ucs_fi_device_console_login(
            ucs_fi_device_console_ip,
            ucs_fi_device_console_username,
            ucs_fi_device_console_password
            )
        if ucs_fi_device_console_login.status_code == 200:
            print("Login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip} was successful.\n")
            # Obtain Claim Code
            print("Attempting to obtain the UCS FI Device Connector Claim "
                  "Code...")
            get_ucs_fi_device_connector_claim_code = _request_ucs_fi_device_connector_claim_code(
                ucs_fi_device_console_ip,
                ucs_fi_device_console_login
                ) 
            if get_ucs_fi_device_connector_claim_code.status_code == 200:
                ucs_fi_device_connector_claim_code_list = get_ucs_fi_device_connector_claim_code.json()
                ucs_fi_device_connector_claim_code = ucs_fi_device_connector_claim_code_list[0]["Token"]
                print("The Claim Code for the Device Connector of "
                      f"{ucs_fi_device_console_ip} has been retrieved.")
                return ucs_fi_device_connector_claim_code
            else:
                print("\nA configuration error has occurred!\n")
                print("Unable to obtain the Claim Code for the Device "
                      f"Connector of {ucs_fi_device_console_ip}.\n")
                print("Exception Message: ")
                print(get_ucs_fi_device_connector_claim_code.json())
                print("A second attempt will be made to obtain Claim "
                      "Code by refreshing the Device Connector...")
                print("Refreshing the Device Connector...")
                # Refresh the Device Connector
                print("Attempting to refresh the UCS FI Device Connector...")
                device_connector_refresh = _request_ucs_fi_device_connector_refresh(
                    ucs_fi_device_console_ip,
                    ucs_fi_device_console_login
                    )
                # Pause to allow Device Connector refresh
                time.sleep(5)
                if device_connector_refresh.status_code == 200:
                    # Obtain Claim Code
                    print("Attempting to obtain the UCS FI Device Connector "
                          "Claim Code...")
                    get_ucs_fi_device_connector_claim_code_second_attempt = _request_ucs_fi_device_connector_claim_code(
                        ucs_fi_device_console_ip,
                        ucs_fi_device_console_login
                        ) 
                    if get_ucs_fi_device_connector_claim_code_second_attempt.status_code == 200:
                        ucs_fi_device_connector_claim_code_list = get_ucs_fi_device_connector_claim_code_second_attempt.json()
                        ucs_fi_device_connector_claim_code = ucs_fi_device_connector_claim_code_list[0]["Token"]
                        print("The Claim Code for the Device Connector of "
                              f"{ucs_fi_device_console_ip} has been "
                              "retrieved.")
                        return ucs_fi_device_connector_claim_code
                    else:
                        print("\nA configuration error has occurred!\n")
                        print("Unable to obtain the Claim Code for the "
                              "Device Connector of "
                              f"{ucs_fi_device_console_ip}.\n")
                        print("Exception Message: ")
                        print(get_ucs_fi_device_connector_claim_code_second_attempt.json())
                else:
                    print("\nA configuration error has occurred!\n")
                    print("Unable to refresh the Device Connector for "
                          f"{ucs_fi_device_console_ip}.\n")
                    print("Exception Message: ")
                    print(device_connector_refresh.json())                        
        else:
            print("\nA configuration error has occurred!\n")
            print("Unable to login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip}.\n")
            print("Exception Message: ")
            print(ucs_fi_device_console_login.json())
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to obtain the Claim Code for the Device "
              f"Connector of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        traceback.print_exc()


# Establish function to obtain UCS IMM FI Device Connector system information
def obtain_ucs_fi_device_connector_system_info(
    ucs_fi_device_console_ip,
    ucs_fi_device_console_username,
    ucs_fi_device_console_password
    ):
    """This is a function to obtain the Device Connector system information for
    a UCS Fabric Interconnect under Intersight Managed Mode (IMM).

    Args:
        ucs_fi_device_console_ip (str):
            The IP address of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_username (str):
            The admin username of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).
        ucs_fi_device_console_password (str):
            The admin password of a UCS Fabric Interconnect under Intersight
            Managed Mode (IMM).

    Returns:
        A list of the Device Connector system information for the UCS Fabric
        Interconnect.

    Raises:
        Exception:
            An exception occurred due to an issue with accessing the provided
            UCS Fabric Interconnect.
    """
    try:
        # Login to UCS FI Device Console
        print("\nAttempting login to the UCS FI Device Console for "
              f"{ucs_fi_device_console_ip}...")
        ucs_fi_device_console_login = _request_ucs_fi_device_console_login(
            ucs_fi_device_console_ip,
            ucs_fi_device_console_username,
            ucs_fi_device_console_password
            )
        if ucs_fi_device_console_login.status_code == 200:
            print("Login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip} was successful.\n")
            # Obtain system information
            print("Attempting to obtain the UCS FI Device Connector system "
                  "information...")
            get_ucs_fi_device_connector_system_info = _request_ucs_fi_device_connector_system_info(
                ucs_fi_device_console_ip,
                ucs_fi_device_console_login
                ) 
            if get_ucs_fi_device_connector_system_info.status_code == 200:
                ucs_fi_device_connector_system_info_list = get_ucs_fi_device_connector_system_info.json()
                print("The system information for the Device Connector of "
                      f"{ucs_fi_device_console_ip} has been retrieved.")
                return ucs_fi_device_connector_system_info_list
            else:
                print("\nA configuration error has occurred!\n")
                print("Unable to obtain the system information for the "
                      f"Device Connector of {ucs_fi_device_console_ip}.\n")
                print("Exception Message: ")
                print(get_ucs_fi_device_connector_system_info.json())
        else:
            print("\nA configuration error has occurred!\n")
            print(f"Unable to login to the UCS FI Device Console for "
                  f"{ucs_fi_device_console_ip}.\n")
            print("Exception Message: ")
            print(ucs_fi_device_console_login.json())
    except Exception:
        print("\nA configuration error has occurred!\n")
        print("Unable to obtain the system information for the Device "
              f"Connector of {ucs_fi_device_console_ip}.\n")
        print("Exception Message: ")
        traceback.print_exc()


# Establish device claim specific classes and functions
class IntersightDeviceClaim:
    """This class is used to claim a device in Intersight.
    """
    object_type = "Intersight Device Claim"
    intersight_api_path = "asset/DeviceClaims"
    
    def __init__(self,
                 intersight_api_key_id,
                 intersight_api_key,
                 device_id,
                 claim_code,
                 intersight_base_url="https://www.intersight.com/api/v1",
                 preconfigured_api_client=None
                 ):
        self.intersight_api_key_id = intersight_api_key_id
        self.intersight_api_key = intersight_api_key
        self.device_id = device_id
        self.claim_code = claim_code
        self.intersight_base_url = intersight_base_url
        if preconfigured_api_client is None:
            self.api_client = get_api_client(api_key_id=intersight_api_key_id,
                                             api_secret_file=intersight_api_key,
                                             endpoint=intersight_base_url
                                             )
        else:
            self.api_client = preconfigured_api_client
        self.intersight_api_body = {
            "SerialNumber": self.device_id,
            "SecurityToken": self.claim_code
            }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"('{self.intersight_api_key_id}', "
            f"'{self.intersight_api_key}', "
            f"'{self.device_id}', "
            f"'{self.claim_code}', "
            f"'{self.intersight_base_url}', "
            f"{self.api_client})"
            )

    def __str__(self):
        return f"{self.__class__.__name__} class object for '{self.device_id}'"

    def _post_intersight_object(self):
        """This is a function to configure an Intersight object by
        performing a POST through the Intersight API.

        Returns:
            A string with a statement indicating whether the POST method
            was successful or failed.
            
        Raises:
            Exception:
                An exception occurred while performing the API call.
                The status code or error message will be specified.
        """
        full_intersight_api_path = f"/{self.intersight_api_path}"
        try:
            self.api_client.call_api(resource_path=full_intersight_api_path,
                                     method="POST",
                                     body=self.intersight_api_body,
                                     auth_settings=['cookieAuth', 'http_signature', 'oAuth2', 'oAuth2']
                                     )
            print(f"The configuration of the {self.object_type} "
                  "has completed.")
            return "The POST method was successful."
        except intersight.exceptions.ApiException as error:
            if error.status == 409:
                existing_intersight_object_name = self.intersight_api_body.get("Name", "object")
                print(f"The targeted {self.object_type} appears to already "
                      "exist.")
                print("An attempt will be made to update the pre-existing "
                      f"{existing_intersight_object_name}...")
                try:
                    existing_intersight_object_moid = intersight_object_moid_retriever(intersight_api_key_id=None,
                                                                                       intersight_api_key=None,
                                                                                       object_name=existing_intersight_object_name,
                                                                                       intersight_api_path=self.intersight_api_path,
                                                                                       object_type=self.object_type,
                                                                                       preconfigured_api_client=self.api_client
                                                                                       )
                    # Update full Intersight API path with the MOID of the existing object
                    full_intersight_api_path_with_moid = f"/{self.intersight_api_path}/{existing_intersight_object_moid}"
                    self.api_client.call_api(resource_path=full_intersight_api_path_with_moid,
                                             method="POST",
                                             body=self.intersight_api_body,
                                             auth_settings=['cookieAuth', 'http_signature', 'oAuth2', 'oAuth2']
                                             )
                    print(f"The update of the {self.object_type} has "
                          "completed.")
                    print(f"The pre-existing {existing_intersight_object_name} "
                          "has been updated.")
                    return "The POST method was successful."
                except Exception:
                    print("\nA configuration error has occurred!\n")
                    print(f"Unable to update the {self.object_type} under the "
                          "Intersight API resource path "
                          f"'{full_intersight_api_path_with_moid}'.\n")
                    print(f"The pre-existing {existing_intersight_object_name} "
                          "could not be updated.")
                    print("Exception Message: ")
                    traceback.print_exc()
                    return "The POST method failed."
            else:
                print("\nA configuration error has occurred!\n")
                print(f"Unable to configure the {self.object_type} under the "
                      "Intersight API resource path "
                      f"'{full_intersight_api_path}'.\n")
                print("Exception Message: ")
                traceback.print_exc()
                return "The POST method failed."
        except Exception:
            print("\nA configuration error has occurred!\n")
            print(f"Unable to configure the {self.object_type} under the "
                  "Intersight API resource path "
                  f"'{full_intersight_api_path}'.\n")
            print("Exception Message: ")
            traceback.print_exc()
            return "The POST method failed."

    def device_claimer(self):
        """This function claims the targeted device.
        """           
        print(f"Configuring the {self.object_type} for "
              f"{self.device_id}...")
        # POST the API body to Intersight
        self._post_intersight_object()


def intersight_device_claimer(
    intersight_api_key_id,
    intersight_api_key,
    device_id,
    claim_code,
    intersight_base_url="https://www.intersight.com/api/v1",
    preconfigured_api_client=None
    ):
    """This is a function used to claim a device on Cisco Intersight.

    Args:
        intersight_api_key_id (str):
            The ID of the Intersight API key.
        intersight_api_key (str):
            The system file path of the Intersight API key.
        device_id (str):
            The ID of the device to be claimed.
        claim_code (str):
            The claim code of the device to be claimed.
        intersight_base_url (str):
            Optional; The base URL for Intersight API paths. The default value
            is "https://www.intersight.com/api/v1". This value typically only
            needs to be changed if using the Intersight Virtual Appliance.
        preconfigured_api_client ("ApiClient"):
            Optional; An ApiClient class instance which handles
            Intersight client-server communication through the use of API keys.
            The default value is None. If a preconfigured_api_client argument
            is provided, empty strings ("") or None can be provided for the
            intersight_api_key_id, intersight_api_key, and intersight_base_url
            arguments.
    """
    def builder(target_object):
        """This is a function used to build the objects that are components of
        the device claim on Cisco Intersight.

        Args:
            target_object (class):
                The class representing the object to be built on Intersight.

        Raises:
            Exception:
                An exception occurred due to an issue accessing the Intersight
                API path. The status code or error message will be specified.
        """
        try:
            target_object.device_claimer()
        except Exception:
            print("\nA configuration error has occurred!\n")
            print("The builder function failed to configure the "
                  f"{target_object.object_type} settings.")
            print("Please check the provided arguments for the "
                  f"{target_object.object_type} settings.\n")
            print("Exception Message: ")
            traceback.print_exc()

    # Define and create device claim object in Intersight
    builder(
        IntersightDeviceClaim(
            intersight_api_key_id=intersight_api_key_id,
            intersight_api_key=intersight_api_key,
            device_id=device_id,
            claim_code=claim_code,
            intersight_base_url=intersight_base_url,
            preconfigured_api_client=preconfigured_api_client
            ))


def main():
    # Establish UCS FI Claim Handler specific variables
    claimer_type = "UCS FI Claim Handler"
    
    # Establish Intersight SDK for Python API client instance
    main_intersight_api_client = get_api_client(api_key_id=key_id,
                                                api_secret_file=key,
                                                endpoint=intersight_base_url,
                                                url_certificate_verification=url_certificate_verification
                                                )
    
    # Starting the UCS FI Claim Handler for Cisco Intersight
    print(f"\nStarting the {claimer_type} for Cisco Intersight.\n")

    # Run the Intersight API and Account Availability Test
    print("Running the Intersight API and Account Availability Test.")
    test_intersight_api_service(
        intersight_api_key_id=None,
        intersight_api_key=None,
        preconfigured_api_client=main_intersight_api_client
        )

    # Cycle through provided UCS FI Device Console IP list and claim devices
    if ucs_fi_device_console_ip_list:
        for ucs_fi_device_console_ip in ucs_fi_device_console_ip_list:
            try:
                # Login to UCS FI Device Console
                print("\nAttempting login to the UCS FI Device Console for "
                      f"{ucs_fi_device_console_ip}...")
                ucs_fi_device_console_login = _request_ucs_fi_device_console_login(
                    ucs_fi_device_console_ip,
                    ucs_fi_device_console_username,
                    ucs_fi_device_console_password
                    )
                if ucs_fi_device_console_login.status_code == 200:
                    print("Login to the UCS FI Device Console for "
                          f"{ucs_fi_device_console_ip} was successful.")
                    # Obtain Claim Code
                    print("Attempting to obtain the UCS FI Device Connector "
                          "Claim Code...")
                    get_ucs_fi_device_connector_claim_code = _request_ucs_fi_device_connector_claim_code(
                        ucs_fi_device_console_ip,
                        ucs_fi_device_console_login
                        ) 
                    if get_ucs_fi_device_connector_claim_code.status_code == 200:
                        ucs_fi_device_connector_claim_code_list = get_ucs_fi_device_connector_claim_code.json()
                        ucs_fi_device_connector_claim_code = ucs_fi_device_connector_claim_code_list[0]["Token"]
                        print("The Claim Code for the Device Connector of "
                              f"{ucs_fi_device_console_ip} has been "
                              "retrieved.")
                        # Obtain Device ID
                        print("Attempting to obtain the UCS FI Device "
                              "Connector Device ID...")
                        get_ucs_fi_device_connector_device_id = _request_ucs_fi_device_connector_device_id(
                            ucs_fi_device_console_ip,
                            ucs_fi_device_console_login
                            ) 
                        if get_ucs_fi_device_connector_device_id.status_code == 200:
                            ucs_fi_device_connector_device_id_list = get_ucs_fi_device_connector_device_id.json()
                            ucs_fi_device_connector_device_id = ucs_fi_device_connector_device_id_list[0]["Id"]
                            print("The Device ID for the Device "
                                  "Connector of "
                                  f"{ucs_fi_device_console_ip} has "
                                  "been retrieved.")
                            # Claim the device in Intersight
                            intersight_device_claimer(
                                intersight_api_key_id=None,
                                intersight_api_key=None,
                                device_id=ucs_fi_device_connector_device_id,
                                claim_code=ucs_fi_device_connector_claim_code,
                                intersight_base_url=intersight_base_url,
                                preconfigured_api_client=main_intersight_api_client
                                )                      
                        else:
                            print("\nA configuration error has "
                                  "occurred!\n")
                            print("Unable to obtain the Device ID for "
                                  "the Device Connector of "
                                  f"{ucs_fi_device_console_ip}.\n")
                            print("Exception Message: ")
                            print(get_ucs_fi_device_connector_device_id.json())        
                    else:
                        print("\nA configuration error has occurred!\n")
                        print("Unable to obtain the Claim Code for the "
                              "Device Connector of "
                              f"{ucs_fi_device_console_ip}.\n")
                        print("Exception Message: ")
                        print(get_ucs_fi_device_connector_claim_code.json())
                        print("\nA second attempt will be made to obtain Claim "
                              "Code by refreshing the Device Connector...")
                        print("Refreshing the Device Connector...")
                        # Refresh the Device Connector
                        print("Attempting to refresh the UCS FI Device "
                              "Connector...")
                        device_connector_refresh = _request_ucs_fi_device_connector_refresh(
                            ucs_fi_device_console_ip,
                            ucs_fi_device_console_login
                            )
                        # Pause to allow Device Connector refresh
                        time.sleep(5)
                        if device_connector_refresh.status_code == 200:
                            # Obtain Claim Code
                            print("Attempting to obtain the UCS FI Device "
                                  "Connector Claim Code...")
                            get_ucs_fi_device_connector_claim_code_second_attempt = _request_ucs_fi_device_connector_claim_code(
                                ucs_fi_device_console_ip,
                                ucs_fi_device_console_login
                                ) 
                            if get_ucs_fi_device_connector_claim_code_second_attempt.status_code == 200:
                                ucs_fi_device_connector_claim_code_list = get_ucs_fi_device_connector_claim_code_second_attempt.json()
                                ucs_fi_device_connector_claim_code = ucs_fi_device_connector_claim_code_list[0]["Token"]
                                print("The Claim Code for the Device Connector "
                                      f"of {ucs_fi_device_console_ip} has been "
                                      "retrieved.")
                                # Obtain Device ID
                                print("Attempting to obtain the UCS FI Device "
                                      "Connector Device ID...")
                                get_ucs_fi_device_connector_device_id = _request_ucs_fi_device_connector_device_id(
                                    ucs_fi_device_console_ip,
                                    ucs_fi_device_console_login
                                    ) 
                                if get_ucs_fi_device_connector_device_id.status_code == 200:
                                    ucs_fi_device_connector_device_id_list = get_ucs_fi_device_connector_device_id.json()
                                    ucs_fi_device_connector_device_id = ucs_fi_device_connector_device_id_list[0]["Id"]
                                    print("The Device ID for the Device "
                                          "Connector of "
                                          f"{ucs_fi_device_console_ip} has "
                                          "been retrieved.")
                                    # Claim the device in Intersight
                                    intersight_device_claimer(
                                        intersight_api_key_id=None,
                                        intersight_api_key=None,
                                        device_id=ucs_fi_device_connector_device_id,
                                        claim_code=ucs_fi_device_connector_claim_code,
                                        intersight_base_url=intersight_base_url,
                                        preconfigured_api_client=main_intersight_api_client
                                        )                      
                                else:
                                    print("\nA configuration error has "
                                          "occurred!\n")
                                    print("Unable to obtain the Device ID for "
                                          "the Device Connector of "
                                          f"{ucs_fi_device_console_ip}.\n")
                                    print("Exception Message: ")
                                    print(get_ucs_fi_device_connector_device_id.json())        
                            else:
                                print("\nA configuration error has occurred!\n")
                                print("Unable to obtain the Claim Code for the "
                                      "Device Connector of "
                                      f"{ucs_fi_device_console_ip}.\n")
                                print("Exception Message: ")
                                print(get_ucs_fi_device_connector_claim_code_second_attempt.json())                        
                        else:
                            print("\nA configuration error has occurred!\n")
                            print("Unable to refresh the Device Connector for "
                                  f"{ucs_fi_device_console_ip}.\n")
                            print("Exception Message: ")
                            print(device_connector_refresh.json())
                else:
                    print("\nA configuration error has occurred!\n")
                    print("Unable to login to the UCS FI Device Console for "
                          f"{ucs_fi_device_console_ip}.\n")
                    print("Exception Message: ")
                    print(ucs_fi_device_console_login.json())
            except Exception:
                print("\nA configuration error has occurred!\n")
                print("There was an issue claiming the device at "
                      f"{ucs_fi_device_console_ip}.\n")
                print("Exception Message: ")
                traceback.print_exc()
    else:
        print("\nThere are no UCS Fabric Interconnects to claim to Intersight.")
        print("There were no IP addresses provided.")

    # UCS FI Claim Handler completion
    print(f"\nThe {claimer_type} has completed.\n")


if __name__ == "__main__":
    main()

# Exiting the UCS FI Claim Handler for Cisco Intersight
sys.exit(0)
