from ui.models import *
b = Bugs.objects.get(bug_id=116)
print b.longdescs_set.all()
