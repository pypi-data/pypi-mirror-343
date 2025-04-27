"""
Основной модуль PySecInspect.
Запускается при вызове `python -m pysec_inspect` или при запуске установленного пакета.
"""
import sys
from pysec_inspect.interfaces.cli.commands import main

if __name__ == "__main__":
    sys.exit(main()) 