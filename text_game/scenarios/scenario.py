import os
from finite_state_machine import StateMachine, transition

from data import DESCRIPTION, GAME_ENDINGS
from animation import animated_print
from location import get_location
from states import States


class Scenario(StateMachine):
    """
        Сценарий игры с ответвлениями
        Возможны 4 варианта концовки
    """
    initial_state = States.START

    def __init__(self):
        self.mental_health = 40
        self.state = self.initial_state
        self.have_pills = False
        super().__init__()

    def check_health(self, points: int) -> None:
        self.mental_health += points
        str_points = f'+{points}' if points > 0 else str(points)
        animated_print(
            f'\n {str_points} к твоему состоянию. Здоровье: {self.mental_health}'
        )

    def retry(self, name: str) -> None:
        animated_print('\nЧто-то пошло не так. Давай попробуем снова.')
        fn = getattr(self, name, None)
        if fn is not None:
            fn()

    def is_healthy(self) -> bool:
        if self.mental_health > 0:
            return True
        self.state = States.BAD_ENDING
        animated_print(GAME_ENDINGS['bad_ending'])
        return False

    def check_location(self) -> bool:
        try:
            input('\nЧтобы идти дальше нажми Enter >')
        except UnicodeDecodeError:
            animated_print('\nНу, просили же только Enter нажать. Ладно, идем дальше.')
        os.system('cls||clear')
        location = get_location(self.state)
        animated_print(
            f'\nЛокация: {location}'
        )
        return True

    def drink_pills(self) -> bool:
        if self.have_pills:
            try:
                answer = input('\n>').lower()
                if answer == 'да':
                    self.mental_health += 1
                    animated_print(
                        '\nВыпил таблетку. +1 к твоему состоянию. '
                        f'Здоровье: {self.mental_health}'
                    )
                    return True
                elif answer == 'нет':
                    self.mental_health -= 1
                    animated_print(
                        '\nТы не выпил таблетку. -1 к твоему состоянию. '
                        f'Здоровье: {self.mental_health}'
                    )
                    return False
            except ValueError:
                self.retry('drink_pills')

    @transition(
        source=States.START,
        target=States.BIRTHDAY
    )
    def start(self):
        animated_print(DESCRIPTION)
        self.state = States.BIRTHDAY
        return self.happy_birthday()

    @transition(
        source=States.BIRTHDAY,
        target=States.BIRTHDAY,
        conditions=[is_healthy, check_location]
    )
    def happy_birthday(self):
        animated_print(
            '\nЦелый день знакомые с родственниками тебе присылают '
            'поздравления и ненавязчиво спрашивают «Ну, как там? После 30 жизнь есть?»'
            '\n1. Игнорировать'
            '\n2. Поблагодарить'
            '\n3. Пошутить на тему возраста'
        )
        options = {
            1: ('\nНа тебя обиделось много людей.', -5),
            2: ('\nТы рад, что так много людей вспомнили о твоем существовании.', 1),
            3: ('\nОтшутился и как-то не такой уже и грустный праздник выходит', 0)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            return self.overtiming()
        except (KeyError, ValueError):
            self.retry('happy_birthday')

    @transition(
        source=States.BIRTHDAY,
        target=States.OVERTIMING,
        conditions=[is_healthy, check_location]
    )
    def overtiming(self):
        animated_print(
            '\nЧто-то ты ничего не успеваешь. Сегодня опять засиделся до '
            'поздна. А количество нерешенных задач не уменшилось. Что будем '
            'делать?'
            '\n1. Лягу спать.'
            '\n2. Не буду спать, но доделаю работу.'
            '\n3. Пойду читать статьи об эффективности'
        )
        options = {
            1: ('\nТы выспался и со свежей головой принялся за работу', 5),
            2: ('\nРабота так и не закончена, код отвратительный, ещё ты '
                'разбит полностью из-за недосыпа.', -5),
            3: ('\nНе самое умное решение в 2 часа ночи.', -10)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.OVERTIMING
            return self.food_problem()
        except (KeyError, ValueError):
            self.retry('overtiming')

    @transition(
        source=States.OVERTIMING,
        target=States.FOOD_PROBLEM,
        conditions=[is_healthy, check_location]
    )
    def food_problem(self):
        animated_print(
            '\nЧто-то ты так увлеченно решал задачи, что забыл поесть. Что '
            'будешь делать?'
            '\n1. Пойду поем.'
            '\n2. Попозже, надо тут ещё допроверить PR и отписаться на счет ТЗ.'
            '\n3. Поем за работой. Главное на созвоне вебку выключить.'
        )
        options = {
            1: ('\nПокушал, можно работать дальше', 5),
            2: ('\nНу, привет, гастрит! Давно не виделись', -10),
            3: ('\nТы забыл выключить микрофон и все слышали как ты сербал супчик.', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.FOOD_PROBLEM
            return self.sleep_problems()
        except (KeyError, ValueError):
            self.retry('food_problem')

    @transition(
        source=States.FOOD_PROBLEM,
        target=States.SLEEP_PROBLEMS,
        conditions=[is_healthy, check_location]
    )
    def sleep_problems(self):
        animated_print(
            '\nТы мало спишь. Всё из-за работы. У тебя начались проблемы со '
            'сном и мелатонин уже не помогает т.к. ложишься ты глубокой ночью. '
            'Сон прерывистый. Тебе то жарко, то ты вспомнил очередную проблему '
            'на проекте. Откуда-то кажется жужжит комар, хотя на дворе ноябрь. '
            'Соседи решили не спать всю ночь и их стоны лишь злят тебя. '
            'Просыпаешься разбитым, будто тебя ночью заставляли разгружать '
            'вагоны. Что будешь делать?'
            '\n1. Где там мой кофе?'
            '\n2. Взять Sick Day, как раз пара таких дней осталась до конца года.'
            '\n3. Выпить ноотропы и сесть работать.'
        )
        options = {
            1: ('\nНе помогло, страдаешь от недосыпа.', -5),
            2: ('\nСтало полегче. Но голова всё ещё ватная.', 5),
            3: ('\nНикакого эффекта. Страдаем дальше.', -1)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.SLEEP_PROBLEMS
            return self.hotfix()
        except (KeyError, ValueError):
            self.retry('sleep_problems')

    @transition(
        source=States.SLEEP_PROBLEMS,
        target=States.HOTFIX,
        conditions=[is_healthy, check_location]
    )
    def hotfix(self):
        animated_print(
            '\nСегодня тестировщики обнаружили очень критичный блокирующий '
            'баг на проде, который ранее не возникал. Написали об этом '
            'конечно же к концу рабочего дня. Ты почти всё время потратил на '
            'его устранение. Всё равно у тебя снова бессоница. В час ночи ты '
            'выкатываешь хотфикс на прод и ложишься спать.\n'
            'У вас прилег прод. Тем временем из-за недостатка сна ты ужасно '
            'тормозишь. Программисты на бэке разводят руками. Логов нет '
            'т.к. место на диске кончилось ещё неделю назад и логи не писались. '
            'Устранить проблему кажется будет сложно. '
            'Менеджер долбит тебя вопросами когда почините всё. Что будешь '
            'делать?'
            '\n1. Бубнишь на экстренном созвоне "Ну, надо поднять наверно"'
            '\n2. Проверить ошибки в Sentry'
            '\n3. Хм? Пойду напишу инструкцию "Как поднять прод"'
        )
        options = {
            1: ('\nКоманда начинает думать, что кажется ты не в адеквате.', -5),
            2: ('\nРуководство не выделило вам бюджет на платную версию '
                'Sentry, а лимит в 10 000 ошибок в этом месяце уже '
                'закончился.', -1),
            3: ('\nМенеджер начинает сомневаться в твоей компетентности. К '
                'счастью один из бекендеров случайно натыкается на место '
                'ошибки и быстро всё исправляет', -10)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.HOTFIX
            return self.covid_vaccine()
        except (KeyError, ValueError):
            self.retry('hotfix')

    @transition(
        source=States.HOTFIX,
        target=States.WITHOUT_VACCINE,
        on_error=States.PANDEMIC_ENDING
    )
    def covid_vaccine(self):
        animated_print('\n Наконец-то поступила в продажу вакцина от COVID-19')
        animated_print('\n Поставить прививку? (да или нет)')
        try:
            answer = input('\n>').lower()
            if answer == 'да':
                self.state = States.PANDEMIC_ENDING
                animated_print(GAME_ENDINGS['pandemic_ending'])
            elif answer == 'нет':
                self.state = States.WITHOUT_VACCINE
                return self.self_digging()
            else:
                self.retry('covid_vaccine')
        except (KeyError, ValueError):
            self.retry('covid_vaccine')

    @transition(
        source=States.WITHOUT_VACCINE,
        target=States.SELF_DIGGING,
        conditions=[is_healthy, check_location]
    )
    def self_digging(self):
        animated_print(
            '\nВ голову опять закралась мысль, что кажется со мной что-то не '
            'так. Что я буду делать?'
            '\n1. Почитаю книги по эффективности «Как лучше делать работу»'
            '\n2. Пойду подышу воздухом'
            '\n3. Буду загоняться'
        )
        options = {
            1: ('\nПоздравляю! После книг по эффективности начинаешь делать '
                'ещё больше херни чем ранее. И ты не осознаешь что кажется '
                'что-то идет не так. Если раньше в твоем листе на день было '
                '5 пунктов херни, то теперь стало 10 пунктов херни.', -10),
            2: ('\nХорошая идея, стало чуть-чуть полгче', 5),
            3: ('\nНу, ты хотя бы честен с собой', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.SELF_DIGGING
            return self.enthusiasm()
        except (KeyError, ValueError):
            self.retry('self_digging')

    @transition(
        source=States.SELF_DIGGING,
        target=States.ENTHUSIASM,
        conditions=[is_healthy, check_location]
    )
    def enthusiasm(self):
        animated_print(
            '\nПоследние дни начинаешь чувствовать всё больше энтузиазм. '
            'Начинаешь подозревать, что в твой кофе из местной кухни на районе '
            'начали подмешивать амфетамин. Иначе как объяснить, что ты '
            'херачишь как проклятый, закрыл 4 огромных таски и ещё и в беклог '
            'залез. При этом менеджер тобой очень доволен. Что будешь делать?'
            '\n1. Куплю себе подарок за хорошую работу. В Стиме как раз '
            'распродажа.'
            '\n2. Возьму ещё задач! Я же так хорошо справляюсь.'
            '\n3. Да я гуру организации рабочего времени! А может мне в '
            'проджекты пойти?'
        )
        options = {
            1: ('\nТы впустую потратил деньги т.к. у тебя нет времени играть', -5),
            2: ('\nЖизнь тебя ничему не учит.', -10),
            3: ('\nТы уверен в этой идее?', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.ENTHUSIASM
            return self.first_meeting()
        except (KeyError, ValueError):
            self.retry('enthusiasm')

    @transition(
        source=States.ENTHUSIASM,
        target=States.EMPTINESS,
        on_error=States.FRIENDSHIP,
        conditions=[is_healthy, check_location]
    )
    def first_meeting(self):
        animated_print(
            '\nКажется у вас по соседству завелся сосед-айтишник. Вы '
            'познакомились в подъезде, когда ты выкидывал мусор. '
            'Он узнал тебя по твоей засаленной призовой футболке, '
            'которую ты выиграл на одной из конференций за вопрос. '
            'Сказал, что вы ранее пересекались конференций по хайлоаду, '
            'но лица ты не узнаешь. Говорит, что зовут Валера. '
            'Он тоже тимлид.\nБудешь ли с ним дальше общаться? (да или нет)'
        )
        try:
            answer = input('\n>').lower()
            if answer == 'да':
                animated_print(
                    '\nВы подружились. В связи с твоим одиночеством и пандемией '
                    'вы видитесь всё чаще. Валера заходит к тебе '
                    'периодически выпить пива и обсудить работу. Тебе '
                    'становиться немного легче. Но где-то на дальнем фоне '
                    'постепенно начинает нарастать некоторое беспокойство.'
                    ' Очень сложно понять что не так. Но вечера так и проходят.\n'
                )
                self.state = States.FRIENDSHIP
                return self.friendship()
            elif answer == 'нет':
                animated_print(
                    '\n Валера показался тебе позорительным. После того '
                    'случая ты его больше не видел.\n'
                )
                self.state = States.EMPTINESS
                return self.emptiness()
        except ValueError:
            self.retry('first_meeting')

    @transition(
        source=States.FRIENDSHIP,
        target=States.HALLUCINATIONS,
        conditions=[check_location]
    )
    def friendship(self):
        animated_print(
            '\nОднажды к тебе в гости приезжает мама. Заглядывает Валера. '
            'Вы разговариваете. Мама заглядывает в комнату и спрашивает с '
            'кем ты говоришь.  Что ответишь?'
            '\n1. Мама, познакомься, это Валера. Мой коллега.'
            '\n2. Да ни с кем'
        )
        try:
            answer = int(input('\n>'))
            if answer == 1:
                animated_print('\nМама говорит что здесь никого нет')
            elif answer == 2:
                animated_print('\nТы оглядываешься. А Валера куда-то исчез.')
            self.state = States.HALLUCINATIONS
            return self.hallucinations()
        except (KeyError, ValueError):
            self.retry('friendship')

    @transition(
        source=States.HALLUCINATIONS,
        target=States.EMPTINESS,
        on_error=States.FRIEND_ENDING,
        conditions=[is_healthy, check_location]
    )
    def hallucinations(self):
        animated_print(
            '\nДо тебя начинает доходить, что кажется Валера всего лишь плод '
            'твоего воображения.  Кажется у тебя начались зрительные '
            'галлюцинации.Что будешь делать?'
            '\n1. Обращусь к врачу'
            '\n2. Проигнорирую. Возможно я заработался. Вот всякая чушь в '
            'голову лезет.'
        )
        try:
            answer = int(input('\n>'))
            if answer == 1:
                animated_print(
                    '\nТебе удалось попасть к хорошему специалисту, '
                    'тебе прописали таблетки, но нужно пропить целый курс. '
                    'Рецепт выписали без вопросов. Только не бросай. А то '
                    'будет хуже.'
                )
                self.check_health(-5)
                self.have_pills = True
                self.state = States.EMPTINESS
                return self.emptiness()
            elif answer == 2:
                animated_print(
                    '\n Твоё состояние становится сильно хуже. На работе люди '
                    'начали замечать, что что-то совсем уже не так. Ты всё '
                    'хуже осознаешь, что реально, а что нет.\n Спустя '
                    'несколько дней... \n'
                )
                self.state = States.FRIEND_ENDING
                animated_print(GAME_ENDINGS['friend_ending'])
        except (KeyError, ValueError):
            self.retry('friendship')

    @transition(
        source=States.EMPTINESS,
        target=States.BACK_TO_OFFICE,
        conditions=[is_healthy, check_location]
    )
    def emptiness(self):
        self.drink_pills()
        animated_print(
            '\nПросыпаешься утром. Как странно. Ты ничего не чувствуешь. '
            'Ни радости, не горя. Ничего. Просто пустота. Ты не понимаешь '
            'зачем ты проснулся. Какой в этом смысл?\nНа автомате открываешь '
            'ноутбук и сразу зарываешься в очередную проблему на проекте. '
            'День проходит незаметно. Уже пора и спать.\nНовый день. '
            'Тебе всё ещё похер. Живешь на автопилоте. Чайка-менеджер '
            'опять поднял шуму на митинге, а тебе уже настолько всё равно, '
            'что пусть этот менеджер сам разбирается с этими проблемами.\n'
            'Рабочий день подходит к концу. Задач всё меньше не становится. '
            'Ты уже настолько устал, что отрываешь взгляд от ноутбука, '
            'смотришь на окно и думаешь «Хм, убить себя что ли? Жизнь '
            'точно стала бы легче». Подойти к окну? (да или нет)'
        )
        try:
            answer = input('\n>').lower()
            if answer == 'да':
                animated_print(
                    '\nТы подходишь к окну и вспоминаешь, что живешь лишь на '
                    'третьем этаже, убить себя не выйдет.'
                )
                self.check_health(-10)
            elif answer == 'нет':
                animated_print(
                    '\nА да, точно. Я же на третьем этаже живу. Убиться будет '
                    'сложно, пойду ещё поработаю'
                )
                self.check_health(1)
            self.state = States.BACK_TO_OFFICE
            return self.back_to_office()
        except ValueError:
            self.retry('emptiness')

    @transition(
        source=States.BACK_TO_OFFICE,
        target=States.PULL_REQUEST,
        conditions=[is_healthy, check_location]
    )
    def back_to_office(self):
        self.drink_pills()
        animated_print(
            '\n Вам объявили, что все снова возвращаются в офис до самых '
            'новогодних праздников. Статистика по заражению похоже не особо '
            'волнует руководство компании. Придется теперь страдать вне '
            'уютных стен дома.\nТы начинаешь напрягаться при попытках выражать '
            'эмоции на разного рода события. У фронтендера бабушка умерла '
            'из-за ковида, а ты даже забыл ему посочувствовать. Внутри '
            'начинает шевелиться страх того, что тебя раскроют. Твои действия?'
            '\n1. Поиграю в доту'
            '\n2. Ничего не буду делать'
        )
        options = {
            1: ('\nУдовольствия от игры ты не получил.', -3),
            2: ('\nНу, да. Зачем ещё напрягаться. Лучше уже не будет.', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.PULL_REQUEST
            return self.pull_request()
        except (KeyError, ValueError):
            self.retry('back_to_office')

    @transition(
        source=States.PULL_REQUEST,
        target=States.MIMICRY,
        conditions=[is_healthy, check_location]
    )
    def pull_request(self):
        self.drink_pills()
        animated_print(
            '\nСегодня знаменательный день. Твой интерн случайно дропнул '
            'базу, благо на тестовом стенде и всё удалось восстановить. '
            'Но на этом ещё не конец. Ты не стал его ругать т.к. очень устал. '
            'Вместо этого ты дал ему задачу с одной мелкой новой фичей. '
            'Пусть развлекается. Спустя несколько часов он прислал пулл '
            'реквест. Надо бы проверить его. Ты открываешь код и видишь '
            'полнейший ад с нарушениями всех правил, дублированием кода и '
            'игнорированием тестов. Уникум ещё и отключил запуск тестов в '
            'TeamCity. На вопрос "Зачем?" он отвечает, что тесты были '
            'красными и это мешало ему. Что будешь делать?'
            '\n1. Коленька, ты по моему ебанулся?'
            '\n2. Коленька, ты что тут мне залил? Ты в своём уме отключать тесты?'
            '\n3. Выдохнуть и полностью прокомментировать весь пулл реквест '
            'на предмет всех ошибок. Тебе уже нечего терять.'
        )
        options = {
            1: ('\nТвою реплику услышал кто-то из руководства и тебе сделали '
                'выговор. Ещё и Коленька обиделся.', -10),
            2: ('\nКоленька обиделся.', -5),
            3: ('\nКоленька очень сильно обиделся.', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.MIMICRY
            return self.mimicry()
        except (KeyError, ValueError):
            self.retry('pull_request')

    @transition(
        source=States.MIMICRY,
        target=States.DEMO,
        conditions=[is_healthy, check_location]
    )
    def mimicry(self):
        self.drink_pills()
        animated_print(
            '\nКажется ты перешел на стадию мимикрии. Ты делаешь всё лишь бы '
            'менеджер отъебался от тебя. Так тебя ещё почему-то за это хвалят. '
            'Ты всё ещё боишься быть раскрытым. Что сделаешь?'
            '\n1. Попробую заглушить это алкоголем.'
            '\n2. Возьму ещё задач себе. Менеджер будет пищать от счастья.'
            '\n3. Делигирую часть задач на подчиненных и постараюсь выдохнуть '
            'и замедлиться.'
        )
        options = {
            1: ('\nТебе кто-нибудь говорил, что это депрессант?', -10),
            2: ('\nМенеджер пищит, а вот ты стонешь от нагрузки.', -5),
            3: ('\nТебе действительно стало чуть легче.', 5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.DEMO
            return self.demo()
        except (KeyError, ValueError):
            self.retry('mimicry')

    @transition(
        source=States.DEMO,
        target=States.ACTION,
        conditions=[is_healthy, check_location]
    )
    def demo(self):
        self.drink_pills()
        animated_print(
            '\nС каждым днем ответственность нарастает. Напряжение растет. Ты '
            'уже задолбался делать таски и спать по 4-5 часов в сутках, но '
            'берешь всё больше и больше на себя. Релиз уже близко, а тестеры '
            'так и не получили версию на тестовом стенде. Фронтендер уехал '
            'на похроны, бэекендеры что-то капаются и очень мало результата '
            'выдают. Интерн уехал на сессию (И слава богу! Им займусь уже в '
            'следующем году). Кажется опять придется делать всё самому.'
            '\nЧас ночи. Ты сидишь в панике перед ноутбуком. Не успеваешь '
            'доделать демо к утренней презентации. Тебя долбят без устали '
            'заказчики. Твои действия?'
            '\n1. Обкидаться энергетиками и доделать.'
            '\n2. Лечь спать на несколько часов и постараться доделать с утра.'
        )
        options = {
            1: ('\nы доделал, тебе очень плохо, на нервной почве у тебя '
                'началась жуткая экзема и исчез голос. В итоге тебя вырвало '
                'в офисе и тебе вызвали скорую. Отдувался за тебя один из '
                'бекендеров', -10),
            2: ('\nС утра ты смог исправить ошибки и подключить других '
                'разработчиков, фронтендер замокал фронт на демостенде и всё '
                'прошло довольно хорошо.', 1),
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.ACTION
            return self.action()
        except (KeyError, ValueError):
            self.retry('demo')

    @transition(
        source=States.ACTION,
        target=States.WALKING,
        conditions=[is_healthy, check_location]
    )
    def action(self):
        self.drink_pills()
        animated_print(
            '\n Ты совсем устал. Остался финальный рывок до конца последнего '
            'спринта. Впереди ещё нужно залить последний релиз. Ты решаешь '
            'хоть что-то предпринять в нынешних условиях т.к. тебе кажется '
            'совсем не хорошо. Что делаем?'
            '\n1. Пойти к врачу'
            '\n2. Погуглить своё состояние'
            '\n3. Остановиться и ничего не делать.'
        )
        options = {
            1: ('\nСпециалист оказался так себе, посоветовал просто пить '
                'побольше водички и не перегружаться. Просто говорит, что с '
                'жиру бесишься. Работа есть, деньги есть, ну что тебе '
                'ещё надо?', -10),
            2: ('\nКажется у меня депрессия? Да не, я же не ебанутый.'
                'Позвоню друзьям и с ними вместе в зуме выпьем', -5),
            3: ('\nНичего не изменилось, но время ушло впустую.', -5)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.state = States.WALKING
            return self.walking()
        except (KeyError, ValueError):
            self.retry('action')

    @transition(
        source=States.WALKING,
        target=States.HAPPY_ENDING,
        on_error=States.BAD_ENDING,
        conditions=[is_healthy, check_location]
    )
    def walking(self) -> None:
        self.drink_pills()
        animated_print(
            '\nТы давно не видел солнца. Как и любой петербуржец. Но тебе '
            'повезло. Выгляднуло солнце. На улице уже предновогодняя '
            'атмосфера. Последние выходные перед новым годом и вроде конец '
            'работе уже виден. Ты задумался о количестве витамина D в твоей '
            'жизни. Как будешь исправлять ситуацию?'
            '\n1. Пойду погуляю и зайду в солярий.'
            '\n2. Погуляю и куплю витамин D'
            '\n3. Останусь сидеть дома'
        )
        options = {
            1: ('\nХорошо конечно было, но ты обгорел. Можно шутить теперь '
                'про выгорание.', -5),
            2: ('\nИз-за пандемии витамин D закончился на прилавках т.к. '
                'кто-то сказал, что он помогает при лечении COVID-19', -5),
            3: ('\nНу, солнце всё равно светило всего 10 минут. Не велика '
                'потеря.', -3)
        }
        try:
            answer = int(input('\n>'))
            animated_print(options[answer][0])
            self.check_health(options[answer][1])
            self.is_healthy()
            self.state = States.HAPPY_ENDING
            animated_print(GAME_ENDINGS['happy_ending'])
        except (KeyError, ValueError):
            self.retry('walking')