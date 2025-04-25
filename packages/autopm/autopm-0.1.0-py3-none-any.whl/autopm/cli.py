# autopm/cli.py
import sys
import runpy
import click
from .tracker import install_import_hook

@click.group()
def main():
    pass

@main.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
@click.argument("script_path", type=click.Path(exists=True))
@click.pass_context
def run(ctx, script_path):
    # 1) install our import‐watcher
    install_import_hook()
    # 2) shift sys.argv so that the script sees its args
    sys.argv = [script_path] + ctx.args
    # 3) execute the target script as __main__
    runpy.run_path(script_path, run_name="__main__")

@main.command()
def install():
    # just forward to pip install -r requirements.txt
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    main()
