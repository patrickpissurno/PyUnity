from pyunity import Game, Scene, Instantiate
from pyunity import GameObject, GameUI, TextUI
from pyunity import Input, KeyCode
from pyunity import Random


#DEFINE OBJECTS


class Player(GameObject):
    def __init__(self):
        self.base()
        self.setSprite("player")
        return

    def onUpdate(self, game):
        if Input.GetKeyDown(KeyCode.S):
            self.vspeed = 0.5
        elif Input.GetKeyDown(KeyCode.W):
            self.vspeed = -0.5
        elif Input.GetKeyUp(KeyCode.S) or Input.GetKeyUp(KeyCode.W):
            self.vspeed = 0

        if Input.GetKeyDown(KeyCode.D):
            self.hspeed = 0.5
        elif Input.GetKeyDown(KeyCode.A):
            self.hspeed = -0.5
        elif Input.GetKeyUp(KeyCode.D) or Input.GetKeyUp(KeyCode.A):
            self.hspeed = 0
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
    def onStart(self, game):
        Instantiate(Player, 500, 80)
        Instantiate(DragSquare, 200, 200)
        Instantiate(HelloWorld, 400, 200)
        Instantiate(Instructions, 100, 50)
        return

    def onUpdate(self, game):
        if Input.GetKeyUp(KeyCode.F5):
            game.loadScene(MyScene)
        return

    def onDraw(self, game):
        if Input.GetMouseButtonUp(2):
            self.backgroundColor = (Random.Range(0, 255), Random.Range(0, 255), Random.Range(0, 255))
        return

#RUN GAME

Game.setTitle("PyUnity - First Game")
Game.init(MyScene)