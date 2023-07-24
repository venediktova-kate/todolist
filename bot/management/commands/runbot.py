from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.offset = 0

    def handle(self, *args, **options):
        offset = 0

        self.stdout.write(self.style.SUCCESS('Bot start handling...'))
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        """
        Функция возвращает ответ на сообщение не авторизированного пользователя.
        """
        tg_user, _ = TgUser.objects.get_or_create(chat_id=msg.msg_from.id, defaults={'username': msg.msg_from.username})
        if not tg_user.is_verified:
            self.tg_client.send_message(msg.msg_from.id, "Здравствуйте!")
            tg_user.update_verification_code()
            self.tg_client.send_message(
                msg.msg_from.id,
                text=f"Подтвердите Ваш аккаунт.\n"
                     f"Для подтверждения введите код:{tg_user.verification_code} на сайте.")
        else:
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message) -> None:
        """
        Функция возвращает ответ на команду пользователя (описаны основные команды представленные ботом).
        """
        if msg.text and msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    goals_str = self.get_goals_list(tg_user=tg_user)
                    self.tg_client.send_message(msg.msg_from.id, goals_str)
                case '/create':
                    pass
                case '/cancel':
                    pass
                case _:
                    self.tg_client.send_message(msg.msg_from.id, "Я не знаю такой команды(")

    def get_goals_list(self, tg_user: TgUser) -> str:
        """
        Функция возвращает строку со всеми целями пользователя
        """
        goals = Goal.objects.filter(user=tg_user.user, category__is_deleted=False).exclude(status=Goal.Status.archived)
        goals_list: list[str] = [f'Цель: {goal.title}' for goal in goals]
        if goals_list:
            goals_str = '\n'.join(goals_list)
        else:
            goals_str = 'У вас пока нет добавленных целей'
        return goals_str

    def get_categories_list(self, tg_user: TgUser):
        pass

    def create_new_goal(self, tg_user: TgUser, category: GoalCategory):
        pass
