import unittest
import pygame
import Controller
import Game
import time

# """
# Here are all the possible methods we can use for our tests:

# assertEquals(a, b) --> a = b
# assertNotEqual(a, b) --> a != b
# assertTrue(x) --> bool(x) is True
# assertFalse(x) --> bool(x) is False
# assertIs(a, b) --> a is b
# assertIsNot(a, b) --> a is not b
# 3assertIsNone(x) --> x is None
# assertIn(a, b) --> a in b
# assertNotIn(a, b) --> a not in b
# assertIsInstance(a, b) --> isinstance(a, b)
# assertNotIsInstance(a, b)  --> not isinstance(a, b)

# """

# below is the structure for creating tests using a simple addition function as an example

# if the game gets to this line of code, then there were no errors creating a player and the test has passed
# this format will be followed in all test cases in which an object is being instantiated


class testFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Controller.add(2, 4), 6)
        self.assertEqual(Controller.add(-1, 1), 0)
        self.assertEqual(Controller.add(-1, -1), -2)
        self.assertEqual(Controller.add(0, -1), -1)


class testController(unittest.TestCase):
    def test_gameInit(self):
        pygame.init()
        self.assertTrue(True)

class testPlayer(unittest.TestCase):
    def test_player(self):
        player = Game.player(100, 640)
        self.assertTrue(True)

    def test_playerUpdate(self):
        player = Game.player(100, 640)
        prevX = player.rect.x
        # move player around
        if (pygame.event.get == pygame.QUIT):
            self.assertNotEqual(player.rect.x, prevX)

class testHyena(unittest.TestCase):
    def test_hyena(self):
        hyena = Game.hyena(100, 50)
        self.assertTrue(True)
class testWorld(unittest.TestCase):
    def test_world(self):
        player = Game.player(100, 640)
        player.createWorld(Game.world_data)
        self.assertTrue(True)

class testCamera(unittest.TestCase):
    def test_camera(self):
        camera_group = Game.CameraGroup()
        self.assertTrue(True)

    def test_cameraUpdate(self):
        camera_group = Game.CameraGroup()
        camera_group.update()
        self.assertTrue(True)

    def test_cameraDraw(self):
        camera_group = Game.CameraGroup()
        player = Game.player(100, 640)
        camera_group.custom_draw(player)
        self.assertTrue(True)

if __name__ == '__Controller__':
    unittest.Controller()