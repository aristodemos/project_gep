# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'formaPtisis.cargo_cycles'
        db.alter_column(u'ef421_formaptisis', 'cargo_cycles', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'formaPtisis.above_6400'
        db.alter_column(u'ef421_formaptisis', 'above_6400', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'formaPtisis.cat_a'
        db.alter_column(u'ef421_formaptisis', 'cat_a', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'formaPtisis.start_stop'
        db.alter_column(u'ef421_formaptisis', 'start_stop', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'formaPtisis.hoist_lifts_sec'
        db.alter_column(u'ef421_formaptisis', 'hoist_lifts_sec', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'formaPtisis.hoist_lifts_main'
        db.alter_column(u'ef421_formaptisis', 'hoist_lifts_main', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'item_movement.date'
        db.alter_column(u'ef421_item_movement', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

    def backwards(self, orm):

        # Changing field 'formaPtisis.cargo_cycles'
        db.alter_column(u'ef421_formaptisis', 'cargo_cycles', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'formaPtisis.above_6400'
        db.alter_column(u'ef421_formaptisis', 'above_6400', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'formaPtisis.cat_a'
        db.alter_column(u'ef421_formaptisis', 'cat_a', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'formaPtisis.start_stop'
        db.alter_column(u'ef421_formaptisis', 'start_stop', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'formaPtisis.hoist_lifts_sec'
        db.alter_column(u'ef421_formaptisis', 'hoist_lifts_sec', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'formaPtisis.hoist_lifts_main'
        db.alter_column(u'ef421_formaptisis', 'hoist_lifts_main', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'item_movement.date'
        db.alter_column(u'ef421_item_movement', 'date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

    models = {
        u'ef421.formaptisis': {
            'Meta': {'object_name': 'formaPtisis'},
            'above_6400': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'aircraft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.Aircraft']"}),
            'cargo_cycles': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cat_a': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'flight_hours_today': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hoist_lifts_main': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'hoist_lifts_sec': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landings_today': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_stop': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'ef421.item_movement': {
            'Meta': {'object_name': 'item_movement'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.Part']"}),
            'rel_ac_hours': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rel_ac_landings': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rel_aircraft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loz_lol.Aircraft']"})
        },
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
            'limit_type': ('django.db.models.fields.CharField', [], {'default': "'FH'", 'max_length': '2'})
        },
        u'loz_lol.part': {
            'Meta': {'object_name': 'Part'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_is_installed': ('django.db.models.fields.BooleanField', [], {}),
            'part_last_in_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['ef421']