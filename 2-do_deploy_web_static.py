#!/usr/bin/python3
""" distributes an archive to your web servers, using the function do_deploy """


from fabric.api import run, env, put
from os.path import exists
env.hosts = ['54.237.4.65', '18.233.64.247']

def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if exists(archive_path) is False:
        return False
    try:
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
    except:
        return False
