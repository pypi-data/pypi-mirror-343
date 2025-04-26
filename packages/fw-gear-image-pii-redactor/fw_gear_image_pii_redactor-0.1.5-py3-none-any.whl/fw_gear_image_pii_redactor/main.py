"""Main module."""

import logging

from flywheel_gear_toolkit import GearToolkitContext

from fw_client import FWClient
from fw_file.dicom import DICOMCollection
from fw_file.dicom.utils import generate_uid

from .utility_helpers import get_protocol_from_name
from .utility_helpers import redact_and_save_dicom
from .utility_helpers import set_output_filename

log = logging.getLogger(__name__)


def run(
    context: GearToolkitContext,
    api_key: str,
    protocol_name: str,
    file_path: str,
    file_id: str,
    output_file_prefix: str,
    project_id: str,
    read_timeout: int,
):
    """Run the algorithm defined in this gear.

    Args:
        context (GearToolkitContext): The gear context.
        api_key (str): The API key generated for this gear run.
        protocol_name (str): The name of the protocol to use.
        file_path (str): The absolute file path of the input file.
        file_id (str): The file id of the input file.
        output_file_prefix (str): The prefix for the output file name.
        project_id (str): The id for the project.
        read_timeout (int): The read timeout for the API requests. Defaults to 60.

    Returns:
        int: The exit code.
    """
    client = FWClient(api_key=api_key, read_timeout=read_timeout)

    if protocol_name:
        # Ensure the protocol exists for that project
        # Protocol Names are unique within a project
        if not (
            protocol := get_protocol_from_name(
                client, protocol_name=protocol_name, project_id=project_id
            )
        ):
            log.error(
                "Protocol %s not found for project (%s).", protocol_name, project_id
            )
            log.info(
                "Check protocol definitions and project permissions for your API key."
            )
            return 1
        log.info("The protocol found is %s", protocol)
    else:
        return 1

    # get the latest created completed task for the project, file and protocol
    all_tasks = client.get(
        "/api/readertasks",
        params={
            "filter": f"parents.file={file_id},parents.project={project_id},protocol_id={protocol._id},status=Complete",
            "sort": "modified:asc",
            "exhaustive": True,
        },
    )
    no_of_tasks = all_tasks["count"]
    if no_of_tasks > 0:
        log.info("There are %d completed tasks; selecting last task", no_of_tasks)
        task = all_tasks.results[-1]

        # get the annotations for that task
        ann = client.get(
            "/api/annotations",
            params={"filter": f"task_id={task._id},file_ref.file_id={file_id}"},
        )
        log.info("Number of annotations in check is %d", ann["count"])

        if file_path.endswith(".zip"):
            col = DICOMCollection.from_zip(file_path)
        else:
            col = DICOMCollection(file_path)

        all_sop_instance_uid = col.bulk_get("SOPInstanceUID")

        for result in ann["results"]:
            start_x = int(result["data"]["handles"]["start"]["x"])
            start_y = int(result["data"]["handles"]["start"]["y"])
            end_x = int(result["data"]["handles"]["end"]["x"])
            end_y = int(result["data"]["handles"]["end"]["y"])
            slice_number = result["data"]["sliceNumber"]
            sop_instance = result["data"]["SOPInstanceUID"]
            if sop_instance in all_sop_instance_uid:
                # key logic: match the sop_instance_uid from
                # the annotations to the correct dicom slice
                index = all_sop_instance_uid.index(sop_instance)
                dcm = col[index]
                redact_and_save_dicom(dcm, start_x, end_x, start_y, end_y)
            log.info(
                "Start: (x: %d, y: %d), End: (x: %d, y: %d), Slice Number: %d",
                start_x,
                start_y,
                end_x,
                end_y,
                slice_number,
            )

        # Update SeriesInstanceUID and StudyInstanceUID
        col.set("SeriesInstanceUID", generate_uid())
        col.set("StudyInstanceUID", generate_uid())

        # walk through the collection and update SOP_Instance_UID
        # for each dicom file. Use fw-file tools to generate UID

        for index in range(0, len(col)):
            col[index].SOPInstanceUID = generate_uid()

        # create output file path:
        output_file_name = set_output_filename(file_path, output_file_prefix)
        output_file_path = f"{context.output_dir}/{output_file_name}"

        log.info("The input file path is %s", file_path)
        log.info("The output path is %s", output_file_path)

        col.to_zip(output_file_path)

    else:
        log.info(f"No completed tasks found for this file ({file_id}).")

    return 0
