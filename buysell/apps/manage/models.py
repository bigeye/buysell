from django.db import models
from django.conf import settings

class Report(models.Model):
    
   REPORT_TYPE = (
        ('post', 'POST'),
        ('message', 'MESSAGE'),
        ('comment', 'COMMENT'),
        ('trans', 'TRANSACTION'),
        ('claim', 'CLAIM'),
        ('other', 'OTHER'),
    )

   report_type = models.CharField(max_length = 10, choices = REPORT_TYPE)
   victim = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            related_name = 'report_victim')
   suspect = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name = 'suspect_victim')
   content = models.TextField()

class Log(models.Model):

    LOG_TYPE = (
        ('login', 'LOGIN'),
        ('logout', 'LOGOUT'),
        ('snd_msg', 'SEND MESSAGE'),
        ('sub_tag', 'SUBSCRIBE TAGS'),
        ('uns_tag', 'UNSUBSCRIBE TAGS'),
        ('a_post', 'ADD POST'),
        ('d_post', 'DELETE POST'),
        ('u_post', 'UPDATE POST'),
        ('w_comment', 'WRITE COMMENT'),
        ('d_comment', 'DELTE COMMENT'),
        ('req_trans', 'REQUEST TRANSACTION'),
        ('acc_trans', 'ACCEPT TRANSACTION'),
        ('den_trans', 'DENY TRANSACTION'),
    )

    log_type = models.CharField(max_length = 10, choices = LOG_TYPE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL)
    action_date = models.DateTimeField(auto_now_add = True)
    info = models.TextField() # to have additional information
