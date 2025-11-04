import azure.functions as func
import logging

app = func.FunctionApp()

# Event Hub Trigger: Event Hub에서 메시지를 읽어오는 함수
@app.event_hub_message_trigger(
    arg_name="azeventhub",
    event_hub_name="test-hub",
    connection="dt2014eventhub_RootManageSharedAccessKey_EVENTHUB"
)
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info(
        'Python EventHub trigger processed an event: %s',
        azeventhub.get_body().decode('utf-8')
    )

# Event Hub Output: HTTP 요청을 받아 Event Hub로 메시지를 보내는 함수
@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
@app.event_hub_output(
    arg_name="event",
    event_hub_name="test-hub",
    connection="dt2014eventhub_RootManageSharedAccessKey_EVENTHUB"
)
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    req_body = req.get_body().decode('utf-8')

    logging.info("HTTP trigger function received a request: %s", req_body)

    # 👇 Event Hub로 메시지 전송
    event.set(req_body)

    return func.HttpResponse(
        "Event Hub output function executed successfully.",
        status_code=200
    )
