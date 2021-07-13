class GameStats:
    """Track statistics for game alien invasion"""

    def __init__(self, ai):
        """Initializing statistics"""
        self.settings = ai.settings
        self.reset_stats()
        self.game = False

        # High score should never be reset.
        self.high_score = self.get_high_score()

    def get_high_score(self):
        """Gets high score from file, if it exists."""
        try:
            with open('high_score.txt') as hr:
                print("JSON 200")
                high = hr.read()
                return high
        except FileNotFoundError:
            print("JSON 404")
            return 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        #  Bug
        # self.dsec_level = f"Fleet : {self.level}"
