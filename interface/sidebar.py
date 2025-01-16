import pygame

class SideBar:
    BLACK_COLOR = [0, 0, 0]

    def __init__(self, screen:pygame.Surface, number_of_packages:int, current_state_of_forklift):
        self.screen = screen
        self.number_of_packages = number_of_packages
        self.current_state_of_forklift = current_state_of_forklift
        self.x = self.screen.get_width() * 0.76
        self.y = self.screen.get_height()
        self.current_package = None

    def show_features(self):
        pygame.font.init()
        font = pygame.font.SysFont("arial", 20)
        
        text_matches = { "select_item": "wybieranie przedmiotu", "move_to_item": "jazda do przedmiotu", "move_to_shelf": "odkładanie przedmiotów na półki" }
        
        self.screen.blit(font.render(text_matches[self.current_state_of_forklift],True, self.BLACK_COLOR), [self.x, self.y * 0.18])
        
        if (self.current_state_of_forklift == "move_to_item"):
            font = pygame.font.SysFont("arial", 22)
            features_text = font.render("cechy paczki: ", True, self.BLACK_COLOR)
            self.screen.blit(features_text, [self.x, self.y * 0.25])
            font = pygame.font.SysFont("arial", 20)

            package_features = [str(self.current_package.name),str(self.current_package.weight) + "kg",
                                str(self.current_package.height) + "cm", str(self.current_package.width) + "cm",
                                str(self.current_package.depth) + "cm", str(self.current_package.days_in_store) + "dni"]
            feature_names = ["nazwa","waga", "wysokość", "szerokość", "głębokość", "ilość dni w magazynie"]
            for i in range(0,  len(package_features)):
                feature_text = font.render(
                    feature_names[i] + ": " + str(package_features[i]),
                    True,
                    self.BLACK_COLOR,
                )
                self.screen.blit(
                        feature_text, [self.x, (self.y * 0.31) + (i * self.y * 0.07)]
                    )
        else:
            for i in range(0, 3):
                blank_text = font.render("", False, [0, 0, 0])
                self.screen.blit(
                    blank_text, [self.x, (self.y * 0.39) + (i * self.y * 0.07)]
                )

    def show_side_bar(self):
        pygame.font.init()
        font = pygame.font.SysFont("arial", 24)
        info_text = font.render("Panel informacyjny", True, self.BLACK_COLOR)
        self.screen.blit(info_text, [self.screen.get_width() * 0.8, 0])

        font = pygame.font.SysFont("arial", 20)
        number_of_items_text = font.render(
            "ilość paczek w wózku: " + str(self.number_of_packages),
            True,
            self.BLACK_COLOR,
        )
        self.screen.blit(number_of_items_text, [self.x, self.y * 0.07])

        current_state_of_forklift_text = font.render(
            "aktualny stan wózka: ", True, self.BLACK_COLOR
        )
        self.screen.blit(current_state_of_forklift_text, [self.x, self.y * 0.14])
        self.show_features()
        self.button()

    def button(self):
        font = pygame.font.Font(None, 24)
        button_surface = pygame.Surface((150, 50))
        text = font.render("zakończ", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(button_surface.get_width() / 2, button_surface.get_height() / 2)
        )
        button_surface.blit(text, text_rect)
        self.screen.blit(button_surface, (self.x * 1.06, self.y * 0.8))
