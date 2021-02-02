import pygame as pg

# Darken col to percent of its initial value
def darken_col(col, percent=0.7):
    darker_col = pg.Color(col)
    h,s,v,a = darker_col.hsva
    darker_col.hsva = (h, s, v*percent, a)
    return darker_col

class Button:
    def __init__(self, text, rect, color, onclick = None):
        self.rect = rect
        self.color = color
        self.color_dark = darken_col(color)
        self.text = text
        self.onclick = onclick

        smallfont = pg.font.SysFont('Corbel', 35)
        self.textsurface = smallfont.render(text, True, pg.Color("white"))

    def draw(self, surface, mpos):
        is_hovered = self.rect.collidepoint(mpos)
        pg.draw.rect(surface, self.color_dark if is_hovered else self.color, self.rect)
        text_rect = self.textsurface.get_rect()
        surface.blit(self.textsurface, (self.rect.x + (self.rect.w - text_rect.w)/2, (self.rect.y+(self.rect.h - text_rect.h)/2)))
    
    def check_press(self, mpos):
        if self.rect.collidepoint(mpos):
            print(f"Button {self.text} pressed")
            if self.onclick is not None:
                self.onclick()