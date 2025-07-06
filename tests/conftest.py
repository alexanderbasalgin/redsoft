import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    yield driver
    driver.quit()

@pytest.fixture
def login(driver):
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    driver.get("https://172.20.10.3/")
    login_page.enter_username("administrator")
    login_page.enter_password("a_11111111")
    login_page.click_login()
    return driver

@pytest.fixture
def manager_installation_page(login):
    from pages.domain_management_page import DomainManagementPage
    from pages.domain_controllers_page import DomainControllersPage
    from pages.manager_installation_page import ManagerInstallationPage
    
    domain_management = DomainManagementPage(login)
    domain_management.go_to_domain_management()
    domain_management.go_to_domain_controllers()
    
    controllers_page = DomainControllersPage(login)
    controllers_page.select_controller()
    controllers_page.click_install_manager()
    
    return ManagerInstallationPage(login)