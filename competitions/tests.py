#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.test import TestCase
from django.contrib.admin.sites import LOGIN_FORM_KEY
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group, User, Permission
from competitions.models import JuryMember

class LoginTest(TestCase):
    fixtures = ['full']

    def setUp(self):
        self.super_login = { # superuser
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'admin',
            'password': 'admin',
        }
        self.compadmin_login = { # staff, member of "competition-admins"
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'compadmin',
            'password': 'compadmin',
        }
        self.jury_login = { # staff, member of "jury-members"
            REDIRECT_FIELD_NAME: '/admin/evaluate/',
            LOGIN_FORM_KEY: 1,
            'username': 'jury',
            'password': 'jury',
        }
        self.staff_login = { # staff
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'staff',
            'password': 'staff',
        }
        self.unauthorized_login = { # simple user, not staff
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'web',
            'password': 'web',
        }
        self.wrong_login = { # wrong login
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'foo',
            'password': 'bar',
        }
        self.bad_login = { # bad login
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'foo',
            'password': '',
        }

    
    def test_competition_admin_login(self):
        """
        Test that only allowed members can login to the competition admin
        """

        login = self.client.post('/admin/', self.super_login) # superuser: OK
        self.assertRedirects(login, '/admin/infos/')
        self.client.get('/admin/logout/')

        login = self.client.post('/admin/', self.compadmin_login) # competition admin: OK
        self.assertRedirects(login, '/admin/infos/')
        self.client.get('/admin/logout/')

        login = self.client.post('/admin/', self.jury_login) # jury member: OK
        self.assertRedirects(login, '/admin/evaluate/')
        self.client.get('/admin/logout/')

        login = self.client.post('/admin/', self.staff_login) # staff: NOK
        self.assertContains(login, u"Seuls les administrateurs de concours, les membres du jury et les super-utilisateurs peuvent se connecter au site d&#39;administration des concours")

        login = self.client.post('/admin/', self.unauthorized_login) # not staff: NOK
        self.assertContains(login, "Please enter a correct username and password.")

        login = self.client.post('/admin/', self.wrong_login) # wrong login: NOK
        self.assertContains(login, "Please enter a correct username and password.")

        login = self.client.post('/admin/', self.bad_login) # bad login: NOK
        self.assertContains(login, "This field is required")

    def test_context_jury_member(self):
        """
        Test that "jury_member" is correctly set in the context
        """

        resp = self.client.post('/admin/', self.jury_login, follow=True)
        self.assertTrue(resp.context['jury_member'])
        resp = self.client.get('/admin/logout/')
        self.assertFalse(resp.context['jury_member'])

        resp = self.client.post('/admin/', self.compadmin_login, follow=True)
        self.assertFalse(resp.context['jury_member'])
        resp = self.client.get('/admin/logout/')
        self.assertFalse(resp.context['jury_member'])

    def test_jury_member_group(self):
        """
        Test that the 'jury-member' group is correctly set and assigned
        """

        Group.objects.get(name=settings.JURY_MEMBER_GROUP).delete()
        u = User.objects.get(username='staff')
        jm = JuryMember(user=u)
        jm.save()

        # make sure the group has been correctly created
        jm_group = Group.objects.get(name=settings.JURY_MEMBER_GROUP)
        # and has the correct permissions
        perms = ['competitions.add_evaluation',
                 'competitions.change_evaluation',
                 'competitions.delete_evaluation',
                 'competitions.add_evaluationnote',
                 'competitions.change_evaluationnote',
                 'competitions.delete_evaluationnote',
                 'competitions.change_candidatetoevaluate']
        self.assertTrue(u.has_perms(perms))
        # and had been assigned to the new JuryMember
        self.assertTrue(jm_group in u.groups.all())

        # also test that the group is removed when JuryMember is deleted
        jm.delete()
        self.assertFalse(jm_group in u.groups.all())


