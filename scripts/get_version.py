# -*- coding: utf-8 -*-
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from subtitle_masker.version import APP_VERSION


def main():
    print(APP_VERSION)


if __name__ == "__main__":
    main()
