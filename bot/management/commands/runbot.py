from unittest import case

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0

        self.stdout.write(self.style.SUCCESS('Bot start handling...'))
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message) -> None:
        tg_user, _ = TgUser.objects.get_or_create(chat_id=msg.msg_from.id, defaults={'username': msg.msg_from.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(
                msg.msg_from.id,
                text=f"Здравствуйте!\n"
                     f"Подтвердите свой аккаунт.\n"
                     f"Для подтверждения необходимо ввести код:{tg_user.verification_code} на сайте.")
        else:
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message) -> None:
        if msg.text and msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    goals = Goal.objects.filter(
                        user=tg_user.user,
                        category__is_deleted=False
                    ).exclude(status=Goal.Status.archived)

                    goals_str = [
                        f'{goal.id}{goal.title}'
                        for goal in goals
                    ]
                    if goals_str:
                        self.tg_client.send_message(msg.msg_from.id, '\n'.join(goals_str))
                    else:
                        self.tg_client.send_message(msg.msg_from.id, "У вас пока нет добавленных целей")
                case '/create':
                    category = GoalCategory.objects.filter(user=tg_user.user)
                case _:
                    self.tg_client.send_message(msg.msg_from.id, "Неизвестная команда..(")
        else:
            self.tg_client.send_message(
                msg.msg_from.id,
                "Давайте приступим к работе.\n"
                "Введите команду начинающуюся со /:")
