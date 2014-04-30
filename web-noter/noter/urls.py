from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<pn>\d*)$', 'note.views.home'),
	url(r'^note/(?P<id>\d+)/$', 'note.views.getNote'),
	url(r'^addnote/$', 'note.views.addNote'),
	url(r'^add/$', 'note.views.addNote_page'),
	url(r'^remove/$', 'note.views.rmNote'),
	url(r'^manage/(?P<pn>\d*)$', 'note.views.manageNotes'),
	url(r'^edit/(?P<id>\d+)/$', 'note.views.edit'),
	url(r'^update/$', 'note.views.update'),
	url(r'^search/(?P<q>.*)/(?P<pn>\d+)/$', 'note.views.search'),
	url(r'^search/(?P<q>.*)/$', 'note.views.search'),
	url(r'^suggestedtags/$', 'note.views.checkSimilarityAjax'),
	url(r'^filter/(?P<pn>\d+)/$', 'note.views.filter_notes'),
	url(r'^filter/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filter_notes'),
	url(r'^filter/(?P<tags>.+)/$', 'note.views.filter_notes'),
	url(r'^filter/$', 'note.views.filter_notes'),
	url(r'^filterdone/(?P<pn>\d+)/$', 'note.views.filterDone'),
	url(r'^filterdone/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterDone'),
	url(r'^filterdone/(?P<tags>.+)/$', 'note.views.filterDone'),
	url(r'^filterdone/$', 'note.views.filterDone'),
	url(r'^filterundone/(?P<pn>\d+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/(?P<tags>.+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/$', 'note.views.filterUndone'),
	url(r'^contact/$', 'note.views.contact'),
	url(r'^about/$', 'note.views.about'),
	url(r'^login/$', 'note.views.login_view'),
	url(r'^logout/$', 'note.views.logout_view'),
	url(r'^register/$', 'note.views.register'),
)
