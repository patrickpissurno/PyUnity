from pyunity import Game, Scene, Instantiate, Defaults
from pyunity import GameObject, GameUI, TextUI
from pyunity import Input, KeyCode
from pyunity import Random, Vector2


#DEFINE OBJECTS


class Player(GameObject):
    def __init__(self):
        self.base()
        self.setSprite("player")
        return

    def onUpdate(self):
        if Input.GetKeyDown(KeyCode.S):
            self.velocity.y = 0.5
        elif Input.GetKeyDown(KeyCode.W):
            self.velocity.y = -0.5
        elif Input.GetKeyUp(KeyCode.S) or Input.GetKeyUp(KeyCode.W):
            self.velocity.y = 0

        if Input.GetKeyDown(KeyCode.D):
            self.velocity.x = 0.5
        elif Input.GetKeyDown(KeyCode.A):
            self.velocity.x = -0.5
        elif Input.GetKeyUp(KeyCode.D) or Input.GetKeyUp(KeyCode.A):
            self.velocity.x = 0
        return


class DragSquare(GameUI):
    def __init__(self):
        self.base()
        self.setSprite("ui")
        self.draggable = True
        return


class HelloWorld(TextUI):
    def __init__(self):
        self.base()
        self.setColor((255, 255, 255))
        self.setText("Hello World (Drag me)")
        self.draggable = True
        return


class Instructions(TextUI):
    def __init__(self):
        self.base()
        self.setColor((255, 255, 255))
        self.setText("Walk with W,A,S,D and Right Mouse Button to change color")
        return


#DEFINE SCENE


class MyScene(Scene):
    def __init__(self):
        self.base()
        self.moving = False
        return

    def onStart(self):
        Instantiate(Player, Vector2(500, 80))
        Instantiate(DragSquare, Vector2(200, 200))
        Instantiate(HelloWorld, Vector2(400, 200))
        Instantiate(Instructions, Vector2(100, 50))
        return

    def onUpdate(self):
        if Input.GetKeyUp(KeyCode.F5):
            Game.loadScene(MyScene)
        if Input.GetKeyUp(KeyCode.P):
            self.moving = not self.moving
        if self.moving:
            self.camera.position.x += 0.05

        if Input.GetKeyUp(KeyCode.F11):
            Game.setFullscreen(not Game.getFullscreen())
        return

    def onDraw(self):
        if Input.GetMouseButtonUp(2):
            self.backgroundColor = (Random.Range(0, 255), Random.Range(0, 255), Random.Range(0, 255))
        return

#RUN GAME

Game.setTitle("PyUnity - First Game")

defaults = Defaults()
defaults.resolution = Vector2(1280, 720)
defaults.fullscreen = False

Game.setDefaults(defaults)
Game.init(MyScene)