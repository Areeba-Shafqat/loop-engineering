import { useState, useEffect, useRef } from 'react'

const API_BASE = 'http://localhost:5000/api'

function App() {
  const [state, setState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [taskDuration, setTaskDuration] = useState(180)
  const [nextCheckIn, setNextCheckIn] = useState(null)
  const [actionLoading, setActionLoading] = useState(false)

  const pollIntervalRef = useRef(null)
  const countdownIntervalRef = useRef(null)

  // Fetch status from backend
  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/status`)
      const result = await response.json()

      if (result.success) {
        setState(result.data)
        setError(null)
      } else {
        setError(result.error || 'Failed to fetch status')
      }
    } catch (err) {
      setError('Cannot connect to backend. Is the server running?')
    } finally {
      setLoading(false)
    }
  }

  // Start polling on mount
  useEffect(() => {
    fetchStatus()

    // Poll every 2 seconds for UI updates
    pollIntervalRef.current = setInterval(fetchStatus, 2000)

    return () => {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current)
      if (countdownIntervalRef.current) clearInterval(countdownIntervalRef.current)
    }
  }, [])

  // Calculate countdown to next check
  useEffect(() => {
    if (!state?.watcher?.last_check_time || state?.watcher?.status !== 'active') {
      setNextCheckIn(null)
      return
    }

    const calculateCountdown = () => {
      const lastCheck = new Date(state.watcher.last_check_time)
      const now = new Date()
      const elapsed = Math.floor((now - lastCheck) / 1000)
      const remaining = Math.max(0, 60 - elapsed)

      setNextCheckIn(remaining)
    }

    calculateCountdown()
    countdownIntervalRef.current = setInterval(calculateCountdown, 1000)

    return () => {
      if (countdownIntervalRef.current) clearInterval(countdownIntervalRef.current)
    }
  }, [state?.watcher?.last_check_time, state?.watcher?.status])

  // API Actions
  const startTask = async () => {
    setActionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/start-task`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration: taskDuration })
      })
      const result = await response.json()

      if (!result.success) {
        setError(result.error)
      } else {
        await fetchStatus()
      }
    } catch (err) {
      setError('Failed to start task')
    } finally {
      setActionLoading(false)
    }
  }

  const stopWatcher = async () => {
    setActionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/stop-watcher`, {
        method: 'POST'
      })
      const result = await response.json()

      if (!result.success) {
        setError(result.error)
      } else {
        await fetchStatus()
      }
    } catch (err) {
      setError('Failed to stop watcher')
    } finally {
      setActionLoading(false)
    }
  }

  const resetSystem = async () => {
    setActionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/reset`, {
        method: 'POST'
      })
      const result = await response.json()

      if (!result.success) {
        setError(result.error)
      } else {
        await fetchStatus()
      }
    } catch (err) {
      setError('Failed to reset system')
    } finally {
      setActionLoading(false)
    }
  }

  const cancelTask = async () => {
    setActionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/cancel-task`, {
        method: 'POST'
      })
      const result = await response.json()

      if (!result.success) {
        setError(result.error)
      } else {
        await fetchStatus()
      }
    } catch (err) {
      setError('Failed to cancel task')
    } finally {
      setActionLoading(false)
    }
  }

  // Format timestamp
  const formatTime = (isoString) => {
    if (!isoString) return 'N/A'
    const date = new Date(isoString)
    return date.toLocaleTimeString()
  }

  // Format duration
  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A'
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}m ${secs}s`
  }

  // Status badge component
  const StatusBadge = ({ status, type }) => {
    const colors = {
      task: {
        idle: 'bg-gray-600',
        running: 'bg-blue-500 animate-pulse',
        finished: 'bg-green-500',
        failed: 'bg-red-500',
        cancelled: 'bg-yellow-500'
      },
      watcher: {
        stopped: 'bg-gray-600',
        active: 'bg-purple-500 animate-pulse'
      }
    }

    const color = colors[type]?.[status] || 'bg-gray-500'

    return (
      <span className={`${color} text-white px-3 py-1 rounded-full text-sm font-semibold uppercase tracking-wide`}>
        {status}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  const taskStatus = state?.task?.status || 'idle'
  const watcherStatus = state?.watcher?.status || 'stopped'
  const canStartTask = taskStatus === 'idle' || taskStatus === 'finished' || taskStatus === 'failed' || taskStatus === 'cancelled'
  const canStopWatcher = watcherStatus === 'active'
  const canCancelTask = taskStatus === 'running'

  // Check for completion event
  const hasCompletionEvent = state?.events?.some(e => e.type === 'completion_detected')

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
            WatchLoop
          </h1>
          <p className="text-slate-400">Agent Loop Monitoring System</p>
        </header>

        {/* Error Alert */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Task Status Card */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">📋</span>
              Task Status
            </h2>

            <div className="space-y-3">
              <div>
                <div className="text-slate-400 text-sm mb-1">Status</div>
                <StatusBadge status={taskStatus} type="task" />
              </div>

              {state?.task?.start_time && (
                <div>
                  <div className="text-slate-400 text-sm">Start Time</div>
                  <div className="text-lg font-mono">{formatTime(state.task.start_time)}</div>
                </div>
              )}

              {state?.task?.completion_time && (
                <div>
                  <div className="text-slate-400 text-sm">Completion Time</div>
                  <div className="text-lg font-mono">{formatTime(state.task.completion_time)}</div>
                </div>
              )}

              {state?.task?.duration && (
                <div>
                  <div className="text-slate-400 text-sm">Duration</div>
                  <div className="text-lg font-mono">{formatDuration(state.task.duration)}</div>
                </div>
              )}

              {state?.task?.error && (
                <div>
                  <div className="text-red-400 text-sm">Error</div>
                  <div className="text-sm">{state.task.error}</div>
                </div>
              )}
            </div>
          </div>

          {/* Watcher Status Card */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">👁️</span>
              WatchLoop Status
            </h2>

            <div className="space-y-3">
              <div>
                <div className="text-slate-400 text-sm mb-1">Status</div>
                <StatusBadge status={watcherStatus} type="watcher" />
              </div>

              <div>
                <div className="text-slate-400 text-sm">Check Count</div>
                <div className="text-3xl font-bold text-purple-400">{state?.watcher?.check_count || 0}</div>
              </div>

              {state?.watcher?.last_check_time && (
                <div>
                  <div className="text-slate-400 text-sm">Last Check</div>
                  <div className="text-lg font-mono">{formatTime(state.watcher.last_check_time)}</div>
                </div>
              )}

              {nextCheckIn !== null && watcherStatus === 'active' && (
                <div>
                  <div className="text-slate-400 text-sm">Next Check In</div>
                  <div className="text-2xl font-bold text-blue-400">{nextCheckIn}s</div>
                </div>
              )}
            </div>
          </div>

          {/* Control Panel Card */}
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">🎮</span>
              Control Panel
            </h2>

            <div className="space-y-4">
              <div>
                <label className="text-slate-400 text-sm block mb-2">Task Duration (seconds)</label>
                <input
                  type="number"
                  value={taskDuration}
                  onChange={(e) => setTaskDuration(Number(e.target.value))}
                  disabled={!canStartTask || actionLoading}
                  className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white disabled:opacity-50"
                  min="10"
                  max="3600"
                />
              </div>

              <button
                onClick={startTask}
                disabled={!canStartTask || actionLoading}
                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition"
              >
                {actionLoading ? 'Starting...' : '▶ Start Task'}
              </button>

              <button
                onClick={cancelTask}
                disabled={!canCancelTask || actionLoading}
                className="w-full bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition"
              >
                ⊗ Cancel Task
              </button>

              <button
                onClick={stopWatcher}
                disabled={!canStopWatcher || actionLoading}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition"
              >
                ⏸ Stop Watcher
              </button>

              <button
                onClick={resetSystem}
                disabled={actionLoading}
                className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition"
              >
                🔄 Reset System
              </button>
            </div>
          </div>
        </div>

        {/* Completion Notification Banner */}
        {hasCompletionEvent && (
          <div className="bg-gradient-to-r from-green-600 to-emerald-600 border-2 border-green-400 rounded-lg p-6 mb-6 shadow-lg">
            <div className="flex items-center gap-3">
              <span className="text-4xl">✓</span>
              <div>
                <h3 className="text-2xl font-bold">Task Completed!</h3>
                <p className="text-green-100">WatchLoop detected task completion and stopped monitoring.</p>
              </div>
            </div>
          </div>
        )}

        {/* Activity Log */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <span className="text-2xl">📜</span>
            Activity Log
          </h2>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {state?.events && state.events.length > 0 ? (
              [...state.events].reverse().map((event, idx) => (
                <div
                  key={idx}
                  className="bg-slate-700/50 rounded px-4 py-3 border border-slate-600 hover:border-slate-500 transition"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold mr-2 ${
                        event.type === 'completion_detected' ? 'bg-green-600' :
                        event.type === 'task_started' ? 'bg-blue-600' :
                        event.type === 'task_failed' ? 'bg-red-600' :
                        event.type === 'watcher_started' ? 'bg-purple-600' :
                        'bg-slate-600'
                      }`}>
                        {event.type}
                      </span>
                      <span className="text-slate-200">{event.message}</span>
                    </div>
                    <div className="text-slate-400 text-sm font-mono whitespace-nowrap">
                      {formatTime(event.timestamp)}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-slate-500 text-center py-8">No events yet</div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-slate-500 text-sm">
          <p>WatchLoop - Demonstrating agent loop patterns for autonomous task monitoring</p>
        </footer>
      </div>
    </div>
  )
}

export default App
