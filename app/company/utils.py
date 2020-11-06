def get_employee_pasport_scan_path(instance, filename) -> str:
    """
    Возвращает путь к директории в которую сохраняются сканы паспортов.
    """
    return f"employees_pasports/{instance.user.first_name}_{instance.user.last_name}"