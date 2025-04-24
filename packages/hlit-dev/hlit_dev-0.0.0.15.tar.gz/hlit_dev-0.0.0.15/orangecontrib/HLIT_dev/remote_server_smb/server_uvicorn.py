import uvicorn
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import socket

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.HLIT_dev.remote_server_smb import convert, hlit_workflow_management
    from Orange.widgets.orangecontrib.AAIT.utils import MetManagement
else:
    from orangecontrib.HLIT_dev.remote_server_smb import convert, hlit_workflow_management
    from orangecontrib.AAIT.utils import MetManagement

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" par une liste de domaines autorisés si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_if_uvicorn_is_running():
    port = 8000
    # Verification of port
    if est_port_occupe(port):
        print(f"Le port {port} est déjà utilisé par un autre workflow.")
        return
    else:
        # Start server
        lauch_uvicorn()

def est_port_occupe(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0  # Retourne True si le port est occupé

def lauch_uvicorn():
    chemin_dossier =MetManagement.get_api_local_folder()
    if os.path.exists(chemin_dossier):
        MetManagement.reset_folder(chemin_dossier, recreate=False)
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get("/chat")
def chat():
    chemin_dossier = MetManagement.get_api_local_folder()
    return StreamingResponse(hlit_workflow_management.stream_tokens_from_file(chemin_dossier), media_type="text/event-stream")


@app.get("/read-config-file-ows-html")
def read_config_file_ows_html():
    list_config_html_ows=[]
    if 0!= hlit_workflow_management.read_config_ows_html_file_as_dict(list_config_html_ows):
        return JSONResponse(
            status_code=404,
            content={"message": f"Error occurs"}
        )
    return {"message" : list_config_html_ows}

@app.get("/open-local-html/{key_name}")
def open_local_html(key_name):
    list_config_html_ows = []
    if 0!= hlit_workflow_management.read_config_ows_html_file_as_dict(list_config_html_ows):
        return JSONResponse(
            status_code=404,
            content={"message": f"Error occurs"}
        )
    if 0!= hlit_workflow_management.open_local_html(list_config_html_ows, key_name):
        return JSONResponse(
            status_code=404,
            content={"message": f"Error occurs to open local html"}
        )
    return {"message" : "Open local html ok"}

@app.get("/start-workflow/{key_name}")
def start_workflow(key_name):
    list_config_html_ows = []
    if 0!= hlit_workflow_management.read_config_ows_html_file_as_dict(list_config_html_ows):
        return JSONResponse(
            status_code=404,
            content={"message": f"Error occurs to get json aait store file"}
        )
    res= hlit_workflow_management.start_workflow(list_config_html_ows, key_name)
    if res==1:
        return JSONResponse(
            status_code=404,
            content={"message": f"Error occurs to start workflow"}
        )
    if res == 2:
        return JSONResponse(
            status_code=404,
            content={"message": f"workflow is already running"}
        )
    return {"_message" : "Start workflow ok", "_statut": "Started", "_result": None}



@app.get("/reset-data-folder-workflow")
def reset_data_folder_workflow():
    chemin_dossier = MetManagement.get_api_local_folder()
    if os.path.exists(chemin_dossier):
        MetManagement.reset_folder(chemin_dossier, recreate=False)
        return {"message": "Reset data folder workflow ok"}
    else:
        return {"message": "Error no folder found"}



@app.get("/output-workflow")
def read_root():
    chemin_dossier = MetManagement.get_api_local_folder()
    if not os.path.exists(chemin_dossier):
        return JSONResponse(
            status_code=404,
            content={"_message": f"Error no folder found"}
        )
    ## on check si le timeout est défini et s'il est atteint
    if 0 != hlit_workflow_management.check_if_timout_is_reached(chemin_dossier):
        return JSONResponse(
            status_code=404,
            content={"_message": f"Timeout has been reached.", "_statut":"Timeout",
                     "_result": None}
        )
    if not os.path.exists(chemin_dossier + ".output_ok") and not os.path.exists(chemin_dossier + "output.json"):
        if os.path.exists(chemin_dossier + ".statut_ok"):
            with open(chemin_dossier + "statut.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return JSONResponse(
                    status_code=200,
                    content={"_message": f"Your data are still being processed.", "_statut": data["value"], "_result": None}
                )
        else:
            return JSONResponse(
                status_code=200,
                content={"_message": f"Your data are still being processed.", "_statut": None, "_result": None}
            )
    if not os.path.exists(chemin_dossier + ".output_ok"):
        with open(chemin_dossier + "output.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        MetManagement.reset_folder(chemin_dossier, recreate=False)
        return JSONResponse(
                    status_code=200,
                    content={"_message": f"Your workflow is finished.", "_statut": "Finished", "_result": data}
                )


@app.post("/input-workflow")
def receive_data(input_data: dict):
    chemin_dossier = MetManagement.get_api_local_folder()
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)
    else:
        print(f"Dossier '{chemin_dossier}' existe déjà.")
        return JSONResponse(
            status_code=404,
            content={"_message": f"The workflow is already running"}
        )
    data_config = []
    if input_data["data"] is not None and input_data["workflow_id"] is not None:
        for key, data in enumerate(input_data["data"]):
            table = convert.convert_json_to_orange_data_table(data)
            if table == 1:
                MetManagement.reset_folder(chemin_dossier, recreate=False)
                return JSONResponse(
                    status_code=404,
                    content={"_message": f"The input data table is not a dict"}
                )

            if table is None or table == []:
                MetManagement.reset_folder(chemin_dossier, recreate=False)
                return JSONResponse(
                    status_code=404,
                    content={"_message": f"The input data table is empty"}
                )
            table.save(chemin_dossier + "input_data_" + str(data["num_input"]) + ".tab")
            data_config.append({"num_input": data["num_input"], "path": "input_data_" + str(data["num_input"]) + ".tab"})
    else:
        return JSONResponse(
            status_code=404,
            content={"_message": f"The input data is not at good format"}
        )
    with open(chemin_dossier + "config.json", "w") as fichier:
        json.dump({"workflow_id": input_data["workflow_id"], "data_config": data_config}, fichier, indent=4)
    with open(chemin_dossier + ".ok", "w") as fichier:
        pass
    MetManagement.write_file_time(chemin_dossier+"time.txt")
    return {"_message" : "the input file has been created", "_statut": "Started", "_result": None}

if __name__ == "__main__":
    lauch_uvicorn()

