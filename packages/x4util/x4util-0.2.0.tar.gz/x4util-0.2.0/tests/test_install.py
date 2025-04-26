import toml
import subprocess


def test_script_installation():
    with open('pyproject.toml', 'r') as f:
        package_toml = toml.load(f)

    expected_scripts = package_toml['project']['scripts']

    for script_name in expected_scripts:

        # check if scripts can be called
        p = subprocess.run(f"{script_name} --help",
                           shell=True, stdout=subprocess.PIPE)
        assert p.returncode == 0

        # expecting to get a help page of the script
        result = p.stdout.decode()
        assert script_name in result
