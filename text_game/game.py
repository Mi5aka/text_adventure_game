from scenarios import Scenario
from animation import animated_print


class Game:
    """
    Базовый класс для запуска игры
    """
    def start_game(self) -> None:
        scenario = Scenario()
        scenario.start()

    def exit(self) -> None:
        pass

    def play_again(self) -> None:
        animated_print('\nСыграешь ещё раз? (да или нет)')
        answer = input(">").lower()
        if answer == 'да':
            self.start_game()
        elif answer == 'нет':
            self.exit()
        else:
            animated_print('\nЧто-то пошло не так.')
            self.play_again()
