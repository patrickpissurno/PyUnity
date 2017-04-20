import pygame
import random
from PPlay.sprite import Sprite
from PPlay.window import *
from PPlay.mouse import *
from keycode import _KeyCode

pygame.init()


class _Game(object):
    def __init__(self):
        self.window = Window(800, 600)
        self.input = _Input()
        self.activeScene = None
        return

    def init(self, scene):
        self.loadScene(scene)
        self.loop()
        return self

    def loadScene(self, scene):
        if scene is not None:
            self.activeScene = scene()
            self.activeScene.onStart(self)
        return

    def update(self):
        if self.activeScene is not None:
            self.activeScene.onUpdate(self)
            for obj in self.activeScene.objects:
                obj.baseUpdate(self)

        self.input.update()
        return

    def draw(self):
        if self.activeScene is not None:
            self.window.set_background_color((self.activeScene.backgroundColor[0], self.activeScene.backgroundColor[1], self.activeScene.backgroundColor[2]))
            self.activeScene.onDraw(self)
            for obj in self.activeScene.objects:
                obj.baseDraw(self)
        return

    def loop(self):
        while True:
            self.update()
            self.draw()
            self.window.update()

    def instantiate(self, obj, x, y):
        if self.activeScene is not None:
            o = obj()
            o.x = x
            o.y = y
            self.activeScene.objects.append(o)
            return o
        else:
            return None

    def setTitle(self, text):
        self.window.set_title(text)
        return


class GameObject(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.vspeed = 0
        self.hspeed = 0
        self.sprite = None
        return

    def base(self):
        GameObject.__init__(self)
        return

    def setSprite(self, name):
        if name == None:
            self.sprite = None
            self.width = 0
            self.height = 0
        else:
            self.sprite = Sprite(name + ".png")
            self.width = self.sprite.width
            self.height = self.sprite.height

    def onUpdate(self, game):
        return

    def onDraw(self, game):
        return

    def baseUpdate(self, game):
        self.onUpdate(game)

        self.x += self.hspeed
        self.y += self.vspeed
        return

    def baseDraw(self, game):
        if self.sprite is not None:
            self.sprite.set_position(self.x, self.y)
            self.sprite.draw()

        self.onDraw(game)
        return


class GameUI(GameObject):
    def __init__(self):
        self.isDragging = False
        self.draggable = False
        return

    def base(self):
        GameObject.base(self)
        GameUI.__init__(self)
        return

    def baseUpdate(self, game):
        if self.draggable:
            if Input.GetMouseButtonDown(0) and self.x <= Input.mousePosition[0] < self.x + self.width and self.y <= \
                    Input.mousePosition[1] < self.y + self.height:
                self.isDragging = True
            elif self.isDragging and Input.GetMouseButtonUp(0):
                self.isDragging = False

            if self.isDragging:
                self.hspeed = 0
                self.vspeed = 0
                self.x = Input.mousePosition[0] - self.width/2
                self.y = Input.mousePosition[1] - self.height/2

        GameObject.baseUpdate(self, game)


class TextUI(GameUI):
    def __init__(self):
        self.text = ""
        self.color = (0, 0, 0)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        return

    def base(self):
        GameUI.base(self)
        TextUI.__init__(self)
        return

    def baseDraw(self, game):
        if self.font is not None:
            surface = self.font.render(self.text, True, self.color)
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            game.window.get_screen().blit(surface, rect)
        return

    def setText(self, text):
        self.text = text
        size = self.font.size(self.text)
        self.width = size[0]
        self.height = size[1]
        return

    def setColor(self, color):
        self.color = color
        return


class Scene(object):
    def __init__(self):
        self.backgroundColor = [0, 0, 0]
        self.objects = []
        return

    def base(self):
        Scene.__init__(self)
        return

    def onStart(self, game):
        return

    def onUpdate(self, game):
        return

    def onDraw(self, game):
        return

    def baseStart(self, game):
        self.onStart(game)
        return

    def baseUpdate(self, game):
        self.onUpdate(game)
        return

    def baseDraw(self, game):
        self.onDraw(game)
        return


class _Input(object):
    def __init__(self):
        self.keyboard = Window.get_keyboard()
        self.mouse = Mouse()

        self.lastKeys = pygame.key.get_pressed()
        self.lastMouseButtons = [pygame.mouse.get_pressed()] * 2
        self.mousePosition = self.mouse.get_position()
        return

    def update(self):
        self.lastKeys = pygame.key.get_pressed()
        self.mousePosition = self.mouse.get_position()

        self.lastMouseButtons[1] = self.lastMouseButtons[0]
        self.lastMouseButtons[0] = pygame.mouse.get_pressed()
        return

    def GetKey(self, key):
        if isinstance(key, basestring):
            key = self.keyboard.to_pattern(key)
        return pygame.key.get_pressed()[key] == 1

    def GetKeyDown(self, key):
        if isinstance(key, basestring):
            key = self.keyboard.to_pattern(key)
        return self.lastKeys[key] != 1 and pygame.key.get_pressed()[key] == 1

    def GetKeyUp(self, key):
        if isinstance(key, basestring):
            key = self.keyboard.to_pattern(key)
        return self.lastKeys[key] == 1 and pygame.key.get_pressed()[key] != 1

    def GetMouseButton(self, button):
        return pygame.mouse.get_pressed()[button] == 1

    def GetMouseButtonDown(self, button):
        return self.lastMouseButtons[1][button] != 1 and pygame.mouse.get_pressed()[button] == 1

    def GetMouseButtonUp(self, button):
        return self.lastMouseButtons[1][button] == 1 and pygame.mouse.get_pressed()[button] != 1


class _Random(object):
    def Range(self, min, max):
        if type(min) == float or type(max) == float:
            return random.uniform(float(min), float(max))
        else:
            return random.randint(min, max)

KeyCode = _KeyCode()
Game = _Game()
Input = Game.input
Random = _Random()
Instantiate = Game.instantiate