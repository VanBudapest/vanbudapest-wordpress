# Hungaroring SFPG Image Downloader
# Specialized downloader for Simple File Photo Gallery (SFPG) system

param(
    [string]$GalleryUrl = "https://hungaroring.hu/press/index.php?sfpg=MjAyNS9GMV8yMDI1L1RodXJzZGF5L0YxIFBhZGRvY2svKipjN2FjZTMwNzBjN2UyNjM3OWRjMDA5MzkxNjEzMmM0M2UxNWM4ODIyOTlkY2ExODE1NzBjMjMwODBmZmQ0MDcz",
    [string]$OutputFolder = ".\hungaroring_images"
)

# Set TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Hungaroring SFPG Image Downloader" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Extract SFPG parameter from URL
if ($GalleryUrl -match 'sfpg=([^&]+)') {
    $sfpgParam = $matches[1]
    Write-Host "[*] SFPG Parameter: $sfpgParam" -ForegroundColor Cyan

    # Decode base64 to see the path
    try {
        $decodedPath = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($sfpgParam))
        Write-Host "[*] Decoded path: $decodedPath" -ForegroundColor Yellow
    }
    catch {
        Write-Host "[!] Could not decode SFPG parameter" -ForegroundColor Red
    }
}
else {
    Write-Host "[!] No SFPG parameter found in URL" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[*] Output folder: $OutputFolder" -ForegroundColor Yellow
Write-Host ""

# Create output folder
if (-not (Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
    Write-Host "[+] Created output folder" -ForegroundColor Green
}

# Setup web client with proper headers
function Get-WebContent {
    param([string]$Url)

    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        $webClient.Headers.Add("Referer", "https://hungaroring.hu/press/")
        $webClient.Headers.Add("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        $webClient.Headers.Add("Accept-Language", "hu-HU,hu;q=0.9,en;q=0.8")
        $webClient.Encoding = [System.Text.Encoding]::UTF8

        $content = $webClient.DownloadString($Url)
        $webClient.Dispose()
        return $content
    }
    catch {
        Write-Host "[!] Error fetching $Url : $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Fetch gallery page
Write-Host "[*] Fetching gallery page..." -ForegroundColor Cyan
$html = Get-WebContent -Url $GalleryUrl

if (-not $html) {
    Write-Host "[!] Failed to fetch gallery page" -ForegroundColor Red
    exit 1
}

Write-Host "[+] Gallery page fetched ($($html.Length) bytes)" -ForegroundColor Green

# Save HTML for debugging
$html | Out-File "$OutputFolder\debug_page.html" -Encoding UTF8
Write-Host "[*] Debug HTML saved to: $OutputFolder\debug_page.html" -ForegroundColor Gray
Write-Host ""

# Method 1: Extract all SFPG image links (index.php?image=...)
Write-Host "[*] Method 1: Looking for SFPG image links..." -ForegroundColor Cyan
$imageLinks = @()
$matches = [regex]::Matches($html, 'index\.php\?image=([^"''&\s]+)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches) {
    $imageParam = $match.Groups[1].Value
    $fullUrl = "https://hungaroring.hu/press/index.php?image=$imageParam"
    $imageLinks += $fullUrl
}
Write-Host "    Found $($imageLinks.Count) image= links" -ForegroundColor Yellow

# Method 2: Extract direct image URLs
Write-Host "[*] Method 2: Looking for direct image URLs..." -ForegroundColor Cyan
$directImages = @()
$matches = [regex]::Matches($html, '(https?://[^"''<>\s]+\.(?:jpg|jpeg|png|gif))', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches) {
    $directImages += $match.Groups[1].Value
}
Write-Host "    Found $($directImages.Count) direct image URLs" -ForegroundColor Yellow

# Method 3: Look for thumbnail/preview links that might lead to full images
Write-Host "[*] Method 3: Looking for thumbnail links..." -ForegroundColor Cyan
$thumbnails = @()
$matches = [regex]::Matches($html, 'href=["'']([^"'']*(?:thumb|preview|image)[^"'']*)[^>]*>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches) {
    $url = $match.Groups[1].Value
    if ($url -notmatch '^https?://') {
        if ($url -match '^/') {
            $url = "https://hungaroring.hu" + $url
        }
        else {
            $url = "https://hungaroring.hu/press/" + $url
        }
    }
    $thumbnails += $url
}
Write-Host "    Found $($thumbnails.Count) thumbnail/preview links" -ForegroundColor Yellow

# Method 4: Look in JavaScript or data attributes
Write-Host "[*] Method 4: Looking for JavaScript image data..." -ForegroundColor Cyan
$jsImages = @()
$matches = [regex]::Matches($html, '(?:data-src|data-image|data-url)=["'']([^"'']+)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches) {
    $url = $match.Groups[1].Value
    if ($url -match '\.(jpg|jpeg|png|gif)' -or $url -match 'image=') {
        if ($url -notmatch '^https?://') {
            $url = "https://hungaroring.hu/press/" + $url
        }
        $jsImages += $url
    }
}
Write-Host "    Found $($jsImages.Count) JavaScript image references" -ForegroundColor Yellow

# Method 5: Look for any onclick or JavaScript that references images
Write-Host "[*] Method 5: Scanning for onclick handlers..." -ForegroundColor Cyan
$onclickImages = @()
$matches = [regex]::Matches($html, "onclick=[\"']([^\"']*image=[^\"']*)[\"']", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches) {
    $onclick = $match.Groups[1].Value
    if ($onclick -match 'image=([^&\s''")]+)') {
        $imageParam = $matches[0].Groups[1].Value
        $url = "https://hungaroring.hu/press/index.php?image=$imageParam"
        $onclickImages += $url
    }
}
Write-Host "    Found $($onclickImages.Count) onclick image handlers" -ForegroundColor Yellow

Write-Host ""

# Combine all found URLs
$allUrls = $imageLinks + $directImages + $thumbnails + $jsImages + $onclickImages | Select-Object -Unique

Write-Host "[*] Total unique image URLs found: $($allUrls.Count)" -ForegroundColor Cyan
Write-Host ""

if ($allUrls.Count -eq 0) {
    Write-Host "[!] No images found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the debug_page.html file." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  1. The gallery might require login/authentication" -ForegroundColor Gray
    Write-Host "  2. Images might be loaded via JavaScript after page load" -ForegroundColor Gray
    Write-Host "  3. The gallery might use a different URL structure" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can try:" -ForegroundColor Yellow
    Write-Host "  - Open the gallery URL in a browser and inspect the network tab" -ForegroundColor Gray
    Write-Host "  - Look for XHR/Fetch requests that load image data" -ForegroundColor Gray
    Write-Host "  - Check if there's a 'Download All' button or similar" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Display sample URLs
Write-Host "Sample URLs to download:" -ForegroundColor Cyan
$allUrls | Select-Object -First 5 | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}
if ($allUrls.Count -gt 5) {
    Write-Host "  ... and $($allUrls.Count - 5) more" -ForegroundColor Gray
}
Write-Host ""

# Download function
function Download-Image {
    param(
        [string]$Url,
        [string]$OutputPath
    )

    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        $webClient.Headers.Add("Referer", $GalleryUrl)
        $webClient.DownloadFile($Url, $OutputPath)
        $webClient.Dispose()

        # Check if file was actually downloaded and is not empty
        if (Test-Path $OutputPath) {
            $fileInfo = Get-Item $OutputPath
            if ($fileInfo.Length -gt 0) {
                return $true
            }
            else {
                Remove-Item $OutputPath -Force
                return $false
            }
        }
        return $false
    }
    catch {
        return $false
    }
}

# Download images
Write-Host "[*] Starting downloads..." -ForegroundColor Cyan
Write-Host ""

$downloaded = 0
$failed = 0
$counter = 1

foreach ($imageUrl in $allUrls) {
    # Determine file extension
    $extension = "jpg"
    if ($imageUrl -match '\.([a-z]+)(?:\?|$|&)') {
        $extension = $matches[1].ToLower()
    }

    $filename = "hungaroring_image_{0:D4}.{1}" -f $counter, $extension
    $outputPath = Join-Path $OutputFolder $filename

    Write-Host "[$counter/$($allUrls.Count)] Downloading: $filename" -ForegroundColor White
    Write-Host "    URL: $imageUrl" -ForegroundColor Gray

    if (Download-Image -Url $imageUrl -OutputPath $outputPath) {
        $fileSize = (Get-Item $outputPath).Length
        $fileSizeKB = [math]::Round($fileSize / 1KB, 2)
        Write-Host "    [OK] Downloaded ($fileSizeKB KB)" -ForegroundColor Green
        $downloaded++
    }
    else {
        Write-Host "    [FAIL] Download failed" -ForegroundColor Red
        $failed++
    }

    $counter++
    Start-Sleep -Milliseconds 300  # Be nice to the server
}

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Download Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Total URLs found:       $($allUrls.Count)" -ForegroundColor White
Write-Host "Successfully downloaded: $downloaded" -ForegroundColor Green
Write-Host "Failed:                 $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "Output folder:          $OutputFolder" -ForegroundColor Yellow
Write-Host ""

if ($downloaded -gt 0) {
    Write-Host "[+] Images saved to: $OutputFolder" -ForegroundColor Green
    Write-Host ""

    # Calculate total size
    $totalSize = (Get-ChildItem "$OutputFolder\*.jpg","$OutputFolder\*.jpeg","$OutputFolder\*.png" -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
    Write-Host "[*] Total size: $totalSizeMB MB" -ForegroundColor Cyan
    Write-Host ""

    # Ask about ZIP
    $createZip = Read-Host "Create ZIP archive? (Y/N)"
    if ($createZip -eq 'Y' -or $createZip -eq 'y') {
        $zipPath = "$OutputFolder.zip"

        if (Test-Path $zipPath) {
            Remove-Item $zipPath -Force
        }

        Write-Host "[*] Creating ZIP archive..." -ForegroundColor Cyan
        Compress-Archive -Path "$OutputFolder\hungaroring_image_*.*" -DestinationPath $zipPath -CompressionLevel Optimal

        $zipSize = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
        Write-Host "[+] ZIP created: $zipPath ($zipSize MB)" -ForegroundColor Green
    }
}
else {
    Write-Host "[!] No images were downloaded." -ForegroundColor Red
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Check debug_page.html to see the actual page content" -ForegroundColor Gray
    Write-Host "  2. Open the gallery URL in a browser" -ForegroundColor Gray
    Write-Host "  3. Use browser dev tools (F12) -> Network tab" -ForegroundColor Gray
    Write-Host "  4. See what requests are made when images load" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
