import unittest

from musicmanager import *

class TestMusicManager(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.muscimanager = MusicManager("pause")
    
    def testInitialisation(self):
        self.assertEqual(self.muscimanager.curent_state,"pause")
        self.assertEqual(list(self.muscimanager.music.keys()),["main_menu","game","pause","game_over","game_win"])
    
    def testPlayTrue(self):
        self.assertTrue(self.muscimanager.play())
    
    def testPlayFalse(self):
        self.muscimanager.music["pause"] = ("",-1)
        self.assertFalse(self.muscimanager.play())
    
    def testUpdate(self):
        self.muscimanager.update("game")
        self.assertEqual(self.muscimanager.curent_state,"game")


if __name__ == '__main__':
    unittest.main()
    pygame.quit()