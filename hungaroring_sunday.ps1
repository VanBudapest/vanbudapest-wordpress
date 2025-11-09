# Hungaroring Image Downloader
# Downloads all images from Hungaroring press gallery

param(
    [string]$GalleryUrl = "https://hungaroring.hu/press/index.php?sfpg=MjAyNS9GMV8yMDI1L1RodHJzZGF5L0YxIFBhZGRvY2svKipjN2FjZTMwNzBjN2UyNjM3OWRjMDA5MzkxNjEzMmM0M2UxNWM4ODIyOTlkY2ExODE1NzBjMjMwODBmZmQ0MDcz",
    [string]$OutputFolder = ".\hungaroring_images"
)

# Set TLS 1.2 for secure connections
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Hungaroring Image Downloader" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Gallery URL: $GalleryUrl" -ForegroundColor Yellow
Write-Host "Output folder: $OutputFolder" -ForegroundColor Yellow
Write-Host ""

# Create output folder if it doesn't exist
if (-not (Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
    Write-Host "[+] Created output folder: $OutputFolder" -ForegroundColor Green
}

# Function to download a file with progress
function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath
    )

    try {
        $webClient = New-Object System.Net.WebClient
        # Add user agent to avoid 403 errors
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        $webClient.Headers.Add("Referer", "https://hungaroring.hu/")
        $webClient.DownloadFile($Url, $OutputPath)
        $webClient.Dispose()
        return $true
    }
    catch {
        Write-Host "[!] Error downloading: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Fetch the gallery page
Write-Host "[*] Fetching gallery page..." -ForegroundColor Cyan

try {
    $webClient = New-Object System.Net.WebClient
    $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    $webClient.Headers.Add("Referer", "https://hungaroring.hu/")
    $webClient.Encoding = [System.Text.Encoding]::UTF8

    $html = $webClient.DownloadString($GalleryUrl)
    $webClient.Dispose()

    Write-Host "[+] Gallery page fetched successfully" -ForegroundColor Green
}
catch {
    Write-Host "[!] Error fetching gallery page: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract image URLs using multiple methods
$imageUrls = @()

# Method 1: Look for direct image links (JPG, PNG)
$matches1 = [regex]::Matches($html, 'https?://[^"''<>\s]+\.(?:jpg|jpeg|png)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches1) {
    $imageUrls += $match.Value
}

# Method 2: Look for sfpg image parameter links
$matches2 = [regex]::Matches($html, 'index\.php\?image=[^"''&\s]+', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches2) {
    $fullUrl = "https://hungaroring.hu/press/" + $match.Value
    $imageUrls += $fullUrl
}

# Method 3: Look for src attributes
$matches3 = [regex]::Matches($html, 'src=["'']([^"'']+\.(?:jpg|jpeg|png)[^"'']*)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches3) {
    $url = $match.Groups[1].Value
    if ($url -notmatch '^https?://') {
        $url = "https://hungaroring.hu" + $url
    }
    $imageUrls += $url
}

# Method 4: Look for data-src attributes (lazy loading)
$matches4 = [regex]::Matches($html, 'data-src=["'']([^"'']+\.(?:jpg|jpeg|png)[^"'']*)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches4) {
    $url = $match.Groups[1].Value
    if ($url -notmatch '^https?://') {
        $url = "https://hungaroring.hu" + $url
    }
    $imageUrls += $url
}

# Method 5: Look for onclick or href with image parameters
$matches5 = [regex]::Matches($html, '(?:href|onclick)=["'']([^"'']*image=[^"'']+)', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
foreach ($match in $matches5) {
    $url = $match.Groups[1].Value
    if ($url -match '^index\.php') {
        $url = "https://hungaroring.hu/press/" + $url
    }
    elseif ($url -notmatch '^https?://') {
        $url = "https://hungaroring.hu/press/" + $url
    }
    $imageUrls += $url
}

# Remove duplicates and filter
$imageUrls = $imageUrls | Select-Object -Unique | Where-Object { $_ -match '\.(jpg|jpeg|png)' -or $_ -match 'image=' }

Write-Host ""
Write-Host "[*] Found $($imageUrls.Count) image URLs" -ForegroundColor Cyan

if ($imageUrls.Count -eq 0) {
    Write-Host ""
    Write-Host "[!] No images found. Saving HTML for debugging..." -ForegroundColor Yellow
    $html | Out-File "$OutputFolder\debug_page.html" -Encoding UTF8
    Write-Host "[+] HTML saved to: $OutputFolder\debug_page.html" -ForegroundColor Green
    Write-Host ""
    Write-Host "Please check the HTML file to see the page structure." -ForegroundColor Yellow
    Write-Host "The gallery might use JavaScript to load images dynamically." -ForegroundColor Yellow
    exit 0
}

# Display found URLs
Write-Host ""
Write-Host "Sample URLs found:" -ForegroundColor Cyan
$imageUrls | Select-Object -First 5 | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
if ($imageUrls.Count -gt 5) {
    Write-Host "  ... and $($imageUrls.Count - 5) more" -ForegroundColor Gray
}
Write-Host ""

# Download images
$downloaded = 0
$failed = 0
$counter = 1

foreach ($imageUrl in $imageUrls) {
    # Generate filename
    $extension = "jpg"
    if ($imageUrl -match '\.([a-z]+)(?:\?|$)') {
        $extension = $matches[1]
    }

    $filename = "image_{0:D4}.{1}" -f $counter, $extension
    $outputPath = Join-Path $OutputFolder $filename

    Write-Host "[*] Downloading [$counter/$($imageUrls.Count)]: $filename" -ForegroundColor Cyan

    if (Download-File -Url $imageUrl -OutputPath $outputPath) {
        $downloaded++
        Write-Host "    [OK] Downloaded successfully" -ForegroundColor Green
    }
    else {
        $failed++
        Write-Host "    [FAIL] Download failed" -ForegroundColor Red
    }

    $counter++
    Start-Sleep -Milliseconds 500  # Be nice to the server
}

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Download Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Total images found: $($imageUrls.Count)" -ForegroundColor White
Write-Host "Successfully downloaded: $downloaded" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "Output folder: $OutputFolder" -ForegroundColor Yellow
Write-Host ""

if ($downloaded -gt 0) {
    Write-Host "[+] Images saved to: $OutputFolder" -ForegroundColor Green

    # Ask if user wants to create a ZIP
    $createZip = Read-Host "Do you want to create a ZIP archive? (Y/N)"
    if ($createZip -eq 'Y' -or $createZip -eq 'y') {
        $zipPath = "$OutputFolder.zip"

        if (Test-Path $zipPath) {
            Remove-Item $zipPath -Force
        }

        Write-Host "[*] Creating ZIP archive..." -ForegroundColor Cyan
        Compress-Archive -Path "$OutputFolder\*" -DestinationPath $zipPath -CompressionLevel Optimal
        Write-Host "[+] ZIP created: $zipPath" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
