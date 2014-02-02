#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
import socket

PORT = 8899
HOSTNAME = socket.gethostname()

html = r"""<!doctype html>
<html>
    <head>
        <title>WebSocket Log Viewer</title>
        <style type="text/css">
        body {
            margin: 20px;
        }
        pre {
           width: 95%%;
           padding: 5px;
           border-width: 1px;
           border-style: solid;
           font-size: %(fontsize)spx;
           overflow: auto;
           white-space: pre-wrap;
        }
        </style>
    </head>
    <body>
<h1>WebSocket Log Viewer</h1>
<div>
    <pre id="contents" class="%(maxlength)s">
    </pre>
</div>

<script type="text/javascript">

function init() {
    var p = document.getElementById("contents");
    var len = parseInt(p.classList[0]);
    var logs = new Array();

    var ws = new WebSocket("ws://%(hostname)s:%(port)s/ws");
    ws.onopen = function() {};
    ws.onmessage = function (evt) {
        logs.push(evt.data);
        if (logs.length > len) {
            logs.shift();
        }
        p.innerHTML = logs.join("\n");
    };
}

document.addEventListener('DOMContentLoaded', function () {
    init();
});

</script>
</body>

</html>
"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        fontsize = self.get_argument("size", "15")
        size = 15
        if fontsize.isdigit():
            size = int(fontsize)
        maxlength = self.get_argument("length", "100")
        length = 100
        if maxlength.isdigit():
            length = int(maxlength)
        self.write(html % {"fontsize": size, "maxlength": length,
                           "hostname": HOSTNAME, "port": PORT})


clients = []

class LogWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)

    def on_message(self, message):
        for client in clients:
            client.write_message(message)

    def on_close(self):
        clients.remove(self)


if __name__ == "__main__":
    application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ws", LogWebSocketHandler),
            ])
    application.listen(PORT)
    print "open http://%s:%d/" % (HOSTNAME, PORT)
    tornado.ioloop.IOLoop.instance().start()

