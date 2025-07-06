import pytest

@pytest.mark.parametrize("port, expected_error", [
    ("80", "Значение порта не должно быть меньше 1024."),
    ("50000", "Значение порта не должно быть больше 49151."),
    ("", "Поле должно быть заполнено."),
    ("1024", None),
    ("49151", None),
], ids=["port_<1024", "port_>49151", "port_empty", "port_min_valid", "port_max_valid"])
def test_invalid_port_validation(manager_installation_page, port, expected_error):
    """Проверка порта"""
    manager_installation_page.force_clear_port_field()
    manager_installation_page.set_port(port)
    manager_installation_page.set_username("valid_user")
    manager_installation_page.set_password("valid_password")
    manager_installation_page.click_install()
    actual_error = manager_installation_page.get_error_message()
    assert actual_error == expected_error, \
        f"Ожидалась ошибка: '{expected_error}', но получено: '{actual_error}'"


@pytest.mark.parametrize("username, password, expected_error", [
    # Невалидные комбинации
    ("", "valid_password", "Поле должно быть заполнено."),
    ("valid_user", "", "Поле должно быть заполнено."),
    ("", "", "Поле должно быть заполнено."),
    ("invalid_user", "wrong_pass", "Incorrect login/password to connect to the SSH-server"),  # Неверные креды
    # Валидные комбинации
    ("root", "11111111", "Менеджер успешно установлен")
], ids=["empty_username", "empty_password", "both_empty", "invalid_credentials", "valid_credentials"])

def test_ssh_credentials_validation(manager_installation_page, username, password, expected_error):
    """
    Проверяет:
    - Пустое имя пользователя
    - Пустой пароль
    - Неверные учетные данные
    - Корректные данные - корректное создание менеджера
    """

    if username:
        manager_installation_page.set_username(username)
    if password:
        manager_installation_page.set_password(password)

    manager_installation_page.click_install()
    
    if "Incorrect login/password" in str(expected_error):
        actual_error = manager_installation_page.get_error_message_incorrect()
        assert "Incorrect login/password" in str(actual_error), \
            f"Ожидалась ошибка авторизации, но получено: '{actual_error}'"
    elif "Менеджер успешно установлен" in str(expected_error):
        actual_error = manager_installation_page.get_error_message_incorrect()
        assert "Менеджер успешно установлен" in str(actual_error), \
            f"Ожидалась авторизация, но получено: '{actual_error}'"
    else:
        actual_error = manager_installation_page.get_error_message()
        assert actual_error == expected_error, \
            f"Ожидалась ошибка: '{expected_error}', но получено: '{actual_error}'"