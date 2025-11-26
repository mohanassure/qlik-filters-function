import os
import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Qlik filters POST received.')

    try:
        filters = req.get_json()
        logging.info(f"Filters received: {filters}")

        # Write to temp directory
        temp_path = os.path.join(os.getenv("TMP", "/tmp"), "latest_filters.json")
        with open(temp_path, "w") as f:
            json.dump(filters, f)
        logging.info(f"Filters saved to {temp_path}")

        return func.HttpResponse(
            json.dumps({"status": "success", "received_filters": filters}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error processing filters: {e}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
