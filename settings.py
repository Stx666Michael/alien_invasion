class Settings():
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (225,225,225)

        self.FPS = 200

        self.ship_speed = 300
        self.ship_speed_factor = self.ship_speed/self.FPS

        self.bullet_speed_factor = 250/self.FPS
        self.bullets_allowed = 10

        self.alien_speed_factor = 400/self.FPS
        self.alien_speed_factor_y = 50/self.FPS

    def set_speed(self,real_fps):
        self.ship_speed_factor = self.ship_speed/real_fps

        self.bullet_speed_factor = 250/real_fps

        self.alien_speed_factor = 400/real_fps
        self.alien_speed_factor_y = 50/real_fps
        

        

