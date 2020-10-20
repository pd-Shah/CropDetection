from .src.day import Day
from .src.file import File
from .src.peak import Peak


class DayFilePeak(Day, File, Peak):
    pass


class DayFile(Day, File):
    pass
