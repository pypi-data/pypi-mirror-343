import os
import re
import json
import logging
import sys
import uuid

import tornado
import tornado.web
from jupyter_server.base.handlers import APIHandler

from pydantic import BaseModel, Field
from typing import List

# Configuring the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler for the standard output (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Log formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


class Summary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    podName: str
    usage: float
    cost: float
    project: str


class SummaryList(BaseModel):
    summaries: List[Summary]


class Detail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    podName: str
    creationTimestamp: str
    deletionTimestamp: str
    cpuLimit: str
    memoryLimit: str
    gpuLimit: str
    volumes: str
    namespace: str
    notebook_duration: str
    session_cost: float
    instance_id: str
    instance_type: str
    region: str
    pricing_type: str
    cost: float
    instanceRAM: int
    instanceCPU: int
    instanceGPU: int
    instanceId: str


class DetailList(BaseModel):
    details: List[Detail]


class LogsHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        logger.info("Getting usages and cost stats")
        try:
            # Verificar que las variables de entorno necesarias están definidas
            required_env_vars = ["OSS_LOG_FILE_PATH", "OSSPI", "OSSPRoject"]
            for var in required_env_vars:
                if var not in os.environ:
                    raise EnvironmentError(
                        f"Missing required environment variable: {var}"
                    )

            local_path = os.environ["OSS_LOG_FILE_PATH"]
            osspi = os.environ.get("OSSPI", "No")
            oss_project = os.environ.get("OSSPRoject", "").strip()

            full_url = self.request.full_url()
            # full_url = "http://localhost:63118/user/yovian/jupyterlab-resource-tracker"
            match = re.search("(\/user\/)(.*)(\/jupyterlab-resource-tracker)", full_url)
            username = match.group(2)

            if not os.path.isfile(local_path):
                raise FileNotFoundError(f"Log file not found: {local_path}")
            logs = self.load_log_file(local_path, osspi, oss_project, username)
            summary_list = SummaryList(summaries=logs)

        except FileNotFoundError as e:
            logger.error("Log file not found: %s", e)
            self.set_status(404)
            self.finish(json.dumps({"error": "Required log file not found."}))
        except EnvironmentError as e:
            logger.error("Environment configuration error: %s", e)
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format in log file: %s", e)
            self.set_status(400)
            self.finish(json.dumps({"error": "Invalid log file format."}))

        self.set_status(200)
        self.finish(
            json.dumps(
                {
                    "summary": [s.model_dump() for s in summary_list.summaries],
                    "details": [],
                }
            )
        )

    def load_log_file(
        self, file_path: str, osspi: str, oss_project: str, username: str
    ) -> list:
        """
        Reads a .log file in JSON Lines format and returns a list of objects.
        Always filters by project == oss_project.
        If OSSPI == "Yes", returns all records for that project.
        If OSSPI == "No", returns only those with podName == jupyterlab-{username}.
        """
        logger.info("User: %s", username)
        logger.info("OSSPI: %s", osspi)
        logger.info("OSSProject: %s", oss_project)
        logger.info("Log file path: %s", file_path)
        data = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON format: %s", line)
                        continue  # skip malformed line

                    if record.get("project") != oss_project:
                        continue

                    if osspi == "yes":
                        data.append(record)
                    elif osspi == "no":
                        expected_podname = f"jupyter-{username}"
                        if record.get("podName") == expected_podname:
                            data.append(record)

        except Exception as e:
            logger.error("Failed to read %s: %s", file_path, e)
            raise FileNotFoundError(f"Could not read log file at {file_path}.") from e

        return data
