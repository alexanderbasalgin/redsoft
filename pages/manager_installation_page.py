# pages/manager_installation_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class ManagerInstallationPage:
    def __init__(self, driver):
        self.driver = driver
        self.port_field = (By.NAME, "port")
        self.username_field = (By.NAME, "sshUsername")
        self.password_field = (By.NAME, "sshPassword")
        self.install_button = (By.XPATH, "//button[normalize-space()='Установить']")
        self.error_message = (By.XPATH, "//div[contains(@class, 'error-message')]")
        self.installation_log = (By.XPATH, "//div[contains(@class, 'installation-log')]")

    def set_port(self, port):
        """Установка значения порта"""
        self.force_clear_port_field()
        
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.port_field)
        )
        
        field.click()
        for char in str(port):
            field.send_keys(char)
            
        self.driver.execute_script("""
            // Для React/Vue
            if (arguments[0]._valueTracker) {
                arguments[0]._valueTracker.setValue(arguments[1]);
            }
            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
        """, field, port)
        
    def force_clear_port_field(self):
        """Комплексный метод очистки поля"""
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.port_field)
        )
        
        field.clear()

        self.driver.execute_script("""
            arguments[0].value = '';
            // Для React/Vue приложений
            if (arguments[0]._valueTracker) {
                arguments[0]._valueTracker.setValue('');
            }
            // Триггер всех событий
            ['input', 'change', 'blur'].forEach(evt => {
                arguments[0].dispatchEvent(new Event(evt, {bubbles: true}));
            });
        """, field)

        field.send_keys(Keys.CONTROL + 'a')
        field.send_keys(Keys.DELETE)

    def set_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_field)
        ).send_keys(username)

    def set_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_field)
        ).send_keys(password)

    def click_install(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.install_button)
        ).click()

    def get_error_message(self):
        """Текст ошибки валидации с учётом всех возможных сообщений"""

        error_messages = [
            "Значение порта не должно быть меньше 1024",
            "Значение порта не должно быть больше 49151",
            "Поле должно быть заполнено",
        ]

        for message in error_messages:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//*[contains(text(), '{message}')]")
                    )
                )
                return element.text
            except:
                continue
            
        return None
            

    def get_error_message_incorrect(self):
        try:
            ssh_error = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(., 'Incorrect login/password') or contains(., 'Менеджер успешно установлен')]")
                )
            )
            return ssh_error.text
        except:
            return None