from time import sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except (NoSuchElementException, StaleElementReferenceException) as e:
        return False
    return True

def preprocess_webpage(driver):
    driver.execute_script(""" 
        var tables = document.getElementsByTagName("table");
        for(let i = 0; i<tables.length; i++) {
            tables[i].parentNode.removeChild(tables[i])
        }

        var captions = document.getElementsByClassName("captions text-s");
        for(let i = 0; i<captions.length; i++) {
            captions[i].parentNode.removeChild(captions[i])
        }

        var referenceButtons = document.getElementsByClassName("anchor workspace-trigger u-display-inline anchor-paragraph");
        for(let i = 0; i<referenceButtons.length; i++) {
            referenceButtons[i].parentNode.removeChild(referenceButtons[i])
        }

        var figures = document.getElementsByTagName("figure");
        for(let i = 0; i<figures.length; i++) {
            figures[i].parentNode.removeChild(figures[i])
        }
        
        var formulas = document.querySelectorAll('span.display')
        for(let i = 0; i<formulas.length; i++) {
            formulas[i].parentNode.removeChild(formulas[i])
        }

        var formulas = document.querySelectorAll('span.display')
        var figures = document.getElementsByTagName("figure");
        var tables = document.getElementsByTagName("table");
        var captions = document.getElementsByClassName("captions text-s");
        var referenceButtons = document.getElementsByClassName("anchor workspace-trigger u-display-inline anchor-paragraph");
   
        console.log(tables)
        console.log(captions)
        console.log(referenceButtons)
        console.log(figures)
    """)