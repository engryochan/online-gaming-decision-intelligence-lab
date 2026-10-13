# Run in a 64-bit PowerShell window opened as Administrator.
# Permanently removes previous Windows upgrade leftovers on C:, including
# Windows.old. This removes the ability to roll back using those files.
# Uses Microsoft's cleanup handler; does not take ownership, change ACLs,
# configure networks, log in, or clean general Downloads/Recycle Bin data.
# /autoclean can also remove other Windows upgrade leftovers on C:.

$ErrorActionPreference = 'Stop'

$taskIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
$taskPrincipal = [Security.Principal.WindowsPrincipal]::new($taskIdentity)
if (-not $taskPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Open 64-bit PowerShell as Administrator and run this script again.'
}
if (-not [Environment]::Is64BitProcess) {
    throw 'Use 64-bit PowerShell.'
}
if (-not [string]::Equals($env:SystemRoot, 'C:\Windows', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Unexpected Windows installation path. No cleanup was started.'
}

$taskTarget = 'C:\Windows.old'
$taskDisk = [IO.DriveInfo]::new('C:\')
$taskBefore = $taskDisk.AvailableFreeSpace
if (-not (Test-Path -LiteralPath $taskTarget)) {
    Write-Host 'C:\Windows.old is already absent. No cleanup was started.'
    Write-Host ('C: free space: {0:N2} GiB' -f ($taskBefore / 1GB))
    return
}
$taskItem = Get-Item -LiteralPath $taskTarget -Force
if (-not $taskItem.PSIsContainer -or
    ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
    -not [string]::Equals($taskItem.FullName, $taskTarget, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Unexpected target or reparse point. No cleanup was started.'
}
if (Get-Process -Name cleanmgr -ErrorAction SilentlyContinue) {
    throw 'Close existing Disk Cleanup windows before running this script.'
}

$taskCleaner = 'C:\Windows\System32\cleanmgr.exe'
$taskSignature = Get-AuthenticodeSignature -LiteralPath $taskCleaner
if ($taskSignature.Status -ne 'Valid') {
    throw 'Disk Cleanup signature verification failed. No cleanup was started.'
}

Write-Host ('Before cleanup: {0:N2} GiB free on C:' -f ($taskBefore / 1GB))
Write-Host 'Removing previous Windows upgrade leftovers on C:. Please wait.'
$taskProcess = Start-Process -FilePath $taskCleaner -ArgumentList '/d', 'C:', '/autoclean' -WindowStyle Hidden -Wait -PassThru
$taskAfter = ([IO.DriveInfo]::new('C:\')).AvailableFreeSpace
$taskRemaining = Test-Path -LiteralPath $taskTarget

[pscustomobject]@{
    Target = $taskTarget
    CleanerExitCode = $taskProcess.ExitCode
    WindowsOldStillExists = $taskRemaining
    FreeBeforeGiB = [math]::Round($taskBefore / 1GB, 2)
    FreeAfterGiB = [math]::Round($taskAfter / 1GB, 2)
    NetSpaceGainGiB = [math]::Round(($taskAfter - $taskBefore) / 1GB, 2)
} | Format-List

if ($taskProcess.ExitCode -ne 0 -or $taskRemaining) {
    throw 'Cleanup is not confirmed complete. Check the result above; no forced deletion or permissions changes were attempted.'
}
Write-Host 'Verified: C:\Windows.old no longer exists.'
