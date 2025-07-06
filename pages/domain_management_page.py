from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DomainManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.domain_management_link = (By.XPATH, "//*[contains(text(), 'Управление доменом')]")
        self.domain_controllers_link = (By.XPATH, "//*[contains(text(), 'Контроллеры домена')]")

    def go_to_domain_management(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.domain_management_link)
        ).click()

    def go_to_domain_controllers(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.domain_controllers_link)
        ).click()