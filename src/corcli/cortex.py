"""
Module containing Cortex related classes
"""
import inquirer
import json
import requests

from time import sleep
from cortex4py.api import Api
from cortex4py.query import *
from inquirer.themes import GreenPassion
from colorama import Fore

class Cortex:
    """Base class for interacting with Cortex.

    Args:
        parameters (dict): Parameters for Cortex configuration.

    """
    def __init__(self, parameters: dict) -> None:
        """
        Initializes a Cortex instance.

        Args:
            parameters (dict): Parameters for Cortex configuration.

        """
        self._cortex_url = parameters.cortex_url
        self._cortex_api = parameters.api_key
        self._verify_cert = parameters.verify_cert
        self._observable_type = parameters.observable_type
        self._observable_data = parameters.observable_data
        self._extract_only = parameters.extract_only
        self._download_files = parameters.download_files
        self._full_report = parameters.full_report
        self._no_cache = parameters.no_cache

    def authentication(self):
        """Authenticates against Cortex

        Returns:
            None

        """

        self._api = Api(self._cortex_url,
                  self._cortex_api,
                  verify_cert=self._verify_cert)

    def list_analyzers(self):
        """List the available analyzers

        Lists the available analyzers for the configured observable type.

        Returns:
            list: List of analyzer names.

        """
        self.authentication()
        analyzers = self._api.analyzers.find_all({}, range='all')
        analyzers = self._api.analyzers.get_by_type(self._observable_type)

        if not analyzers:
            print(f'There are no available analysers for type {self._observable_type}.')
            exit(1)

        analyzer_names = []

        for analyzer in analyzers:
            analyzer_names.append(analyzer.name)

        return analyzer_names

    def select_analyzers(self):
        """Selection of analyzers

        Displays a list of available analyzers and allows the user to select multiple analyzers.

        Returns:
            list: List of selected analyzers.
        """
        self._list_analyzers = self.list_analyzers()
        questions = [
        inquirer.Checkbox('EnabledAnalyzers',
                        message="Select one or multiple analysers",
                        choices= self._list_analyzers,
                    ),
        ]
        answers = inquirer.prompt(questions, theme=GreenPassion())
        try:
            options = answers['EnabledAnalyzers']
        except TypeError:
            print("No analyzers selected.")
            exit(1)
        except Exception:
            raise Exception("Something unexepected happened...")

        return options

    def download_file(self, file_id, filename):
        """Download a file attachment from job

        This method downloads a file attachment from Cortex's datastore using the given file ID.
        The downloaded file will be saved with the provided filename as a zip file.

        Returns:
            None

        """
        headers = {
            "Authorization": f"Bearer {self._cortex_api}"
        }

        url = f'{self._cortex_url}/api/datastorezip/{file_id}'

        response = requests.get(url, headers=headers)

        filename = filename + '.zip'

        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {filename}")

    def run_analyzer_job(self, target_observable, target_analyzer):
        """
        Runs an analyzer job for the specified analyzers and target

        Args:
            target_analyzers (list): List of analyzer names to run.

        Returns:
            str: JSON-formatted result of the analyzer job.
        """

        self._target_analyzer = target_analyzer

        job = self._api.analyzers.run_by_name(self._target_analyzer, {
            'data': target_observable,
            'dataType': self._observable_type,
            'tlp': 2
        }, force=self._no_cache)

        self._job_id = job.json()['id']

        job_status = self._api.jobs.get_report(self._job_id).status

        while job_status in ("Waiting", "InProgress"):
            sleep(2)
            job_status = self._api.jobs.get_report(self._job_id).status

        if job_status == "Failure":
            result = f"Job ID {self._job_id} failed."
            return result

        if job_status == "Deleted":
            result = f"Job ID {self._job_id} was deleted."
            return result

        job_result = self._api.jobs.get_report(self._job_id).report

        if self._extract_only:
            artifacts = self._api.jobs.get_artifacts(self._job_id)

            results = []

            for a in artifacts:
                if a.dataType == "file":
                    result = '- [{}]: {}, size: {}'.format(a.dataType, a.attachment['name'], a.attachment['size'])
                    if self._download_files:
                        self.download_file(a.attachment['id'], a.attachment['name'])
                else:
                    result = '- [{}]: {}'.format(a.dataType, a.data)
                results.append(result)
            return results

        elif self._full_report:
            result = json.dumps(job_result.get('full', {}), indent=2)
            return result
        else: # Report level summary by default
            summary  = json.dumps(job_result.get('summary', {}), indent=2)

            if summary == '{}':
                summary = False
                return summary

            summary = json.loads(summary)

            results = []

            for taxonomy in summary["taxonomies"]:
                level = taxonomy["level"]
                namespace = taxonomy["namespace"]
                predicate = taxonomy["predicate"]
                value = taxonomy["value"]

                if level == 'malicious':
                    level = f"{Fore.RED}{level}{Fore.RESET}"
                elif level == 'suspicious':
                    level = f"{Fore.YELLOW}{level}{Fore.RESET}"
                else:
                    level = f"{Fore.BLUE}{level}{Fore.RESET}"

                result = f'- {level} / {namespace}:{predicate}=\"{value}\"'
                results.append(result)

            return results