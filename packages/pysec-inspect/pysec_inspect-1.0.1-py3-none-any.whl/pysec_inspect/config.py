"""
Модуль конфигурации для PySecInspect.
Содержит все настройки и конфигурационные параметры для работы инструмента.
"""
import os
import json
import yaml
from typing import Dict, List, Any, Optional

DEFAULT_CONFIG_FILE = ".pysec_inspect.yml"

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "global": {
        "severity_levels": ["critical", "warning", "info"],
        "default_severity": "warning",
        "output_format": "text",
        "enable_ai_recommendations": True,
        "ai_model": "gpt-4o-mini",
        "max_recommendations_per_issue": 3
    },
    "security_rules": {
        "SEC001": {
            "name": "Insecure Function Usage",
            "description": "Detects usage of unsafe functions like eval, exec",
            "enabled": True,
            "severity": "critical",
            "patterns": [
                "eval\\(",
                "exec\\(",
                "os\\.system\\(",
                "__import__\\("
            ],
            "exceptions": [
                "# nosec",
                "# pysec:ignore:SEC001"
            ]
        },
        "SEC002": {
            "name": "SQL Injection",
            "description": "Detects potential SQL injection vulnerabilities",
            "enabled": True,
            "severity": "critical",
            "patterns": [
                "execute\\(.*\\+.*\\)",
                "execute\\(f\".*{.*}.*\"\\)",
                "raw\\(.*\\%.*\\)"
            ],
            "exceptions": [
                "# pysec:ignore:SEC002",
                "# nosql"
            ]
        },
        "SEC003": {
            "name": "Plaintext Passwords",
            "description": "Detects passwords stored in plaintext",
            "enabled": True,
            "severity": "critical",
            "patterns": [
                "password\\s*=\\s*['\"][^'\"]+['\"]",
                "passwd\\s*=\\s*['\"][^'\"]+['\"]",
                "pwd\\s*=\\s*['\"][^'\"]+['\"]"
            ],
            "exceptions": [
                "# nosec",
                "test_",
                "dummy_"
            ]
        }
    },
    "performance_rules": {
        "PERF001": {
            "name": "Inefficient Loops",
            "description": "Detects inefficient loop patterns",
            "enabled": True,
            "severity": "warning",
            "patterns": [
                "for .* in range\\(len\\(.*\\)\\):"
            ],
            "suggestions": [
                "Consider using enumerate() instead of range(len())"
            ]
        }
    },
    "quality_rules": {
        "QUAL001": {
            "name": "PEP8 Compliance",
            "description": "Checks compliance with PEP8 style guide",
            "enabled": True,
            "severity": "info"
        }
    },
    "ignore_patterns": [
        "*/tests/*",
        "*/migrations/*",
        "setup.py",
        "*.pyc",
        "__pycache__/*",
        ".git/*",
        ".env/*",
        "venv/*"
    ]
}


class Config:
    """Класс для управления конфигурацией PySecInspect."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Инициализация конфигурации.
        
        Args:
            config_file: Путь к файлу конфигурации. Если None, будет искать в текущей директории.
        """
        self.config = DEFAULT_CONFIG.copy()
        
        if config_file:
            self.load_config(config_file)
        elif os.path.exists(DEFAULT_CONFIG_FILE):
            self.load_config(DEFAULT_CONFIG_FILE)
    
    def load_config(self, config_file: str) -> None:
        """
        Загрузка конфигурации из файла.
        
        Args:
            config_file: Путь к файлу конфигурации.
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                loaded_config = json.load(f)
            elif config_file.endswith(('.yml', '.yaml')):
                loaded_config = yaml.safe_load(f)
            else:
                raise ValueError("Unsupported config file format. Use .json, .yml or .yaml")
        
        # Обновляем только указанные в файле настройки, сохраняя дефолты для остальных
        self._update_nested_dict(self.config, loaded_config)
    
    def _update_nested_dict(self, d: Dict, u: Dict) -> Dict:
        """
        Рекурсивно обновляет вложенный словарь.
        
        Args:
            d: Исходный словарь
            u: Словарь с обновлениями
            
        Returns:
            Обновленный словарь
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                d[k] = self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    def get_rule(self, rule_id: str) -> Dict:
        """
        Получает настройки правила по его ID.
        
        Args:
            rule_id: Идентификатор правила (например, SEC001)
            
        Returns:
            Словарь с настройками правила
        """
        category = self._get_rule_category(rule_id)
        if not category:
            raise ValueError(f"Unknown rule ID: {rule_id}")
        
        return self.config[category].get(rule_id, {})
    
    def _get_rule_category(self, rule_id: str) -> Optional[str]:
        """
        Определяет категорию правила по его ID.
        
        Args:
            rule_id: Идентификатор правила
            
        Returns:
            Строка с категорией правила или None, если категория не найдена
        """
        if rule_id.startswith("SEC"):
            return "security_rules"
        elif rule_id.startswith("PERF"):
            return "performance_rules"
        elif rule_id.startswith("QUAL"):
            return "quality_rules"
        return None
    
    def should_ignore_file(self, file_path: str) -> bool:
        """
        Проверяет, должен ли файл быть исключен из анализа.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True, если файл должен быть исключен, иначе False
        """
        import fnmatch
        import os
        
        # Нормализуем путь для более надежного сравнения
        file_path = os.path.normpath(file_path)
        
        # Проверяем наличие ключевых слов в пути
        path_parts = file_path.split(os.sep)
        key_ignore_dirs = ['venv', 'site-packages', '__pycache__', '.git', 'migrations']
        for part in path_parts:
            if part in key_ignore_dirs:
                return True
        
        # Применяем шаблоны игнорирования
        for pattern in self.config["ignore_patterns"]:
            # Нормализуем шаблон
            norm_pattern = pattern.replace('/', os.sep)
            
            # Проверяем соответствие шаблону
            if fnmatch.fnmatch(file_path, norm_pattern):
                return True
            
            # Проверяем каждую часть пути отдельно для случаев с */
            if pattern.startswith('*/'):
                # Убираем */ из начала шаблона
                sub_pattern = pattern[2:]
                # Проверяем, заканчивается ли путь этим шаблоном
                if file_path.endswith(sub_pattern):
                    return True
                # Проверяем, содержит ли путь этот шаблон в любой из своих частей
                for part in path_parts:
                    if fnmatch.fnmatch(part, sub_pattern):
                        return True
        
        return False
    
    def is_rule_enabled(self, rule_id: str) -> bool:
        """
        Проверяет, включено ли правило.
        
        Args:
            rule_id: Идентификатор правила
            
        Returns:
            True, если правило включено, иначе False
        """
        try:
            rule = self.get_rule(rule_id)
            return rule.get("enabled", False)
        except ValueError:
            return False
    
    def save_config(self, config_file: str) -> None:
        """
        Сохраняет текущую конфигурацию в файл.
        
        Args:
            config_file: Путь к файлу для сохранения
        """
        with open(config_file, 'w') as f:
            if config_file.endswith('.json'):
                json.dump(self.config, f, indent=2)
            elif config_file.endswith(('.yml', '.yaml')):
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                raise ValueError("Unsupported config file format. Use .json, .yml or .yaml") 