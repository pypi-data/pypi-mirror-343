# pygame-addons
Contains classes and functions to help make games and guis with pygame

# Notes
I don't know what version of python is needed for this package to work.

Anywhere in the documentation where it says `pg`, it is referring to `pygame`.

This is mainly just a passion project/project to help future projects, but it would be nice if it had some use.

# Features

Here's a list of features that are currently available in this package:

## Classes

Examples of how to use these classes can be found in the examples folder.

### Button
A class that creates a button that can be clicked on.

Parameters:
- pos - The position of the button
- size - The size of the button
- colour - The colour of the button
- text - The text that will be displayed on the button - Default: ""
- text_colour - The colour of the text - Format: str, tuple[int, int, int] or pg.Color - Default: pg.Color("white")
- font - The font of the text - Format: str, pg.font.Font or pg.font.SysFont - Default: "freesansbold"
- font_size - The size of the font - Default: 30


### Input Field
A class that creates an input field that can be typed in.

Parameters:
- pos - The position of the input field
- size - The size of the input field
- colour - The colour of the input field
- active_colour - The colour of the input field when it is active
- background_text - The text that will be displayed when the input field is empty - Format: str or list - Default: ""
- font_colour - The colour of the text - Format: str, tuple[int, int, int] or pg.Color - Default: pg.Color("white")
- font - The font of the text - Format: str, pg.font.Font or pg.font.SysFont - Default: "freesansbold"
- font_size - The size of the font - Default: 30
- max_length - The maximum length of the text in the input field - Default: 10


### Slider
A class that creates a slider that can be used to go through numbers.

Parameters:
- pos - The position of the slider
- size - The size of the slider
- colour - The colour of the slider

pos, size, colour: tuple[int, int, int] | pg.Color, border_colour: tuple[int, int, int] | pg.Color, min_value: int, max_value: int, start_value: int, border_size: int = 3, background_text: str = "", font: str | type[pg.font.Font] | type[pg.font.SysFont] = "freesansbold", font_size=25, font_colour: str | tuple[int, int, int] | pg.Color = pg.Color("white"))
