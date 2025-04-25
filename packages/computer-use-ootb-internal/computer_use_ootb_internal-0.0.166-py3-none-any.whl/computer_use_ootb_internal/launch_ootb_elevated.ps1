# launch_ootb_elevated.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$TargetExePath,

    [Parameter(Mandatory=$true)]
    [string]$Port,

    [Parameter(Mandatory=$true)]
    [string]$TargetUser,

    [Parameter(Mandatory=$true)]
    [string]$WorkingDirectory
)

try {
    Write-Host "--- OOTB Elevation Helper ---"
    Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host "Received parameters:"
    Write-Host "  Target Exe Path : $TargetExePath"
    Write-Host "  Port            : $Port"
    Write-Host "  Target User     : $TargetUser"
    Write-Host "  Working Dir     : $WorkingDirectory"
    Write-Host ""

    # Validate paths
    if (-not (Test-Path -Path $TargetExePath -PathType Leaf)) {
        throw "Target executable not found at '$TargetExePath'"
    }
    if (-not (Test-Path -Path $WorkingDirectory -PathType Container)) {
        throw "Working directory not found at '$WorkingDirectory'"
    }

    # Construct the argument list string for the target executable
    # Ensure target user is single-quoted for the argument parser
    $argumentList = "--port $Port --target_user '$TargetUser'"

    Write-Host "Constructed ArgumentList for Target Exe: $argumentList"
    Write-Host "Executing elevated process..."
    Write-Host "Command: Start-Process -FilePath `$TargetExePath` -ArgumentList `$argumentList` -WorkingDirectory `$WorkingDirectory` -Verb RunAs"
    Write-Host "--- Waiting for UAC prompt if necessary ---"

    # Execute the command to launch the target exe elevated directly
    Start-Process -FilePath $TargetExePath -ArgumentList $argumentList -WorkingDirectory $WorkingDirectory -Verb RunAs

    Write-Host "--- OOTB Elevation Helper: Start-Process command executed. ---"
    # The calling powershell window (started by CreateProcessAsUser with -NoExit) will remain open.

} catch {
    Write-Error "--- OOTB Elevation Helper Error ---"
    Write-Error "Error launching elevated process: $($_.Exception.Message)"
    Write-Error "Script Parameters:"
    Write-Error "  Target Exe Path : $TargetExePath"
    Write-Error "  Port            : $Port"
    Write-Error "  Target User     : $TargetUser"
    Write-Error "  Working Dir     : $WorkingDirectory"
    Write-Host "Press Enter to exit..."
    Read-Host # Keep window open on error
    Exit 1
}

# Exit gracefully if successful
Exit 0 