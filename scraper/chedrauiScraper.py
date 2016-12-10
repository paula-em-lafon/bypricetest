from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
import sys
import traceback
import re
import requests
import http.client
import socket

from settings import db, conn

PHANTOMJS_PATH = './phantomjs/phantomjs'

FARMACIA_URL = 'http://www.chedraui.com.mx/index.php/ajusco/endeca/\
category/view/id/457/'

browser = webdriver.PhantomJS(PHANTOMJS_PATH)
browser2 = webdriver.PhantomJS(PHANTOMJS_PATH)


def open_url(openUrl):
    for i in range(0, 20):
        try:
            browser.get(openUrl)
            return browser
        except:
            continue
        raise requests.ConnectionError(
            'Could not reach the site' + FARMACIA_URL)


def page_iterator(browser):
    # check connection is well
    get_status(browser)
    # catch errors
    try:
        # Read important info on page
        read_page(browser)
        # Try to Find and declare next page button
        # If it doesn't appear, the parsing has been completed :)
        try:
            next_page = browser.find_element_by_xpath(
                "/descendant::a[@title='Siguiente'][1]")
        except:
            print("parsing completed succesfully")
            browser.quit()
            return
        # Find element to test next page is loading
        test_elem = browser.find_element_by_xpath(
            "./descendant::div[@class='item last']")
        # Click next page button
        webdriver.ActionChains(browser).move_to_element(
            next_page).click().perform()
        # check current page has become stale
        WebDriverWait(browser, 80).until(
            EC.staleness_of(test_elem)
        )
        # Call self method in order to start again
        page_iterator(browser)
    except:
        e = sys.exc_info()
        print("".join(traceback.format_exception(
            etype=type(e), value=e, tb=e.__traceback__)))


def read_page(browser):
    print("---------------------------NEW PAGE ------------------------------")
    rows_in_page = browser.find_elements_by_xpath(
        "/descendant::div[@class='products-list row-fluid']")
    for row in rows_in_page:
        WebDriverWait(row, 300).until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//div[@class='item last']")))
        # parse for items
        get_items(row)

    return


def get_items(row):
    items = row.find_elements_by_xpath(
        "./descendant::a[@class='product-image']")
    for item in items:
        for i in range(0, 100):
            try:
                item_link = item.get_attribute('href')
                break
            except:
                continue
            break
        read_item_page(item_link)
    return


def read_item_page(item_link):
    browser2.get(item_link)
    for i in range(0, 15):
        try:
            WebDriverWait(browser2, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='upc']")))
            break
        except:
            browser2.refresh()
            continue
    get_status(browser2)
    soup = BeautifulSoup(browser2.page_source, "html.parser")
    if soup.find("div", class_="upc").find('span') is None:
        return
    item_dict = {}
    item_dict['upc'] = soup.find("div", class_="upc").find('span').text
    item_dict['item_name'] = soup.find(
        "div", class_="product-name").find('span').text.replace(
            "%", "%%").replace("'", "\'\'")
    item_price_raw = ''
    if soup.find("span", class_="regular-price"):
        item_price_raw = soup.find(
            "span", class_="regular-price").find('span').text
    elif soup.find("span", class_="special-price"):
        item_price_raw = soup.find(
            "span", class_="special-price").find('span').text
    else:
        return
    item_dict['price'] = float(
        item_price_raw.replace("$", "").replace(",", ""))
    item_dict['image'] = soup.find("a", class_="cloud-zoom")['href']
    add_edit_content(item_dict)
    return


def add_edit_content(item_dict):
    print (item_dict)
    query = db.query(
        "SELECT * from products WHERE upc = '{}';".format(item_dict['upc'])
    )
    prod_edit = query.fetch()
    print(prod_edit)
    if prod_edit == []:
        max_val = db.query(
            "SELECT MAX(id) from products;"
        )
        max_val = max_val.fetch()
        if max_val[0]['max'] is None:
            max_val_int = 0
        else:
            max_val_int = int(max_val[0]['max']) + 1
        print(max_val_int)
        db.query(
            """
            INSERT INTO products(id, upc, item_name, price, image)
            VALUES({}, '{}',' {}', {}, '{}');
            """.format(max_val_int, item_dict['upc'], item_dict['item_name'],
                       item_dict['price'], item_dict['image'])
        )
    else:
        if len(prod_edit) >= 1:
            prod_edit_len = len(prod_edit)
            for i in range(1, prod_edit_len):
                db.query(
                    """
                    DELETE * from products WHERE id = {};
                    """.format(prod_edit[i]['id'])
                )
        db.query(
            """
            UPDATE  products SET upc = '{}', item_name = '{}',
            price = {} , image = '{}' WHERE id = {};
            """.format(item_dict['upc'], item_dict['item_name'],
                       item_dict['price'], item_dict['image'],
                       prod_edit[0]['id'])
        )


def get_status(driver):
    try:
        driver.execute(Command.STATUS)
        return
    except (socket.error, http.client.CannotSendRequest):
        return "the connection died"

if __name__ == "__main__":
    connection = open_url(FARMACIA_URL)
    page_iterator(connection)
