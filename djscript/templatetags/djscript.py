from django import template
from django.conf import settings
import os
import subprocess

register = template.Library()

djurls = getattr(settings, 'DJSCRIPT_PATHS')

# settings value
@register.simple_tag
def djurl(dot_path):
    """ 
        DEBUG == True ? Compiles and serves file at dot_path
        DEBUG == False ? Serves pre-compiled file path
    
        Usage:  {% djurl 'path.to.file' %}
    """
    try:
        http_path = os.path.join(getattr(settings, 'STATIC_URL', ''), djurls[dot_path])
        if settings.DEBUG:
            # 1) Compile!
            source_path = "%s.pyj" % os.path.join(getattr(settings, 'PROJECT_HOME'), *dot_path.split('.'))
            target_path = os.path.join(getattr(settings, 'STATIC_ROOT'), djurls[dot_path])

            cmd = ['rapydscript', source_path, '-o', target_path]
            proc = subprocess.Popen([' '.join(cmd)], shell=True)

        return http_path
    except KeyError:
        return None
