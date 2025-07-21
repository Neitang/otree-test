from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'binary_count_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    TABLE_ROWS = 10
    TABLE_COLS = 15
    TIME_LIMIT = 60  # seconds per task
    REWARD_THRESHOLDS = [(3, 60), (6, 120), (9, 180), (12, 200)]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    table_data = models.LongStringField()
    target_digit = models.IntegerField()  # 0 or 1
    correct_count = models.IntegerField()
    user_count = models.IntegerField()
    is_correct = models.BooleanField(initial=False)
    total_correct = models.IntegerField(initial=0)
    reward = models.CurrencyField(initial=0)

def creating_session(subsession):
    for p in subsession.get_players():
        generate_table(p)

def generate_table(player):
    table = []
    all_digits = []
    for _ in range(C.TABLE_ROWS):
        row = [random.choice([0, 1]) for _ in range(C.TABLE_COLS)]
        all_digits.extend(row)
        table.append(row)
    flat = ','.join(map(str, all_digits))
    player.table_data = flat
    player.target_digit = random.choice([0, 1])
    player.correct_count = all_digits.count(player.target_digit)


# PAGES
class BinaryCount(Page):
    form_model = 'player'
    form_fields = ['user_count']
    timeout_seconds = C.TIME_LIMIT

    @staticmethod
    def vars_for_template(player):
        table = list(map(int, player.table_data.split(',')))
        rows = [table[i:i + C.TABLE_COLS] for i in range(0, len(table), C.TABLE_COLS)]
        return dict(
            rows=rows,
            target=player.target_digit
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.user_count == player.correct_count:
            player.is_correct = True
            player.total_correct += 1
        if player.round_number == C.NUM_ROUNDS:
            set_reward(player)

    def set_reward(player):
        correct = player.total_correct
        for threshold, reward in reversed(C.REWARD_THRESHOLDS):
            if correct >= threshold:
                player.reward = reward
                break

class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        return dict(
            total_correct=player.total_correct,
            reward=player.reward
        )

page_sequence = [BinaryCount] * C.NUM_ROUNDS + [Results]
