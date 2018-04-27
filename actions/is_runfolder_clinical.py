from st2actions.runners.pythonrunner import Action

from genologics.lims import Lims
from genologics.config import BASEURI, USERNAME, PASSWORD


class IsRunfolderClinical(Action):
    """
    Looks up a runfolder in Clarity LIMS and decides whether it contains clinical projects
    """

    FACILITY_UDF = "Facility"
    CLINICAL_GENOMICS_KEY = "Clinical Genomics"

    @staticmethod
    def projects_from_containers(containers):
        """
        Traverse the contents of a container and return the project objects having samples on the container

        :param containers: list of container objects
        :return: list of project objects associated with the container, in no particular order
        """
        projects = set()
        for container in containers:
            for well_artifact in container.get_placements().values():
                for sample in well_artifact.samples:
                    projects.add(sample.project)
        return list(filter(lambda p: p is not None, projects))

    def run(self, flowcell_name):
        lims = Lims(BASEURI, USERNAME, PASSWORD)
        containers = lims.get_containers(name=flowcell_name)
        projects = projects_from_containers(containers)
        is_clinical = self.CLINICAL_GENOMICS_KEY in [project.udf.get(self.FACILITY_UDF) for project in projects]
        return True, is_clinical
