import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Qlik filters request received.')

    try:
        if req.method == "POST":
            # Get filters from Qlik
            filters = req.get_json()
            logging.info(f"Filters received: {filters}")

            # Return filters immediately
            return func.HttpResponse(
                json.dumps({"status": "success", "filters": filters}),
                status_code=200,
                mimetype="application/json"
            )

        else:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Only POST allowed"}),
                status_code=405,
                mimetype="application/json"
            )

    except Exception as e:
        logging.error(f"Error processing filters: {e}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
