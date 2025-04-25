info = """    
# enhanced_colored_text.py    
# Original Author: Basit Ahmad Ganie    
# email: basitahmed1412@gmail.com    
# Enhanced version with additional features and methods    
# This code provides a comprehensive solution for colored terminal text output    
# with support for gradients, animations, presets, and more.    
"""    
    
import time    
import sys    
import random    
import math    
from typing import List, Dict, Union, Tuple, Optional, Callable    
    
    
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
    DIM = 2    
    ITALIC = 3  # Not widely supported    
    UNDERLINE = 4    
    BLINK = 5    
    RAPID_BLINK = 6  # Not widely supported    
    REVERSE = 7    
    HIDDEN = 8    
    STRIKETHROUGH = 9  # Not widely supported    
    RESET = 0    
    
    # Common color presets (RGB values)    
    COLOR_PRESETS = {    
        "forest_green": (34, 139, 34),    
        "sky_blue": (135, 206, 235),    
        "coral": (255, 127, 80),    
        "gold": (255, 215, 0),    
        "lavender": (230, 230, 250),    
        "tomato": (255, 99, 71),    
        "teal": (0, 128, 128),    
        "salmon": (250, 128, 114),    
        "violet": (238, 130, 238),    
        "khaki": (240, 230, 140),    
        "turquoise": (64, 224, 208),    
        "firebrick": (178, 34, 34),    
        "navy": (0, 0, 128),    
        "steel_blue": (70, 130, 180),    
        "olive": (128, 128, 0),    
        "spring_green": (0, 255, 127),    
        "crimson": (220, 20, 60),    
        "chocolate": (210, 105, 30),    
        "midnight_blue": (25, 25, 112),    
        "orchid": (218, 112, 214),    
    }    
    
    # Terminal theme presets    
    THEME_PRESETS = {    
        "matrix": {"fg": (0, 255, 0), "bg": (0, 0, 0), "style": BOLD},    
        "ocean": {"fg": (0, 191, 255), "bg": (0, 0, 139), "style": None},    
        "sunset": {"fg": (255, 165, 0), "bg": (178, 34, 34), "style": None},    
        "forest": {"fg": (34, 139, 34), "bg": (0, 100, 0), "style": None},    
        "neon": {"fg": (255, 0, 255), "bg": (0, 0, 0), "style": BOLD},    
        "pastel": {"fg": (255, 192, 203), "bg": (230, 230, 250), "style": None},    
        "retro": {"fg": (255, 165, 0), "bg": (0, 0, 0), "style": BOLD},    
        "cyberpunk": {"fg": (0, 255, 255), "bg": (139, 0, 139), "style": BOLD},    
        "desert": {"fg": (210, 180, 140), "bg": (244, 164, 96), "style": None},    
        "dracula": {"fg": (248, 248, 242), "bg": (40, 42, 54), "style": None},    
    }    
    
    @staticmethod    
    def colorize(text, fg_color=None, bg_color=None, style=None):    
        """Apply color and style to text."""    
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
        """Print text with color and style."""    
        print(ColoredText.colorize(text, fg_color, bg_color, style))    
    
    @staticmethod    
    def color256(text, color_code, bg_code=None, style=None):    
        """Apply a color from the 256-color palette."""    
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
        """Apply an RGB color to text."""    
        # Ensure RGB values are within valid range    
        r = max(0, min(255, r))    
        g = max(0, min(255, g))    
        b = max(0, min(255, b))    
            
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
    
    @staticmethod    
    def rgb_bg(text, r, g, b, fg_r=None, fg_g=None, fg_b=None, style=None):    
        """Apply an RGB background color with optional RGB foreground."""    
        # Ensure RGB values are within valid range    
        r = max(0, min(255, r))    
        g = max(0, min(255, g))    
        b = max(0, min(255, b))    
            
        codes = []    
        if style is not None:    
            codes.append(str(style))    
            
        # Add foreground color if provided    
        if fg_r is not None and fg_g is not None and fg_b is not None:    
            fg_r = max(0, min(255, fg_r))    
            fg_g = max(0, min(255, fg_g))    
            fg_b = max(0, min(255, fg_b))    
            codes.append(f"38;2;{fg_r};{fg_g};{fg_b}")    
            
        # Add background color    
        codes.append(f"48;2;{r};{g};{b}")    
            
        color_prefix = f"\033[{';'.join(codes)}m"    
        color_suffix = "\033[0m"    
        return f"{color_prefix}{text}{color_suffix}"    
    
    @staticmethod    
    def hex_color(text, hex_code, bg=False, style=None):    
        """Apply a color using a hex color code (e.g., #FF5733)."""    
        hex_code = hex_code.lstrip('#')    
        if len(hex_code) == 3:  # Handle shorthand hex code    
            hex_code = ''.join([c * 2 for c in hex_code])    
            
        if len(hex_code) != 6:    
            raise ValueError("Invalid hex code. Expected format: #RRGGBB")    
            
        # Convert hex to RGB    
        r = int(hex_code[0:2], 16)    
        g = int(hex_code[2:4], 16)    
        b = int(hex_code[4:6], 16)    
            
        return ColoredText.rgb(text, r, g, b, bg=bg, style=style)    
    
    @staticmethod    
    def hex_bg(text, hex_code, fg_hex=None, style=None):    
        """Apply a hex background color with optional hex foreground."""    
        # Background color    
        hex_code = hex_code.lstrip('#')    
        if len(hex_code) == 3:  # Handle shorthand hex code    
            hex_code = ''.join([c * 2 for c in hex_code])    
            
        if len(hex_code) != 6:    
            raise ValueError("Invalid hex code for background. Expected format: #RRGGBB")    
            
        # Convert hex to RGB for background    
        r = int(hex_code[0:2], 16)    
        g = int(hex_code[2:4], 16)    
        b = int(hex_code[4:6], 16)    
            
        # Foreground color if provided    
        fg_r, fg_g, fg_b = None, None, None    
        if fg_hex:    
            fg_hex = fg_hex.lstrip('#')    
            if len(fg_hex) == 3:  # Handle shorthand hex code    
                fg_hex = ''.join([c * 2 for c in fg_hex])    
                
            if len(fg_hex) != 6:    
                raise ValueError("Invalid hex code for foreground. Expected format: #RRGGBB")    
                
            fg_r = int(fg_hex[0:2], 16)    
            fg_g = int(fg_hex[2:4], 16)    
            fg_b = int(fg_hex[4:6], 16)    
            
        return ColoredText.rgb_bg(text, r, g, b, fg_r, fg_g, fg_b, style)    
    
    @staticmethod    
    def hsl_to_rgb(h, s, l):    
        """Convert HSL to RGB color values."""    
        # Normalize values    
        h = h % 360    
        s = max(0, min(1, s))    
        l = max(0, min(1, l))    
            
        if s == 0:    
            r = g = b = l    
        else:    
            def hue_to_rgb(p, q, t):    
                t %= 1    
                if t < 1/6: return p + (q - p) * 6 * t    
                if t < 1/2: return q    
                if t < 2/3: return p + (q - p) * (2/3 - t) * 6    
                return p    
                
            q = l * (1 + s) if l < 0.5 else l + s - l * s    
            p = 2 * l - q    
            r = hue_to_rgb(p, q, h / 360 + 1/3)    
            g = hue_to_rgb(p, q, h / 360)    
            b = hue_to_rgb(p, q, h / 360 - 1/3)    
            
        return (int(r * 255), int(g * 255), int(b * 255))    
    
    @staticmethod    
    def hsl(text, h, s, l, bg=False, style=None):    
        """Apply an HSL color to text."""    
        r, g, b = ColoredText.hsl_to_rgb(h, s, l)    
        return ColoredText.rgb(text, r, g, b, bg=bg, style=style)    
    
    @staticmethod    
    def hsl_bg(text, h, s, l, fg_h=None, fg_s=None, fg_l=None, style=None):    
        """Apply an HSL background color with optional HSL foreground."""    
        r, g, b = ColoredText.hsl_to_rgb(h, s, l)    
            
        fg_r, fg_g, fg_b = None, None, None    
        if fg_h is not None and fg_s is not None and fg_l is not None:    
            fg_r, fg_g, fg_b = ColoredText.hsl_to_rgb(fg_h, fg_s, fg_l)    
            
        return ColoredText.rgb_bg(text, r, g, b, fg_r, fg_g, fg_b, style)    
    
    @staticmethod    
    def from_preset(text, preset_name, style=None):    
        """Use a predefined color preset."""    
        if preset_name not in ColoredText.COLOR_PRESETS:    
            available = ', '.join(ColoredText.COLOR_PRESETS.keys())    
            raise ValueError(f"Unknown preset '{preset_name}'. Available presets: {available}")    
            
        r, g, b = ColoredText.COLOR_PRESETS[preset_name]    
        return ColoredText.rgb(text, r, g, b, style=style)    
    
    @staticmethod    
    def from_theme(text, theme_name):    
        """Apply a predefined theme (foreground and background colors)."""    
        if theme_name not in ColoredText.THEME_PRESETS:    
            available = ', '.join(ColoredText.THEME_PRESETS.keys())    
            raise ValueError(f"Unknown theme '{theme_name}'. Available themes: {available}")    
            
        theme = ColoredText.THEME_PRESETS[theme_name]    
        fg_r, fg_g, fg_b = theme["fg"]    
        bg_r, bg_g, bg_b = theme["bg"]    
        style = theme["style"]    
            
        return ColoredText.rgb_bg(text, bg_r, bg_g, bg_b, fg_r, fg_g, fg_b, style)    
    
    @staticmethod    
    def random_color(text, style=None):    
        """Apply a random color to text."""    
        r = random.randint(0, 255)    
        g = random.randint(0, 255)    
        b = random.randint(0, 255)    
        return ColoredText.rgb(text, r, g, b, style=style)    
    
    @staticmethod    
    def random_bg(text, style=None):    
        """Apply a random background color to text with auto-contrasting foreground."""    
        bg_r = random.randint(0, 255)    
        bg_g = random.randint(0, 255)    
        bg_b = random.randint(0, 255)    
            
        # Calculate perceived brightness (luminance) of background    
        luminance = (0.299 * bg_r + 0.587 * bg_g + 0.114 * bg_b) / 255    
            
        # Choose white or black text based on background brightness    
        fg_r, fg_g, fg_b = (0, 0, 0) if luminance > 0.5 else (255, 255, 255)    
            
        return ColoredText.rgb_bg(text, bg_r, bg_g, bg_b, fg_r, fg_g, fg_b, style)    
    
    @staticmethod    
    def gradient_text(text, start_rgb, end_rgb, style=None):    
        """Apply a horizontal gradient to text."""    
        start_r, start_g, start_b = start_rgb    
        end_r, end_g, end_b = end_rgb    
            
        result = ""    
        for i, char in enumerate(text):    
            if char.isspace():    
                result += char    
                continue    
                    
            # Calculate the color for this position    
            ratio = i / max(1, len(text) - 1)    
            r = int(start_r + (end_r - start_r) * ratio)    
            g = int(start_g + (end_g - start_g) * ratio)    
            b = int(start_b + (end_b - start_b) * ratio)    
                
            result += ColoredText.rgb(char, r, g, b, style=style)    
            
        return result    
    
    @staticmethod    
    def rainbow(text, style=None):    
        """Apply rainbow colors to text."""    
        colors = [    
            (255, 0, 0),    # Red    
            (255, 127, 0),  # Orange    
            (255, 255, 0),  # Yellow    
            (0, 255, 0),    # Green    
            (0, 0, 255),    # Blue    
            (75, 0, 130),   # Indigo    
            (143, 0, 255)   # Violet    
        ]    
            
        result = ""    
        for i, char in enumerate(text):    
            if char.isspace():    
                result += char    
                continue    
                    
            # Choose a color from the rainbow    
            color_idx = i % len(colors)    
            r, g, b = colors[color_idx]    
                
            result += ColoredText.rgb(char, r, g, b, style=style)    
            
        return result    
    
    @staticmethod    
    def animate_text(text, animation_type='typing', speed=0.05, cycles=1):    
        """    
        Animate text using various effects.    
            
        animation_type options:    
        - 'typing': Simulates typing effect    
        - 'fade_in': Characters fade in from dim to bright    
        - 'blink': Text blinks    
        - 'rainbow_wave': Rainbow colors moving through the text    
        - 'bounce': Text appears to bounce    
        """    
        def clear_line():    
            sys.stdout.write('\r')    
            sys.stdout.write(' ' * (len(text) + 10))    
            sys.stdout.write('\r')    
            sys.stdout.flush()    
            
        if animation_type == 'typing':    
            for i in range(len(text) + 1):    
                sys.stdout.write('\r' + text[:i])    
                sys.stdout.flush()    
                time.sleep(speed)    
            print()    
            
        elif animation_type == 'fade_in':    
            for brightness in range(0, 101, 5):    
                # Convert brightness percentage to RGB value    
                value = int(brightness * 2.55)    
                colored_text = ColoredText.rgb(text, value, value, value)    
                sys.stdout.write('\r' + colored_text)    
                sys.stdout.flush()    
                time.sleep(speed)    
            print()    
            
        elif animation_type == 'blink':    
            for _ in range(cycles):    
                # Show    
                sys.stdout.write('\r' + text)    
                sys.stdout.flush()    
                time.sleep(speed)    
                    
                # Hide    
                clear_line()    
                time.sleep(speed)    
                
            # Ensure text is visible at the end    
            print(text)    
            
        elif animation_type == 'rainbow_wave':    
            hue_offset = 0    
            for _ in range(cycles * 360):    
                result = ""    
                for i, char in enumerate(text):    
                    if char.isspace():    
                        result += char    
                        continue    
                        
                    # Calculate color based on position and time    
                    hue = (i * 10 + hue_offset) % 360    
                    r, g, b = ColoredText.hsl_to_rgb(hue, 1, 0.5)    
                    result += ColoredText.rgb(char, r, g, b)    
                    
                sys.stdout.write('\r' + result)    
                sys.stdout.flush()    
                time.sleep(speed)    
                hue_offset = (hue_offset + 5) % 360    
                
            print()    
            
        elif animation_type == 'bounce':    
            baseline = 0    
            for _ in range(cycles):    
                for amplitude in range(0, 5) + list(reversed(range(1, 4))):    
                    result = ""    
                    for i, char in enumerate(text):    
                        if char.isspace():    
                            result += char    
                            continue    
                            
                        # Calculate vertical position for this character    
                        char_amplitude = amplitude * math.sin(i / 2)    
                        padding = ' ' * int(abs(char_amplitude))    
                            
                        if char_amplitude >= 0:    
                            result += padding + char    
                        else:    
                            result += char + padding    
                        
                    sys.stdout.write('\r' + result)    
                    sys.stdout.flush()    
                    time.sleep(speed)    
                
            print()    
            
        else:    
            print(f"Unknown animation type: {animation_type}")    
    
    @staticmethod    
    def table(text, padding=1, border_style='single', fg_color=None, bg_color=None, style=None):    
        """    
        Create a box around text with customizable borders and padding.    
            
        border_style options:    
        - 'single': Single line box    
        - 'double': Double line box    
        - 'rounded': Rounded corners    
        - 'bold': Bold lines    
        - 'dashed': Dashed lines    
        """    
        lines = text.split('\n')    
        width = max(len(line) for line in lines)    
            
        # Set border characters based on style    
        if border_style == 'single':    
            tl, t, tr = '┌', '─', '┐'    
            l, r = '│', '│'    
            bl, b, br = '└', '─', '┘'    
        elif border_style == 'double':    
            tl, t, tr = '╔', '═', '╗'    
            l, r = '║', '║'    
            bl, b, br = '╚', '═', '╝'    
        elif border_style == 'rounded':    
            tl, t, tr = '╭', '─', '╮'    
            l, r = '│', '│'    
            bl, b, br = '╰', '─', '╯'    
        elif border_style == 'bold':    
            tl, t, tr = '┏', '━', '┓'    
            l, r = '┃', '┃'    
            bl, b, br = '┗', '━', '┛'    
        elif border_style == 'dashed':    
            tl, t, tr = '┌', '┄', '┐'    
            l, r = '┆', '┆'    
            bl, b, br = '└', '┄', '┘'    
        else:    
            tl, t, tr = '+', '-', '+'    
            l, r = '|', '|'    
            bl, b, br = '+', '-', '+'    
            
        # Create horizontal border line    
        horizontal_border = tl + t * (width + padding * 2) + tr    
        bottom_border = bl + b * (width + padding * 2) + br    
            
        # Create padding line    
        padding_line = l + ' ' * (width + padding * 2) + r    
            
        # Build the result    
        result = [horizontal_border]    
            
        # Add top padding    
        for _ in range(padding):    
            result.append(padding_line)    
            
        # Add content with padding    
        for line in lines:    
            padded_line = l + ' ' * padding + line.ljust(width) + ' ' * padding + r    
            result.append(padded_line)    
            
        # Add bottom padding    
        for _ in range(padding):    
            result.append(padding_line)    
            
        result.append(bottom_border)    
            
        # Apply colors if specified    
        if fg_color is not None or bg_color is not None or style is not None:    
            return ColoredText.colorize('\n'.join(result), fg_color, bg_color, style)    
            
        return '\n'.join(result)    
    
    @staticmethod    
    def progress_bar(progress, width=50, fill_char='█', empty_char='░',     
                     start_char='|', end_char='|', show_percentage=True,     
                     bar_color=None, percentage_color=None):    
        """    
        Create a customizable progress bar.    
            
        Args:    
            progress: Float between 0 and 1    
            width: Width of the progress bar in characters    
            fill_char: Character to use for filled portion    
            empty_char: Character to use for empty portion    
            start_char/end_char: Characters at the start/end of the bar    
            show_percentage: Whether to show percentage    
            bar_color/percentage_color: Optional colors for the bar and percentage    
        """    
        progress = max(0, min(1, progress))  # Ensure progress is between 0 and 1    
        filled_width = int(width * progress)    
        empty_width = width - filled_width    
            
        # Create the bar    
        filled_part = fill_char * filled_width    
        empty_part = empty_char * empty_width    
            
        # Apply color to the bar if specified    
        if bar_color is not None:    
            if isinstance(bar_color, tuple) and len(bar_color) == 3:    
                filled_part = ColoredText.rgb(filled_part, *bar_color)    
            else:    
                filled_part = ColoredText.colorize(filled_part, bar_color)    
                
        # Create the full bar    
        bar = f"{start_char}{filled_part}{empty_part}{end_char}"    
            
        # Add percentage if requested    
        if show_percentage:    
            percentage = f" {int(progress * 100)}%"    
            if percentage_color is not None:    
                if isinstance(percentage_color, tuple) and len(percentage_color) == 3:    
                    percentage = ColoredText.rgb(percentage, *percentage_color)    
                else:    
                    percentage = ColoredText.colorize(percentage, percentage_color)    
            bar += percentage
            
        return bar
        
    @staticmethod
    def multi_color_text(text, color_map=None):
        """
        Apply different colors to different parts of text based on a color map.
        
        Args:
            text: String to color
            color_map: Dictionary mapping substrings to colors (RGB tuples or color constants)
                       e.g. {'error': (255,0,0), 'warning': ColoredText.YELLOW}
        """
        if color_map is None:
            return text
            
        result = text
        for substring, color in color_map.items():
            if substring in text:
                colored_substring = ''
                if isinstance(color, tuple) and len(color) == 3:
                    colored_substring = ColoredText.rgb(substring, *color)
                else:
                    colored_substring = ColoredText.colorize(substring, color)
                result = result.replace(substring, colored_substring)
                
        return result
    
    @staticmethod
    def highlight_text(text, pattern, fg_color=None, bg_color=None, style=None, case_sensitive=False):
        """
        Highlight occurrences of a pattern within text.
        
        Args:
            text: String to search in
            pattern: String to highlight
            fg_color/bg_color/style: Styling for the highlighted text
            case_sensitive: Whether pattern matching should be case sensitive
        """
        if not pattern or pattern not in text:
            if not case_sensitive and pattern.lower() in text.lower():
                # Case-insensitive search
                import re
                result = ''
                last_idx = 0
                for match in re.finditer(re.escape(pattern), text, re.IGNORECASE):
                    result += text[last_idx:match.start()]
                    result += ColoredText.colorize(text[match.start():match.end()], fg_color, bg_color, style)
                    last_idx = match.end()
                result += text[last_idx:]
                return result
            else:
                return text
                
        # Case-sensitive search (default)
        parts = text.split(pattern)
        return pattern.join([parts[0]] + [ColoredText.colorize(pattern, fg_color, bg_color, style) + part for part in parts[1:]])
    
#    @staticmethod
#    def typewriter_effect(text, speed=0.05, style=None, color=None):
#        """
#        Display text with a typewriter effect and optional styling.
#        
#        Args:
#            text: String to display
#            speed: Delay between characters in seconds
#            style: Text style to apply
#            color: Text color to apply
#        """
#        for char in text:
#            if color is not None:
#                if isinstance(color, tuple) and len(color) == 3:
#                    char_display = ColoredText.

if __name__ == '__main__':
    print(ColoredText.rainbow(info))

