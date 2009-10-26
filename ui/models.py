# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Profiles(models.Model):
    userid = models.IntegerField(primary_key=True)
    login_name = models.CharField(unique=True, max_length=255)
    cryptpassword = models.CharField(max_length=384, blank=True)
    realname = models.CharField(max_length=765)
    disabledtext = models.TextField()
    mybugslink = models.IntegerField()
    extern_id = models.CharField(max_length=192, blank=True)
    disable_mail = models.IntegerField()
    class Meta:
        db_table = u'profiles'

class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    classification_id = models.IntegerField()
    description = models.TextField(blank=True)
    milestoneurl = models.TextField()
    disallownew = models.IntegerField()
    votesperuser = models.IntegerField()
    maxvotesperbug = models.IntegerField()
    votestoconfirm = models.IntegerField()
    defaultmilestone = models.CharField(max_length=60)
    class Meta:
        db_table = u'products'

class Components(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=192)
    product = models.ForeignKey(Products)
    #initialowner = models.ForeignKey(Profiles, db_column='initialowner')
    #initialqacontact = models.ForeignKey(Profiles, null=True, db_column='initialqacontact', blank=True)
    description = models.TextField()
    class Meta:
        db_table = u'components'

class Keyworddefs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'keyworddefs'

class OpSys(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    class Meta:
        db_table = u'op_sys'

class RepPlatform(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    class Meta:
        db_table = u'rep_platform'

class Versions(models.Model):
    value = models.CharField(unique=True, max_length=192)
    product = models.ForeignKey(Products, unique=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'versions'

class Milestones(models.Model):
    product = models.ForeignKey(Products, unique=True)
    value = models.CharField(unique=True, max_length=60)
    sortkey = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'milestones'


class Bugs(models.Model):
    bug_id = models.AutoField(primary_key=True)
    assigned_to = models.ForeignKey(Profiles, db_column="assigned_to",
            related_name="assigned_to_set")
    bug_file_loc = models.TextField(blank=True)
    bug_severity = models.CharField(max_length=192)
    bug_status = models.CharField(max_length=192)
    creation_ts = models.DateTimeField(null=True, blank=True)
    delta_ts = models.DateTimeField()
    short_desc = models.CharField(max_length=765)
    op_sys = models.CharField(max_length=192)
    priority = models.CharField(max_length=192)
    product = models.ForeignKey(Products)
    rep_platform = models.CharField(max_length=192)
    reporter = models.ForeignKey(Profiles, db_column="reporter")
    version = models.CharField(max_length=192)
    component = models.ForeignKey(Components)
    resolution = models.CharField(max_length=192)
    target_milestone = models.CharField(max_length=60)
    qa_contact = models.IntegerField(null=True, blank=True)
    status_whiteboard = models.TextField()
    votes = models.IntegerField()
    keywords_field = models.TextField(db_column="keywords")
    kws = models.ManyToManyField(Keyworddefs, through="Keywords")
    lastdiffed = models.DateTimeField(null=True, blank=True)
    everconfirmed = models.IntegerField()
    reporter_accessible = models.IntegerField()
    cclist_accessible = models.IntegerField()
    estimated_time = models.DecimalField(max_digits=7, decimal_places=2)
    remaining_time = models.DecimalField(max_digits=7, decimal_places=2)
    deadline = models.DateTimeField(null=True, blank=True)
    alias = models.CharField(unique=True, max_length=60, blank=True)
    class Meta:
        db_table = u'bugs'

class Attachments(models.Model):
    attach_id = models.IntegerField(primary_key=True)
    bug = models.ForeignKey(Bugs)
    creation_ts = models.DateTimeField()
    description = models.TextField()
    mimetype = models.TextField()
    ispatch = models.IntegerField(null=True, blank=True)
    filename = models.CharField(max_length=300)
    submitter = models.ForeignKey(Profiles)
    isobsolete = models.IntegerField()
    isprivate = models.IntegerField()
    isurl = models.IntegerField()
    modification_time = models.DateTimeField()
    class Meta:
        db_table = u'attachments'

class AttachData(models.Model):
    id = models.ForeignKey(Attachments, primary_key=True, db_column="id")
    thedata = models.TextField()
    class Meta:
        db_table = u'attach_data'

class Longdescs(models.Model):
    bug = models.ForeignKey(Bugs)
    who = models.ForeignKey(Profiles, db_column="who")
    bug_when = models.DateTimeField()
    work_time = models.DecimalField(max_digits=7, decimal_places=2)
    thetext = models.TextField()
    isprivate = models.IntegerField()
    already_wrapped = models.IntegerField()
    comment_id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    extra_data = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'longdescs'

class Keywords(models.Model):
    bug_id = models.ForeignKey(Bugs, db_column="bug_id")
    keywordid = models.ForeignKey(Keyworddefs, db_column="keywordid")
    class Meta:
        db_table = u'keywords'


"""
class BugGroupMap(models.Model):
    bug_id = models.IntegerField(unique=True)
    group_id = models.IntegerField()
    class Meta:
        db_table = u'bug_group_map'

class BugSeverity(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    class Meta:
        db_table = u'bug_severity'

class BugStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    is_open = models.IntegerField()
    class Meta:
        db_table = u'bug_status'

class BugsActivity(models.Model):
    bug_id = models.IntegerField()
    attach_id = models.IntegerField(null=True, blank=True)
    who = models.ForeignKey(Profiles, db_column='who')
    bug_when = models.DateTimeField()
    fieldid = models.IntegerField()
    added = models.TextField(blank=True)
    removed = models.TextField(blank=True)
    class Meta:
        db_table = u'bugs_activity'

class BugsFulltext(models.Model):
    bug_id = models.IntegerField(primary_key=True)
    short_desc = models.CharField(max_length=765)
    comments = models.TextField(blank=True)
    comments_noprivate = models.TextField(blank=True)
    class Meta:
        db_table = u'bugs_fulltext'

class BzSchema(models.Model):
    schema_data = models.TextField()
    version = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = u'bz_schema'

class CategoryGroupMap(models.Model):
    category_id = models.IntegerField(unique=True)
    group_id = models.IntegerField(unique=True)
    class Meta:
        db_table = u'category_group_map'

class Cc(models.Model):
    bug_id = models.IntegerField(unique=True)
    who = models.ForeignKey(Profiles, db_column='who')
    class Meta:
        db_table = u'cc'

class Classifications(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField(blank=True)
    sortkey = models.IntegerField()
    class Meta:
        db_table = u'classifications'

class ComponentCc(models.Model):
    user = models.ForeignKey(Profiles)
    component_id = models.IntegerField(unique=True)
    class Meta:
        db_table = u'component_cc'

class Dependencies(models.Model):
    blocked = models.IntegerField()
    dependson = models.IntegerField()
    class Meta:
        db_table = u'dependencies'

class Duplicates(models.Model):
    dupe_of = models.IntegerField()
    dupe = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'duplicates'

class EmailSetting(models.Model):
    user = models.ForeignKey(Profiles)
    relationship = models.IntegerField(unique=True)
    event = models.IntegerField(unique=True)
    class Meta:
        db_table = u'email_setting'

class Fielddefs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField()
    mailhead = models.IntegerField()
    sortkey = models.IntegerField()
    obsolete = models.IntegerField()
    type = models.IntegerField()
    custom = models.IntegerField()
    enter_bug = models.IntegerField()
    class Meta:
        db_table = u'fielddefs'

class Flagexclusions(models.Model):
    type_id = models.IntegerField()
    product_id = models.IntegerField(null=True, blank=True)
    component_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'flagexclusions'

class Flaginclusions(models.Model):
    type_id = models.IntegerField()
    product_id = models.IntegerField(null=True, blank=True)
    component_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'flaginclusions'

class Flags(models.Model):
    id = models.IntegerField(primary_key=True)
    type_id = models.IntegerField()
    status = models.CharField(max_length=3)
    bug_id = models.IntegerField()
    attach_id = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField(null=True, blank=True)
    setter_id = models.IntegerField(null=True, blank=True)
    requestee_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'flags'

class Flagtypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    cc_list = models.CharField(max_length=600, blank=True)
    target_type = models.CharField(max_length=3)
    is_active = models.IntegerField()
    is_requestable = models.IntegerField()
    is_requesteeble = models.IntegerField()
    is_multiplicable = models.IntegerField()
    sortkey = models.IntegerField()
    grant_group_id = models.IntegerField(null=True, blank=True)
    request_group_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'flagtypes'

class GroupControlMap(models.Model):
    group_id = models.IntegerField()
    product_id = models.IntegerField(unique=True)
    entry = models.IntegerField()
    membercontrol = models.IntegerField()
    othercontrol = models.IntegerField()
    canedit = models.IntegerField()
    editcomponents = models.IntegerField()
    editbugs = models.IntegerField()
    canconfirm = models.IntegerField()
    class Meta:
        db_table = u'group_control_map'

class GroupGroupMap(models.Model):
    member_id = models.IntegerField(unique=True)
    grantor_id = models.IntegerField(unique=True)
    grant_type = models.IntegerField(unique=True)
    class Meta:
        db_table = u'group_group_map'

class Groups(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=765)
    description = models.TextField()
    isbuggroup = models.IntegerField()
    userregexp = models.TextField()
    isactive = models.IntegerField()
    icon_url = models.TextField(blank=True)
    class Meta:
        db_table = u'groups'

class Logincookies(models.Model):
    cookie = models.CharField(max_length=48, primary_key=True)
    userid = models.ForeignKey(Profiles, db_column='userid')
    ipaddr = models.CharField(max_length=120)
    lastused = models.DateTimeField()
    class Meta:
        db_table = u'logincookies'

class Namedqueries(models.Model):
    userid = models.ForeignKey(Profiles, db_column='userid')
    name = models.CharField(unique=True, max_length=192)
    query = models.TextField()
    query_type = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'namedqueries'

class NamedqueriesLinkInFooter(models.Model):
    namedquery = models.ForeignKey(Namedqueries)
    user = models.ForeignKey(Profiles)
    class Meta:
        db_table = u'namedqueries_link_in_footer'

class NamedqueryGroupMap(models.Model):
    namedquery_id = models.IntegerField(unique=True)
    group_id = models.IntegerField()
    class Meta:
        db_table = u'namedquery_group_map'

class Priority(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    class Meta:
        db_table = u'priority'

class ProfileSetting(models.Model):
    user = models.ForeignKey(Profiles)
    setting_name = models.CharField(unique=True, max_length=96)
    setting_value = models.CharField(max_length=96)
    class Meta:
        db_table = u'profile_setting'

class ProfilesActivity(models.Model):
    userid = models.ForeignKey(Profiles, db_column='userid')
    who = models.ForeignKey(Profiles, db_column='who')
    profiles_when = models.DateTimeField()
    fieldid = models.ForeignKey(Fielddefs, db_column='fieldid')
    oldvalue = models.TextField(blank=True)
    newvalue = models.TextField(blank=True)
    class Meta:
        db_table = u'profiles_activity'

class Quips(models.Model):
    quipid = models.IntegerField(primary_key=True)
    userid = models.IntegerField(null=True, blank=True)
    quip = models.TextField()
    approved = models.IntegerField()
    class Meta:
        db_table = u'quips'

class Resolution(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    isactive = models.IntegerField()
    class Meta:
        db_table = u'resolution'

class Series(models.Model):
    series_id = models.IntegerField(primary_key=True)
    creator = models.IntegerField(unique=True, null=True, blank=True)
    category = models.IntegerField(unique=True)
    subcategory = models.IntegerField(unique=True)
    name = models.CharField(unique=True, max_length=192)
    frequency = models.IntegerField()
    last_viewed = models.DateTimeField(null=True, blank=True)
    query = models.TextField()
    is_public = models.IntegerField()
    class Meta:
        db_table = u'series'

class SeriesCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    class Meta:
        db_table = u'series_categories'

class SeriesData(models.Model):
    series_id = models.IntegerField(unique=True)
    series_date = models.DateTimeField(unique=True)
    series_value = models.IntegerField()
    class Meta:
        db_table = u'series_data'

class Setting(models.Model):
    name = models.CharField(max_length=96, primary_key=True)
    default_value = models.CharField(max_length=96)
    is_enabled = models.IntegerField()
    subclass = models.CharField(max_length=96, blank=True)
    class Meta:
        db_table = u'setting'

class SettingValue(models.Model):
    name = models.CharField(unique=True, max_length=96)
    value = models.CharField(unique=True, max_length=96)
    sortindex = models.IntegerField(unique=True)
    class Meta:
        db_table = u'setting_value'

class StatusWorkflow(models.Model):
    old_status = models.IntegerField(unique=True, null=True, blank=True)
    new_status = models.IntegerField(unique=True)
    require_comment = models.IntegerField()
    class Meta:
        db_table = u'status_workflow'

class Tokens(models.Model):
    userid = models.ForeignKey(Profiles, null=True, db_column='userid', blank=True)
    issuedate = models.DateTimeField()
    token = models.CharField(max_length=48, primary_key=True)
    tokentype = models.CharField(max_length=24)
    eventdata = models.TextField(blank=True)
    class Meta:
        db_table = u'tokens'

class UserGroupMap(models.Model):
    user_id = models.IntegerField(unique=True)
    group_id = models.IntegerField(unique=True)
    isbless = models.IntegerField(unique=True)
    grant_type = models.IntegerField(unique=True)
    class Meta:
        db_table = u'user_group_map'

class Votes(models.Model):
    who = models.ForeignKey(Profiles, db_column='who')
    bug_id = models.IntegerField()
    vote_count = models.IntegerField()
    class Meta:
        db_table = u'votes'

class Watch(models.Model):
    watcher = models.ForeignKey(Profiles, db_column='watcher')
    watched = models.ForeignKey(Profiles, db_column='watched')
    class Meta:
        db_table = u'watch'

class WhineEvents(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_userid = models.ForeignKey(Profiles, db_column='owner_userid')
    subject = models.CharField(max_length=384, blank=True)
    body = models.TextField(blank=True)
    class Meta:
        db_table = u'whine_events'

class WhineQueries(models.Model):
    id = models.IntegerField(primary_key=True)
    eventid = models.ForeignKey(WhineEvents, db_column='eventid')
    query_name = models.CharField(max_length=192)
    sortkey = models.IntegerField()
    onemailperbug = models.IntegerField()
    title = models.CharField(max_length=384)
    class Meta:
        db_table = u'whine_queries'

class WhineSchedules(models.Model):
    id = models.IntegerField(primary_key=True)
    eventid = models.ForeignKey(WhineEvents, db_column='eventid')
    run_day = models.CharField(max_length=96, blank=True)
    run_time = models.CharField(max_length=96, blank=True)
    run_next = models.DateTimeField(null=True, blank=True)
    mailto = models.IntegerField()
    mailto_type = models.IntegerField()
    class Meta:
        db_table = u'whine_schedules'
"""
