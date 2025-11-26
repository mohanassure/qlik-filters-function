import os
import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Qlik filters request received.')

    temp_path = os.path.join(os.getenv("TMP", "/tmp"), "latest_filters.json")

    try:
        if req.method == "POST":
            # Save filters sent from Qlik
            filters = req.get_json()
            logging.info(f"Filters received: {filters}")
            with open(temp_path, "w") as f:
                json.dump(filters, f)
            logging.info(f"Filters saved to {temp_path}")
            return func.HttpResponse(
                json.dumps({"status": "success", "received_filters": filters}),
                status_code=200,
                mimetype="application/json"
            )
        elif req.method == "GET":
            # Return last saved filters
            if os.path.exists(temp_path):
                with open(temp_path, "r") as f:
                    filters = json.load(f)
                return func.HttpResponse(
                    json.dumps({"status": "success", "filters": filters}),
                    status_code=200,
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({"status": "success", "filters": []}),
                    status_code=200,
                    mimetype="application/json"
                )
        else:
            return func.HttpResponse("Method not allowed", status_code=405)
    except Exception as e:
        logging.error(f"Error processing filters: {e}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
