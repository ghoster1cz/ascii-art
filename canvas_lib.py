class Canvas:
    def __init__(self, width, height, characters):
        self.width = width
        self.height = height
        self.characters = characters

    def get_character_from_brightness(self, brightness):
        closest = 255
        closest_value = ""
        for key, value in self.characters.items():
            if abs(key - brightness) < closest:
                closest = abs(key - brightness)
                closest_value = value

        return closest_value
