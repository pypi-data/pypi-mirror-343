from pathlib import Path

from PySide6.QtCore import QSettings, QTimer, Signal


class Settings(QSettings):
    shPathChanged = Signal(Path)

    def __init__(self):
        super().__init__("jbosse3", "excel2moodle")
        if self.contains("core/spreadsheet"):
            self.sheet = self.value("core/spreadsheet")
            try:
                self.sheet.resolve(strict=True)
                if self.sheet.is_file():
                    QTimer.singleShot(0, self._emitSpreadsheetChanged)
            except Exception:
                return None
        self.ensureSettings()

    def ensureSettings(self) -> None:
        """Makes sure all necessary settings are made

        if not yet inside the settings file, they will be appended
        """
        print("setting necessary settings")

        if not self.contains("parser/nf/tolerance"):
            self.setValue("parser/nf/tolerance", 1)

        if not self.contains("core/pictureSubFolder"):
            self.set("core/pictureSubFolder", "Abbildungen_SVG")

    def _emitSpreadsheetChanged(self) -> None:
        self.shPathChanged.emit(self.sheet)
        print("Emitting Spreadsheet Changed Event")

    def get(self, value, default=None):
        return self.value(value, default)

    def set(self, setting, value):
        self.setValue(setting, value)

    def parserSet(self, setting, value) -> None:
        self.beginGroup("parser")
        self.setValue(setting, value)
        self.endGroup()

    def nfParserSet(self, setting, value) -> None:
        self.beginGroup("parser")
        self.setValue(setting, value)
        self.endGroup()

    def parserGet(self, value, default=None, **kwargs):
        self.beginGroup("parser")
        return self.value(value, default, **kwargs)

    def testgenSet(self, setting, value) -> None:
        self.beginGroup("testGen")
        self.setValue(setting, value)
        self.endGroup()

    def testgenGet(self, value, default=None):
        self.beginGroup("testGen")
        return self.value(value, default)

    def setSpreadsheet(self, sheet: Path) -> None:
        if isinstance(sheet, Path):
            self.sheet = sheet.resolve(strict=True)
            self.setValue("core/spreadsheet", self.sheet)
            self.shPathChanged.emit(sheet)
            return None
