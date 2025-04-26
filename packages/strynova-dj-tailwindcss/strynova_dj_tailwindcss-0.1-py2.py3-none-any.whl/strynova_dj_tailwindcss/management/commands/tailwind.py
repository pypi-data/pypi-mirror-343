"""
Management command to run the Tailwind CSS CLI.
"""
import os
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Runs the Tailwind CSS CLI to build and watch for changes'

    def get_tailwind_cli_path(self):
        """
        Get the path to the bundled tailwindcss CLI executable.
        """
        # First, try to get the path from settings
        cli_path = getattr(settings, 'TAILWIND_CLI_PATH', None)
        if cli_path and os.path.exists(cli_path):
            return cli_path

        # If not in settings, find the package directory and look for the executable
        package_dir = Path(__file__).resolve().parent.parent.parent

        # Check for platform-specific executable
        if sys.platform == 'win32':
            cli_path = package_dir / 'bin' / 'tailwindcss.exe'
        else:
            cli_path = package_dir / 'bin' / 'tailwindcss'

        # If the executable exists, return its path
        if cli_path.exists():
            return str(cli_path)

        # If we can't find the bundled executable, fall back to the command in PATH
        return 'tailwindcss'

    def add_arguments(self, parser):
        parser.add_argument(
            '--watch',
            action='store_true',
            help='Watch for changes and rebuild automatically',
        )
        parser.add_argument(
            '--input',
            type=str,
            help='Path to the input CSS file',
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Path to the output CSS file',
        )

    def handle(self, *args, **options):
        # Get the input and output paths from options or settings
        input_path = options.get('input') or getattr(settings, 'TAILWIND_INPUT_PATH', None)
        output_path = options.get('output') or getattr(settings, 'TAILWIND_OUTPUT_PATH', None)

        # Check if input and output paths are provided
        if not input_path or not output_path:
            raise CommandError(
                'Input and output paths must be provided either through command line arguments '
                'or in settings.py as TAILWIND_INPUT_PATH and TAILWIND_OUTPUT_PATH.'
            )

        # Make sure the input file exists, if not create it with the proper import statement
        if not os.path.exists(input_path):
            # Make sure the input directory exists
            input_dir = os.path.dirname(input_path)
            if not os.path.exists(input_dir):
                os.makedirs(input_dir)

            # Create the input file with the proper import statement
            with open(input_path, 'w') as f:
                f.write('@import "tailwindcss";')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created input file {input_path} with tailwindcss import statement'
                )
            )

        # Make sure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get the path to the tailwindcss CLI executable
        tailwind_cli = self.get_tailwind_cli_path()

        # Build the command
        cmd = [
            tailwind_cli,
            '-i', input_path,
            '-o', output_path,
        ]

        # Add the watch flag if specified
        if options.get('watch'):
            cmd.append('--watch')
            self.stdout.write(
                self.style.SUCCESS(
                    f'Watching for changes to {input_path} and rebuilding {output_path}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Building {output_path} from {input_path}'
                )
            )

        try:
            # Run the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # If we're not watching, wait for the process to complete
            if not options.get('watch'):
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    raise CommandError(f'Error running tailwindcss: {stderr}')
                self.stdout.write(self.style.SUCCESS('Tailwind CSS build completed successfully'))
                return

            # If we are watching, keep the process running
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.stdout.write(output.strip())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Tailwind CSS build process stopped'))
            process.terminate()
        except Exception as e:
            raise CommandError(f'Error running tailwindcss: {e}')
