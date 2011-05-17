# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field notes on 'Evaluation'
        db.delete_table('competitions_evaluation_notes')


    def backwards(self, orm):
        
        # Adding M2M table for field notes on 'Evaluation'
        db.create_table('competitions_evaluation_notes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('evaluation', models.ForeignKey(orm['competitions.evaluation'], null=False)),
            ('evaluationnote', models.ForeignKey(orm['competitions.evaluationnote'], null=False))
        ))
        db.create_unique('competitions_evaluation_notes', ['evaluation_id', 'evaluationnote_id'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'competitions.candidate': {
            'Meta': {'unique_together': "(('composer', 'competition'),)", 'object_name': 'Candidate'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['composers.Composer']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competitions.CandidateGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'competitions.candidatedocument': {
            'Meta': {'object_name': 'CandidateDocument'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reference.DocumentType']"}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'competitions.candidategroup': {
            'Meta': {'object_name': 'CandidateGroup'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'competitions.candidatejuryallocation': {
            'Meta': {'object_name': 'CandidateJuryAllocation'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jury_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competitions.JuryMember']", 'symmetrical': 'False'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.CompetitionStep']"})
        },
        'competitions.candidatetextelement': {
            'Meta': {'object_name': 'CandidateTextElement'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reference.TextElementType']"}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'competitions.candidatework': {
            'Meta': {'object_name': 'CandidateWork'},
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'audio_url': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'score_url': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'competitions.competition': {
            'Meta': {'object_name': 'Competition'},
            'additional_partners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'additional_partners'", 'blank': 'True', 'to': "orm['partners.Partner']"}),
            'closing_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information_date': ('django.db.models.fields.DateField', [], {}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'managing_partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['partners.Partner']"}),
            'opening_date': ('django.db.models.fields.DateField', [], {}),
            'presentation': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'result_date': ('django.db.models.fields.DateField', [], {}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'competitions.competitionmanager': {
            'Meta': {'unique_together': "(('user', 'competition'),)", 'object_name': 'CompetitionManager'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'competitions.competitionnews': {
            'Meta': {'object_name': 'CompetitionNews'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'competitions.competitionstep': {
            'Meta': {'object_name': 'CompetitionStep'},
            'closing_date': ('django.db.models.fields.DateField', [], {}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'competitions.evaluation': {
            'Meta': {'unique_together': "(('competition_step', 'candidate', 'jury_member'),)", 'object_name': 'Evaluation'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'competition_step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.CompetitionStep']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jury_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.JuryMember']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.EvaluationStatus']"})
        },
        'competitions.evaluationnote': {
            'Meta': {'object_name': 'EvaluationNote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.EvaluationNoteType']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'competitions.evaluationnotetype': {
            'Meta': {'object_name': 'EvaluationNoteType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'competitions.evaluationstatus': {
            'Meta': {'object_name': 'EvaluationStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'competitions.jurymember': {
            'Meta': {'object_name': 'JuryMember'},
            'competitions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['competitions.Competition']", 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['competitions.JuryMemberGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'competitions.jurymembergroup': {
            'Meta': {'object_name': 'JuryMemberGroup'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'composers.composer': {
            'Meta': {'object_name': 'Composer'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'citizenship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reference.Citizenship']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'partners.partner': {
            'Meta': {'object_name': 'Partner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'presentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reference.citizenship': {
            'Meta': {'object_name': 'Citizenship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reference.documenttype': {
            'Meta': {'object_name': 'DocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'reference.textelementtype': {
            'Meta': {'object_name': 'TextElementType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['competitions']
