from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DomainControllersPage:
    def __init__(self, driver):
        self.driver = driver
        self.controller_row = (By.XPATH, "//div[@role='row'][.//div[text()='dc.red.soft']]")
        self.install_manager_button = (By.XPATH, "//*[contains(text(), 'Установить менеджер')]")

    def select_controller(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.controller_row)
        ).click()

    def click_install_manager(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.install_manager_button)
        ).click()