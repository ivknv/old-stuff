from django.conf.urls import patterns, include, url
from django.conf import settings

from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

APIPatterns = [
	url(r'^getNotes/$', 'note.api.API_getNotes', name="getNotes"),
	url(r'^rmNote/$', 'note.api.API_rmNote', name="rmNote"),
	url(r'^rmNotes/$', 'note.api.API_rmNotes', name="rmNotes"),
	url(r'^register/$', 'note.api.API_register', name="register"),
	url(r'^addNote/$', 'note.api.API_addNote', name="addNote"),
	url(r'^addNotes/$', 'note.api.API_addNotes', name="addNotes"),
	url(r'^deleteAccount/$', 'note.api.API_deleteAccount', name="deleteAccount"),
	url(r'^getNote/$', 'note.api.API_getNote', name="getNote"),
	url(r'^getUserInfo/$', 'note.api.API_getUserInfo', name="getUserInfo"),
]

urlpatterns = patterns('',
	
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<pn>\d*)$', 'note.views.home', name="Home"),
	url(r'^note/(?P<id>\d+)/$', 'note.views.getNote', name="getNote"),
	url(r'^addnote/$', 'note.views.addNote', name="addNote"),
	url(r'^add/$', 'note.views.addNote_page', name="Add"),
	url(r'^remove/$', 'note.views.rmNote', name="rmNote"),
	url(r'^manage/(?P<pn>\d*)$', 'note.views.manageNotes'),
	url(r'^edit/(?P<id>\d+)/$', 'note.views.edit', name="Edit"),
	url(r'^update/$', 'note.views.update', name="Update"),
	url(r'^search/(?P<q>.*)/(?P<pn>\d+)/$', 'note.views.search'),
	url(r'^search/(?P<q>.*)/$', 'note.views.search', name="Search"),
	url(r'^suggestedtags/$', 'note.views.checkSimilarityAjax', name="checkSimilarityAjax"),
	url(r'^filter/(?P<pn>\d+)/$', 'note.views.filter_notes'),
	url(r'^filter/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filter_notes'),
	url(r'^filter/(?P<tags>.+)/$', 'note.views.filter_notes'),
	url(r'^filter/$', 'note.views.filter_notes', name="filter"),
	url(r'^filterdone/(?P<pn>\d+)/$', 'note.views.filterDone'),
	url(r'^filterdone/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterDone'),
	url(r'^filterdone/(?P<tags>.+)/$', 'note.views.filterDone'),
	url(r'^filterdone/$', 'note.views.filterDone', name="filterDone"),
	url(r'^filterundone/(?P<pn>\d+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/(?P<tags>.+)/$', 'note.views.filterUndone'),
	url(r'^filterundone/$', 'note.views.filterUndone', name="filterUndone"),
	url(r'^filtersnippets/(?P<pn>\d+)/$', 'note.views.filterSnippets'),
	url(r'^filtersnippets/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterSnippets'),
	url(r'^filtersnippets/(?P<tags>.+)/$', 'note.views.filterSnippets'),
	url(r'^filtersnippets/$', 'note.views.filterSnippets', name="filterSnippets"),
	url(r'^filterwarnings/(?P<pn>\d+)/$', 'note.views.filterWarnings'),
	url(r'^filterwarnings/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterWarnings'),
	url(r'^filterwarnings/(?P<tags>.+)/$', 'note.views.filterWarnings'),
	url(r'^filterwarnings/$', 'note.views.filterWarnings', name="filterWarnings"),
	url(r'^filternotes/(?P<pn>\d+)/$', 'note.views.filterNotes'),
	url(r'^filternotes/(?P<tags>.+)/(?P<pn>\d+)/$', 'note.views.filterNotes'),
	url(r'^filternotes/(?P<tags>.+)/$', 'note.views.filterNotes'),
	url(r'^filternotes/$', 'note.views.filterNotes', name="fitlerNotes"),
	url(r'^contact/$', 'note.views.contact', name="Contact"),
	url(r'^about/$', TemplateView.as_view(template_name="about.html"), name="About"),
	url(r'^login/$', 'note.views.login_view', name="Login"),
	url(r'^logout/$', 'note.views.logout_view', name="Logout"),
	url(r'^register/$', 'note.views.register', name="Register"),
	url(r'^profile/$', 'note.views.profile', name="Profile"),
	url(r'^update-username/$', 'note.views.update_username', name="updateUsername"),
	url(r'^update-password/$', 'note.views.update_password', name="updatePassword"),
	url(r'^update-firstname/$', 'note.views.update_first_name', name="updateFirstName"),
	url(r'^update-lastname/$', 'note.views.update_last_name', name="updateLastName"),
	url(r'^delete-account/$', 'note.views.delete_account', name="deleteAccount"),
	url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'note.views.reset_password_confirm', name="password_reset_confirm"),
	url(r'^reset/$', 'note.views.reset_password', name="password_reset"),
	url(r'^reset/complete/$', TemplateView.as_view(template_name="registration/password_reset_complete.html")),
	url(r'^reset/sent/$', TemplateView.as_view(template_name="registration/password_reset_sent.html")),
	url(r'^api/', include(APIPatterns, namespace="API")),
	url(r'^api-info/$', TemplateView.as_view(template_name="api-info.html")),
)
