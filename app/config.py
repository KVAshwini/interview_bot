import sys
from pathlib import Path


PROJECT_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
DATA_DIR = PROJECT_ROOT / "data"
QA_LIBRARY_DIR = PROJECT_ROOT / "qa_library"
MEMORY_DIR = PROJECT_ROOT / "memory"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DB_PATH = DATA_DIR / "interview_library.db"

HIGH_CONFIDENCE = 0.85
MEDIUM_CONFIDENCE = 0.60
