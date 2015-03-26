# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Part.part_date_of_manuf'
        db.add_column(u'loz_lol_part', 'part_date_of_manuf',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Part.part_last_oh'
        db.add_column(u'loz_lol_part', 'part_last_oh',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lifetime_Limit.limit_starts'
        db.add_column(u'loz_lol_lifetime_limit', 'limit_starts',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Part.part_date_of_manuf'
        db.delete_column(u'loz_lol_part', 'part_date_of_manuf')

        # Deleting field 'Part.part_last_oh'
        db.delete_column(u'loz_lol_part', 'part_last_oh')

        # Deleting field 'Lifetime_Limit.limit_starts'
        db.delete_column(u'loz_lol_lifetime_limit', 'limit_starts')


    models = {
        u'loz_lol.aircraft': {
            'Meta': {'object_name': 'Aircraft'},
            'ac_flight_hours': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_landings': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_marks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_sn': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ac_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'loz_lol.lifetime_limit': {
            'Meta': {'object_name': 'Lifetime_Limit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_calendar_days': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'limit_calendar_months': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'limit_calendar_years': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'limit_flight_hours': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'limit_landings': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'limit_starts': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'limit_type': ('django.db.models.fields.CharField', [], {'default': "'FH'", 'max_length': '2'})
        },
        u'loz_lol.part': {
            'Meta': {'object_name': 'Part'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_date_of_manuf': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'part_is_installed': ('django.db.models.fields.BooleanField', [], {}),
            'part_last_in_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'part_last_oh': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'part_last_rem_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'part_location': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'part_number': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.PartList']"}),
            'part_position': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'part_serial': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'part_tot_flight_hours': ('django.db.models.fields.PositiveIntegerField', [], {}),
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