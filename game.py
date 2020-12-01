from scenarios import BasicScenario


class Game:
    """
    Базовый класс для запуска игры
    """
    def start_game(self):
        scenario = BasicScenario()
        scenario.start()

    def game_over(self):
        pass

    def exit(self):
        pass

    def play_again(self):
        print('\nСыграешь ещё раз? (да или нет)')
        answer = input(">").lower()
        if answer == 'да':
            self.start_game()
        elif answer == 'нет':
            self.exit()
        else:
            print('\nЧто-то пошло не так.')
            self.play_again()
