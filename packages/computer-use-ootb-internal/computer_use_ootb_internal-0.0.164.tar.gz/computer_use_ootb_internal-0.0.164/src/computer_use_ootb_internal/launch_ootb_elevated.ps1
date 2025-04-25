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

    # Construct the second argument for cmd.exe /K, precisely matching the working command
    # Format: "<quoted_exe_path>" --port <port> --target_user ''<username>''
    # Note: PowerShell handles escaping within double quotes differently.
    #       Using backticks ` before inner quotes is safer here.
    $cmdKSecondArg = "`"`"$TargetExePath`"`" --port $Port --target_user ''$TargetUser''"

    # Construct the argument list array for Start-Process launching cmd.exe
    $startProcessArgs = @('/K', $cmdKSecondArg)

    Write-Host "Constructed cmd.exe /K arguments: $cmdKSecondArg"
    Write-Host "Constructed Start-Process arguments array: $($startProcessArgs -join ' ')" # For logging
    Write-Host "Executing elevated process..."
    Write-Host "Command: Start-Process -FilePath cmd.exe -ArgumentList @('/K', '$cmdKSecondArg') -WorkingDirectory '$WorkingDirectory' -Verb RunAs"
    Write-Host "--- Waiting for UAC prompt if necessary ---"

    # Execute the command to launch cmd elevated, which runs the target app
    Start-Process -FilePath cmd.exe -ArgumentList $startProcessArgs -WorkingDirectory $WorkingDirectory -Verb RunAs

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