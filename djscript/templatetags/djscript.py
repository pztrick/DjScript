from django import template
from django.conf import settings
from django.shortcuts import render_to_response

import os
import subprocess

register = template.Library()

djurls = getattr(settings, 'DJSCRIPT_PATHS')
prettify = getattr(settings, 'DJSCRIPT_PRETTIFY', False)
logger_name = getattr(settings, 'DJSCRIPT_LOGGER_HANDLE', 'django.request')
djglobals = getattr(settings, 'DJSCRIPT_GLOBAL_DICT', None)

import logging
logger = logging.getLogger(logger_name)

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
            source_path = "%s.pyj" % os.path.join(getattr(settings, 'PROJECT_HOME'), *dot_path.split('.'))
            target_path = os.path.join(getattr(settings, 'STATIC_ROOT'), djurls[dot_path])

            # 1) Parse any templatetags
            temp_file = open(source_path + ".temp", 'w')
            temp_path = temp_file.name
            fake_response = render_to_response(source_path)
            temp_file.write(fake_response.content)
            temp_file.close()

            # 2) Compile to javascript
            cmd = ['rapydscript', temp_path, '-p' if prettify else '']
            
            if djglobals:
                javascript = "if(%s === undefined){var %s = {};}" % (djglobals, djglobals)
                cmd.insert(0, "echo '%s' &&" % javascript)

            output = subprocess.check_output([' '.join(cmd)], shell=True)

            with open(target_path, 'w') as fd:
                fd.write(output)

        return http_path
    except Exception as exception:
        logger.exception(exception)
        return "djscript-djurl-exception.500"