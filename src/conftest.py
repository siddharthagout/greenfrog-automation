

import logging
import pytest

@pytest.fixture(autouse=True)
def log_seperator(request):
    """Log separator method for test space"""
    test_name = request.node.name
    logging.info("---------------------------------------------")
    logging.info("Start of Test method : %s", test_name)
    yield
    logging.info("End of Test method : %s", test_name)