#!/usr/bin/python3
"""
creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['54.237.4.65', '18.233.64.247']


def do_pack():
    """ generates a tgz archive """
    date = datetime.now()
    name_archive = 'web_static_' + date.strftime('%Y%m%d%H%M%S') + '.tgz'
    local('sudo mkdir -p versions')
    archive = local('tar -cvzf versions/{} web_static'.format(name_archive))

    if archive is not None:
        return name_archive
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if exists(archive_path) is False:
        return False
    else:
        file = archive_path.split('/')[-1]
        file_name = file.split('.')[0]
        path = '/data/web_static/releases/'
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, file_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file, path, file_name))
        run('rm /tmp/{}'.format(file))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, file_name))
        run('rm -rf {}{}/web_static'.format(path, file_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, file_name))
        return True


def deploy():
    """ creates and distributes an archive to your web servers """
    path = do_pack()
    if path is None:
        return False

    return do_deploy(path)
