from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q_gender = models.CharField(initial = None,
                                choices = ['男性','女性', '回答しない'],
                                label='性別を選んでください',
                                widget = widgets.RadioSelect)
    # ラジオボタンを使うときは widget = widgets.RadioSelectを記述する
    q_age = models.IntegerField(initial = None,
                                verbose_name = 'あなたの年齢を教えてください',
                                choices = range(0,120)
                                )
    # 数字の場合は"choices"を使うことで範囲を指定できる

    q_area = models.CharField(initial = None,
                              choices = ['北海道', '東北地方', '関東地方',
                                         '中部地方', '近畿地方', '中国地方',
                                         '四国地方', '九州地方'],
                              verbose_name = 'あなたのお住まいの地域を教えてください'
                              )
    q_tanmatsu = models.CharField(initial = None,
                                  choices = ['パソコン', 'タブレット', 'スマートフォン',
                                             'それ以外'],
                                  verbose_name = '解答端末を教えてください',
                                  widget = widgets.RadioSelect
                                  )
    q_hitorigurashi = models.CharField(initial=None,
                                  choices=['はい','いいえ'],
                                  verbose_name='あなたは現在, 一人暮らしですか？',
                                  widget=widgets.RadioSelect
                                  )
    q_gakusei = models.BooleanField(initial = False,
                                    choices = [
                                        [True,"はい"],
                                        [False, "いいえ"],
                                        ]
                                    )


# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = [
        'q_gender', 'q_age', 'q_area', 'q_tanmatsu', 'q_hitorigurashi', 'q_gakusei'
    ]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Page1]
