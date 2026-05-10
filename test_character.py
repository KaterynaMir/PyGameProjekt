import unittest
import pygame

from character import Character, Enemy, Wolf

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.image = pygame.image.load("./Assets/wolf.png")
        self.character = Character("Wolf", self.image, 3, (605, 405))
    

    def testInitialisation(self):
        self.assertEqual(self.character.name, "Wolf")
        self.assertEqual(self.character.width, self.image.get_width())
        self.assertEqual(self.character.height, self.image.get_height())
        self.assertEqual(self.character.speed, 3)
        self.assertEqual(self.character.x, 605)
        self.assertEqual(self.character.y, 405)
    

    def testCheckInsideScreen(self):
        self.assertTrue(self.character.check_inside_screen(800, 600))
        self.assertFalse(self.character.check_inside_screen(600, 400))
        self.assertEqual(self.character.x, 600 - self.character.width)
        self.assertEqual(self.character.y, 400 - self.character.height)


class TestEnemy(unittest.TestCase):

    def setUp(self):
        self.image = pygame.image.load("./Assets/wolf.png")
        self.enemy = Enemy("Wolf", self.image, 5, (605, 0), "V")

    def testInitialisation(self):
        self.assertEqual(self.enemy.name, "Wolf")
        self.assertEqual(self.enemy.speed, 5)
        self.assertEqual(self.enemy.x, 605)
        self.assertEqual(self.enemy.y, 0)
        self.assertEqual(self.enemy.direction, "V")
    
    def testMove(self):
        self.enemy.move()
        self.assertEqual(self.enemy.y, 5)
        self.enemy.move()
        self.assertEqual(self.enemy.y, 10)
        self.enemy.direction = "H"
        self.enemy.move()
        self.assertEqual(self.enemy.x, 610)
    

class TestWolf(unittest.TestCase):

    def setUp(self):
        self.image = pygame.image.load("./Assets/wolf.png")
        self.wolf = Wolf("Wolf", self.image, 5, (600, 400))
    
    def testInitialisation(self):
        self.assertEqual(self.wolf.name, "Wolf")
        self.assertEqual(self.wolf.speed, 5)
        self.assertEqual(self.wolf.x, 600)
        self.assertEqual(self.wolf.y, 400)
    
    def testMove(self):
        self.wolf.move((0, 3))
        self.assertEqual(self.wolf.x, 595)
        self.assertEqual(self.wolf.y, 400)
        self.wolf.move((0, 3))
        self.assertEqual(self.wolf.x, 590)




if __name__ == '__main__':
    unittest.main()



