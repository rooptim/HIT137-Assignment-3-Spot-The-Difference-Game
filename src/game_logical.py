class GameLogic:
    """
    Controls the rules and flow of the Spot-the-Difference game.
    Tracks regions, mistakes, and win/lose conditions.
    """

    def __init__(self, image_manager, max_mistakes=3):
        self.image_manager = image_manager
        self.max_mistakes = max_mistakes
        self.mistakes = 0
        self.game_over = False

    def start_game(self):
        """
        Load a new image and prepare a fresh round.
        """
        self.mistakes = 0
        self.game_over = False
        self.image_manager.prepare_image()

    def check_click(self, x, y):
        """
        Check whether a click matches an unfound difference.

        Returns:
            tuple: (found, region)
                found: True if a difference was found, otherwise False
                region: the matched DifferenceRegion, or None
        """
        if self.game_over:
            return False, None

        for region in self.image_manager.regions:
            if not region.is_found() and region.contains_point(x, y):
                region.mark_found()
                if self.all_found():
                    self.game_over = True
                return True, region

        self.mistakes += 1
        if self.mistakes >= self.max_mistakes:
            self.game_over = True

        return False, None

    def all_found(self):
        """
        Return True if all difference regions have been found.
        """
        return all(region.is_found() for region in self.image_manager.regions)

    def remaining_differences(self):
        """
        Return the number of unfound differences.
        """
        return sum(not region.is_found() for region in self.image_manager.regions)

    def is_game_over(self):
        """
        Return True if the current round is finished.
        """
        return self.game_over

    def get_mistakes(self):
        """
        Return the current number of mistakes.
        """
        return self.mistakes

    def reveal_all(self):
        """
        Mark every region as found and end the game.
        """
        for region in self.image_manager.regions:
            region.mark_found()
        self.game_over = True

    def reset(self):
        """
        Reset the game state for the current image.
        """
        self.mistakes = 0
        self.game_over = False
        for region in self.image_manager.regions:
            region.found = False

    def get_found_regions(self):
        """
        Return a list of all found regions.
        """
        return [region for region in self.image_manager.regions if region.is_found()]

    def get_unfound_regions(self):
        """
        Return a list of all unfound regions.
        """
        return [region for region in self.image_manager.regions if not region.is_found()]
