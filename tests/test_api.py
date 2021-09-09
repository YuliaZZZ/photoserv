from idlelib.iomenu import encoding

from django.test import TestCase

from tests.fixtures.users_model import NEW_USER, FAILURES_BODY


class UserTests(TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        resp = self.client.post('/api/v1/user/', data=NEW_USER, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_create_wrong_user(self):
        resp = self.client.post('/api/v1/user/', data={}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, FAILURES_BODY)



        # user = User.objects.create_user('Myuser', 'proba@ya.ru',
        #                                 'usertest1234')
        # user1 = User.objects.create_user('newuser1', 'test@mail.ru',
        #                                  'codestyle')
        # valid_date_in_future = datetime.date.today() + datetime.timedelta(
        #     weeks=2)
        # tag = Tag.objects.create(name='happy')
        # task1 = Task.objects.create(author=user, name='Check',
        #                             deadline=valid_date_in_future)
        # task1.executors.add(user1)
        # task1.tags.add(tag)
        # task1.save()
        # PersonalTask.objects.create(task=task1, executor=user1)
        # user2 = User.objects.create_user('newuser2', 'ex@mail.ru',
        #                                  'abbrwalk')
        # task2 = Task.objects.create(author=user1, name='New task',
        #                             deadline=timezone.now())
        # task2.executors.add(user2)
        # task2.save()
        # PersonalTask.objects.create(task=task2, executor=user2,
        #                             status=Task.DONE)