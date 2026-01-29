"""
WSGI Entry Point for Production Deployment
"""
from app import create_app

app = create_app()
socketio = app.socketio if hasattr(app, 'socketio') else None

if __name__ == '__main__':
    if socketio:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)

