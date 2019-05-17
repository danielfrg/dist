import os

from resource_management import Script, Execute, ClientComponentHasNoStatus
import ambari_helpers as helpers


class Client(Script):

    def install(self, env):
        self.configure(env)
        self.install_packages(env)

        package_dir = helpers.package_dir()
        files_dir = os.path.join(package_dir, 'files')
        scripts_dir = os.path.join(package_dir, 'scripts')

        anaconda_setup_sh = os.path.join(scripts_dir, 'shell', 'conda_setup.sh')

        commands = ['cd /tmp; sh ' + anaconda_setup_sh + ' ' + files_dir]

        for command in commands:
            Execute(command)

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        pass


if __name__ == "__main__":
    Client().execute()
