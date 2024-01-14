# from download_excel import handler
from libs.selenium import GoogleSearchSampleDriver
from libs.log import get_logger

log = get_logger(__name__)

def handler(event, context):
    driver = GoogleSearchSampleDriver()
    log.info(f"Crawled page title is {driver.test()}")
    return {"statusCode": 200, "body": "OK"}
