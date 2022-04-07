import os
import pathlib
import logging
from logging.handlers import RotatingFileHandler
import datetime

# Check initial Application environment and create if missing
basedir = os.path.abspath(os.path.dirname(__file__))
for xdir in ['Outbound', 'Response', 'Logs']:
    if not os.path.exists(xdir):
        os.mkdir(xdir)

# Setup error log creation

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)
f_handler = RotatingFileHandler(basedir + '\\Logs\\faxservice.log', maxBytes=20480, backupCount=10)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

# Setup RingCentral Fax Transmission logging

rc_logger = logging.getLogger()
rc_handler = RotatingFileHandler(basedir + '\\Logs\\RC_Transmission.log', maxBytes=20480, backupCount=30)
rc_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rc_handler.setFormatter(f_format)
rc_logger.addHandler(rc_handler)


# Setup directory path for json response's from Ring Central

def rc_confirm(response):
    f_json = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + response)
    f_w_response = os.path.join(basedir + '\\Response\\' + f_json)
    return f_w_response


class FaxValidate:
    # Create Class to manage validation of parameters passed for faxing
    # Validate the fax numbers passed to RingCentral function

    def valid_num(fx_to, fx_from):

        for fx_num in [fx_to, fx_from]:
            if len(fx_num) < 12:
                return False
            elif len(fx_num) > 12:
                return False
            else:
                return True

    # Validate fax document is correct file type
    def valid_doc(fx_doc):

        fx_doctype = pathlib.Path(fx_doc).suffix
        if fx_doctype == ".pdf":
            return True
        else:
            logger.error("Document Passed is not a PDF")
            return False


# Make Methods Static
FaxValidate.valid_num = staticmethod(FaxValidate.valid_num)
FaxValidate.valid_doc = staticmethod(FaxValidate.valid_doc)
