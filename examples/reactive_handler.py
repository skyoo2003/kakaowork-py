from http.server import HTTPServer, BaseHTTPRequestHandler

from kakaowork import (
    Kakaowork,
    SubmitActionReactiveBody,
    BaseReactiveActionHandler,
)


class ReactiveActionHandler(BaseReactiveActionHandler):
    def __init__(self, client):
        self.client = client

    def handle_submit(self, body: SubmitActionReactiveBody) -> bool:
        if body.action_name == 'confirm':
            self.client.messages.send(
                conversation_id=body.message.conversation_id,
                text='Thanks for your response',
            )
            return True
        elif body.action_name == "cancel":
            self.client.messages.send(
                conversation_id=body.message.conversation_id,
                text='See you later',
            )
        return False


handler = ReactiveActionHandler(Kakaowork(app_key='<your_app_key>'))


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')

        try:
            body = SubmitActionReactiveBody.parse_raw(body)
        except Exception as e:
            print(str(e))
            self.send_response(400)
            return

        if not handler.handle_submit(body):
            self.send_response(400)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write('{}'.encode('utf-8'))


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), HTTPRequestHandler)
    server.serve_forever()
