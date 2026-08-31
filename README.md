# Loop Engineering - 12 Portfolio Projects

A collection of 12 advanced engineering projects demonstrating various loop patterns, monitoring systems, and autonomous agent behaviors.

## 📁 Repository Structure

```
loop-engineering/
├── 01-watchloop/          ✅ COMPLETE - In-Session Agent Loop Monitor
├── 02-testloop/           ✅ COMPLETE - Conditional Loop with Maker-Checker
├── 03-project-name/       📝 Coming soon
├── 04-project-name/       📝 Coming soon
├── 05-project-name/       📝 Coming soon
├── 06-project-name/       📝 Coming soon
├── 07-project-name/       📝 Coming soon
├── 08-project-name/       📝 Coming soon
├── 09-project-name/       📝 Coming soon
├── 10-project-name/       📝 Coming soon
├── 11-project-name/       📝 Coming soon
└── 12-project-name/       📝 Coming soon
```

---

## 🎯 Project 01: WatchLoop ✅

**Status**: ✅ Complete & Deployed  
**Tech Stack**: Python (Flask) + React + Vite + Tailwind CSS

### 🌐 Live Demo
- **Frontend**: https://frontend-fawn-six-17.vercel.app
- **Backend API**: https://loop-engineering-production-36ef.up.railway.app

### Overview
An in-session agent loop monitoring system that autonomously watches long-running tasks, checks status every 60 seconds, detects completion, and reports exactly once - similar in concept to Claude's `/loop` command.

### Key Features
- Autonomous task monitoring with periodic checks
- Single completion notification guarantee
- Real-time dashboard with countdown timers
- Thread-safe concurrent operations
- Clean lifecycle management (start/stop/reset)
- Comprehensive testing (13/13 acceptance criteria passed)

[📖 Full Documentation →](./01-watchloop/README.md)

---

## 🎯 Project 02: TestLoop ✅

**Status**: ✅ Complete  
**Tech Stack**: Python + pytest

### Overview
A demonstration of Concept 5 (Conditional Loop - run-until-done) and Concept 11 (Maker-Checker Separation). Shows how an AI worker iteratively fixes code until an independent test runner verifies completion.

### Key Features
- Conditional loop that runs until tests pass
- Maker-checker separation (worker fixes, pytest verifies)
- Maximum 6 attempts with clear stopping conditions
- Transparent test output for verification
- Immutable test suite as acceptance criteria

### Core Concepts
- **Concept 5**: Loop continues while condition is false, stops when true
- **Concept 11**: Worker cannot approve own work - independent checker required

[📖 Full Documentation →](./02-testloop/README.md)

---

## 🎯 Project 04: FixLoop ✅

**Status**: ✅ Complete  
**Tech Stack**: Python + pytest + Git branches

### Overview
A maker-checker bug fix workflow demonstrating branch isolation, reusable skills, and independent review. An implementer fixes bugs in isolation, and a separate reviewer must approve before a PR can be opened.

### Key Features
- Isolated branch-based bug fixing workflow
- Reusable fix-bug skill procedure
- Independent code review with PASS/FAIL verdicts
- PR gate enforcement (only open after PASS)
- Two-scenario demonstration (good fix + bad fix)
- Real bugs with regression tests

### Core Concepts
- **Concept 8**: Branch/worktree isolation for safe development
- **Concept 9**: Reusable skills for consistent procedures
- **Concept 11**: Maker-checker separation (no self-approval)

### Demonstration Results
- ✅ Good fix: Both bugs fixed → Reviewer PASS → PR opened
- ❌ Bad fix: Incomplete (1 bug unfixed) → Reviewer FAIL → No PR

[📖 Full Documentation →](./04-fixloop/README.md)

---

## 🚀 Coming Soon

Projects 05-12 will be added progressively, each demonstrating different engineering concepts and patterns.

**Potential Project Ideas:**
- ScheduleLoop - Cron-like task scheduler
- RetryLoop - Automatic retry mechanism
- PollLoop - API polling system
- WorkerLoop - Background job queue
- CircuitBreaker - Circuit breaker pattern
- EventLoop - Event-driven architecture
- RateLimiter - Rate limiting service
- HealthCheckLoop - Service monitoring
- DataSyncLoop - Data synchronization
- BatchProcessor - Batch job processing
- MetricsCollector - System metrics collection

[📋 View Project Planning →](./PROJECT_PLANNING.md)

---

## 📊 Progress

- **Completed**: 4/12 projects
- **In Progress**: 0/12 projects
- **Planned**: 8/12 projects

---

## 🎓 About This Collection

This repository showcases advanced software engineering skills including:
- Full-stack development (Python, JavaScript, React)
- Concurrent programming and threading
- System design and architecture
- API design and implementation
- Modern UI/UX development
- Comprehensive testing strategies
- Professional documentation
- Production deployment (Vercel + Railway)

---

## 📝 License

Each project may have its own license. See individual project folders for details.

---

## 👤 Author

**Areeba Shafqat**  
GitHub: [@Areeba-Shafqat](https://github.com/Areeba-Shafqat)

---

**Last Updated**: 2026-08-30
