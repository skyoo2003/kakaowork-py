Reactive Handler
================

This is how to implement handlers for the KakaoWork user reactions.

Reactive action handlers are implemented below. Reactive modal handlers are also implemented similarly.

.. code-block:: python3

   # handler.py
   from kakaowork.reactive import BaseReactiveActionHandler
   from kakaowork.models import SubmitActionReactiveBody
   from kakaowork.client import Kakaowork


   class MyReactiveActionHandler(BaseReactiveActionHandler):
      def __init__(self, client: Kakaowork) -> None:
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

   # server.py
   from flask import Flask, request, abort
   from kakaowork.client import Kakaowork
   from kakaowork.models import SubmitActionReactiveBody
   from myhandler import MyReactiveActionHandler

   app = Flask(__name__)
   client = Kakaowork(app_key='my_app_key')
   handler = MyReactiveActionHandler(client)


   @app.route("/callback")
   def callback():
      body = SubmitActionReactiveBody.from_json(request.data)
      ok = handler.handle_submit(body)
      if not ok:
         abort(400)
      return 'OK'
