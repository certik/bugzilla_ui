from django.conf.urls.defaults import *

import os.path
p = os.path.join(os.path.dirname(__file__), 'media_files/')

urlpatterns = patterns('',
    (r'^$', 'bugzilla_ui.ui.views.redirect_index'),
    (r'^bugs-ui/media_files/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': p}),
    (r'^bugs-ui/', include('bugzilla_ui.ui.views')),
)
