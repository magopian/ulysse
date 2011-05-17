# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Competition'
        db.create_table('competitions_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('presentation', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('managing_partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partners.Partner'])),
            ('information_date', self.gf('django.db.models.fields.DateField')()),
            ('opening_date', self.gf('django.db.models.fields.DateField')()),
            ('closing_date', self.gf('django.db.models.fields.DateField')()),
            ('result_date', self.gf('django.db.models.fields.DateField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('competitions', ['Competition'])

        # Adding M2M table for field additional_partners on 'Competition'
        db.create_table('competitions_competition_additional_partners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm['competitions.competition'], null=False)),
            ('partner', models.ForeignKey(orm['partners.partner'], null=False))
        ))
        db.create_unique('competitions_competition_additional_partners', ['competition_id', 'partner_id'])

        # Adding model 'CompetitionManager'
        db.create_table('competitions_competitionmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
        ))
        db.send_create_signal('competitions', ['CompetitionManager'])

        # Adding unique constraint on 'CompetitionManager', fields ['user', 'competition']
        db.create_unique('competitions_competitionmanager', ['user_id', 'competition_id'])

        # Adding model 'CompetitionStep'
        db.create_table('competitions_competitionstep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('order_index', self.gf('django.db.models.fields.IntegerField')()),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closing_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('competitions', ['CompetitionStep'])

        # Adding model 'CompetitionNews'
        db.create_table('competitions_competitionnews', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal('competitions', ['CompetitionNews'])

        # Adding model 'JuryMemberGroup'
        db.create_table('competitions_jurymembergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('competitions', ['JuryMemberGroup'])

        # Adding model 'JuryMember'
        db.create_table('competitions_jurymember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('competitions', ['JuryMember'])

        # Adding M2M table for field competitions on 'JuryMember'
        db.create_table('competitions_jurymember_competitions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jurymember', models.ForeignKey(orm['competitions.jurymember'], null=False)),
            ('competition', models.ForeignKey(orm['competitions.competition'], null=False))
        ))
        db.create_unique('competitions_jurymember_competitions', ['jurymember_id', 'competition_id'])

        # Adding M2M table for field groups on 'JuryMember'
        db.create_table('competitions_jurymember_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jurymember', models.ForeignKey(orm['competitions.jurymember'], null=False)),
            ('jurymembergroup', models.ForeignKey(orm['competitions.jurymembergroup'], null=False))
        ))
        db.create_unique('competitions_jurymember_groups', ['jurymember_id', 'jurymembergroup_id'])

        # Adding model 'CandidateGroup'
        db.create_table('competitions_candidategroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('competitions', ['CandidateGroup'])

        # Adding model 'Candidate'
        db.create_table('competitions_candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['composers.Composer'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('competitions', ['Candidate'])

        # Adding unique constraint on 'Candidate', fields ['composer', 'competition']
        db.create_unique('competitions_candidate', ['composer_id', 'competition_id'])

        # Adding M2M table for field groups on 'Candidate'
        db.create_table('competitions_candidate_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('candidate', models.ForeignKey(orm['competitions.candidate'], null=False)),
            ('candidategroup', models.ForeignKey(orm['competitions.candidategroup'], null=False))
        ))
        db.create_unique('competitions_candidate_groups', ['candidate_id', 'candidategroup_id'])

        # Adding model 'CandidateWork'
        db.create_table('competitions_candidatework', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('score', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('audio', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('score_url', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('audio_url', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=4000, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order_index', self.gf('django.db.models.fields.IntegerField')()),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Candidate'])),
        ))
        db.send_create_signal('competitions', ['CandidateWork'])

        # Adding model 'CandidateDocument'
        db.create_table('competitions_candidatedocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reference.DocumentType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=200)),
            ('order_index', self.gf('django.db.models.fields.IntegerField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Candidate'])),
        ))
        db.send_create_signal('competitions', ['CandidateDocument'])

        # Adding model 'CandidateTextElement'
        db.create_table('competitions_candidatetextelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reference.TextElementType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('order_index', self.gf('django.db.models.fields.IntegerField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Candidate'])),
        ))
        db.send_create_signal('competitions', ['CandidateTextElement'])

        # Adding model 'CandidateJuryAllocation'
        db.create_table('competitions_candidatejuryallocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Candidate'])),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.CompetitionStep'])),
        ))
        db.send_create_signal('competitions', ['CandidateJuryAllocation'])

        # Adding M2M table for field jury_members on 'CandidateJuryAllocation'
        db.create_table('competitions_candidatejuryallocation_jury_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('candidatejuryallocation', models.ForeignKey(orm['competitions.candidatejuryallocation'], null=False)),
            ('jurymember', models.ForeignKey(orm['competitions.jurymember'], null=False))
        ))
        db.create_unique('competitions_candidatejuryallocation_jury_members', ['candidatejuryallocation_id', 'jurymember_id'])

        # Adding model 'EvaluationNoteType'
        db.create_table('competitions_evaluationnotetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('competitions', ['EvaluationNoteType'])

        # Adding model 'EvaluationNote'
        db.create_table('competitions_evaluationnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.EvaluationNoteType'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('competitions', ['EvaluationNote'])

        # Adding model 'Evaluation'
        db.create_table('competitions_evaluation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition_step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.CompetitionStep'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Candidate'])),
            ('jury_member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.JuryMember'])),
        ))
        db.send_create_signal('competitions', ['Evaluation'])

        # Adding M2M table for field notes on 'Evaluation'
        db.create_table('competitions_evaluation_notes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('evaluation', models.ForeignKey(orm['competitions.evaluation'], null=False)),
            ('evaluationnote', models.ForeignKey(orm['competitions.evaluationnote'], null=False))
        ))
        db.create_unique('competitions_evaluation_notes', ['evaluation_id', 'evaluationnote_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Candidate', fields ['composer', 'competition']
        db.delete_unique('competitions_candidate', ['composer_id', 'competition_id'])

        # Removing unique constraint on 'CompetitionManager', fields ['user', 'competition']
        db.delete_unique('competitions_competitionmanager', ['user_id', 'competition_id'])

        # Deleting model 'Competition'
        db.delete_table('competitions_competition')

        # Removing M2M table for field additional_partners on 'Competition'
        db.delete_table('competitions_competition_additional_partners')

        # Deleting model 'CompetitionManager'
        db.delete_table('competitions_competitionmanager')

        # Deleting model 'CompetitionStep'
        db.delete_table('competitions_competitionstep')

        # Deleting model 'CompetitionNews'
        db.delete_table('competitions_competitionnews')

        # Deleting model 'JuryMemberGroup'
        db.delete_table('competitions_jurymembergroup')

        # Deleting model 'JuryMember'
        db.delete_table('competitions_jurymember')

        # Removing M2M table for field competitions on 'JuryMember'
        db.delete_table('competitions_jurymember_competitions')

        # Removing M2M table for field groups on 'JuryMember'
        db.delete_table('competitions_jurymember_groups')

        # Deleting model 'CandidateGroup'
        db.delete_table('competitions_candidategroup')

        # Deleting model 'Candidate'
        db.delete_table('competitions_candidate')

        # Removing M2M table for field groups on 'Candidate'
        db.delete_table('competitions_candidate_groups')

        # Deleting model 'CandidateWork'
        db.delete_table('competitions_candidatework')

        # Deleting model 'CandidateDocument'
        db.delete_table('competitions_candidatedocument')

        # Deleting model 'CandidateTextElement'
        db.delete_table('competitions_candidatetextelement')

        # Deleting model 'CandidateJuryAllocation'
        db.delete_table('competitions_candidatejuryallocation')

        # Removing M2M table for field jury_members on 'CandidateJuryAllocation'
        db.delete_table('competitions_candidatejuryallocation_jury_members')

        # Deleting model 'EvaluationNoteType'
        db.delete_table('competitions_evaluationnotetype')

        # Deleting model 'EvaluationNote'
        db.delete_table('competitions_evaluationnote')

        # Deleting model 'Evaluation'
        db.delete_table('competitions_evaluation')

        # Removing M2M table for field notes on 'Evaluation'
        db.delete_table('competitions_evaluation_notes')


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
            'Meta': {'object_name': 'Evaluation'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Candidate']"}),
            'competition_step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.CompetitionStep']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jury_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.JuryMember']"}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competitions.EvaluationNote']", 'symmetrical': 'False'})
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
