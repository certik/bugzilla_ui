from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'bugzilla_ui.ui.views.redirect_index'),
    (r'^ui/', include('bugzilla_ui.ui.views')),
)
