$exclude = @("venv", "BotGimp.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotGimp.zip" -Force