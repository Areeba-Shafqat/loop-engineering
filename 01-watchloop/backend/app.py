"""
Flask API Server - Provides endpoints for the WatchLoop frontend
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

from state_manager import load_state, reset_state, add_event
from task_runner import task_runner
from watcher import watch_loop

app = Flask(__name__)

# Configure CORS for both development and production
cors_origins = [
    "http://localhost:5173",  # Local Vite dev server
    "http://localhost:4173",  # Local Vite preview
    "https://frontend-fawn-six-17.vercel.app",  # Production frontend
]

# Add production origins from environment variable if provided
if os.environ.get('FRONTEND_URL'):
    cors_origins.append(os.environ.get('FRONTEND_URL'))

# Use regex pattern to allow all Vercel deployments
CORS(app, origins=cors_origins, supports_credentials=False,
     origin_regex=r"https://.*\.vercel\.app")


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current task and watcher status"""
    try:
        state = load_state()
        return jsonify({
            "success": True,
            "data": state
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/start-task', methods=['POST'])
def start_task():
    """Start a new long-running task"""
    try:
        data = request.get_json() or {}
        duration = data.get('duration', 180)  # Default 3 minutes

        # Validate duration
        if not isinstance(duration, (int, float)) or duration <= 0:
            return jsonify({
                "success": False,
                "error": "Duration must be a positive number"
            }), 400

        if duration > 3600:
            return jsonify({
                "success": False,
                "error": "Duration cannot exceed 3600 seconds (1 hour)"
            }), 400

        # Start the task
        success, message = task_runner.start_task(int(duration))

        if not success:
            return jsonify({
                "success": False,
                "error": message
            }), 400

        # Automatically start the watcher
        watch_success, watch_message = watch_loop.start()

        return jsonify({
            "success": True,
            "message": message,
            "watcher_started": watch_success
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/stop-watcher', methods=['POST'])
def stop_watcher():
    """Manually stop the watcher loop"""
    try:
        success, message = watch_loop.stop()

        if not success:
            return jsonify({
                "success": False,
                "error": message
            }), 400

        return jsonify({
            "success": True,
            "message": message
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/cancel-task', methods=['POST'])
def cancel_task():
    """Cancel the running task"""
    try:
        success, message = task_runner.cancel_task()

        if not success:
            return jsonify({
                "success": False,
                "error": message
            }), 400

        add_event("task_cancel_requested", "User requested task cancellation")

        return jsonify({
            "success": True,
            "message": message
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset all state to initial"""
    try:
        # Stop watcher if running
        if watch_loop.is_running:
            watch_loop.stop()

        # Cancel task if running
        task_runner.cancel_task()

        # Reset state
        state = reset_state()

        add_event("system_reset", "System reset to initial state")

        return jsonify({
            "success": True,
            "message": "System reset successfully",
            "data": state
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  WatchLoop Backend Server")
    print("="*60)
    print("  Starting Flask server on http://localhost:5000")
    print("  API endpoints available:")
    print("    GET  /api/status       - Get current status")
    print("    POST /api/start-task   - Start a task")
    print("    POST /api/stop-watcher - Stop watcher")
    print("    POST /api/cancel-task  - Cancel task")
    print("    POST /api/reset        - Reset state")
    print("    GET  /api/health       - Health check")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
