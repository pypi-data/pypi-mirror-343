# colored_text.py
# Author: Basit Ahmad Ganie 
# email: basitahmed1412@gmail.com 
# this code was written to ease the effort of putting colored text to the terminal.

class ColoredText:
    # Foreground Colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    # Bright Foreground Colors
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97

    # Background Colors
    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_WHITE = 47

    # Bright Background Colors
    BG_BRIGHT_BLACK = 100
    BG_BRIGHT_RED = 101
    BG_BRIGHT_GREEN = 102
    BG_BRIGHT_YELLOW = 103
    BG_BRIGHT_BLUE = 104
    BG_BRIGHT_MAGENTA = 105
    BG_BRIGHT_CYAN = 106
    BG_BRIGHT_WHITE = 107

    # Styles
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8
    RESET = 0

    @staticmethod
    def colorize(text, fg_color=None, bg_color=None, style=None):
        codes = []

        if style is not None:
            codes.append(str(style))
        if fg_color is not None:
            codes.append(str(fg_color))
        if bg_color is not None:
            codes.append(str(bg_color))

        color_prefix = f"\033[{';'.join(codes)}m" if codes else ''
        color_suffix = "\033[0m"  # Reset code

        return f"{color_prefix}{text}{color_suffix}"

    @staticmethod
    def print_colored(text, fg_color=None, bg_color=None, style=None):
        print(ColoredText.colorize(text, fg_color, bg_color, style))

    @staticmethod
    def color256(text, color_code, bg_code=None, style=None):
        fg_code = f"38;5;{color_code}"
        bg_code = f"48;5;{bg_code}" if bg_code is not None else ''
        codes = [fg_code]
        if bg_code:
            codes.append(bg_code)
        if style:
            codes.insert(0, str(style))
        
        color_prefix = f"\033[{';'.join(codes)}m"
        color_suffix = "\033[0m"
        return f"{color_prefix}{text}{color_suffix}"

    @staticmethod
    def rgb(text, r, g, b, bg=False, style=None):
        fg_code = f"38;2;{r};{g};{b}"
        bg_code = f"48;2;{r};{g};{b}" if bg else ''
        codes = [fg_code]
        if bg_code:
            codes.append(bg_code)
        if style:
            codes.insert(0, str(style))
        
        color_prefix = f"\033[{';'.join(codes)}m"
        color_suffix = "\033[0m"
        return f"{color_prefix}{text}{color_suffix}"

    # Methods for Standard Colors
    @staticmethod
    def black(text, style=None):
        return ColoredText.colorize(text, ColoredText.BLACK, style=style)

    @staticmethod
    def red(text, style=None):
        return ColoredText.colorize(text, ColoredText.RED, style=style)

    @staticmethod
    def green(text, style=None):
        return ColoredText.colorize(text, ColoredText.GREEN, style=style)

    @staticmethod
    def yellow(text, style=None):
        return ColoredText.colorize(text, ColoredText.YELLOW, style=style)

    @staticmethod
    def blue(text, style=None):
        return ColoredText.colorize(text, ColoredText.BLUE, style=style)

    @staticmethod
    def magenta(text, style=None):
        return ColoredText.colorize(text, ColoredText.MAGENTA, style=style)

    @staticmethod
    def cyan(text, style=None):
        return ColoredText.colorize(text, ColoredText.CYAN, style=style)

    @staticmethod
    def white(text, style=None):
        return ColoredText.colorize(text, ColoredText.WHITE, style=style)

    # Methods for Bright Colors
    @staticmethod
    def bright_black(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_BLACK, style=style)

    @staticmethod
    def bright_red(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_RED, style=style)

    @staticmethod
    def bright_green(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_GREEN, style=style)

    @staticmethod
    def bright_yellow(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_YELLOW, style=style)

    @staticmethod
    def bright_blue(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_BLUE, style=style)

    @staticmethod
    def bright_magenta(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_MAGENTA, style=style)

    @staticmethod
    def bright_cyan(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_CYAN, style=style)

    @staticmethod
    def bright_white(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_WHITE, style=style)

    # Methods for Color Combinations
    @staticmethod
    def red_on_white(text, style=None):
        return ColoredText.colorize(text, ColoredText.RED, bg_color=ColoredText.BG_WHITE, style=style)

    @staticmethod
    def blue_on_yellow(text, style=None):
        return ColoredText.colorize(text, ColoredText.BLUE, bg_color=ColoredText.BG_YELLOW, style=style)

    @staticmethod
    def bright_cyan_on_black(text, style=None):
        return ColoredText.colorize(text, ColoredText.BRIGHT_CYAN, bg_color=ColoredText.BG_BLACK, style=style)

# uncomment the below chunk of code to see the example usage 

# Example usage:
#if __name__ == "__main__":
#    print(ColoredText.red("This is red text.", style=ColoredText.BOLD))
#    print(ColoredText.green("This is green text with no style."))
#    print(ColoredText.bright_blue("This is bright blue text."))
#    print(ColoredText.red_on_white("This is red text on a white background.", style=ColoredText.UNDERLINE))
#    print(ColoredText.rgb("This is custom RGB text.", 255, 165, 0))  # Orange color
#    print(ColoredText.color256("This is a 256-color text.", 160))  # Custom 256-color
#    print(ColoredText.bright_cyan_on_black("Bright cyan on black background"))
    