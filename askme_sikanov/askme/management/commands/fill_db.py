from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint, choice

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
            text = f'Text {i} Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent euismod metus id turpis ultricies dapibus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque id lectus quam. Cras odio odio, accumsan dictum nisl et, fringilla fringilla urna. Nulla facilisi. \nPraesent quis tincidunt nisi, at ultricies nisl. Cras vel justo eget velit cursus pharetra in non nunc. Proin euismod commodo sem nec malesuada.Donec tempor ante lacus, et semper mi blandit ac. Vestibulum hendrerit nunc sit amet faucibus vulputate. \nNulla lectus nibh, congue nec tortor in, lacinia congue metus. Aliquam et ligula accumsan, dignissim ligula sit amet, pulvinar velit. In consequat.'
            create_date = now - timedelta(days=i)
            profile = profiles[i % ratio]
            question = Question(title=title, text=text[:randint(10, len(text))], create_date=create_date, profile=profile, like=randint(1,200))
            questions.append(question)

        Question.objects.bulk_create(questions)
        for i, question in enumerate(questions):
            random_tags = Tag.objects.order_by('?')[:randint(2,10)]
            question.tag.clear()
            question.tag.add(*random_tags)

        # Создаем ответы
        for i in range(ratio * 100):
            text = f'Text {i} Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent euismod metus id turpis ultricies dapibus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque id lectus quam. Cras odio odio, accumsan dictum nisl et, fringilla fringilla urna. Nulla facilisi. Praesent quis tincidunt nisi, at ultricies nisl. Cras vel justo eget velit cursus pharetra in non nunc. Proin euismod commodo sem nec malesuada.'
            create_date = now - timedelta(days=i)
            profile = profiles[i % ratio]
            question = questions[randint(1,10000) % len(questions)]
            answer = Answer(text=text[:randint(10, len(text))], correct=False, create_date=create_date, profile=profile, question=question, like=randint(1,200))
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        # Создаем оценки пользователей
        variants = set()
        for i in range(ratio * 200):
            element = [choice(answers), choice(questions)]
            content_type = [ContentType.objects.get_for_model(element[0]), ContentType.objects.get_for_model(element[1])]
            n = randint(1, 10) % 2
            obj = (content_type[n], element[n].id, choice(profiles))  # Конвертируем список в кортеж
            if obj not in variants:
                like = Like(content_type=obj[0], object_id=obj[1], profile=obj[2])
                likes.append(like)
                variants.add(obj)


        Like.objects.bulk_create(likes)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database.'))
