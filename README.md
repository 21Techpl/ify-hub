# IFY Hub

Thin API gateway for SmartAGD devices. Apps (Flutter/Android/iOS/web) talk to this
API; the hub owns the device credentials (Tuya Cloud Access ID/Secret, WLED is
direct-to-device and bypasses the hub).

## Design invariants
- **Keys never leave the server.** Mobile apps authenticate to the hub (owner token), never to Tuya.
- **Contract-driven**: every device capability comes from `21Techpl/ify-device-contracts` (vendored). No ad-hoc DP handling outside the Tuya adapter module.
- Local-first later: the adapter interface must allow a local tinytuya implementation without app changes.
- Loopback + Tailscale: bind 127.0.0.1, expose via tunnel; never public internet without explicit decision.
- TDD: mock Tuya client for tests; real cloud client is a thin wrapper (verified against the live API before merge).

## Endpoints (v0 plan)
- `GET  /health`
- `GET  /devices`
- `GET  /ac/{device_id}/status`
- `PUT  /ac/{device_id}/command` (power/temp/mode/fan/swing/timer — validated against contract)
