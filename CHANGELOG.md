# Changelog

All notable changes to Smriti will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.5.0] - 2026-03-14

### Added
- **Production-ready Cognitive OS** with 5 integrated systems
- **Quality Engine** with 5 meta-metrics (M1-M5)
  - M1: Predictive Surprise
  - M2: Denkraum-Expansion
  - M3: Paradigmen-Shift
  - M4: Session Velocity
  - M5: Anti-Fragile Resonanz
- **Pattern Engine (Reflecty)** with L1-L3 intelligence
  - L1: Pattern Detection
  - L2: Cross-Domain Analogies
  - L3: 7-Day Predictions
- **Improvement Engine (OUROBOROS)** with actual mutations
  - Type A: Parameter tuning (auto)
  - Type B: Structural changes (approval)
  - Type C: Architectural changes (manual)
  - Automatic backup before mutations
  - Rollback support
- **BRIDGE** for real-time event routing
  - File locking for race conditions
  - Schema validation
  - Conflict detection
  - Health monitoring
- **Memory Infrastructure** with 4 layers
  - L1: Context window
  - L2: File system (always works)
  - L3: Semantic (mem0 with fallback)
  - L4: Graph (Neo4j, optional)
- **One-Click Installer** (`install.mjs`)
- **Test Suite** (`test.mjs`)
- **OpenClaw Integration** via session hook
- **Environment-based configuration** (no hardcoded paths)
- **Graceful degradation** with Layer 2 fallback
- **Comprehensive documentation**

### Changed
- Complete rewrite from v3.0 (configs only) to v3.5 (fully executable)
- All components now environment-aware
- Improved error handling throughout
- Better logging with structured format

### Fixed
- Hardcoded paths → Environment variables
- Silent failures → Proper error handling
- Config-only → Actual implementation
- No mutations → Real config changes

## [3.0.0] - 2026-03-10

### Added
- Initial configuration-based system
- 3 core systems defined
- Basic documentation

### Notes
- v3.0 was configuration-only, not executable
- v3.5 is the first fully executable release

## [2.1.0] - 2026-03-08 (Pre-release)

### Added
- Advanced features (Temporal Versioning, M1-M4 tracking)
- 10 systems (too complex for production)
- 30+ files

### Notes
- v2.1 was powerful but too complex
- v3.5 simplifies to essential complexity only

## [1.0.0] - 2026-03-05 (Prototype)

### Added
- Initial prototype
- Basic memory concepts

[3.5.0]: https://github.com/your-org/smriti/releases/tag/v3.5.0
[3.0.0]: https://github.com/your-org/smriti/releases/tag/v3.0.0
[2.1.0]: https://github.com/your-org/smriti/releases/tag/v2.1.0
[1.0.0]: https://github.com/your-org/smriti/releases/tag/v1.0.0
