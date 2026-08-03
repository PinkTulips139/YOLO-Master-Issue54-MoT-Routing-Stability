# Manual fallback publication commands. Review before running; this file is never executed by validation.
$PortfolioRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
Set-Location -LiteralPath $PortfolioRoot
gh auth status
gh repo view PinkTulips139/YOLO-Master-Issue54-MoT-Routing-Stability
# Continue only if the repository does not exist and local validation passes.
gh repo create PinkTulips139/YOLO-Master-Issue54-MoT-Routing-Stability --public --source $PortfolioRoot --remote origin --push --description 'Audited multi-seed MoT routing stability, architecture controls, and reproducible evidence for YOLO-Master Issue #54.'
git push origin v1.0.0
gh repo edit PinkTulips139/YOLO-Master-Issue54-MoT-Routing-Stability --add-topic computer-vision --add-topic object-detection --add-topic mixture-of-transformers --add-topic mixture-of-experts --add-topic routing-stability --add-topic reproducible-research --add-topic visdrone --add-topic pytorch --add-topic yolo --add-topic research-portfolio --enable-wiki=false --enable-projects=false
