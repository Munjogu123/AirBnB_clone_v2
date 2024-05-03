#!/usr/bin/python3
from datetime import datetime
from fabric.api import local


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder """
    date = datetime.now()
    name_archive = 'web_static_' + date.strftime('%Y%m%d%H%M%S') + '.tgz'
    local('sudo mkdir -p versions')
    archive = local('tar -cvzf versions/{} web_static'.format(name_archive))

    if archive is not None:
        return name_archive
    else:
        return None
