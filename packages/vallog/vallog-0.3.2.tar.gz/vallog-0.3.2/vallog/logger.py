"""
Logger module containing the logger class
"""

import shutil

_ansi_colors = {
    "white": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}


class Logger:
    """Logger class"""

    _terminal_width = shutil.get_terminal_size().columns
    _mode_list: list[str] = ["Debug", "Release", "Test"]

    class LogCategory:
        """
        subclass off Logger for the most customizable options
        """

        def __init__(self, name: str, color: str = "white", mode: list[str] = None):
            self.name = name
            self.clr_str = color
            self.color = _ansi_colors[color] if color in _ansi_colors.keys() else color
            self.mode = mode if mode is not None else ["Debug", "Release", "Test"]

        def __len__(self) -> int:
            return len(self.name)

        def __repr__(self):
            return self.name + ":\tcolor=" + self.clr_str + "\tmode=" + str(self.mode)

    default = LogCategory("Default", "white")
    info = LogCategory("Info", "green", ["Debug", "Release"])
    warning = LogCategory("Warning", "purple")
    error = LogCategory("Error", "red")
    debug = LogCategory("Debug", "blue", ["Debug"])
    header = LogCategory("Heading", _ansi_colors["bold"] + _ansi_colors["cyan"])
    header.clr_str = "bold + cyan"

    _category_list: list[LogCategory] = [default, info, warning, error, debug, header]

    def __init__(self, mode: str = "Debug", cout: bool = True):
        self._check_mode(mode)
        self.cout = cout
        self.mode = mode
        self.usr_categories = {}

    def _check_mode(self, mode: str) -> None:
        if mode not in Logger._mode_list:
            raise ValueError(f"{mode} is not a valid mode. Try one of these instead: {Logger._mode_list}")

    def _check_category(self, category: LogCategory | str) -> bool:
        return (
            category in Logger._category_list
            or category in self.usr_categories.values()
            or isinstance(category, Logger.LogCategory)
        )

    def _get_indent(self) -> int:
        indent = (
            int(0.1 * Logger._terminal_width) if Logger._terminal_width >= 100 else int(0.3 * Logger._terminal_width)
        )
        return indent

    def _break_massage(self, massage: str, indent: int) -> str:
        def _get_break_index(space_inidces: list[int], target_index: int) -> int:
            filtered_indices = [index for index in space_inidces if index <= target_index]
            return filtered_indices[-1]

        if indent + len(massage) <= Logger._terminal_width:
            return massage

        for i in range(Logger._terminal_width - indent, len(massage), Logger._terminal_width):
            space_indices: list = [index for index, char in enumerate(massage) if char == " "]
            break_index = _get_break_index(space_indices, i)
            massage = massage[:break_index] + f"\n{' '*indent}" + massage[break_index + 1 :]

            return massage

    def log(
        self,
        massage: str,
        category: LogCategory | str = default,
        display_category: bool = True,
        colored_text: bool = False,
    ) -> None:
        """
        print a log massage to the terminal with sensible formatting and different lo categories.
        massages tagged with the 'debug' category will only get displayed if the Logger is set to debug mode
        """

        is_valid_category = self._check_category(category)

        if not is_valid_category:

            category = Logger.LogCategory(category, _ansi_colors["white"])

        indent = self._get_indent()
        massage = self._break_massage(massage, indent)

        prefix = ""
        spacing = indent
        if display_category:
            prefix = f"[{category.color}{category.name}{_ansi_colors["white"]}]"
            spacing = indent - (len(category) + 2)

        text_color = category.color if colored_text else _ansi_colors["white"]

        if self.mode in category.mode and self.cout:
            print(f"{prefix}{' '*spacing}{text_color}{massage}{_ansi_colors["white"]}")

    def sep(self, char: str = "=") -> None:
        """
        create a seperation in the terminal output. Provide a 'char' for custom seperation line
        """
        char = char[0] if len(char) > 0 else "="
        if self.cout:
            print(f"\n\n{char*Logger._terminal_width}\n")

    def heading(self, massage: str) -> None:
        """
        method for quickly setting a header in the terminal output, e.g. to specify a new section of debug massages
        """
        indent = self._get_indent()
        massage = f"\n{' '*indent}" + massage
        self.log(massage, Logger.header, display_category=False, colored_text=True)

    def add_category(self, name: str, color: str = None, mode: list[str] = None) -> None:
        """
        create a new user defined category that is limited to an instance of the Logger class
        """
        new_category = Logger.LogCategory(name, color, mode)
        setattr(self, name, new_category)
        self.usr_categories[name] = new_category

    def list_categories(self) -> None:
        """
        list all available categories
        """
        self.sep()
        self.heading("Default categories:")
        for cat in Logger._category_list:
            self.log(str(cat), cat)

        self.heading("User defined categories:")
        for cat in self.usr_categories.values():

            self.log(str(cat), cat)

    def toggle_cout(self) -> None:
        """toggle terminal output"""
        self.cout = not self.cout
