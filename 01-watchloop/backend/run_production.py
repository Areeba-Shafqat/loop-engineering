"""
Production startup script - Run without debug mode for proper watcher operation
"""
from app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  WatchLoop Backend Server (PRODUCTION MODE)")
    print("="*60)
    print("  Starting Flask server on http://localhost:5000")
    print("  Debug mode: OFF (for proper watcher thread operation)")
    print("  API endpoints available:")
    print("    GET  /api/status       - Get current status")
    print("    POST /api/start-task   - Start a task")
    print("    POST /api/stop-watcher - Stop watcher")
    print("    POST /api/cancel-task  - Cancel task")
    print("    POST /api/reset        - Reset state")
    print("    GET  /api/health       - Health check")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