class JuryAdminTest(TestCase):
    fixtures = ['full']

    def setUp(self):
        self.jury_login = { # two competitions
            REDIRECT_FIELD_NAME: '/admin/evaluate/',
            LOGIN_FORM_KEY: 1,
            'username': 'jury',
            'password': 'jury',
        }
        self.jury_1_login = { # one competition
            REDIRECT_FIELD_NAME: '/admin/evaluate/',
            LOGIN_FORM_KEY: 1,
            'username': 'jury_1',
            'password': 'jury',
        }
        self.jury_2_login = { # one competition
            REDIRECT_FIELD_NAME: '/admin/evaluate/',
            LOGIN_FORM_KEY: 1,
            'username': 'jury_2',
            'password': 'jury',
        }
        self.jury_3_login = { # no competitions
            REDIRECT_FIELD_NAME: '/admin/evaluate/',
            LOGIN_FORM_KEY: 1,
            'username': 'jury_3',
            'password': 'jury',
        }
        self.compadmin_login = { # staff, member of "competition-admins"
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'compadmin',
            'password': 'compadmin',
        }

        # reset the "jury-members" group permissions (not in fixture)
        jury_member_group = Group.objects.get(name=settings.JURY_MEMBER_GROUP)
        permissions = Permission.objects.filter(
                Q(codename__endswith='evaluation') |
                Q(codename__endswith='evaluationnote') |
                Q(codename__exact='change_candidatetoevaluate'))
        jury_member_group.permissions.add(*permissions)

        # reset the "competitions-admins" group permissions (not in fixture)
        ca_group = Group.objects.get(name=settings.COMPETITION_ADMIN_GROUP)
        permissions = Permission.objects.filter(
                content_type__app_label="competitions")
        ca_group.permissions.add(*permissions)

    def test_jury_competition_selection(self):
        """
        Test the admin competition selection for jury members
        """

        resp = self.client.post('/admin/', self.jury_login, follow=True)
        self.assertContains(resp, "Ircam - Cursus 1")
        self.assertContains(resp, "IRCAM - Résidence Musicale")
        self.client.get('/admin/logout/')

        resp = self.client.post('/admin/', self.jury_1_login, follow=True)
        self.assertContains(resp, "Ircam - Cursus 1")
        self.assertNotContains(resp, "IRCAM - Résidence Musicale")
        self.client.get('/admin/logout/')

        resp = self.client.post('/admin/', self.jury_2_login, follow=True)
        self.assertNotContains(resp, "Ircam - Cursus 1")
        self.assertContains(resp, "IRCAM - Résidence Musicale")
        self.client.get('/admin/logout/')

        resp = self.client.post('/admin/', self.jury_3_login, follow=True)
        self.assertNotContains(resp, "Ircam - Cursus 1")
        self.assertNotContains(resp, "IRCAM - Résidence Musicale")
        self.client.get('/admin/logout/')

    def test_jury_restricted_admin(self):
        """
        Test that a JuryMember has a restricted competition admin
        """

        resp = self.client.post('/admin/', self.jury_login, follow=True)
        resp = self.client.get('/admin/select_competition/1', follow=True)

        # jury member must be redirected straight to the evaluate tab
        self.assertEqual(resp.request["PATH_INFO"], '/admin/evaluate/')
        self.assertEqual(resp.status_code, 200)
        # no tabs other than "evaluate" should be visible
        self.assertNotContains(resp, "Informations")
        self.assertNotContains(resp, "News")
        self.assertNotContains(resp, "Jury member")
        # all other links shouldn't be accessible
        resp = self.client.get('/admin/infos/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get('/admin/news/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get('/admin/candidates/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get('/admin/jury_members/')
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get('/admin/logout/')

        # competition admin doesn't have the "evaluate tab"
        resp = self.client.post('/admin/', self.compadmin_login, follow=True)
        resp = self.client.get('/admin/select_competition/1', follow=True)
        self.assertNotContains(resp, "To evaluate")
        resp = self.client.get('/admin/logout/')

        # unless he is also jury member
        u = User.objects.get(username='compadmin')
        JuryMember(user=u).save()
        resp = self.client.post('/admin/', self.compadmin_login, follow=True)
        resp = self.client.get('/admin/select_competition/1', follow=True)
        resp = self.client.get('/admin/evaluate/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/admin/logout/')


class SuperAdminTest(TestCase):
    fixtures = ['full']

    def setUp(self):
        self.super_login = { # superuser
            REDIRECT_FIELD_NAME: '/admin/infos/',
            LOGIN_FORM_KEY: 1,
            'username': 'admin',
            'password': 'admin',
        }
    
    def test_super_admin_competitions_app(self):
        """
        Test the access to the competitions app through the super-admin
        """

        resp = self.client.post('/super-admin/', self.super_login, follow=True)

        resp = self.client.get('/super-admin/competitions/candidate/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/candidate/add/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/candidate/1/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/super-admin/competitions/competition/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/competition/add/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/competition/1/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/super-admin/competitions/jurymember/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/jurymember/add/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/super-admin/competitions/jurymember/2/')
        self.assertEqual(resp.status_code, 200)
