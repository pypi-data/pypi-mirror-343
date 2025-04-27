"""
Тесты для анализатора безопасности.
"""
import os
import unittest
import tempfile

from pysec_inspect.config import Config
from pysec_inspect.core.analyzer.security_analyzer import SecurityAnalyzer, Issue


class TestSecurityAnalyzer(unittest.TestCase):
    """Тесты для класса SecurityAnalyzer."""
    
    def setUp(self):
        """Подготовка тестового окружения."""
        # Создаем тестовую конфигурацию
        self.config = Config()
        
        # Создаем временный файл с тестовым кодом
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, "test_security.py")
        
        # Тестовый код с проблемами безопасности
        test_code = """
import os

# SEC001: Insecure Function Usage
def execute_user_code(user_input):
    result = eval(user_input)  # Небезопасно
    return result

# SEC001: Insecure Function Usage (os.system)
def run_command(cmd):
    os.system(cmd)  # Небезопасно

# SEC002: SQL Injection
def get_user(user_id):
    import sqlite3
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(user_id)  # SQL инъекция
    cursor.execute(query)
    return cursor.fetchone()

# SEC003: Plaintext Passwords
def save_user():
    username = "admin"
    password = "super_secret"  # Пароль в открытом виде
    # Сохранение...

# Безопасный код
def safe_function():
    return "This is safe"
"""
        
        # Записываем тестовый код в файл
        with open(self.test_file_path, 'w') as f:
            f.write(test_code)
        
        # Создаем анализатор
        self.analyzer = SecurityAnalyzer(self.config)
    
    def tearDown(self):
        """Очистка после тестов."""
        self.temp_dir.cleanup()
    
    def test_analyze_file(self):
        """Тест анализа файла на наличие проблем безопасности."""
        # Запускаем анализатор
        issues = self.analyzer.analyze_file(self.test_file_path)
        
        # Проверяем, что найдены проблемы
        self.assertGreater(len(issues), 0)
        
        # Считаем количество проблем по типам
        counts = {
            "SEC001": 0,
            "SEC002": 0,
            "SEC003": 0
        }
        
        for issue in issues:
            if issue.rule_id in counts:
                counts[issue.rule_id] += 1
        
        # Проверяем, что найдены ожидаемые проблемы
        self.assertGreaterEqual(counts["SEC001"], 2)  # eval и os.system
        self.assertGreaterEqual(counts["SEC002"], 1)  # SQL инъекция
        self.assertGreaterEqual(counts["SEC003"], 1)  # Пароль в открытом виде
    
    def test_issue_to_dict(self):
        """Тест преобразования проблемы в словарь."""
        # Создаем тестовую проблему
        issue = Issue(
            rule_id="SEC001",
            file_path="test.py",
            line_number=10,
            code="eval('2+2')",
            message="Использование небезопасной функции eval",
            severity="critical",
            category="security",
            cwe="CWE-95"
        )
        
        # Преобразуем в словарь
        issue_dict = issue.to_dict()
        
        # Проверяем, что все поля сохранены
        self.assertEqual(issue_dict["rule_id"], "SEC001")
        self.assertEqual(issue_dict["file_path"], "test.py")
        self.assertEqual(issue_dict["line_number"], 10)
        self.assertEqual(issue_dict["code"], "eval('2+2')")
        self.assertEqual(issue_dict["message"], "Использование небезопасной функции eval")
        self.assertEqual(issue_dict["severity"], "critical")
        self.assertEqual(issue_dict["category"], "security")
        self.assertEqual(issue_dict["cwe"], "CWE-95")
        self.assertIsNone(issue_dict["ai_recommendation"])


if __name__ == '__main__':
    unittest.main() 