from os import environ

SESSION_CONFIGS = [
    dict(
        name = 'questionnaire',
        # この構成の名前の設定
        display_name = 'はじめてのアンケート',
        # oTreeの出も画面で表示される名前の設定
        num_demo_participants = 1,
        # demo画面に参加する人数を設定しておく必要がある
        app_sequence = ['questionnaire']
        # この構成で使用するアプリケーションの選択

    ),
    dict(
        name = 'PG3',
        display_name = "はじめての公共財ゲーム",
        num_demo_participants = 2,
        app_sequence = ['publicgoods_trial']
    ),
    dict(
        name = 'counting',
        display_name = "01カウントゲーム",
        num_demo_participants = 2,
        app_sequence = ['counting_task']
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

ROOMS = [
    dict(
        name = 'label',
        display_name = '実験参加者label',
        participant_label_file = '_rooms/label.txt'
    )
]

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4009486563986'
