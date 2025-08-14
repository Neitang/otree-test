from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator_trial'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    proposal = models.CurrencyField(
        choices = currency_range(cu(0), C.ENDOWMENT, cu(1)),
        label = 'プレイヤー2にいくら渡しますか？'
    )

class Player(BasePlayer):
    pass

def compute(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.proposal
    p2.payoff = group.proposal
# PAGES
class Page1(Page):
    pass

class Page2(Page):
    form_model = 'group'
    form_fields = ['proposal']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class Page3(WaitPage):
    after_all_players_arrive = compute

class Page4(Page):
    pass

page_sequence = [Page1,Page2,Page3,Page4]
