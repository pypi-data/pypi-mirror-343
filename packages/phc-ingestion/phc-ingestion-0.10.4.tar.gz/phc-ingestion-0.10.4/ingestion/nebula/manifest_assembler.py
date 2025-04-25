from typing import Optional, TypedDict, Any
from datetime import datetime
from ingestion.shared_util.lambda_client import LambdaClient


class HumanName(TypedDict):
    use: str
    given: list[str]
    family: str


class Identifier(TypedDict):
    system: str
    value: str


class Reference(TypedDict):
    reference: str | None


class Resource(TypedDict):
    id: str | None
    identifier: list[Identifier] | None


class Patient(Resource):
    name: list[HumanName] | None
    gender: str | None
    birthDate: str | None
    managingOrganization: Reference | None
    generalPractitioner: Reference | None


class Organization(Resource):
    name: str | None


class Practitioner(Resource):
    name: list[HumanName] | None


class ManifestAssembler:
    def __init__(self, ingestion_id: str, account_id: str, project_id: str, kit_id: str):
        self.ingestion_id = ingestion_id
        self.account_id = account_id
        self.project_id = project_id
        self.kit_id = kit_id
        self.client = LambdaClient(
            "patient-service",
            {
                "Content-Type": "application/json",
                "LifeOmic-Account": self.account_id,
                "LifeOmic-Correlation-Id": self.ingestion_id,
            },
        )

    def __fetch_patient_by_kit_id(self) -> Optional[Patient]:
        path = f"/{self.account_id}/dstu3/Patient"
        params = {
            "_tag": f"http://lifeomic.com/fhir/dataset|{self.project_id}",
            "identifier": f"http://lifeomic.com/fhir/nebula-kit-id|{self.kit_id}",
        }

        response = self.client.invoke(path, "get", None, params)
        entries = response.get("entry", [])
        patient = entries[0]["resource"] if len(entries) > 0 else None

        return patient

    def __fetch_resource_by_type_and_reference(
        self,
        resource_type: str,
        reference: Reference | None,
    ) -> Any:
        if not reference:
            return None

        resource_id = self.__extract_id_from_reference(reference)
        path = f"/{self.account_id}/dstu3/{resource_type}/{resource_id}"

        try:
            return self.client.invoke(path, "get")
        except RuntimeError as e:
            return None

    def __extract_identifier_from_resource(self, resource: Resource | None) -> str:
        if not resource:
            return ""

        identifiers = resource.get("identifier", [])
        return identifiers[0].get("value", "") if identifiers else ""

    def __extract_id_from_reference(self, reference: Reference) -> str:
        if not reference or not reference.get("reference"):
            return ""

        ref_string = reference.get("reference")
        if not ref_string:
            return ""

        parts = ref_string.split("/")
        return parts[1] if len(parts) > 1 else parts[0]

    def __parse_human_name(self, human_name: list[HumanName] | None):
        if not human_name or len(human_name) == 0:
            return None

        last_name = human_name[0].get("family", "")
        first_name = human_name[0].get("given", [])[0]

        return {
            "lastName": last_name,
            "firstName": first_name,
            "fullName": f"{first_name} {last_name}",
        }

    def create_manifest(self) -> dict[str, Any]:
        patient = self.__fetch_patient_by_kit_id()

        if not patient:
            raise RuntimeError(f"Patient with kit id {self.kit_id} not found")
        patient_birth_date = patient.get("birthDate")
        if not patient_birth_date:
            raise RuntimeError(f"Patient birth date is a required to create a manifest")

        organization: Organization | None = self.__fetch_resource_by_type_and_reference(
            "Organization", patient.get("managingOrganization")
        )

        general_practitioner: Practitioner | None = self.__fetch_resource_by_type_and_reference(
            "Practitioner", patient.get("generalPractitioner")
        )

        patient_info = self.__parse_human_name(patient["name"])
        practitioner_info = self.__parse_human_name(
            general_practitioner.get("name") if general_practitioner else None
        )

        return {
            "name": "Nebula",
            "indexedDate": datetime.now().strftime("%Y-%m-%d"),
            "reference": "GRCh38",  # TODO: Get from project?
            "mrn": patient.get("id"),
            "bodySite": "Buccal Swab",
            "bodySiteDisplay": "Buccal Swab",
            "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
            "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
            "indication": "Genetic Health Screening",
            "indicationDisplay": "Genetic Health Screening",
            "patientInfo": {
                "lastName": patient_info.get("lastName"),
                "dob": datetime.fromisoformat(patient_birth_date).strftime("%Y-%m-%d"),
                "firstName": patient_info.get("firstName"),
                "gender": patient["gender"],
            },
            **(
                {
                    "medFacilName": organization.get("name"),
                    "medFacilID": self.__extract_identifier_from_resource(organization),
                }
                if organization
                else {}
            ),
            **(
                {
                    "orderingMDName": practitioner_info.get("fullName"),
                    "orderingMDNPI": self.__extract_identifier_from_resource(general_practitioner),
                }
                if general_practitioner
                else {}
            ),
        }
