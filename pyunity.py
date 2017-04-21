import pygame
import random
from PPlay.sprite import Sprite
from PPlay.window import *
from PPlay.mouse import *
from keycode import _KeyCode

pygame.init()


class _Game(object):
    def __init__(self):
        self.defaults = Defaults()
        self.window = Window(self.defaults.resolution.x, self.defaults.resolution.y)
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
            if self.defaults.fullscreen:
                self.window.set_fullscreen()
            self.activeScene.onStart()
        return

    def update(self):
        if self.activeScene is not None:
            if len(self.activeScene.toDestroy) > 0:
                self.activeScene.objects = filter(lambda o: o.destroyed is not True, self.activeScene.objects)

            self.activeScene.onUpdate()
            for obj in self.activeScene.objects:
                obj.baseUpdate()

        self.input.update()
        return

    def draw(self):
        if self.activeScene is not None:
            bgColor = self.activeScene.backgroundColor
            self.window.set_background_color((bgColor[0], bgColor[1], bgColor[2]))

            self.activeScene.onDraw()

            camera = self.activeScene.camera

            for obj in self.activeScene.objects:
                if not isinstance(obj, GameUI):
                    #check if object is inside the screen
                    if obj.position.x + obj.size.x > camera.position.x and obj.position.x < camera.position.x + camera.getSize().x and obj.position.y + obj.size.y > camera.position.y and obj.position.y < camera.position.y + camera.getSize().y:
                        realPos = obj.position

                        #Calculate camera-based position
                        obj.position = obj.position.sumWith(self.activeScene.camera.position.byScalar(-1))

                        obj.baseDraw()

                        #Restore real position
                        obj.position = realPos
                else:
                    obj.baseDraw()
        return

    def setFullscreen(self, boolean):
        if boolean:
            self.window.set_fullscreen()
        else:
            self.window.restoreScreen()
        return

    def getFullscreen(self):
        return self.window.fullscreen_enabled

    def loop(self):
        while True:
            self.update()
            self.draw()
            self.window.update()

    def instantiate(self, obj, position):
        if self.activeScene is not None:
            o = obj()
            o.position = position.clone()
            self.activeScene.objects.append(o)
            return o
        else:
            return None

    def setTitle(self, text):
        self.window.set_title(text)
        return

    def setDefaults(self, defaults):
        self.defaults = defaults
        self.window.set_resolution(self.defaults.resolution.x, self.defaults.resolution.y)
        self.setFullscreen(self.defaults.fullscreen)
        return


class GameObject(object):
    def __init__(self):
        self.position = Vector2.zero()
        self.size = Vector2.zero()
        self.velocity = Vector2.zero()
        self.sprite = None
        self.destroyed = False
        return

    def base(self):
        GameObject.__init__(self)
        return

    def __str__(self):
        return str(self.__class__.__name__)

    def setSprite(self, name):
        if name is None:
            self.sprite = None
            self.size = Vector2.zero()
        else:
            self.sprite = Sprite(name + ".png")
            self.size = Vector2(self.sprite.width, self.sprite.height)

    def onUpdate(self):
        return

    def onDraw(self):
        return

    def baseUpdate(self):
        self.onUpdate()
        self.position = self.position.sumWith(self.velocity)
        return

    def baseDraw(self):
        if self.sprite is not None:
            self.sprite.set_position(self.position.x, self.position.y)
            self.sprite.draw()

        self.onDraw()
        return

    def destroy(self):
        self.destroyed = True
        Game.activeScene.toDestroy.append(self)
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

    def baseUpdate(self):
        if self.draggable:
            if Input.GetMouseButtonDown(0) and self.position.x <= Input.mousePosition.x < self.position.x + self.size.x and self.position.y <= \
                    Input.mousePosition.y < self.position.y + self.size.y:
                self.isDragging = True
            elif self.isDragging and Input.GetMouseButtonUp(0):
                self.isDragging = False

            if self.isDragging:
                self.velocity = Vector2.zero()
                self.position = Input.mousePosition.sumWith(self.size.byScalar(-0.5))
                # self.position.x = Input.mousePosition.x - self.size.x / 2
                # self.position.y = Input.mousePosition.y - self.size.y / 2

        GameObject.baseUpdate(self)


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

    def baseDraw(self):
        if self.font is not None:
            surface = self.font.render(self.text, True, self.color)
            rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
            Game.window.get_screen().blit(surface, rect)
        return

    def setText(self, text):
        self.text = text
        size = self.font.size(self.text)
        self.size = Vector2(size[0], size[1])
        return

    def setColor(self, color):
        self.color = color
        return


class Camera(object):
    def __init__(self, position):
        self.position = position.clone()
        return

    def getSize(self):
        return Vector2(Game.window.width, Game.window.height)


class Scene(object):
    def __init__(self):
        self.backgroundColor = (0, 0, 0)
        self.objects = []
        self.toDestroy = []
        self.camera = Camera(Vector2.zero())
        return

    def base(self):
        Scene.__init__(self)
        return

    def onStart(self):
        return

    def onUpdate(self):
        return

    def onDraw(self):
        return

    def baseStart(self):
        self.onStart()
        return

    def baseUpdate(self):
        self.onUpdate()
        return

    def baseDraw(self):
        self.onDraw()
        return


class _Input(object):
    def __init__(self):
        self.keyboard = Window.get_keyboard()
        self.mouse = Mouse()

        self.lastKeys = pygame.key.get_pressed()
        self.lastMouseButtons = [pygame.mouse.get_pressed()] * 2

        mPos = self.mouse.get_position()
        self.mousePosition = Vector2(mPos[0], mPos[1])
        return

    def update(self):
        self.lastKeys = pygame.key.get_pressed()

        mPos = self.mouse.get_position()
        self.mousePosition = Vector2(mPos[0], mPos[1])

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


class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def sumWith(self, vector2):
        clone = self.clone()
        if vector2 is not None:
            clone.x += vector2.x
            clone.y += vector2.y
        return clone

    def byScalar(self, factor):
        clone = self.clone()
        if factor is not None:
            clone.x *= factor
            clone.y *= factor
        return clone

    def clone(self):
        return Vector2(self.x, self.y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    @staticmethod
    def zero():
        return Vector2(0, 0)


class Defaults():
    def __init__(self):
        self.resolution = Vector2(800, 600)
        self.fullscreen = False
        return


KeyCode = _KeyCode()
Game = _Game()
Input = Game.input
Random = _Random()
Instantiate = Game.instantiate