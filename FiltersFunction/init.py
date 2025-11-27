import logging
import azure.functions as func
import json

# --------- MEMORY STORAGE FOR FILTERS ----------
LAST_FILTERS = []

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function invoked")

    global LAST_FILTERS

    try:
        if req.method == "POST":
            # Try reading body
            try:
                body = req.get_json()
            except:
                body = None

            logging.info(f"Incoming body: {body}")

            # If Qlik extension sent filters (list)
            if isinstance(body, list):
                LAST_FILTERS = body
                logging.info(f"Updated LAST_FILTERS = {LAST_FILTERS}")

                return func.HttpResponse(
                    json.dumps({"status": "updated", "filters": LAST_FILTERS}),
                    status_code=200,
                    mimetype="application/json",
                )

            # If chatbot calls without filters → return stored filters
            logging.info("Chatbot requested filters — returning LAST_FILTERS")
            return func.HttpResponse(
                json.dumps({"status": "success", "filters": LAST_FILTERS}),
                status_code=200,
                mimetype="application/json",
            )

        else:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Only POST allowed"}),
                status_code=405,
                mimetype="application/json",
            )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=400,
            mimetype="application/json",
        )
