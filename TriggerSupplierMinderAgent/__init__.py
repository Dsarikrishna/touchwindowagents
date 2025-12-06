import logging
import json
import azure.functions as func
from shared.agents import run_supplier_minder_agent


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('TriggerSupplierMinderAgent HTTP trigger function processed a request.')
    
    try:
        result = run_supplier_minder_agent()
        return func.HttpResponse(
            body=json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error running SupplierMinderAgent: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"status": "error", "error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
