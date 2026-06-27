import datetime

class Logger:
    gui_callback = None
    gui_clear_callback = None
    copy_callback = None

    @staticmethod
    def _log(message: str, level: str):
        now = datetime.datetime.now()
        timestamp = now.strftime("%H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
        formatted = f"[{timestamp}][{level}] {message}"

        print(formatted)

        if Logger.gui_callback:
            Logger.gui_callback(formatted, level)

    @staticmethod
    def Clear():
        print("\033c", end="")
        if Logger.gui_clear_callback:
            Logger.gui_clear_callback()
        Logger.Info("-------- Console Cleared --------")

    @staticmethod
    def Copy():
        if Logger.copy_callback:
            Logger.copy_callback()
            Logger.Success("-------- Log Copied to Clipboard --------")

    @staticmethod
    def Info(msg): Logger._log(msg, "INFO")
    @staticmethod
    def Action(msg): Logger._log(msg, "ACTION")
    @staticmethod
    def Error(msg): Logger._log(msg, "ERROR")
    @staticmethod
    def Success(msg): Logger._log(msg, "SUCCESS")
    @staticmethod
    def Debug(msg): Logger._log(msg, "DEBUG")