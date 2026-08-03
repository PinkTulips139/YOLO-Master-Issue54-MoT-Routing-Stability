# Copy-only private archive reference. Review exact sources before running.
$SourceRepo = $env:ISSUE54_SOURCE_REPO
$ExistingArchive = $env:ISSUE54_LOCAL_ARCHIVE
$PrivateArchive = $env:ISSUE54_PRIVATE_ARCHIVE
if (-not $SourceRepo -or -not $ExistingArchive -or -not $PrivateArchive) {
    throw 'Set ISSUE54_SOURCE_REPO, ISSUE54_LOCAL_ARCHIVE, and ISSUE54_PRIVATE_ARCHIVE before continuing.'
}
# Never delete or move files from $SourceRepo or $ExistingArchive.
# Public metadata must use ${ISSUE54_PRIVATE_ARCHIVE} rather than this machine path.
Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $SourceRepo 'docs\issue54\phase3_mot_routing\phase3_cross_seed_routing.json')
Get-ChildItem -LiteralPath $PrivateArchive -Recurse -File | Get-FileHash -Algorithm SHA256
