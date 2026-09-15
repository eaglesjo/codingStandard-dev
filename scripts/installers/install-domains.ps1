param(
  [string]$Target='.',
  [ValidateSet('en','ko','fr','es','zh-CN','ja','ru','tr','de','it','pt','ar','hi','id','vi','th','nl','pl','sv','uk')][string]$Language,
  [ValidateSet('common','ml','llm','vision','colab','all')][string]$Domain,
  [ValidateSet('Ask','Merge','Overwrite','Skip')][string]$ConflictAction='Ask',
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$policy=$ConflictAction.ToLowerInvariant()
$languageArg=if($Language){$Language}else{''}
$domainArg=if($Domain){$Domain}else{''}
$dryRunArg=if($DryRun){'true'}else{'false'}
& python (Join-Path $Root 'scripts/installers/installation.py') install $Target $languageArg $domainArg $policy $dryRunArg
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
