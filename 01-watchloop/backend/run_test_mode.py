"""
Test Mode Startup - Run with faster check intervals for testing
"""
import os
from app import app

if __name__ == '__main__':
    # Set test interval (10 seconds instead of 60)
    os.environ['WATCHLOOP_CHECK_INTERVAL'] = '10'

    print("\n" + "="*60)
    print("  WatchLoop Backend Server (TEST MODE)")
    print("="*60)
    print("  Starting Flask server on http://localhost:5000")
    print("  Check interval: 10 seconds (TEST MODE - faster verification)")
    print("  Production default is 60 seconds")
    print("  API endpoints available:")
    print("    GET  /api/status       - Get current status")
    print("    POST /api/start-task   - Start a task")
    print("    POST /api/stop-watcher - Stop watcher")
    print("    POST /api/cancel-task  - Cancel task")
    print("    POST /api/reset        - Reset state")
    print("    GET  /api/health       - Health check")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
