class InvalidFont(Exception):
    def __init__(self, font):
        self.font = font
        super().__init__(f"Invalid font: {self.font}. Please use a font from pygame.font.get_fonts()")
