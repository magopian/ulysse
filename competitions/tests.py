#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.admin.sites import LOGIN_FORM_KEY
from django.contrib.auth import REDIRECT_FIELD_NAME

class LoginTest(TestCase):
    fixtures = ['login_fixture']

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
            REDIRECT_FIELD_NAME: '/admin/infos/',
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
        self.assertRedirects(login, '/admin/infos/')
        self.client.get('/admin/logout/')

        login = self.client.post('/admin/', self.staff_login) # staff: NOK
        self.assertContains(login, u"Seuls les administrateurs de concours, les membres du jury et les super-utilisateurs peuvent se connecter au site d&#39;administration des concours")

        login = self.client.post('/admin/', self.unauthorized_login) # not staff: NOK
        self.assertContains(login, "Please enter a correct username and password.")

        login = self.client.post('/admin/', self.wrong_login) # wrong login: NOK
        self.assertContains(login, "Please enter a correct username and password.")

        login = self.client.post('/admin/', self.bad_login) # bad login: NOK
        self.assertContains(login, "This field is required")

    def test_session_jury_member(self):
        """
        Test that "jury_member" is correctly set in the session
        """

        resp = self.client.post('/admin/', self.jury_login, follow=True)
        self.assertTrue(resp.context['jury_member'])
        self.assertTrue(self.client.session['jury_member'])
        resp = self.client.get('/admin/logout/')
        self.assertFalse(resp.context['jury_member'])
        self.assertFalse('jury_member' in self.client.session)

        resp = self.client.post('/admin/', self.compadmin_login, follow=True)
        resp = self.client.get('/admin/infos')
        self.assertFalse(resp.context['jury_member'])
        self.assertFalse('jury_member' in self.client.session)
        resp = self.client.get('/admin/logout/')
        self.assertFalse(resp.context['jury_member'])
        self.assertFalse('jury_member' in self.client.session)

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
