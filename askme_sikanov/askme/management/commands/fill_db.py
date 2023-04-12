from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import timedelta
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.utils import IntegrityError

from askme.models import Profile, Tag, Question, Answer, Like


class Command(BaseCommand):
    help = 'Fills the database with test data.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient of filling entities.')

    def handle(self, *args, **options):
        ratio = options['ratio']
        users = []
        profiles = []
        tags = []
        questions = []
        answers = []
        likes = []

        # Создаем пользователей
        for i in range(ratio):
            username = f'user{i}'
            email = f'{username}@example.com'
            password = 'password'
            user = User(username=username, email=email)
            user.set_password(password)
            users.append(user)

        User.objects.bulk_create(users)

        # Создаем профили пользователей
        for usr in users:
            profile = Profile(user=usr)
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)

        # Создаем теги
        for i in range(ratio):
            tag_name = f'tag{i}'
            tag = Tag(name=tag_name)
            tags.append(tag)

        Tag.objects.bulk_create(tags)

        # Создаем вопросы
        now = timezone.datetime.now(timezone.utc)
        for i in range(ratio * 10):
            title = f'Title {i}'
            text = f'Text {i}'
            create_date = now - timedelta(days=i)
            profile = profiles[i % ratio]
            question = Question(title=title, text=text, create_date=create_date, profile=profile)
            questions.append(question)

        Question.objects.bulk_create(questions)
        for i, question in enumerate(questions):
            question.tag.set(tags[i % ratio:ratio+i % ratio:1])

        # Создаем ответы
        for i in range(ratio * 100):
            text = f'Text {i}'
            create_date = now - timedelta(days=i)
            profile = profiles[i % ratio]
            question = questions[i % len(questions)]
            answer = Answer(text=text, correct=False, create_date=create_date, profile=profile, question=question)
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        # Создаем оценки пользователей
        for answer in answers[:ratio * 200]:
            content_type = ContentType.objects.get_for_model(answer)
            like = Like(content_type=content_type, object_id=answer.id, profile=profiles[0])
            likes.append(like)

        Like.objects.bulk_create(likes)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database.'))
