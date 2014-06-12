from setuptools import setup
import os
import sys
import subprocess
from distutils.errors import DistutilsPlatformError, DistutilsInternalError
from setuptools.command.install import install

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('djscript')

npm_dependencies = {
    'rapydscript': '0.2.0'
}

class custom_install(install):
    def run_npm(self):
        """ h/t https://github.com/elbaschid/virtual-node/blob/master/setup.py """

        for name, version in npm_dependencies.items():
            # packages are installed globally to make sure that they are
            # installed in the virtualenv rather than the current directory.
            # it is also necessary for packages containing scripts, e.g. less
            dep_name = '%s@%s' % (name, version)
            self.run_cmd(['npm', 'install', '-g', dep_name])

    def run_cmd(self, cmd, cwd=None, extra_env=None):
        """ h/t https://github.com/elbaschid/virtual-node/blob/master/setup.py """
        all_output = []
        cmd_parts = []

        for part in cmd:
            if len(part) > 45:
                part = part[:20] + "..." + part[-20:]
            if ' ' in part or '\n' in part or '"' in part or "'" in part:
                part = '"%s"' % part.replace('"', '\\"')
            cmd_parts.append(part)
        cmd_desc = ' '.join(cmd_parts)
        logger.debug(" ** Running command %s" % cmd_desc)

        # output
        stdout = subprocess.PIPE

        # env
        if extra_env:
            env = os.environ.copy()
            if extra_env:
                env.update(extra_env)
        else:
            env = None

        # execute
        try:
            proc = subprocess.Popen(
                [' '.join(cmd)], stderr=subprocess.STDOUT, stdin=None, stdout=stdout,
                cwd=cwd, env=env, shell=True)
        except Exception:
            e = sys.exc_info()[1]
            logger.error("Error %s while executing command %s" % (e, cmd_desc))
            raise

        stdout = proc.stdout
        while stdout:
            line = stdout.readline()
            if not line:
                break
            line = line.rstrip()
            all_output.append(line)
            logger.info(line)
        proc.wait()

        # error handler
        if proc.returncode:
            for s in all_output:
                logger.critical(s)
            raise OSError("Command %s failed with error code %s"
                % (cmd_desc, proc.returncode))

        return proc.returncode, all_output

    def run(self):
        if not os.environ.get('VIRTUAL_ENV', None):
            raise DistutilsPlatformError('You must install djscript into a virtualenv. Aborting.')

        install.do_egg_install(self)

        # POST INSTALL
        print "* * * Beginning post-install scripts"

        # module_path = self.install_headers
        # for thing in dir(self):
        #     print "%s : %s\n\n" % (thing, str(getattr(self, thing)))

        # 1) Install npm depencies into virtualenv/virtual-node
        print "* * * \t 1) installing npm dependencies"
        self.run_npm()


setup(
    cmdclass={'install': custom_install},
    name='DjScript',
    version='0.1.0',
    author='Patrick Paul',
    author_email='pztrick44@gmail.com',
    packages=['djscript', ],
    scripts=[],
    url='https://github.com/pztrick/djscript/',
    license='MIT-LICENSE.txt',
    description='Django package for using the RapydScript javascript compiler',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.5.0",
        "virtual-node == 0.1.0",
    ],
)