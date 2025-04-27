"""
Тесты для модуля конфигурации.
"""
import os
import tempfile
import unittest
import yaml

from pysec_inspect.config import Config


class TestConfig(unittest.TestCase):
    """Тесты для класса Config."""

    def setUp(self):
        """Подготовка тестового окружения."""
        # Создаем временный файл конфигурации
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "test_config.yml")
        
        # Тестовая конфигурация
        self.test_config = {
            "version": "1.0.0",
            "global": {
                "severity_levels": ["critical", "warning", "info"],
                "default_severity": "critical",
                "output_format": "json",
                "enable_ai_recommendations": False
            },
            "security_rules": {
                "SEC001": {
                    "name": "Test Rule",
                    "enabled": False,
                    "severity": "info"
                }
            },
            "ignore_patterns": [
                "*/test_pattern/*"
            ]
        }
        
        # Записываем конфигурацию в файл
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config, f)
    
    def tearDown(self):
        """Очистка после тестов."""
        self.temp_dir.cleanup()
    
    def test_load_config(self):
        """Тест загрузки конфигурации из файла."""
        config = Config(self.config_path)
        
        # Проверяем, что конфигурация загружена правильно
        self.assertEqual(config.config["version"], "1.0.0")
        self.assertEqual(config.config["global"]["default_severity"], "critical")
        self.assertEqual(config.config["global"]["output_format"], "json")
        self.assertFalse(config.config["global"]["enable_ai_recommendations"])
        self.assertFalse(config.config["security_rules"]["SEC001"]["enabled"])
    
    def test_get_rule(self):
        """Тест получения настроек правила по ID."""
        config = Config(self.config_path)
        
        # Получаем правило
        rule = config.get_rule("SEC001")
        
        # Проверяем, что правило получено правильно
        self.assertEqual(rule["name"], "Test Rule")
        self.assertFalse(rule["enabled"])
        self.assertEqual(rule["severity"], "info")
    
    def test_should_ignore_file(self):
        """Тест проверки, должен ли файл быть исключен из анализа."""
        config = Config(self.config_path)
        
        # Проверяем, что файл в игнорируемой директории исключен
        self.assertTrue(config.should_ignore_file("some/path/test_pattern/file.py"))
        
        # Проверяем, что обычный файл не исключен
        self.assertFalse(config.should_ignore_file("some/path/file.py"))
    
    def test_is_rule_enabled(self):
        """Тест проверки, включено ли правило."""
        config = Config(self.config_path)
        
        # Правило SEC001 отключено в тестовой конфигурации
        self.assertFalse(config.is_rule_enabled("SEC001"))
        
        # Изменяем настройку правила
        config.config["security_rules"]["SEC001"]["enabled"] = True
        
        # Теперь правило должно быть включено
        self.assertTrue(config.is_rule_enabled("SEC001"))
    
    def test_unknown_rule(self):
        """Тест обработки неизвестного правила."""
        config = Config(self.config_path)
        
        # Неизвестное правило должно быть отключено
        self.assertFalse(config.is_rule_enabled("UNKNOWN123"))
        
        # Получение неизвестного правила должно вызвать исключение
        with self.assertRaises(ValueError):
            config.get_rule("UNKNOWN123")


if __name__ == '__main__':
    unittest.main() 