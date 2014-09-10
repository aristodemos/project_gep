# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Aircraft'
        db.create_table(u'loz_lol_aircraft', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ac_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ac_sn', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ac_marks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ac_flight_hours', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('ac_landings', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'loz_lol', ['Aircraft'])

        # Adding model 'Lifetime_Limit'
        db.create_table(u'loz_lol_lifetime_limit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('limit_type', self.gf('django.db.models.fields.CharField')(default='FH', max_length=2)),
            ('limit_calendar_years', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('limit_calendar_months', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('limit_calendar_days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('limit_flight_hours', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('limit_landings', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'loz_lol', ['Lifetime_Limit'])

        # Adding model 'PartList'
        db.create_table(u'loz_lol_partlist', (
            ('part_number', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True)),
            ('part_description', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('part_ata_chapter', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
        ))
        db.send_create_signal(u'loz_lol', ['PartList'])

        # Adding model 'Part_Life'
        db.create_table(u'loz_lol_part_life', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loz_lol.PartList'])),
            ('lifetime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loz_lol.Lifetime_Limit'])),
        ))
        db.send_create_signal(u'loz_lol', ['Part_Life'])

        # Adding model 'Part'
        db.create_table(u'loz_lol_part', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loz_lol.PartList'])),
            ('part_serial', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('part_position', self.gf('django.db.models.fields.CharField')(default='0', max_length=1, null=True, blank=True)),
            ('part_is_installed', self.gf('django.db.models.fields.BooleanField')()),
            ('part_location', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('part_tot_flight_hours', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('part_tot_landings', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('part_tot_life', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('part_last_in_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('part_last_rem_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'loz_lol', ['Part'])


    def backwards(self, orm):
        # Deleting model 'Aircraft'
        db.delete_table(u'loz_lol_aircraft')

        # Deleting model 'Lifetime_Limit'
        db.delete_table(u'loz_lol_lifetime_limit')

        # Deleting model 'PartList'
        db.delete_table(u'loz_lol_partlist')

        # Deleting model 'Part_Life'
        db.delete_table(u'loz_lol_part_life')

        # Deleting model 'Part'
        db.delete_table(u'loz_lol_part')


    models = {
        u'loz_lol.aircraft': {
            'Meta': {'object_name': 'Aircraft'},
            'ac_flight_hours': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'ac_landings': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_marks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_sn': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'loz_lol.lifetime_limit': {
            'Meta': {'object_name': 'Lifetime_Limit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_calendar_days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_calendar_months': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_calendar_years': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_flight_hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_landings': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_type': ('django.db.models.fields.CharField', [], {'default': "'FH'", 'max_length': '2'})
        },
        u'loz_lol.part': {
            'Meta': {'object_name': 'Part'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_is_installed': ('django.db.models.fields.BooleanField', [], {}),
            'part_last_in_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'part_last_rem_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'part_location': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'part_number': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.PartList']"}),
            'part_position': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'part_serial': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'part_tot_flight_hours': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'part_tot_landings': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'part_tot_life': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'loz_lol.part_life': {
            'Meta': {'object_name': 'Part_Life'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifetime': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.Lifetime_Limit']"}),
            'part_number': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.PartList']"})
        },
        u'loz_lol.partlist': {
            'Meta': {'object_name': 'PartList'},
            'lifetime': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['loz_lol.Lifetime_Limit']", 'symmetrical': 'False', 'through': u"orm['loz_lol.Part_Life']", 'blank': 'True'}),
            'part_ata_chapter': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'part_description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'})
        }
    }

    complete_apps = ['loz_lol']