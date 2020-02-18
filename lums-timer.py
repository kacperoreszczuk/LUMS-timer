import pygame
import jsonpickle
import datetime
import time
import os


class LumsTimer:
    def __init__(self):
        self.init_window()
        self.read_configuration()
        self.init_fonts()

    def init_window(self):
        pygame.init()
        self.display_height = pygame.display.Info().current_h
        self.display_width = pygame.display.Info().current_w
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        self.screen = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

    def read_configuration(self):
        with open("config.json", "r", encoding='utf-8') as file:
            json_string = file.read().encode()
            self.config, self.stages = jsonpickle.decode(json_string)
        for i in range(5):  # poor way to avoid crashing when user scrolls beyond the agenda
            self.stages.append({"name": "", "duration": 0})
        self.stage = 0
        self.phase = "waiting"  # or "counting"
        self.start_time = 0

    def init_fonts(self):
        self.name_fontsize = 180 * self.display_width * self.config["scaling"] // 100 // 1920
        self.next_fontsize = 130 * self.display_width * self.config["scaling"] // 100 // 1920
        self.digits_fontsize = 600 * self.display_width * self.config["scaling"] // 100 // 1920
        self.base_margin = 50 * self.display_width // 1920
        self.cached_fonts = {}

    def get_font(self, size):
        if size not in self.cached_fonts:
            self.cached_fonts[size] = (pygame.font.SysFont("cambria", size))
        return self.cached_fonts[size]

    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    self.event_next()
                if event.key == pygame.K_LEFT or event.key == pygame.K_BACKSPACE:
                    self.event_back()
                if event.key == pygame.K_a:
                    self.event_add_announcement()
                if event.key == pygame.K_s:
                    self.event_swap_with_next()
                if event.key == pygame.K_d:
                    self.event_delete_next()
        return True

    def event_next(self):
        if self.stages[self.stage]["duration"] > 0 and self.phase == "waiting":
            self.phase = "counting"
            self.start_time = time.time()
        else:
            self.phase = "waiting"
            self.stage += 1

    def event_back(self):
        if self.phase == "waiting":
            if self.stage > 0:
                self.stage -= 1
                if self.stages[self.stage]["duration"] > 0:
                    self.phase = "counting"
        else:
            self.phase = "waiting"

    def event_add_announcement(self):
        try:
            announcement_text = self.config["announcement_text"]
        except (LookupError, TypeError):
            announcement_text = "Announcement"  # revert to default text
        self.stages.insert(self.stage + 1, {"name": announcement_text, "duration": 0})

    def event_swap_with_next(self):
        self.stages[self.stage], self.stages[self.stage + 1] = \
            self.stages[self.stage + 1], self.stages[self.stage]

    def event_delete_next(self):
        self.stages.pop(self.stage + 1)

    def get_warning_time(self, duration):
        try:
            return self.config["yellow_warning_time"][str(duration)]
        except (LookupError, TypeError):
            return 120  # revert to default value

    def plot_digits(self):
        duration = self.stages[self.stage]["duration"]
        if duration == 0:
            text = self.render_text_time_o_clock()
        else:
            if self.phase == "waiting":
                text = self.render_text_duration(duration)
            else:
                text = self.render_text_time_left(self.start_time, duration)
        self.screen.blit(text, (self.display_width // 2 - text.get_width() // 2,
                                self.display_height // 4 + 350 * self.display_height // 1080 - text.get_height()))

    def render_text_time_o_clock(self):
        color = (177, 177, 177)
        clock_text = datetime.datetime.fromtimestamp(time.time()).strftime("%H") + ":" + \
            datetime.datetime.fromtimestamp(time.time()).strftime("%M")
        return self.get_font(self.digits_fontsize).render(clock_text, True, color)

    def render_text_duration(self, duration):
        color = (0, 150, 0)
        clock_text = f"{duration // 60:2}:{duration % 60:02}"
        return self.get_font(self.digits_fontsize).render(clock_text, True, color)

    def render_text_time_left(self, start_time, duration):
        time_left = max(0, round(duration - (time.time() - start_time)))
        clock_text = f"{time_left // 60:2}:{time_left % 60:02}"
        if time_left == 0:
            color = (255, 0, 0)
        else:
            if time_left >= self.get_warning_time(duration):
                color = (0, 150, 0)
            else:
                color = (190, 160, 0)
        return self.get_font(self.digits_fontsize).render(clock_text, True, color)

    def render_text_resized_to_window(self, string, init_fontsize, color):
        size = init_fontsize
        allowed_width = self.display_width - self.base_margin * 2
        text = self.get_font(size).render(string, True, color)
        if text.get_width() > allowed_width:
            size = size * allowed_width // text.get_width()
            text = self.get_font(size).render(string, True, color)
        return text

    def loop(self):
        while True:
            if not self.parse_events():
                break

            self.screen.fill((0, 0, 0))

            self.plot_digits()

            # self.name_fontsize
            string_to_plot = self.stages[self.stage]["name"]
            current_text = self.render_text_resized_to_window(string_to_plot, self.name_fontsize, (255, 255, 255))
            self.screen.blit(current_text,
                             (self.display_width // 2 - current_text.get_width() // 2,
                              2 * self.display_height // 3 - current_text.get_height() // 2))

            # print next stage info
            next_name = self.stages[self.stage + 1]["name"]
            if next_name.strip() != "":
                string_to_plot = "Next: " + self.stages[self.stage + 1]["name"]
                next_text = self.render_text_resized_to_window(string_to_plot, self.next_fontsize, (180, 180, 180))
                self.screen.blit(next_text,
                                 (self.display_width - next_text.get_width() - self.base_margin,
                                  self.display_height - next_text.get_height() - self.base_margin // 2))

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(20)


if __name__ == "__main__":
    lums_timer = LumsTimer()
    lums_timer.loop()
