<#[
.SYNOPSIS
Capture a Windows Performance Recorder trace around a native command.
.EXAMPLE
.\profile-windows.ps1 -Executable '.\target\release\trit.exe' -Arguments @('--help')
#>
param(
    [Parameter(Mandatory = $true)][string]$Executable,
    [string[]]$Arguments = @(),
    [string]$Trace = 'cpu-profile.etl',
    [string]$Profile = 'CPU'
)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command wpr.exe -ErrorAction SilentlyContinue)) {
    throw 'Windows Performance Recorder (wpr.exe) not found. Install Windows Performance Toolkit.'
}
Write-Host 'Starting WPR. Check wpr -profiles for valid profiles on this system.'
& wpr.exe -start $Profile -filemode
if ($LASTEXITCODE -ne 0) { throw 'Could not start WPR. Check permissions and profile name.' }
try {
    & $Executable @Arguments
    $exitCode = $LASTEXITCODE
} finally {
    & wpr.exe -stop $Trace
    if ($LASTEXITCODE -ne 0) { Write-Warning 'WPR failed to stop or save trace' }
}
Write-Host "Open $Trace in Windows Performance Analyzer. Profiling changes execution overhead."
if ($exitCode -ne 0) { exit $exitCode }
