"""
Init function for API Objects
"""

# pylint: disable=relative-beyond-top-level

# Libs
import logging
import requests

# This Lib
from .client import ProAPI, ClassicAPI, AuthManagerProAPI, JamfTenant
from .logging import get_logger
from .auth import OAuth, BearerAuth
from .utility import import_json
from ..config.defaultconfig import defaultconfig, MasterConfig
from .exceptions import JamfPiInitError, ConfigError


def init_client(
        tenant_name: str,
        config_filepath: str = None,
        basic_token: str = None,
        username: str = None,
        password: str = None,
        client_id: str = None,
        client_secret: str = None,
        session: requests.Session = None,
        custom_logger: logging.Logger = None,
        logging_level=None,
        logging_format: str = None,
        token_exp_threshold_mins: int = None,
        mode: str = None,
        debug_params: list = None,
        custom_auth: OAuth or BearerAuth = None
        # custom_endpoints: str = None // TODO
):

    """Initilizes a new Jamf instance object"""


    # Logger Setup
    if custom_logger:
        if not isinstance(custom_logger, logging.Logger):
            raise RuntimeError("Bad custom logger type", type(custom_logger))


    logger_config = {
        "custom_logger": custom_logger,
        "logging_level": logging_level,
        "logging_format": logging_format
    }
    

    # Logger for init function
    logger: logging.Logger = custom_logger or get_logger(
        name=f"{tenant_name}-ini",
        config=logger_config
    )
    logger.debug("Init Logger initialised")


    # Init Start
    logger.debug("%s client init started", tenant_name)


    # Config File
    if config_filepath:
        imported = import_json(config_filepath)
        libconfig = MasterConfig(imported)
        logger.info("Config: Custom - PATH %s", config_filepath)
    else:
        libconfig = MasterConfig(defaultconfig)
        logger.info("Config: Default")
    # Validate config HERE


    # Session
    if session:
        if isinstance(session, requests.Session):
            raise RuntimeError("Bad custom Session Type", session)
        
    session = session or requests.Session()
    logger.debug("Shared requests.Session initialised")


    # Auth - WIP
    if client_id and client_secret:
        auth_method = "oauth"
        auth = OAuth(
            tenant=tenant_name,
            libconfig=libconfig,
            logger_cfg=logger_config,
            token_exp_thold_mins=token_exp_threshold_mins,
            oauth_cid=client_id,
            oauth_cs=client_secret
        )
    elif (username and password) or basic_token:
        auth_method = "bearer"
        auth = BearerAuth(
            tenant=tenant_name,
            libconfig=libconfig,
            logger_cfg=logger_config,
            token_exp_thold_mins=token_exp_threshold_mins,
            username=username,
            password=password,
            basic_auth_token=basic_token,
        )
    else:
        raise JamfPiInitError("Bad combination of Authentication info provided.\nPlease refer to docs.")

    auth._set_new_token()
    
    # Master Config
    api_config = {
        "tenant": tenant_name,
        "libconfig": libconfig,
        "logging": logger_config,
        "session": session,
        "auth_method": auth_method,
        "auth": auth,
        "debug_params": debug_params
    }


    # Mode
    if not mode:
        classic = ClassicAPI(api_config)
        pro = ProAPI(api_config)

    elif mode == "classic":
        classic = ClassicAPI(api_config)
        pro = None

    elif mode == "pro":
        classic = None
        pro = ProAPI(api_config)

    elif mode == "auth":
        classic = None
        pro = AuthManagerProAPI(api_config)

    elif mode == "custom":
        print("Feature not built yet")
        raise Exception("Nope try again...") # WIP.

    else:
        raise ConfigError("Invalid API Mode")

    logger.info("%s Init Complete", tenant_name)

    # Cleanup
    del logger

    # Return Tenant
    return JamfTenant(
        tenant=tenant_name,
        auth_method=auth_method,
        logger_config=logger_config,
        classic=classic,
        pro=pro
    )




def init_auth():
    """
    Function for initialising an Auth object
    for use in multiple API objects

    Advanced users only
    
    """
    pass