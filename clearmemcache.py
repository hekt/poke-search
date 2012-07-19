#! /user/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import memcache

memcache.flush_all()
print "Content-Type: text/plain"
print ''
print 'flush_all';
