from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'basicincome'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 実験参加の意思を確認するパラメータ
    read_all = models.BooleanField(initial=False,
                                  verbose_name='',
                                  label='read_all'
                                  )
    # 実験中止フラグ
    consent = models.BooleanField(initial=False,
                                  choices=[
                                      [True, '同意する'],
                                      [False, '同意しない（実験を終了します）'],
                                  ],
                                  verbose_name = '',
                                  label = 'consent'
    )

    # 属性調査で用いる設問
    q_gender = models.CharField(initial=None,
                                choices=['男性', '女性', '回答しない'],
                                verbose_name='質問１：あなたの性別を選んでください',
                                label='sex',
                                widget=widgets.RadioSelect
                                )

    q_age = models.IntegerField(initial=None,
                                choices=range(0, 120),
                                verbose_name='質問２：あなたの年齢を入力してください',
                                label='age'
                                )

    q_tanmatsu = models.CharField(initial = None,
                                  choices = ['パソコン', 'タブレット', 'スマートフォン',
                                             'それ以外'],
                                  verbose_name='質問３：この画面を見ている端末を選んでください',
                                  label='environment',
                                  widget = widgets.RadioSelect
                                  )

    q_income = models.CharField(initial=None,
                                choices=['〜200万円', '201〜400万円',
                                        '401〜600万円', '601〜800万円',
                                        '801〜1000万円', '1001〜1200万円',
                                        '1201万円～'],
                                verbose_name='質問４：あなたの現在の年収で近いものを選んでください',
                                label='income',
                                widget=widgets.RadioSelect
                                )

    q_occupation = models.CharField(initial=None,
                                    choices=[
                                        '正社員', '契約社員', '派遣社員', '専業主婦・専業主夫',
                                        'パート・アルバイト', '自営業・フリーランス',
                                        '学生', '無職', 'その他'
                                    ],
                                    verbose_name='質問５：あなたの現在の職業を選んでください',
                                    label='occupation'
                                    )

# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['read_all', 'consent']

class Question(Page):
    form_model = 'player'
    form_fields = [
        'q_gender', 'q_age', 'q_tanmatsu', 'q_income', 'q_occupation'
    ]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Introduction, Question]
