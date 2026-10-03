# Link Hstack skill folders into the shared skills directory.
# No args installs every skill. -List prints status and changes nothing.
param(
  [switch]$List,
  [switch]$DryRun,
  [string]$Only,
  [string]$SkillsDir
)

$ErrorActionPreference = 'Stop'

function Show-Use {
  Write-Output 'use: install.ps1 [-List] [-DryRun] [-Only <folder>] [-SkillsDir <path>]'
  exit 2
}

if ($args.Count -gt 0) { Show-Use }

$repo = Split-Path $PSScriptRoot -Parent

function Get-Members {
  Get-ChildItem $repo -Directory | Where-Object {
    $_.Name -ne 'scripts' -and (Get-ChildItem $_.FullName -Recurse -Filter SKILL.md -File -ErrorAction SilentlyContinue | Select-Object -First 1)
  } | Sort-Object Name
}

function Resolve-SkillsDir {
  if ($SkillsDir) {
    if (-not (Test-Path $SkillsDir)) { New-Item -ItemType Directory -Path $SkillsDir | Out-Null }
    return (Resolve-Path $SkillsDir).Path
  }
  $shared = Join-Path $env:USERPROFILE 'Desktop\Skills'
  if (Test-Path $shared) { return (Resolve-Path $shared).Path }
  $fallback = Join-Path $env:USERPROFILE '.agents\skills'
  if (-not (Test-Path $fallback)) { New-Item -ItemType Directory -Path $fallback | Out-Null }
  return (Resolve-Path $fallback).Path
}

function Test-SameTree([string]$left, [string]$right) {
  $skip = '\\(\.git|__pycache__|node_modules)\\'
  $map = @{}
  Get-ChildItem $left -Recurse -File -Force | Where-Object { $_.FullName -notmatch $skip } | ForEach-Object {
    $map[$_.FullName.Substring($left.Length).TrimStart('\')] = $_.FullName
  }
  $other = @{}
  Get-ChildItem $right -Recurse -File -Force | Where-Object { $_.FullName -notmatch $skip } | ForEach-Object {
    $other[$_.FullName.Substring($right.Length).TrimStart('\')] = $_.FullName
  }
  if ($map.Count -ne $other.Count) { return $false }
  $sha = [Security.Cryptography.SHA256]::Create()
  foreach ($key in $map.Keys) {
    if (-not $other.ContainsKey($key)) { return $false }
    $bytesA = [IO.File]::ReadAllBytes($map[$key])
    $bytesB = [IO.File]::ReadAllBytes($other[$key])
    $binary = ($bytesA -contains 0) -or ($bytesB -contains 0)
    if ($binary) {
      $hashA = [BitConverter]::ToString($sha.ComputeHash($bytesA))
      $hashB = [BitConverter]::ToString($sha.ComputeHash($bytesB))
    } else {
      $textA = ([Text.Encoding]::UTF8.GetString($bytesA) -replace "`r`n", "`n" -replace "`r", "`n")
      $textB = ([Text.Encoding]::UTF8.GetString($bytesB) -replace "`r`n", "`n" -replace "`r", "`n")
      $hashA = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($textA)))
      $hashB = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($textB)))
    }
    if ($hashA -ne $hashB) { return $false }
  }
  return $true
}

function Get-LinkTarget([System.IO.FileSystemInfo]$item) {
  $target = $item.Target
  if ($target -is [array]) { return [string]$target[0] }
  return [string]$target
}

function Get-SkillStatus([string]$name, [string]$dir) {
  $src = Join-Path $repo $name
  $dest = Join-Path $dir $name
  $srcFull = (Resolve-Path $src).Path
  if (-not (Test-Path $dest)) { return 'missing' }
  $item = Get-Item $dest -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    $target = Get-LinkTarget $item
    if ($target -and ((Resolve-Path $target -ErrorAction SilentlyContinue).Path -eq $srcFull)) { return 'linked' }
    return 'other-link'
  }
  if (Test-Path (Join-Path $dest '.git')) { return 'own-repo' }
  if (Test-SameTree $srcFull $dest) { return 'copy' }
  return 'differs'
}

function Install-Skill([string]$name, [string]$dir) {
  $status = Get-SkillStatus $name $dir
  if ($List) { return $status }
  if ($status -eq 'linked' -or $status -eq 'own-repo' -or $status -eq 'other-link' -or $status -eq 'differs') {
    return $status
  }
  $srcFull = (Resolve-Path (Join-Path $repo $name)).Path
  $dest = Join-Path $dir $name
  if ($DryRun) {
    if ($status -eq 'copy') { return 'would-relink' }
    return 'would-link'
  }
  if ($status -eq 'copy') { Remove-Item -Recurse -Force $dest }
  New-Item -ItemType Junction -Path $dest -Target $srcFull | Out-Null
  if ($status -eq 'copy') { return 'relinked' }
  return 'linked'
}

$members = @(Get-Members | Select-Object -ExpandProperty Name)
if ($Only) {
  if ($members -notcontains $Only) {
    Write-Output "unknown skill: $Only"
    Write-Output ("known: " + ($members -join ', '))
    exit 2
  }
  $members = @($Only)
}

$dir = Resolve-SkillsDir
Write-Output "dir: $dir"
Write-Output ("count: {0} skills" -f $members.Count)
$tallies = @{}
foreach ($name in $members) {
  $status = Install-Skill $name $dir
  if (-not $tallies.ContainsKey($status)) { $tallies[$status] = 0 }
  $tallies[$status]++
  Write-Output "$name`: $status"
}
$summary = ($tallies.Keys | Sort-Object | ForEach-Object { "$_=$($tallies[$_])" }) -join ' '
Write-Output "result: $summary"
exit 0
