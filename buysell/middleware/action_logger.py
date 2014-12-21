from buysell.api.manage.models import Log
from buysell import settings
import json

class ActionLoggerMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not (request.path.startswith(settings.MEDIA_URL) or \
                request.path.startswith(settings.STATIC_URL)) and \
                hasattr(request, 'user') and request.user.is_authenticated():

            log_t = None
            log_i = {}

            if view_func.__name__ == 'SessionLoginHandler':
                log_t = 'login'
            elif view_func.__name__ == 'SessionLogoutHandler':
                log_t = 'logout'
            elif view_func.__name__ == 'PostCreateHandler':
                log_t = 'a_post'
            elif view_func.__name__ == 'TransactionCreateHandler':
                log_t = 'req_trans'
                log_i['post_id'] = view_kwargs['post_id']
                log_i['content'] = json.loads(request.POST['_content'])
            elif view_func.__name__ == 'TransactionHandler':
                log_t = 'a_post'
            elif view_func.__name__ == 'PostCreateHandler':
                log_t = 'a_post'
            elif view_func.__name__ == 'PostCreateHandler':
                log_t = 'a_post'
            elif view_func.__name__ == 'PostCreateHandler':
                log_t = 'a_post'
            elif view_func.__name__ == 'PostCreateHandler':
                log_t = 'a_post'

            request.ACTION_LOGGER = {
                    'log_type' : log_t,
                    'info' : log_i,
            }


    def process_response(self, request, response):
        
        if not (request.path.startswith(settings.MEDIA_URL) or \
                request.path.startswith(settings.STATIC_URL)) and \
                hasattr(request, 'user') and \
                request.user.is_authenticated():

            log_t = None
            log_i = None
            if request.ACTION_LOGGER is not None:
                log_t = request.ACTION_LOGGER['log_type']
                log_i = request.ACTION_LOGGER['info']
                print log_i
                
            if log_t is not None:
                new_log = Log(actor=request.user, log_type=log_t, info=json.dumps(log_i))
                new_log.save()

        return response
