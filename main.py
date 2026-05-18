# -*- coding: utf-8 -*-
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def run_self_test():
    import subtitle_masker
    import subtitle_masker.main

    print("SubtitleMasker self-test ok:", subtitle_masker.__file__)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        run_self_test()
        sys.exit(0)

    from subtitle_masker.main import main

    main()
