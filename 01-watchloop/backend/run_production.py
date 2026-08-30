"""
Production startup script - Run without debug mode for proper watcher operation
"""
import os
from app import app

if __name__ == '__main__':
    # Get port from environment variable (for Railway, Render, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))

    print("\n" + "="*60)
    print("  WatchLoop Backend Server (PRODUCTION MODE)")
    print("="*60)
    print(f"  Starting Flask server on port {port}")
    print("  Debug mode: OFF (for proper watcher thread operation)")
    print("  API endpoints available:")
    print("    GET  /api/status       - Get current status")
    print("    POST /api/start-task   - Start a task")
    print("    POST /api/stop-watcher - Stop watcher")
    print("    POST /api/cancel-task  - Cancel task")
    print("    POST /api/reset        - Reset state")
    print("    GET  /api/health       - Health check")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
