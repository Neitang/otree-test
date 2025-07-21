from otree.api import *


doc = """
公共財実験ゲーム
"""


class C(BaseConstants):
    NAME_IN_URL = 'publicgoods_trial'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = cu(20)
    MULTIPLIER = 1.8


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    # 各グループの貢献額の合計を入れるオブジェクト
    individual_share = models.CurrencyField()
    # 各プレイヤーの個別の分配額を入れるオブジェクト

class Player(BasePlayer):
    # 各プレイヤーの資産を入れるオブジェクト
    contribution = models.CurrencyField(
        # プレイヤーの貢献額を入れるオブジェクト
        #choices = currency_range(cu(0), cu(C.ENDOWMENT), cu(5)),
        # 0から保有額までの5ポイント刻みの選択肢を表示する
        label = 'あなたはいくら貢献しますか？'
        # 貢献額の選択肢の前に設問文を表示する
    )
    prev_payoff = models.CurrencyField(
        min = 0,
        initial = 0
    )


def compute(group: Group):
    players = group.get_players()
    # groupクラスに所属するプレイヤーの情報を取得
    contributions = [p.contribution for p in players]
    # プレイヤーの貢献額をリストに格納
    group.total_contribution = sum(contributions)
    # groupの総貢献額を計算
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    # 各プレイヤーの分配額を計算
    for p in players:
        # 各プレイヤーの獲得額を計算
        if group.round_number == 1:
            p.payoff = C.ENDOWMENT - p.contribution + group.individual_share
            # 各プレイヤーのpayoffは初期保有額から貢献額を取り除いて
            # 各プレイヤーへの分配額を加えたものである
        else:
            p.payoff = p.prev_payoff - p.contribution + group.individual_share


def calc_prev_payoff(group: Group):
    for p in group.get_players():
        # 前ラウンドの payoffs を各プレイヤーの prev_payoff に格納
        prev = p.in_round(p.round_number - 1).payoff
        p.prev_payoff = prev


def contribution_max(player):
    if player.round_number == 1:
        return C.ENDOWMENT
    else:
        return player.in_round(player.round_number - 1).payoff

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
        # ランダムにグループに割り当てる
    else:
        subsession.group_like_round(1)
        # 一期目と同じグループに割り当てる
# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = ['contribution']
    # playerが貢献額を入力する
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Page4(Page):
    form_model = 'player'
    form_fields = ['contribution']
    # playerが貢献額を入力する
    after_all_players_arrive = calc_prev_payoff
    # 全プレイヤースタート時に前のラウンドの資産を計算
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != 1


class Page2(WaitPage):
    after_all_players_arrive = compute
    # 全員が2ページ目に来たらcompute関数を実行する


class Page3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Page5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != 1

class Page6(WaitPage):
    if Player.round_number != 1:
        after_all_players_arrive = calc_prev_payoff
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != 1

page_sequence = [Page6, Page1, Page4, Page2, Page3, Page5,]
