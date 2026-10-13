# OpenSpace 0.22.0 runtime check — 2026-10-13

Result: NOT fully functional; default scene crashed during loading.

- New installation: C:\work\OpenSpace-0.22.0
- Old installation path: local junction to the new installation.
- Required data/user/sync/cache/config/logs/module/script/shader/temp directories and default profile exist.
- OPENSPACE_USER, OPENSPACE_SYNC, OPENSPACE_GLOBEBROWSING, OPENSPACE_LEVEL: no process/user/machine overrides found.
- Launcher started successfully with an explicit installation-root working directory; version 0.22.0 and default profile were recognized.
- The default scene began loading assets using the new C:\work path.
- Runtime log: OpenGL 4.6; Intel UHD Graphics 730; driver 32.0.101.7088.
- Windows Application Error event 1000 at 09:42:22 (Asia/Tbilisi): OpenSpace.exe; fault module ucrtbase.dll; exception 0xc0000409. Windows Error Reporting event 1001 also recorded BEX64.
- No Error/Fatal/Warning rows were found in the captured application log; absence of logged errors does not override the OS crash evidence.
- Old-path control: launcher started; scene control could not be completed because the computer-use helper twice failed with "foreground window did not report a process id". This uses the same physical executable and is not an independent pre-migration baseline.
- FPS, camera navigation, stable scene rendering, every dataset/addon, screenshots/export, and sustained performance: NOT verified.
- Cause of crash is undetermined. The evidence does not establish migration, GPU driver, or any security product as its cause.
- No login, security permission changes, GPU configuration changes, network/IP configuration changes, or ES settings actions were performed. Existing program defaults can contact public OpenSpace/science-data servers during scene loading; no forbidden sites were opened.

Evidence: first_run_log.html; first_run_crash.json.
