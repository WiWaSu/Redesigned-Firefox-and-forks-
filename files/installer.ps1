param(
  [ValidateSet("install", "uninstall")]
  [string]$Action = "install",
  # ask | all | список ключей через запятую (floorp,firefox,librewolf,...). both = all
  [string]$Target = "ask",
  [ValidateSet("ask", "oneui", "ios", "material", "fluent", "macos", "nothing", "nightdrive", "aero", "retro", "terminal", "paper", "cyber")]
  [string]$Theme = "ask",
  # ask | yes | no — новый просмотрщик PDF
  [ValidateSet("ask", "yes", "no")]
  [string]$Pdf = "ask",
  # windows — акцент из Windows, или свой цвет #RRGGBB
  [string]$Accent = "windows",
  # keep — не трогать; auto | light | dark
  [ValidateSet("keep", "auto", "light", "dark")]
  [string]$Mode = "keep",
  # theme — как в теме; none — без скруглений вообще; square | standard | round
  [ValidateSet("theme", "none", "square", "standard", "round")]
  [string]$Corners = "theme",
  # анимации: apple — пружины как в iOS, smooth — плавные, system — как в Windows, off — выключены
  [ValidateSet("apple", "smooth", "system", "off")]
  [string]$Motion = "apple",
  # обои новой вкладки: keep — не менять, theme — как в теме, aurora|iris|sunset|ocean|forest|night|rose|graphite|bloom|dune,
  # или путь к своей картинке (jpg, png, webp)
  [string]$Wall = "keep",
  # включённые функции через запятую
  [string]$Features = "nowbar,progress,center,clock,wallpaper",
  [switch]$Gui,
  [string]$UserAppData = $env:APPDATA,
  # для тестов: принудительные пути к папкам браузеров ("ключ=путь;ключ=путь")
  [string]$Dirs = "",
  [string]$FloorpDir = "",
  [string]$FirefoxDir = "",
  [switch]$SkipAdmin
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}

# версия установщика (меняется вместе с файлом VERSION и CHANGELOG.md)
$Version = "1.16.0"
$Here = $PSScriptRoot
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$Ru = $true
try { $Ru = (Get-UICulture).Name -like "ru*" } catch {}
function T($ru, $en) { if ($Ru) { $ru } else { $en } }

$script:GuiLog = $null
$script:GuiWindow = $null
function Say($text, $color = "Gray") {
  if ($script:GuiLog) {
    $script:GuiLog.Text += "$text`n"
    $script:GuiLog.Parent.ScrollToEnd()
    $script:GuiWindow.Dispatcher.Invoke([action] {}, "Render")
  } else {
    Write-Host $text -ForegroundColor $color
  }
}

# ================================================================ темы
$Themes = [ordered]@{
  oneui    = @{ Name = "One UI";            Desc = (T "Samsung Galaxy: чёрный фон, «таблетки», акцент Windows" "Samsung Galaxy: pure black, pills, Windows accent") }
  ios      = @{ Name = "iOS · Liquid Glass"; Desc = (T "iOS 26: жидкое стекло, обои под окном, стеклянные часы" "iOS 26: Liquid Glass, wallpaper, glass clock") }
  material = @{ Name = "Material You";      Desc = (T "Android / Pixel: тональные цвета из акцента, часы столбиком" "Android / Pixel: tonal colors, stacked clock") }
  fluent   = @{ Name = "Windows 11";        Desc = (T "Fluent: строгие углы, акцентная полоска, обои Bloom" "Fluent: crisp corners, accent underline, Bloom wallpaper") }
  macos    = @{ Name = "macOS";             Desc = (T "Светофор вместо кнопок окна, синие меню, обои-волны" "Traffic-light window buttons, blue menus, wave wallpaper") }
  nothing  = @{ Name = "Nothing";           Desc = (T "Монохром, красная точка, часы из точек" "Monochrome, red dot, dot-matrix clock") }
  nightdrive = @{ Name = "Night Drive";     Desc = (T "Ночная дорога за запотевшим стеклом: размытые огни по краям, тонкие часы" "Night road behind a fogged window: blurred lights at the edges, thin clock") }
  aero     = @{ Name = "Aero";              Desc = (T "Windows 7: голубое стекло с бликом, глянцевые кнопки" "Windows 7: glossy blue glass, shiny buttons") }
  retro    = @{ Name = "Retro 98";          Desc = (T "Windows 98: серые выпуклые кнопки, синие заголовки, никаких скруглений" "Windows 98: grey bevelled buttons, navy title bars, no rounding") }
  terminal = @{ Name = "Terminal";          Desc = (T "Зелёный фосфор, моноширинный шрифт, строки развёртки" "Green phosphor, monospace font, scanlines") }
  paper    = @{ Name = "Paper";             Desc = (T "Тёплая бумага, шрифт с засечками, плоско и спокойно" "Warm paper, serif font, flat and calm") }
  cyber    = @{ Name = "Cyberpunk";         Desc = (T "Срезанные углы, жёлтый неон, розово-голубой город" "Cut corners, yellow neon, pink and cyan city") }
}

# ================================================================ браузеры (Firefox и форки)
# Pale Moon и Basilisk не поддерживаются: у них старый движок без userChrome Firefox 100+.
$Browsers = [ordered]@{
  floorp          = @{ Name = "Floorp";                     Exe = "floorp.exe";    Process = "floorp";    Profiles = "Floorp\Profiles";          Dirs = @("Ablaze Floorp") }
  firefox         = @{ Name = "Firefox";                    Exe = "firefox.exe";   Process = "firefox";   Profiles = "Mozilla\Firefox\Profiles"; Dirs = @("Mozilla Firefox") }
  "firefox-dev"   = @{ Name = "Firefox Developer Edition";  Exe = "firefox.exe";   Process = "firefox";   Profiles = "Mozilla\Firefox\Profiles"; Dirs = @("Firefox Developer Edition") }
  "firefox-nightly" = @{ Name = "Firefox Nightly";          Exe = "firefox.exe";   Process = "firefox";   Profiles = "Mozilla\Firefox\Profiles"; Dirs = @("Firefox Nightly") }
  librewolf       = @{ Name = "LibreWolf";                  Exe = "librewolf.exe"; Process = "librewolf"; Profiles = "librewolf\Profiles";       Dirs = @("LibreWolf") }
  waterfox        = @{ Name = "Waterfox";                   Exe = "waterfox.exe";  Process = "waterfox";  Profiles = "Waterfox\Profiles";        Dirs = @("Waterfox") }
  zen             = @{ Name = "Zen Browser";                Exe = "zen.exe";       Process = "zen";       Profiles = "zen\Profiles";             Dirs = @("Zen Browser") }
  mercury         = @{ Name = "Mercury";                    Exe = "mercury.exe";   Process = "mercury";   Profiles = "mercury\Profiles";         Dirs = @("Mercury") }
}

$overrides = @{}
foreach ($pair in ($Dirs -split ";")) {
  if ($pair -match "^\s*([\w-]+)\s*=\s*(.+?)\s*$") { $overrides[$Matches[1]] = $Matches[2] }
}
if ($FloorpDir) { $overrides["floorp"] = $FloorpDir }
if ($FirefoxDir) { $overrides["firefox"] = $FirefoxDir }
$testMode = $overrides.Count -gt 0

function Find-BrowserDir($key) {
  $b = $Browsers[$key]
  if ($testMode) {
    $o = $overrides[$key]
    if ($o -and (Test-Path (Join-Path $o $b.Exe))) { return $o }
    return $null
  }
  $candidates = @()
  if ($key -notlike "firefox-*") {
    foreach ($hive in @("HKLM:", "HKCU:")) {
      try {
        $exe = (Get-ItemProperty -Path "$hive\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\$($b.Exe)" -ErrorAction Stop).'(default)'
        if ($exe) {
          $d = Split-Path $exe.Trim('"') -Parent
          # firefox.exe из App Paths может оказаться Developer Edition или Nightly
          if ($key -ne "firefox" -or ($d -notmatch "Developer Edition|Nightly")) { $candidates += $d }
        }
      } catch {}
    }
  }
  foreach ($name in $b.Dirs) {
    $candidates += @("$env:ProgramFiles\$name", "${env:ProgramFiles(x86)}\$name", "$env:LOCALAPPDATA\$name", "$env:LOCALAPPDATA\Programs\$name")
  }
  foreach ($c in $candidates) {
    if ($c -and (Test-Path (Join-Path $c $b.Exe))) { return $c }
  }
  return $null
}

function Get-Profiles($key) {
  $root = Join-Path $UserAppData $Browsers[$key].Profiles
  if (-not (Test-Path $root)) { return @() }
  return @(Get-ChildItem $root -Directory | Where-Object { Test-Path (Join-Path $_.FullName "prefs.js") })
}

$found = [ordered]@{}
foreach ($key in $Browsers.Keys) {
  $dir = Find-BrowserDir $key
  if ($dir -and -not ($found.Values -contains $dir)) { $found[$key] = $dir }
}

# ================================================================ права администратора
function Test-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  return (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# ================================================================ файлы и блоки
function Read-Text($path) { if (Test-Path $path) { return [IO.File]::ReadAllText($path, $Utf8) } return "" }
function Write-Text($path, $text) { [IO.File]::WriteAllText($path, $text, $Utf8) }

$PdfRegex    = '(?s)\r?\n?/\*\s*=+\s*PDF-TWEAKS.*?PDF-TWEAKS END\s*=+\s*\*/\r?\n?'
$ModernRegex = '(?s)\r?\n?/\*\s*=+\s*FLOORP-MODERN BEGIN.*?FLOORP-MODERN END\s*=+\s*\*/\r?\n?'
$LoaderRegex = '(?s)\r?\n?// FLOORP-MODERN LOADER BEGIN.*?// FLOORP-MODERN LOADER END\r?\n?'
$UiRegex     = '(user_pref\("floorp\.design\.configs", ".*?\\"userInterface\\":\\")([a-z]+)(\\")'
$PrefComment = '// Floorp Modern: enables userChrome.css / userContent.css'
$PrefLine    = 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
$OurPrefs = @"
$PrefComment
$PrefLine
// Floorp Modern: Firefox Nova design, tabs expand on hover
user_pref("browser.nova.enabled", true);
user_pref("sidebar.visibility", "expand-on-hover");
// Floorp Modern: lets toolbar icons take the theme colour (without it Firefox draws them black)
user_pref("svg.context-properties.content.enabled", true);
"@

function Remove-OurBlocks($text) {
  $text = [regex]::Replace($text, $PdfRegex, "`n")
  return [regex]::Replace($text, $ModernRegex, "`n")
}
function Remove-OurPrefs($text) {
  $lines = $text -split "`r?`n" | Where-Object {
    $_ -notmatch 'toolkit\.legacyUserProfileCustomizations\.stylesheets|browser\.nova\.enabled|widget\.windows\.mica|sidebar\.visibility|svg\.context-properties\.content\.enabled|ui\.prefersReducedMotion|sidebar\.animation\.|floorp\.pdftweaks\.enabled|^// (Floorp PDF|Floorp Modern|Включает userChrome)'
  }
  return ($lines -join "`n")
}
# вставить надстройку перед END-маркером блока (одна замена)
function Add-Overlay($block, $overlay, $endName) {
  if (-not $overlay) { return $block }
  $rx = New-Object System.Text.RegularExpressions.Regex ('(/\*\s*=+\s*' + $endName + ')')
  $safe = $overlay.Replace('$', '$$')
  return $rx.Replace($block, ($safe.TrimEnd() + "`n`n`$1"), 1)
}
# задать или заменить user_pref в prefs.js
function Set-PrefLine($text, $name, $literal) {
  $line = "user_pref(""$name"", $literal);"
  $rx = '(?m)^user_pref\("' + [regex]::Escape($name) + '",[^\n]*$'
  if ([regex]::IsMatch($text, $rx)) { return [regex]::Replace($text, $rx, $line.Replace('$', '$$')) }
  return $text.TrimEnd() + "`n" + $line + "`n"
}

# ---------------------------------------------------------------- настройки темы
function New-Options {
  return @{
    Theme = "oneui"; Pdf = $true; Accent = "windows"; Mode = "keep"; Corners = "theme"; Motion = "apple"; Wall = "keep"; WallFile = ""
    NowBar = $true; Progress = $true; Center = $true; Clock = $true; Wallpaper = $true
  }
}
function Get-OnAccent($hex) {
  $n = [Convert]::ToInt32($hex.TrimStart('#'), 16)
  $r = ($n -shr 16) -band 255; $g = ($n -shr 8) -band 255; $b = $n -band 255
  if ((0.299 * $r + 0.587 * $g + 0.114 * $b) -gt 160) { return "#000000" } else { return "#ffffff" }
}
# обои новой вкладки (те же ключи, что в FloorpPdfTweaksChild.sys.mjs; цвета — для превью в установщике)
$WallPresets = [ordered]@{
  aurora   = @{ Name = (T "Аврора" "Aurora");   Colors = @("#6B4DFF", "#00B4FF", "#05060C") }
  iris     = @{ Name = (T "Ирис" "Iris");       Colors = @("#409CFF", "#7A3CC8", "#FF5C8C") }
  sunset   = @{ Name = (T "Закат" "Sunset");    Colors = @("#2B1055", "#7A2A7A", "#FF7E5F", "#FEB47B") }
  ocean    = @{ Name = (T "Океан" "Ocean");     Colors = @("#00C6FF", "#0072FF", "#021B3A") }
  forest   = @{ Name = (T "Лес" "Forest");      Colors = @("#A8E063", "#2F8F5B", "#0B2E22") }
  night    = @{ Name = (T "Ночь" "Night");      Colors = @("#0F2027", "#203A43", "#2C5364") }
  rose     = @{ Name = (T "Пудра" "Rose");      Colors = @("#F9C5D1", "#C7B5F0", "#9795EF") }
  graphite = @{ Name = (T "Графит" "Graphite"); Colors = @("#4A4D55", "#2A2C31", "#141518") }
  bloom    = @{ Name = "Bloom";                 Colors = @("#78AAFF", "#2864E6", "#0B1A3A") }
  dune     = @{ Name = (T "Дюна" "Dune");       Colors = @("#F2C98A", "#C07A3A", "#2A1810") }
}
$WallTypes = @{ ".jpg" = "image/jpeg"; ".jpeg" = "image/jpeg"; ".png" = "image/png"; ".webp" = "image/webp"; ".gif" = "image/gif"; ".bmp" = "image/bmp"; ".avif" = "image/avif" }
# применить выбор обоев к профилю (prefs.js уже прочитан в $prefs)
function Set-Wallpaper($o, $chrome, $prefs) {
  if ($o.WallFile) {
    $ext = [IO.Path]::GetExtension($o.WallFile).ToLower()
    if ((Test-Path -LiteralPath $o.WallFile) -and $WallTypes.Contains($ext)) {
      Copy-Item -LiteralPath $o.WallFile (Join-Path $chrome "pdf-tweaks\fm-wallpaper.img") -Force
      $prefs = Set-PrefLine $prefs "floorp.modern.wallpaper.type" ('"' + $WallTypes[$ext] + '"')
      $prefs = Set-PrefLine $prefs "floorp.modern.wallpaper.rev" ([string](Get-Random -Maximum 1000000))
      $prefs = Set-PrefLine $prefs "floorp.modern.wallpaper" '"custom"'
    } else {
      Say ((T "  ! картинка для обоев не найдена или не поддерживается: " "  ! wallpaper image not found or unsupported: ") + $o.WallFile) Yellow
    }
  } elseif ($o.Wall -eq "theme" -or $WallPresets.Contains([string]$o.Wall)) {
    $prefs = Set-PrefLine $prefs "floorp.modern.wallpaper" ('"' + $o.Wall + '"')
  }
  return $prefs
}

# пружины для режима анимаций «Как в iOS»
$SpringBounce = "linear(0, 0.0385, 0.135, 0.2646, 0.4078, 0.5501, 0.6814, 0.7955, 0.8894, 0.9626, 1.016, 1.0519, 1.073, 1.0823, 1.0828, 1.0772, 1.0676, 1.0561, 1.0441, 1.0325, 1.0222, 1.0134, 1.0063, 1.0009, 0.9972, 0.9947, 0.9934, 0.993, 0.9932, 0.9939, 0.9948, 0.9958, 0.9968, 0.9977, 0.9985, 0.9992, 0.9997, 1.0001, 1.0003, 1.0005, 1.0006, 1.0006, 1.0005, 1.0005, 1)"
$SpringSmooth = "linear(0, 0.0661, 0.2032, 0.3554, 0.4963, 0.6161, 0.7127, 0.7881, 0.8454, 0.8883, 0.9199, 0.9429, 0.9596, 0.9715, 0.98, 0.986, 0.9902, 0.9932, 0.9953, 0.9967, 0.9978, 0.9985, 0.9989, 0.9993, 1)"
# настройки анимаций браузера (user.js)
function Get-MotionPrefs($motion) {
  $l = @()
  switch ($motion) {
    "apple" {
      $l += 'user_pref("ui.prefersReducedMotion", 0);'
      $l += 'user_pref("sidebar.animation.enabled", true);'
      $l += 'user_pref("sidebar.animation.duration-ms", 320);'
      $l += 'user_pref("sidebar.animation.expand-on-hover.duration-ms", 380);'
      $l += 'user_pref("sidebar.animation.expand-on-hover.delay-duration-ms", 120);'
    }
    "smooth" {
      $l += 'user_pref("ui.prefersReducedMotion", 0);'
      $l += 'user_pref("sidebar.animation.enabled", true);'
    }
    "off" { $l += 'user_pref("ui.prefersReducedMotion", 1);' }
  }
  if ($l.Count) { $l = @("// Floorp Modern: animations ($motion)") + $l }
  return ($l -join "`n")
}
# CSS-блок «настройки из установщика»: вставляется после темы, поэтому важнее её
function Get-SettingsCss($o) {
  $chrome = @(); $content = @(); $global = @(); $pdf = @()
  if ($o.Accent -match '^#[0-9a-fA-F]{6}$') {
    $on = Get-OnAccent $o.Accent
    $global += ":root { --fm-user-accent: $($o.Accent) !important; --fm-user-on-accent: $on !important; }"
    $chrome += ":root, menupopup, panel, tooltip, #urlbar, .urlbarView { --fm-user-accent: $($o.Accent) !important; --fm-user-on-accent: $on !important; }"
  }
  $radius = @{ square = 6; standard = 18; round = 30 }[$o.Corners]
  if ($radius) {
    $menu = [math]::Min($radius + 2, 26)
    $chrome += ":root { --fm-radius: ${radius}px !important; }"
    $chrome += ":root:not([inDOMFullscreen], [inFullscreen]) #tabbrowser-tabpanels .browserContainer { border-radius: ${radius}px !important; }"
    $chrome += "menupopup::part(content), panel::part(content) { border-radius: ${menu}px !important; }"
    $content += "  :is(setting-group, groupbox):not([hidden]), .card, .addon.card, moz-card { border-radius: ${radius}px !important; }"
  }
  if ($o.Motion -eq "apple") {
    # настоящие пружины (затухающие колебания), посчитанные заранее: лёгкий перелёт ~8 %, как в iOS
    $vars = "--fm-spring: $SpringBounce !important; --fm-ease: $SpringSmooth !important; --fm-k: 1.15 !important;"
    $chrome += ":root { $vars }"
    $global += ":root { $vars }"
  }
  if (-not $o.NowBar)   { $chrome += ".fm-nowbar { display: none !important; }" }
  if (-not $o.Progress) { $chrome += ".fm-progress { display: none !important; }" }
  if (-not $o.Center)   { $chrome += ":root #urlbar:not([focused], [open]) #urlbar-input, :root moz-urlbar:not([focused], [open]) .urlbar-input { text-align: start !important; }" }
  $newtab = @()
  if (-not $o.Clock)     { $newtab += "  .absolute.top-4.right-4 { display: none !important; }"; $newtab += "  :root:has(#fm-clock) .outer-wrapper { padding-top: revert !important; }" }
  if (-not $o.Wallpaper) { $newtab += "  #root::before { animation: none !important; }" }

  # всё в слое fm-settings: настройки сильнее темы, а Studio (слой fm-studio) — сильнее настроек
  $head = "/* ---------------- Настройки из установщика ---------------- */"
  $order = "@layer fm-studio, fm-settings;"
  $c = @($head, $order, "@layer fm-settings {") + $chrome + @("}")
  $t = @($head, $order, "@layer fm-settings {") + $global + @("}")
  if ($content.Count) { $t += '@-moz-document url-prefix("about:"), url-prefix("chrome://browser/content/") {'; $t += "@layer fm-settings {"; $t += $content; $t += "}"; $t += "}" }
  if ($newtab.Count) { $t += '@-moz-document url-prefix("chrome://noraneko-newtab/"), url("about:newtab"), url("about:home") {'; $t += "@layer fm-settings {"; $t += $newtab; $t += "}"; $t += "}" }
  if ($o.Corners -eq "none") {
    # без скруглений вообще: окно, меню, вкладки, страницы браузера, новая вкладка, PDF
    $c += (Read-Text (Join-Path $Here "pdf-tweaks\square-chrome.css")).Replace("@layer LAYER", "@layer fm-settings")
    $t += (Read-Text (Join-Path $Here "pdf-tweaks\square-content.css")).Replace("@layer LAYER", "@layer fm-settings")
  }
  return @{ Chrome = ($c -join "`n"); Content = ($t -join "`n") }
}

function Get-Blocks($o) {
  $chrome  = Read-Text (Join-Path $Here "floorp-modern-chrome.css")
  $content = Read-Text (Join-Path $Here "floorp-modern-content.css")
  $pdf     = Read-Text (Join-Path $Here "pdf-viewer-theme.css")
  # тема вписывается между метками FM-THEME BEGIN/END — браузер умеет менять её сам (кнопка «Дизайн»)
  $tdir = Join-Path $Here "pdf-tweaks\themes"
  foreach ($part in @("chrome", "content", "pdf")) {
    if (-not (Test-Path (Join-Path $tdir "$($o.Theme)-$part.css"))) { throw (T "нет файла темы pdf-tweaks\themes\$($o.Theme)-$part.css" "missing theme file pdf-tweaks\themes\$($o.Theme)-$part.css") }
  }
  $chrome  = Add-Overlay $chrome  (Read-Text (Join-Path $tdir "$($o.Theme)-chrome.css"))  "FLOORP-MODERN END"
  $content = Add-Overlay $content (Read-Text (Join-Path $tdir "$($o.Theme)-content.css")) "FLOORP-MODERN END"
  $pdf     = Add-Overlay $pdf     (Read-Text (Join-Path $tdir "$($o.Theme)-pdf.css"))     "PDF-TWEAKS END"
  $s = Get-SettingsCss $o
  $chrome  = Add-Overlay $chrome  $s.Chrome  "FLOORP-MODERN END"
  $content = Add-Overlay $content $s.Content "FLOORP-MODERN END"
  return @{ Chrome = $chrome; Content = $content; Pdf = $pdf }
}

# ---------------------------------------------------------------- загрузчик скриптов в папке браузера
# Обычно кладём config.js + defaults\pref\config-prefs.js. Если у браузера уже
# свой autoconfig (LibreWolf: librewolf.cfg), дописываем наш загрузчик в его файл
# между метками, чтобы не сломать его настройки.
function Get-ForeignCfg($appDir) {
  $prefDir = Join-Path $appDir "defaults\pref"
  if (-not (Test-Path $prefDir)) { return $null }
  foreach ($f in Get-ChildItem $prefDir -Filter *.js -File) {
    if ($f.Name -eq "config-prefs.js") { continue }
    $m = [regex]::Match((Read-Text $f.FullName), 'pref\(\s*"general\.config\.filename"\s*,\s*"([^"]+)"')
    if ($m.Success -and $m.Groups[1].Value -ne "config.js") { return (Join-Path $appDir $m.Groups[1].Value) }
  }
  return $null
}
function Install-Loader($appDir) {
  $cfg = Get-ForeignCfg $appDir
  if ($cfg) {
    $code = (Read-Text (Join-Path $Here "config.js")).TrimEnd()
    $text = [regex]::Replace((Read-Text $cfg), $LoaderRegex, "`n")
    if (-not $text) { $text = "// autoconfig`n" }
    Write-Text $cfg ($text.TrimEnd() + "`n`n// FLOORP-MODERN LOADER BEGIN`n" + $code + "`n// FLOORP-MODERN LOADER END`n")
    return (T "загрузчик дописан в " "loader added to ") + (Split-Path $cfg -Leaf)
  }
  Copy-Item (Join-Path $Here "config.js") (Join-Path $appDir "config.js") -Force
  $prefDir = Join-Path $appDir "defaults\pref"
  New-Item -ItemType Directory -Force -Path $prefDir | Out-Null
  Copy-Item (Join-Path $Here "config-prefs.js") (Join-Path $prefDir "config-prefs.js") -Force
  return (T "загрузчик скриптов" "script loader")
}
function Remove-Loader($appDir) {
  $cfg = Get-ForeignCfg $appDir
  if ($cfg -and (Test-Path $cfg)) {
    Write-Text $cfg (([regex]::Replace((Read-Text $cfg), $LoaderRegex, "`n")).TrimEnd() + "`n")
  }
  foreach ($f in @((Join-Path $appDir "config.js"), (Join-Path $appDir "defaults\pref\config-prefs.js"))) {
    if (Test-Path $f) {
      # чужой config.js (не наш) не трогаем
      if ((Split-Path $f -Leaf) -eq "config.js" -and (Read-Text $f) -notmatch "Floorp Modern loader") { continue }
      Remove-Item $f -Force
    }
  }
}

function Close-Browser($key) {
  $b = $Browsers[$key]
  $procs = Get-Process -Name $b.Process -ErrorAction SilentlyContinue
  if (-not $procs) { return $true }
  if ($SkipAdmin) { return $true }
  if ($script:GuiWindow) {
    $msg = T "$($b.Name) сейчас открыт. Закрыть его, чтобы применить оформление?`n(Вкладки восстановятся при следующем запуске.)" `
             "$($b.Name) is running. Close it to apply the theme?`n(Tabs are restored on next start.)"
    $r = [System.Windows.MessageBox]::Show($msg, "Redesigned Fox", "YesNo", "Question")
    if ($r -ne "Yes") { return $false }
    foreach ($p in $procs) { try { [void]$p.CloseMainWindow() } catch {} }
    for ($i = 0; $i -lt 16 -and (Get-Process -Name $b.Process -ErrorAction SilentlyContinue); $i++) {
      Start-Sleep -Milliseconds 500
      $script:GuiWindow.Dispatcher.Invoke([action] {}, "Render")
    }
    Get-Process -Name $b.Process -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 600
    return $true
  }
  while (Get-Process -Name $b.Process -ErrorAction SilentlyContinue) {
    Say ""
    Say (T "$($b.Name) сейчас открыт. Закройте все его окна и нажмите Enter." "$($b.Name) is running. Close all its windows and press Enter.") Yellow
    Say (T "(или введите «п» и Enter, чтобы продолжить так — тогда перезапустите браузер потом)" "(or type 's' and Enter to skip — then restart the browser later)") DarkGray
    $answer = Read-Host
    if ($answer -match '^[pпPПsS]') { return $true }
  }
  return $true
}

# ================================================================ установка / удаление
function Invoke-Modern($action, $keys, $o) {
  $ok = $true
  $blocks = if ($action -eq "install") { Get-Blocks $o } else { $null }
  $doneRoots = @{}
  foreach ($key in $keys) {
    $b = $Browsers[$key]
    $appDir = $found[$key]
    Say ""
    Say "— $($b.Name) —" Cyan
    if (-not $appDir) { Say (T "  не установлен, пропускаю" "  not installed, skipping") Red; continue }
    $profiles = Get-Profiles $key
    if ($profiles.Count -eq 0) {
      Say (T "  нет профилей — запустите $($b.Name) хотя бы раз" "  no profiles — start $($b.Name) at least once") Red
      $ok = $false; continue
    }
    if (-not (Close-Browser $key)) { Say (T "  пропущено: браузер открыт" "  skipped: browser is running") Yellow; $ok = $false; continue }

    try {
      if ($action -eq "install") {
        Say ("  ✓ " + (Install-Loader $appDir)) Green
      } else {
        Remove-Loader $appDir
        Say (T "  ✓ загрузчик удалён" "  ✓ loader removed") Green
      }
      # у Firefox, Developer Edition и Nightly общая папка профилей — обрабатываем её один раз
      $root = Join-Path $UserAppData $b.Profiles
      if ($doneRoots[$root]) { Say (T "  ✓ профили уже обработаны выше" "  ✓ profiles already handled above") Green; continue }
      $doneRoots[$root] = $true

      foreach ($p in $profiles) {
        $chrome = Join-Path $p.FullName "chrome"
        $userJs = Join-Path $p.FullName "user.js"
        $prefsJs = Join-Path $p.FullName "prefs.js"
        if ($action -eq "install") {
          New-Item -ItemType Directory -Force -Path $chrome | Out-Null
          $dst = Join-Path $chrome "pdf-tweaks"
          New-Item -ItemType Directory -Force -Path $dst | Out-Null
          Copy-Item (Join-Path $Here "pdf-tweaks\*") $dst -Recurse -Force

          foreach ($pair in @(
              @{ File = "userContent.css"; Blocks = $(if ($o.Pdf) { @($blocks.Content, $blocks.Pdf) } else { @($blocks.Content) }) },
              @{ File = "userChrome.css";  Blocks = @($blocks.Chrome) })) {
            $path = Join-Path $chrome $pair.File
            $text = Read-Text $path
            if ($text -and -not (Test-Path "$path.bak-floorp-modern")) { Copy-Item $path "$path.bak-floorp-modern" }
            $text = Remove-OurBlocks $text
            foreach ($blk in $pair.Blocks) { $text = $text.TrimEnd() + "`n`n" + $blk.Trim() + "`n" }
            Write-Text $path $text.TrimStart()
          }
          Write-Text (Join-Path $chrome "floorp-modern-theme.txt") $o.Theme
          Write-Text (Join-Path $chrome "floorp-modern-version.txt") $Version
          Write-Text (Join-Path $chrome "floorp-modern-settings.json") ($o | ConvertTo-Json -Compress)

          $u = Remove-OurPrefs (Read-Text $userJs)
          $pdfPref = "// Floorp Modern: new PDF viewer on/off`nuser_pref(""floorp.pdftweaks.enabled"", $(if ($o.Pdf) { 'true' } else { 'false' }));"
          $motionPrefs = Get-MotionPrefs $o.Motion
          if ($motionPrefs) { $pdfPref += "`n" + $motionPrefs }
          Write-Text $userJs ($u.TrimEnd() + "`n" + $OurPrefs.Trim() + "`n" + $pdfPref + "`n").TrimStart()

          $prefs = Read-Text $prefsJs
          $prefs = [regex]::Replace($prefs, '(?m)^user_pref\("widget\.windows\.mica[a-z.-]*",[^\n]*\n', '')
          if ($o.Motion -eq "system") { $prefs = [regex]::Replace($prefs, '(?m)^user_pref\("(ui\.prefersReducedMotion|sidebar\.animation\.[a-z.-]+)",[^\n]*\n', '') }
          $prefs = Set-PrefLine $prefs "floorp.modern.nowbar" $(if ($o.NowBar) { "true" } else { "false" })
          $prefs = Set-Wallpaper $o $chrome $prefs
          $prefs = Set-PrefLine $prefs "floorp.modern.version" ('"' + $Version + '"')
          $prefs = Set-PrefLine $prefs "floorp.modern.theme" ('"' + $o.Theme + '"')
          if ($o.Mode -ne "keep") {
            $v = @{ dark = 0; light = 1; auto = 2 }[$o.Mode]
            $prefs = Set-PrefLine $prefs "browser.theme.toolbar-theme" $v
            $prefs = Set-PrefLine $prefs "browser.theme.content-theme" $v
          }
          if ($key -eq "floorp") {
            $m = [regex]::Match($prefs, $UiRegex)
            if ($m.Success -and $m.Groups[2].Value -ne "proton") {
              $backup = Join-Path $chrome "floorp-modern-previous-ui.txt"
              if (-not (Test-Path $backup)) { Write-Text $backup $m.Groups[2].Value }
              $prefs = [regex]::Replace($prefs, $UiRegex, '${1}proton${3}')
            }
          }
          Write-Text $prefsJs $prefs
          Say ((T "  ✓ профиль " "  ✓ profile ") + $p.Name) Green
        } else {
          $dst = Join-Path $chrome "pdf-tweaks"
          if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
          foreach ($file in @("userContent.css", "userChrome.css")) {
            $path = Join-Path $chrome $file
            if (Test-Path $path) { Write-Text $path ((Remove-OurBlocks (Read-Text $path)).TrimEnd() + "`n") }
          }
          foreach ($f in @("floorp-modern-theme.txt", "floorp-modern-version.txt", "floorp-modern-settings.json")) {
            $x = Join-Path $chrome $f
            if (Test-Path $x) { Remove-Item $x -Force }
          }
          if (Test-Path $userJs) {
            $u = Remove-OurPrefs (Read-Text $userJs)
            Write-Text $userJs ($u.TrimEnd() + "`n$PrefComment`n$PrefLine`n").TrimStart()
          }
          $prefs = Read-Text $prefsJs
          $prefs = [regex]::Replace($prefs, '(?m)^user_pref\("(browser\.nova\.enabled|widget\.windows\.mica[a-z.-]*|sidebar\.visibility|sidebar\.animation\.[a-z.-]+|ui\.prefersReducedMotion|svg\.context-properties\.content\.enabled|floorp\.pdftweaks\.enabled|floorp\.modern\.[a-z.]+)",[^\n]*\n', '')
          $backup = Join-Path $chrome "floorp-modern-previous-ui.txt"
          if (Test-Path $backup) {
            $old = (Read-Text $backup).Trim()
            if ($old -match '^[a-z]+$') { $prefs = [regex]::Replace($prefs, $UiRegex, '${1}' + $old + '${3}') }
            Remove-Item $backup -Force
          }
          Write-Text $prefsJs $prefs
          Say ((T "  ✓ профиль очищен: " "  ✓ profile cleaned: ") + $p.Name) Green
        }
      }
    } catch {
      Say ((T "  ✗ ошибка: " "  ✗ error: ") + $_.Exception.Message) Red
      $ok = $false
    }
  }
  return $ok
}

# прошлые настройки (из первого найденного профиля) — чтобы окно открывалось с ними
function Get-SavedOptions {
  $o = New-Options
  foreach ($key in $found.Keys) {
    foreach ($p in (Get-Profiles $key)) {
      $f = Join-Path $p.FullName "chrome\floorp-modern-settings.json"
      if (Test-Path $f) {
        try {
          $j = (Read-Text $f) | ConvertFrom-Json
          foreach ($k in @($o.Keys)) { if ($null -ne $j.$k) { $o[$k] = $j.$k } }
          if (-not $Themes.Contains([string]$o.Theme)) { $o.Theme = "oneui" }
          return $o
        } catch {}
      }
    }
  }
  return $o
}

# ================================================================ окно установщика (стекло Windows 11)
function Get-WindowsAccent {
  try {
    $v = [uint32](Get-ItemProperty "HKCU:\Software\Microsoft\Windows\DWM" -Name AccentColor -ErrorAction Stop).AccentColor
    $r = [byte]($v -band 0xFF); $g = [byte](($v -shr 8) -band 0xFF); $b = [byte](($v -shr 16) -band 0xFF)
    $mix = { param($c) [byte]([math]::Round($c * 0.7 + 255 * 0.3)) }
    return [Windows.Media.Color]::FromRgb((& $mix $r), (& $mix $g), (& $mix $b))
  } catch {
    return [Windows.Media.Color]::FromRgb(0x4C, 0x9A, 0xFF)
  }
}

# как выглядит каждая тема в превью окна установщика
$PreviewLook = @{
  oneui    = @{ Frame = @("#000000");                         Bar = "#1F2022"; BarR = 13; Card = @("#0B0C12", "#16245A", "#3A1E66"); CardR = 14; Clock = "Light";    Font = "Segoe UI Variable Display"; ClockFg = "#FFFFFF"; Search = "#E6161719"; SearchR = 11; Lights = $false; Swatch = @("#000000", "#1F2022") }
  ios      = @{ Frame = @("#2F7BFF", "#2A1C8C", "#FF5C8C");   Bar = "#30FFFFFF"; BarR = 13; Card = @("#3C8CFF", "#2A1C8C", "#FF5C8C"); CardR = 16; Clock = "Bold";   Font = "Segoe UI Variable Display"; ClockFg = "#D9FFFFFF"; Search = "#26FFFFFF"; SearchR = 12; Lights = $false; Swatch = @("#2F7BFF", "#7A3CC8", "#FF5C8C") }
  material = @{ Frame = @("#14171C");                         Bar = "#2A2F3A"; BarR = 13; Card = @("#1C2433", "#2B3D66", "#6B5A8A"); CardR = 18; Clock = "Normal";   Font = "Segoe UI Variable Display"; ClockFg = "#C9D8FF"; Search = "#2B3550"; SearchR = 12; Lights = $false; Swatch = @("#2B3D66", "#C9D8FF") }
  fluent   = @{ Frame = @("#202020");                         Bar = "#2D2D2D"; BarR = 4;  Card = @("#07122B", "#2860E6", "#0A1838"); CardR = 6;  Clock = "SemiBold"; Font = "Segoe UI Variable Display"; ClockFg = "#FFFFFF"; Search = "#E6202020"; SearchR = 5;  Lights = $false; Swatch = @("#0B2A6B", "#78AAFF") }
  macos    = @{ Frame = @("#1F1E23");                         Bar = "#38373D"; BarR = 7;  Card = @("#3A1D5C", "#C846A0", "#FF8C3C"); CardR = 9;  Clock = "SemiBold"; Font = "Segoe UI Variable Display"; ClockFg = "#EBFFFFFF"; Search = "#29FFFFFF"; SearchR = 8;  Lights = $true;  Swatch = @("#3A1D5C", "#FF8C3C") }
  nothing  = @{ Frame = @("#000000");                         Bar = "#000000"; BarR = 13; Card = @("#000000", "#000000", "#0D0D0D"); CardR = 14; Clock = "Black";    Font = "Consolas";                  ClockFg = "#FFFFFF"; Search = "#000000"; SearchR = 11; Lights = $false; Swatch = @("#000000", "#D71921") }
  nightdrive = @{ Frame = @("#07080D");                       Bar = "#151822"; BarR = 7;  Card = @("#3A0A0A", "#05060B", "#3A2A0A"); CardR = 12; Clock = "Light";    Font = "Segoe UI Variable Display"; ClockFg = "#F0FFFFFF"; Search = "#14FFFFFF"; SearchR = 8;  Lights = $false; Swatch = @("#FF3C32", "#05060B", "#FFB25B") }
  aero     = @{ Frame = @("#9FC2EA", "#C9DCF2");              Bar = "#C0FFFFFF"; BarR = 3; Card = @("#0B4FA8", "#3FA0E0", "#0A2F6B"); CardR = 5;  Clock = "Light";    Font = "Segoe UI";                  ClockFg = "#FFFFFF"; Search = "#80FFFFFF"; SearchR = 4;  Lights = $false; Swatch = @("#5AA2EC", "#1F62B5") }
  retro    = @{ Frame = @("#C0C0C0");                         Bar = "#FFFFFF"; BarR = 0;  Card = @("#008080");                       CardR = 0;  Clock = "Bold";     Font = "Courier New";               ClockFg = "#000000"; Search = "#FFFFFF"; SearchR = 0;  Lights = $false; Swatch = @("#C0C0C0", "#000080") }
  terminal = @{ Frame = @("#030603");                         Bar = "#000000"; BarR = 1;  Card = @("#010301", "#0F3A18", "#010301"); CardR = 1;  Clock = "Normal";   Font = "Consolas";                  ClockFg = "#5CFF85"; Search = "#000000"; SearchR = 0;  Lights = $false; Swatch = @("#000000", "#33FF66") }
  paper    = @{ Frame = @("#EFE9DE");                         Bar = "#FFFDF8"; BarR = 3;  Card = @("#FBF7EF", "#ECE4D5");            CardR = 4;  Clock = "Normal";   Font = "Georgia";                   ClockFg = "#2B2622"; Search = "#00FFFFFF"; SearchR = 0;  Lights = $false; Swatch = @("#F4EFE6", "#B4532A") }
  cyber    = @{ Frame = @("#0B0912");                         Bar = "#1A1526"; BarR = 0;  Card = @("#0A0614", "#4A0B4E", "#07050D"); CardR = 2;  Clock = "Bold";     Font = "Bahnschrift";               ClockFg = "#FCEE0A"; Search = "#D90A0614"; SearchR = 0;  Lights = $false; Swatch = @("#FCEE0A", "#FF00AA", "#00F0FF") }
}
$AccentPresets = @("#0A84FF", "#8E6BFF", "#FF375F", "#FF453A", "#FF9F0A", "#30D158", "#40C8E0", "#8E8E93")

function Show-Gui {
  Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase
  $xaml = @'
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Redesigned Fox" Width="540" SizeToContent="Height" WindowStartupLocation="CenterScreen"
        ResizeMode="NoResize" Background="Transparent"
        FontFamily="Segoe UI Variable Display, Segoe UI" UseLayoutRounding="True" TextOptions.TextFormattingMode="Display">
  <WindowChrome.WindowChrome>
    <WindowChrome CaptionHeight="0" ResizeBorderThickness="0" GlassFrameThickness="-1" CornerRadius="0" UseAeroCaptionButtons="False"/>
  </WindowChrome.WindowChrome>
  <Window.Resources>
    <SolidColorBrush x:Key="Accent" Color="#4C9AFF"/>
    <SolidColorBrush x:Key="SwitchOn" Color="#4C9AFF"/>
    <SolidColorBrush x:Key="Ink" Color="#FFFFFFFF"/>
    <SolidColorBrush x:Key="Muted" Color="#99EBEBF5"/>
    <LinearGradientBrush x:Key="Rim" StartPoint="0,0" EndPoint="0,1">
      <GradientStop Color="#66FFFFFF" Offset="0"/>
      <GradientStop Color="#14FFFFFF" Offset="0.45"/>
      <GradientStop Color="#26FFFFFF" Offset="1"/>
    </LinearGradientBrush>
    <LinearGradientBrush x:Key="Sheen" StartPoint="0,0" EndPoint="0,1">
      <GradientStop Color="#24FFFFFF" Offset="0"/>
      <GradientStop Color="#0DFFFFFF" Offset="0.6"/>
      <GradientStop Color="#12FFFFFF" Offset="1"/>
    </LinearGradientBrush>

    <Style x:Key="Cell" TargetType="Border">
      <Setter Property="CornerRadius" Value="18"/>
      <Setter Property="Background" Value="{StaticResource Sheen}"/>
      <Setter Property="BorderBrush" Value="{StaticResource Rim}"/>
      <Setter Property="BorderThickness" Value="1"/>
    </Style>
    <Style x:Key="Caption" TargetType="TextBlock">
      <Setter Property="Foreground" Value="{StaticResource Muted}"/>
      <Setter Property="FontSize" Value="12"/>
      <Setter Property="FontWeight" Value="SemiBold"/>
      <Setter Property="Margin" Value="16,16,0,7"/>
    </Style>
    <Style x:Key="RowTitle" TargetType="TextBlock">
      <Setter Property="Foreground" Value="{StaticResource Ink}"/>
      <Setter Property="FontSize" Value="15"/>
      <Setter Property="FontWeight" Value="SemiBold"/>
    </Style>
    <Style x:Key="RowHint" TargetType="TextBlock">
      <Setter Property="Foreground" Value="{StaticResource Muted}"/>
      <Setter Property="FontSize" Value="12"/>
      <Setter Property="TextWrapping" Value="Wrap"/>
      <Setter Property="Margin" Value="0,1,66,0"/>
    </Style>

    <!-- переключатель с «пружинкой» -->
    <Style x:Key="Switch" TargetType="CheckBox">
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="HorizontalAlignment" Value="Right"/>
      <Setter Property="VerticalAlignment" Value="Center"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="CheckBox">
            <Border x:Name="Track" Width="52" Height="32" CornerRadius="16" Background="#33FFFFFF" BorderBrush="#22FFFFFF" BorderThickness="1">
              <Ellipse x:Name="Knob" Width="26" Height="26" Fill="White" Margin="2,0,0,0" HorizontalAlignment="Left" VerticalAlignment="Center">
                <Ellipse.RenderTransform><TranslateTransform x:Name="KnobMove" X="0"/></Ellipse.RenderTransform>
                <Ellipse.Effect><DropShadowEffect BlurRadius="8" ShadowDepth="1" Opacity="0.3"/></Ellipse.Effect>
              </Ellipse>
            </Border>
            <ControlTemplate.Triggers>
              <Trigger Property="IsChecked" Value="True">
                <Setter TargetName="Track" Property="Background" Value="{DynamicResource SwitchOn}"/>
                <Trigger.EnterActions>
                  <BeginStoryboard>
                    <Storyboard>
                      <DoubleAnimation Storyboard.TargetName="KnobMove" Storyboard.TargetProperty="X" To="20" Duration="0:0:0.32">
                        <DoubleAnimation.EasingFunction><BackEase EasingMode="EaseOut" Amplitude="0.45"/></DoubleAnimation.EasingFunction>
                      </DoubleAnimation>
                    </Storyboard>
                  </BeginStoryboard>
                </Trigger.EnterActions>
                <Trigger.ExitActions>
                  <BeginStoryboard>
                    <Storyboard>
                      <DoubleAnimation Storyboard.TargetName="KnobMove" Storyboard.TargetProperty="X" To="0" Duration="0:0:0.32">
                        <DoubleAnimation.EasingFunction><BackEase EasingMode="EaseOut" Amplitude="0.45"/></DoubleAnimation.EasingFunction>
                      </DoubleAnimation>
                    </Storyboard>
                  </BeginStoryboard>
                </Trigger.ExitActions>
              </Trigger>
              <Trigger Property="IsEnabled" Value="False">
                <Setter TargetName="Track" Property="Opacity" Value="0.35"/>
              </Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>

    <!-- сегмент: выбранный — светлая «таблетка» -->
    <Style x:Key="Seg" TargetType="RadioButton">
      <Setter Property="Foreground" Value="White"/>
      <Setter Property="FontSize" Value="13"/>
      <Setter Property="FontWeight" Value="SemiBold"/>
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="RadioButton">
            <Border x:Name="B" CornerRadius="12" Background="Transparent" BorderThickness="1" BorderBrush="Transparent" Padding="4,8">
              <ContentPresenter HorizontalAlignment="Center" VerticalAlignment="Center"/>
            </Border>
            <ControlTemplate.Triggers>
              <Trigger Property="IsChecked" Value="True">
                <Setter TargetName="B" Property="Background" Value="#33FFFFFF"/>
                <Setter TargetName="B" Property="BorderBrush" Value="{StaticResource Rim}"/>
              </Trigger>
              <Trigger Property="IsMouseOver" Value="True"><Setter Property="Opacity" Value="0.92"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>

    <!-- карточка темы в галерее -->
    <Style x:Key="ThemeCard" TargetType="RadioButton">
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Margin" Value="5"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="RadioButton">
            <Border x:Name="B" CornerRadius="18" BorderThickness="2" BorderBrush="Transparent" Background="#14FFFFFF" Padding="6">
              <ContentPresenter/>
            </Border>
            <ControlTemplate.Triggers>
              <Trigger Property="IsChecked" Value="True">
                <Setter TargetName="B" Property="BorderBrush" Value="{DynamicResource Accent}"/>
                <Setter TargetName="B" Property="Background" Value="#24FFFFFF"/>
              </Trigger>
              <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="B" Property="Background" Value="#22FFFFFF"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>

    <!-- кружок цвета акцента -->
    <Style x:Key="Chip" TargetType="RadioButton">
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Margin" Value="0,0,8,8"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="RadioButton">
            <Grid Width="34" Height="34">
              <Ellipse x:Name="Ring" Stroke="Transparent" StrokeThickness="2"/>
              <Border Margin="5" CornerRadius="12" Background="{TemplateBinding Background}">
                <ContentPresenter HorizontalAlignment="Center" VerticalAlignment="Center"/>
              </Border>
            </Grid>
            <ControlTemplate.Triggers>
              <Trigger Property="IsChecked" Value="True"><Setter TargetName="Ring" Property="Stroke" Value="White"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>

    <Style x:Key="Primary" TargetType="Button">
      <Setter Property="Foreground" Value="White"/>
      <Setter Property="FontSize" Value="16"/>
      <Setter Property="FontWeight" Value="SemiBold"/>
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="Button">
            <Grid Height="50">
              <Border x:Name="Bg" CornerRadius="25" Background="{DynamicResource Accent}">
                <Border.Effect><DropShadowEffect BlurRadius="22" ShadowDepth="4" Opacity="0.4"/></Border.Effect>
              </Border>
              <Border CornerRadius="25" BorderThickness="1">
                <Border.Background>
                  <LinearGradientBrush StartPoint="0,0" EndPoint="0,1">
                    <GradientStop Color="#40FFFFFF" Offset="0"/>
                    <GradientStop Color="#00FFFFFF" Offset="0.6"/>
                  </LinearGradientBrush>
                </Border.Background>
                <Border.BorderBrush>
                  <LinearGradientBrush StartPoint="0,0" EndPoint="0,1">
                    <GradientStop Color="#80FFFFFF" Offset="0"/>
                    <GradientStop Color="#10FFFFFF" Offset="1"/>
                  </LinearGradientBrush>
                </Border.BorderBrush>
              </Border>
              <Border x:Name="Shade" CornerRadius="25" Background="#000000" Opacity="0"/>
              <ContentPresenter HorizontalAlignment="Center" VerticalAlignment="Center"/>
            </Grid>
            <ControlTemplate.Triggers>
              <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="Bg" Property="Opacity" Value="0.92"/></Trigger>
              <Trigger Property="IsPressed" Value="True"><Setter TargetName="Shade" Property="Opacity" Value="0.15"/></Trigger>
              <Trigger Property="IsEnabled" Value="False"><Setter Property="Opacity" Value="0.5"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>
    <Style x:Key="Link" TargetType="Button">
      <Setter Property="Foreground" Value="{DynamicResource Accent}"/>
      <Setter Property="FontSize" Value="14.5"/>
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="Button">
            <Border x:Name="B" Background="Transparent" CornerRadius="16" Padding="14,8"><ContentPresenter HorizontalAlignment="Center"/></Border>
            <ControlTemplate.Triggers>
              <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="B" Property="Background" Value="#14FFFFFF"/></Trigger>
              <Trigger Property="IsEnabled" Value="False"><Setter Property="Opacity" Value="0.4"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>
    <Style x:Key="Step" TargetType="Button">
      <Setter Property="Foreground" Value="{StaticResource Muted}"/>
      <Setter Property="FontSize" Value="13"/>
      <Setter Property="FontWeight" Value="SemiBold"/>
      <Setter Property="Cursor" Value="Hand"/>
      <Setter Property="Template">
        <Setter.Value>
          <ControlTemplate TargetType="Button">
            <Border x:Name="B" Background="Transparent" CornerRadius="14" Padding="12,6"><ContentPresenter HorizontalAlignment="Center"/></Border>
            <ControlTemplate.Triggers>
              <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="B" Property="Background" Value="#14FFFFFF"/></Trigger>
            </ControlTemplate.Triggers>
          </ControlTemplate>
        </Setter.Value>
      </Setter>
    </Style>
  </Window.Resources>

  <Grid x:Name="Root" Background="#3A0E0F14" RenderTransformOrigin="0.5,0.5">
    <Grid.RenderTransform><ScaleTransform x:Name="RootScale" ScaleX="0.96" ScaleY="0.96"/></Grid.RenderTransform>
    <Ellipse Width="340" Height="340" HorizontalAlignment="Left" VerticalAlignment="Top" Margin="-150,-160,0,0" Opacity="0.55" IsHitTestVisible="False">
      <Ellipse.Fill><RadialGradientBrush><GradientStop x:Name="GlowAColor" Color="#4C9AFF" Offset="0"/><GradientStop Color="#004C9AFF" Offset="1"/></RadialGradientBrush></Ellipse.Fill>
    </Ellipse>
    <Ellipse Width="320" Height="320" HorizontalAlignment="Right" VerticalAlignment="Top" Margin="0,-130,-160,0" Opacity="0.4" IsHitTestVisible="False">
      <Ellipse.Fill><RadialGradientBrush><GradientStop x:Name="GlowBColor" Color="#8E6BFF" Offset="0"/><GradientStop Color="#008E6BFF" Offset="1"/></RadialGradientBrush></Ellipse.Fill>
    </Ellipse>

    <Grid Margin="24,18,24,22">
      <StackPanel x:Name="MainPanel">
        <!-- шапка -->
        <Grid x:Name="DragArea" Background="Transparent">
          <Button x:Name="CloseBtn" HorizontalAlignment="Right" VerticalAlignment="Top" Width="32" Height="32" Cursor="Hand" Margin="0,-4,-10,0">
            <Button.Template>
              <ControlTemplate TargetType="Button">
                <Border x:Name="B" CornerRadius="16" Background="#1AFFFFFF" BorderBrush="{StaticResource Rim}" BorderThickness="1">
                  <TextBlock Text="✕" Foreground="#CCFFFFFF" FontSize="12" HorizontalAlignment="Center" VerticalAlignment="Center"/>
                </Border>
                <ControlTemplate.Triggers>
                  <Trigger Property="IsMouseOver" Value="True"><Setter TargetName="B" Property="Background" Value="#E0FF453A"/></Trigger>
                </ControlTemplate.Triggers>
              </ControlTemplate>
            </Button.Template>
          </Button>
          <StackPanel Orientation="Horizontal" Margin="0,6,0,0">
            <Border x:Name="AppIcon" Width="52" Height="52" CornerRadius="15" BorderBrush="{StaticResource Rim}" BorderThickness="1">
              <Border.Effect><DropShadowEffect BlurRadius="18" ShadowDepth="3" Opacity="0.4"/></Border.Effect>
              <TextBlock Text="F" Foreground="White" FontSize="27" FontWeight="Bold" HorizontalAlignment="Center" VerticalAlignment="Center"/>
            </Border>
            <StackPanel Margin="14,0,0,0" VerticalAlignment="Center">
              <StackPanel Orientation="Horizontal">
                <TextBlock Text="Redesigned Fox" Foreground="{StaticResource Ink}" FontSize="24" FontWeight="Bold"/>
                <Border CornerRadius="9" Background="#1FFFFFFF" BorderBrush="{StaticResource Rim}" BorderThickness="1" Padding="8,2" Margin="10,0,0,0" VerticalAlignment="Center">
                  <TextBlock x:Name="VersionLabel" Foreground="{StaticResource Muted}" FontSize="12" FontWeight="SemiBold"/>
                </Border>
              </StackPanel>
              <TextBlock x:Name="Subtitle" Foreground="{StaticResource Muted}" FontSize="13.5"/>
            </StackPanel>
          </StackPanel>
        </Grid>

        <!-- шаги -->
        <Border Style="{StaticResource Cell}" CornerRadius="16" Padding="3" Margin="0,16,0,0">
          <UniformGrid Columns="3">
            <Button x:Name="Step1" Style="{StaticResource Step}"/>
            <Button x:Name="Step2" Style="{StaticResource Step}"/>
            <Button x:Name="Step3" Style="{StaticResource Step}"/>
          </UniformGrid>
        </Border>

        <Grid Margin="0,4,0,0">
          <!-- 1. тема -->
          <StackPanel x:Name="Page1">
            <Border x:Name="PrevFrame" CornerRadius="20" Height="150" Margin="0,12,0,0" BorderBrush="#26FFFFFF" BorderThickness="1" ClipToBounds="True">
              <Grid Margin="11">
                <Grid.RowDefinitions><RowDefinition Height="28"/><RowDefinition Height="*"/></Grid.RowDefinitions>
                <StackPanel x:Name="PrevLights" Orientation="Horizontal" VerticalAlignment="Center" Margin="2,0,0,0">
                  <Ellipse Width="11" Height="11" Fill="#FF5F57"/>
                  <Ellipse Width="11" Height="11" Fill="#FEBC2E" Margin="6,0,0,0"/>
                  <Ellipse Width="11" Height="11" Fill="#28C840" Margin="6,0,0,0"/>
                </StackPanel>
                <StackPanel x:Name="PrevBtns" Orientation="Horizontal" VerticalAlignment="Center">
                  <Ellipse x:Name="PrevBtnA" Width="20" Height="20" Fill="#1F2022"/>
                  <Ellipse x:Name="PrevBtnB" Width="20" Height="20" Fill="#1F2022" Margin="6,0,0,0"/>
                </StackPanel>
                <Border x:Name="PrevBar" Height="24" CornerRadius="12" Background="#1F2022" BorderThickness="1.5" BorderBrush="{DynamicResource Accent}" Margin="66,0,30,0" VerticalAlignment="Center">
                  <TextBlock Text="floorp.app" Foreground="#C8FFFFFF" FontSize="11" HorizontalAlignment="Center" VerticalAlignment="Center"/>
                </Border>
                <Border x:Name="PrevCard" Grid.Row="1" CornerRadius="14" Margin="0,8,0,0" ClipToBounds="True">
                  <Grid>
                    <TextBlock x:Name="PrevClock" Text="18:18" FontSize="40" HorizontalAlignment="Center" VerticalAlignment="Top" Margin="0,2,0,0"/>
                    <Border x:Name="PrevSearch" Width="190" Height="22" CornerRadius="11" BorderBrush="#2AFFFFFF" BorderThickness="1" VerticalAlignment="Bottom" Margin="0,0,0,8"/>
                  </Grid>
                </Border>
              </Grid>
            </Border>
            <TextBlock x:Name="ThemeCaption" Style="{StaticResource Caption}"/>
            <UniformGrid x:Name="ThemeGrid" Columns="4" Margin="-5,0,-5,0"/>
            <TextBlock x:Name="ThemeHint" Foreground="{StaticResource Muted}" FontSize="13" Margin="16,8,16,0" TextWrapping="Wrap" MinHeight="34"/>
            <TextBlock x:Name="WallCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}" Padding="14,14,6,6">
              <StackPanel>
                <WrapPanel x:Name="WallChips"/>
                <TextBlock x:Name="WallHint" Foreground="{StaticResource Muted}" FontSize="12" Margin="2,0,8,8" TextWrapping="Wrap"/>
              </StackPanel>
            </Border>
          </StackPanel>

          <!-- 2. настройка -->
          <StackPanel x:Name="Page2" Visibility="Hidden">
            <TextBlock x:Name="AccentCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}" Padding="14,14,6,6">
              <StackPanel>
                <WrapPanel x:Name="AccentChips"/>
                <Grid x:Name="HexRow" Margin="0,2,8,8" Visibility="Collapsed">
                  <TextBlock x:Name="HexLabel" Foreground="{StaticResource Muted}" FontSize="13" VerticalAlignment="Center"/>
                  <Border CornerRadius="12" Background="#1AFFFFFF" BorderBrush="{StaticResource Rim}" BorderThickness="1" Width="140" HorizontalAlignment="Right">
                    <TextBox x:Name="HexBox" Text="#0A84FF" Background="Transparent" BorderThickness="0" Foreground="White" CaretBrush="White" FontFamily="Cascadia Mono, Consolas" FontSize="14" Padding="10,6" MaxLength="7"/>
                  </Border>
                </Grid>
              </StackPanel>
            </Border>
            <TextBlock x:Name="ModeCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}" CornerRadius="16" Padding="3">
              <UniformGrid Columns="4">
                <RadioButton x:Name="ModeKeep" Style="{StaticResource Seg}" GroupName="mode" IsChecked="True"/>
                <RadioButton x:Name="ModeAuto" Style="{StaticResource Seg}" GroupName="mode"/>
                <RadioButton x:Name="ModeLight" Style="{StaticResource Seg}" GroupName="mode"/>
                <RadioButton x:Name="ModeDark" Style="{StaticResource Seg}" GroupName="mode"/>
              </UniformGrid>
            </Border>
            <TextBlock x:Name="CornersCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}" CornerRadius="16" Padding="3">
              <UniformGrid Columns="5">
                <RadioButton x:Name="CornTheme" Style="{StaticResource Seg}" GroupName="corn" IsChecked="True"/>
                <RadioButton x:Name="CornNone" Style="{StaticResource Seg}" GroupName="corn"/>
                <RadioButton x:Name="CornSquare" Style="{StaticResource Seg}" GroupName="corn"/>
                <RadioButton x:Name="CornStandard" Style="{StaticResource Seg}" GroupName="corn"/>
                <RadioButton x:Name="CornRound" Style="{StaticResource Seg}" GroupName="corn"/>
              </UniformGrid>
            </Border>
            <TextBlock x:Name="MotionCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}" CornerRadius="16" Padding="3">
              <UniformGrid Columns="4">
                <RadioButton x:Name="MotApple" Style="{StaticResource Seg}" GroupName="motion" IsChecked="True"/>
                <RadioButton x:Name="MotSmooth" Style="{StaticResource Seg}" GroupName="motion"/>
                <RadioButton x:Name="MotSystem" Style="{StaticResource Seg}" GroupName="motion"/>
                <RadioButton x:Name="MotOff" Style="{StaticResource Seg}" GroupName="motion"/>
              </UniformGrid>
            </Border>
            <TextBlock x:Name="FeaturesCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}">
              <StackPanel x:Name="FeatureList"/>
            </Border>
          </StackPanel>

          <!-- 3. браузеры -->
          <StackPanel x:Name="Page3" Visibility="Hidden">
            <TextBlock x:Name="BrowsersCaption" Style="{StaticResource Caption}"/>
            <Border Style="{StaticResource Cell}">
              <ScrollViewer VerticalScrollBarVisibility="Auto" MaxHeight="300">
                <StackPanel x:Name="BrowserList"/>
              </ScrollViewer>
            </Border>
            <TextBlock x:Name="NotFound" Foreground="{StaticResource Muted}" FontSize="12" Margin="16,8,16,0" TextWrapping="Wrap"/>
            <TextBlock x:Name="Summary" Foreground="{StaticResource Ink}" FontSize="13" Margin="16,12,16,0" TextWrapping="Wrap"/>
            <Border x:Name="LogBox" Style="{StaticResource Cell}" Margin="0,14,0,0" Visibility="Collapsed" MaxHeight="150">
              <ScrollViewer VerticalScrollBarVisibility="Auto" Margin="16,10">
                <TextBlock x:Name="Log" Foreground="#D9FFFFFF" FontSize="12.5" TextWrapping="Wrap" FontFamily="Cascadia Mono, Consolas, Segoe UI"/>
              </ScrollViewer>
            </Border>
          </StackPanel>
        </Grid>

        <!-- кнопки -->
        <Grid Margin="0,20,0,0">
          <Grid.ColumnDefinitions><ColumnDefinition Width="Auto"/><ColumnDefinition Width="*"/></Grid.ColumnDefinitions>
          <Button x:Name="BackBtn" Style="{StaticResource Link}" VerticalAlignment="Center" Margin="0,0,12,0"/>
          <Button x:Name="NextBtn" Grid.Column="1" Style="{StaticResource Primary}"/>
        </Grid>
        <Button x:Name="UninstallBtn" Style="{StaticResource Link}" Margin="0,6,0,0" HorizontalAlignment="Center" Visibility="Hidden"/>
      </StackPanel>

      <!-- экран «Готово» -->
      <Grid x:Name="DonePanel" Visibility="Collapsed" Opacity="0">
        <StackPanel VerticalAlignment="Center">
          <Grid Width="112" Height="112" RenderTransformOrigin="0.5,0.5">
            <Grid.RenderTransform><ScaleTransform x:Name="DoneScale" ScaleX="0.4" ScaleY="0.4"/></Grid.RenderTransform>
            <Ellipse Fill="#30D158">
              <Ellipse.Effect><DropShadowEffect BlurRadius="40" ShadowDepth="0" Opacity="0.7" Color="#30D158"/></Ellipse.Effect>
            </Ellipse>
            <Ellipse Stroke="#80FFFFFF" StrokeThickness="1.5">
              <Ellipse.Fill>
                <LinearGradientBrush StartPoint="0,0" EndPoint="0,1">
                  <GradientStop Color="#55FFFFFF" Offset="0"/>
                  <GradientStop Color="#00FFFFFF" Offset="0.6"/>
                </LinearGradientBrush>
              </Ellipse.Fill>
            </Ellipse>
            <Path Data="M 34,58 L 50,74 L 80,40" Stroke="White" StrokeThickness="9" StrokeStartLineCap="Round" StrokeEndLineCap="Round" StrokeLineJoin="Round"/>
          </Grid>
          <TextBlock x:Name="DoneTitle" Foreground="{StaticResource Ink}" FontSize="28" FontWeight="Bold" HorizontalAlignment="Center" Margin="0,26,0,0"/>
          <TextBlock x:Name="DoneText" Foreground="{StaticResource Muted}" FontSize="14.5" HorizontalAlignment="Center" TextAlignment="Center" TextWrapping="Wrap" Margin="20,8,20,0"/>
          <Button x:Name="DoneBtn" Style="{StaticResource Primary}" Margin="0,30,0,0"/>
          <Button x:Name="DoneLogBtn" Style="{StaticResource Link}" Margin="0,8,0,0" HorizontalAlignment="Center"/>
        </StackPanel>
      </Grid>
    </Grid>
  </Grid>
</Window>
'@
  $window = [Windows.Markup.XamlReader]::Parse($xaml)
  $script:GuiWindow = $window
  $get = { param($n) $window.FindName($n) }
  $res = { param($k) $window.Resources[$k] }

  # ---------- стекло Windows 11 ----------
  $glass = $false
  try {
    if ([Environment]::OSVersion.Version.Build -ge 22621) {
      if (-not ("FloorpModern.Dwm" -as [type])) {
        Add-Type -Namespace FloorpModern -Name Dwm -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("dwmapi.dll")]
public static extern int DwmSetWindowAttribute(System.IntPtr hwnd, int attr, ref int value, int size);
'@
      }
      $hwnd = (New-Object System.Windows.Interop.WindowInteropHelper($window)).EnsureHandle()
      [System.Windows.Interop.HwndSource]::FromHwnd($hwnd).CompositionTarget.BackgroundColor = [Windows.Media.Colors]::Transparent
      $v = 1; [void][FloorpModern.Dwm]::DwmSetWindowAttribute($hwnd, 20, [ref]$v, 4)
      $v = 2; [void][FloorpModern.Dwm]::DwmSetWindowAttribute($hwnd, 33, [ref]$v, 4)
      $v = 3; $glass = ([FloorpModern.Dwm]::DwmSetWindowAttribute($hwnd, 38, [ref]$v, 4) -eq 0)
    }
  } catch { $glass = $false }
  if (-not $glass) {
    (& $get "Root").Background = New-Object Windows.Media.SolidColorBrush ([Windows.Media.Color]::FromRgb(0x12, 0x13, 0x17))
  }

  # ---------- помощники ----------
  $conv = New-Object Windows.Media.BrushConverter
  $color = { param($s) [Windows.Media.Color][Windows.Media.ColorConverter]::ConvertFromString($s) }
  $solid = { param($c) [Windows.Media.SolidColorBrush]::new([Windows.Media.Color]$c) }
  $grad = {
    param($list, $diag = $true)
    if ($list.Count -eq 1) { return [Windows.Media.Brush]$conv.ConvertFromString($list[0]) }
    $g = New-Object Windows.Media.LinearGradientBrush
    $g.StartPoint = "0,0"; $g.EndPoint = $(if ($diag) { "1,1" } else { "0,1" })
    for ($i = 0; $i -lt $list.Count; $i++) {
      $g.GradientStops.Add((New-Object Windows.Media.GradientStop ((& $color $list[$i]), ($i / [math]::Max(1, $list.Count - 1)))))
    }
    return [Windows.Media.Brush]$g
  }
  $ms = { param($n) New-Object System.Windows.Duration ([TimeSpan]::FromMilliseconds($n)) }
  $animate = {
    param($target, $prop, $to, $dur, $amp)
    $a = New-Object System.Windows.Media.Animation.DoubleAnimation
    $a.To = $to
    $a.Duration = & $ms $dur
    $e = New-Object System.Windows.Media.Animation.BackEase
    $e.EasingMode = "EaseOut"; $e.Amplitude = $amp
    $a.EasingFunction = $e
    $target.BeginAnimation($prop, $a)
  }
  $fadeIn = { param($el) $el.BeginAnimation([Windows.UIElement]::OpacityProperty, (New-Object System.Windows.Media.Animation.DoubleAnimation (0, 1, (& $ms 260)))) }
  $text = { param($t, $style) $tb = New-Object Windows.Controls.TextBlock; $tb.Text = $t; $tb.Style = & $res $style; $tb }
  $sep = { $b = New-Object Windows.Controls.Border; $b.Height = 1; $b.Background = & $solid (& $color "#1AFFFFFF"); $b.Margin = New-Object Windows.Thickness (18, 0, 0, 0); $b }
  $switchRow = {
    param($title, $hint, $checked)
    $g = New-Object Windows.Controls.Grid; $g.Margin = New-Object Windows.Thickness (18, 11, 14, 11)
    $sp = New-Object Windows.Controls.StackPanel; $sp.VerticalAlignment = [Windows.VerticalAlignment]::Center
    [void]$sp.Children.Add((& $text $title "RowTitle"))
    if ($hint) { [void]$sp.Children.Add((& $text $hint "RowHint")) }
    $cb = New-Object Windows.Controls.CheckBox; $cb.Style = & $res "Switch"; $cb.IsChecked = $checked
    [void]$g.Children.Add($sp); [void]$g.Children.Add($cb)
    return @{ Row = $g; Box = $cb; Hint = $sp }
  }

  # ---------- состояние ----------
  $opt = Get-SavedOptions
  # обои по умолчанию не трогаем: их могли сменить прямо на новой вкладке
  $opt.Wall = "keep"; $opt.WallFile = ""
  $winAccent = Get-WindowsAccent
  $state = @{ Page = 1 }

  # ---------- тексты ----------
  (& $get "VersionLabel").Text = "v$Version"
  $window.Title = "Redesigned Fox $Version"
  (& $get "Subtitle").Text = T "Новый вид для Floorp, Firefox и их форков" "A fresh look for Floorp, Firefox and forks"
  (& $get "Step1").Content = T "1  Тема" "1  Theme"
  (& $get "Step2").Content = T "2  Настройка" "2  Customize"
  (& $get "Step3").Content = T "3  Браузеры" "3  Browsers"
  (& $get "ThemeCaption").Text = T "ТЕМА" "THEME"
  (& $get "AccentCaption").Text = T "ЦВЕТ АКЦЕНТА" "ACCENT COLOR"
  (& $get "HexLabel").Text = T "Свой цвет (HEX)" "Custom color (HEX)"
  (& $get "ModeCaption").Text = T "СВЕТЛАЯ ИЛИ ТЁМНАЯ" "LIGHT OR DARK"
  (& $get "ModeKeep").Content = T "Не менять" "Keep"
  (& $get "ModeAuto").Content = T "Как в Windows" "System"
  (& $get "ModeLight").Content = T "Светлая" "Light"
  (& $get "ModeDark").Content = T "Тёмная" "Dark"
  (& $get "CornersCaption").Text = T "СКРУГЛЕНИЕ СТРАНИЦЫ И МЕНЮ" "PAGE AND MENU CORNERS"
  (& $get "CornTheme").Content = T "Как в теме" "Theme"
  (& $get "CornNone").Content = T "Без" "None"
  (& $get "CornSquare").Content = T "Строгие" "Square"
  (& $get "CornStandard").Content = T "Обычные" "Standard"
  (& $get "CornRound").Content = T "Круглые" "Round"
  (& $get "MotionCaption").Text = T "АНИМАЦИИ" "ANIMATIONS"
  (& $get "MotApple").Content = T "Как в iOS" "iOS springs"
  (& $get "MotSmooth").Content = T "Плавные" "Smooth"
  (& $get "MotSystem").Content = T "Как в Windows" "System"
  (& $get "MotOff").Content = T "Выкл" "Off"
  (& $get "MotApple").ToolTip = T "Пружинистые анимации с лёгким перелётом, как в iPhone. Включаются, даже если в Windows эффекты анимации выключены." "Springy iPhone-like motion, on even if Windows animations are off."
  (& $get "MotSystem").ToolTip = T "Анимации есть, только если в Windows включены эффекты анимации." "Animate only if Windows animation effects are on."
  (& $get "FeaturesCaption").Text = T "ФУНКЦИИ" "FEATURES"
  (& $get "BrowsersCaption").Text = T "КУДА УСТАНОВИТЬ" "INSTALL INTO"
  (& $get "BackBtn").Content = T "Назад" "Back"
  (& $get "UninstallBtn").Content = T "Удалить оформление" "Remove theme"
  (& $get "DoneBtn").Content = T "Закрыть" "Close"
  (& $get "DoneLogBtn").Content = T "Показать подробности" "Show details"

  # ---------- акцент ----------
  $currentAccent = {
    if ($opt.Accent -match '^#[0-9a-fA-F]{6}$') { return (& $color $opt.Accent) }
    if ($opt.Theme -in @("ios", "macos")) { return (& $color "#0A84FF") }
    if ($opt.Theme -eq "nothing") { return (& $color "#D71921") }
    return $winAccent
  }

  # ---------- превью и цвета окна ----------
  $applyLook = {
    $L = $PreviewLook[$opt.Theme]
    $acc = & $currentAccent
    $window.Resources["Accent"] = [Windows.Media.SolidColorBrush](& $solid $acc)
    $window.Resources["SwitchOn"] = [Windows.Media.SolidColorBrush]($(if ($opt.Theme -eq "ios") { & $solid (& $color "#30D158") } else { & $solid $acc }))
    (& $get "GlowAColor").Color = $acc
    $sw = $L.Swatch
    (& $get "GlowBColor").Color = & $color $sw[$sw.Count - 1]
    $icon = New-Object Windows.Media.LinearGradientBrush
    $icon.StartPoint = "0,0"; $icon.EndPoint = "1,1"
    $icon.GradientStops.Add((New-Object Windows.Media.GradientStop ($acc, 0)))
    $icon.GradientStops.Add((New-Object Windows.Media.GradientStop ((& $color $sw[$sw.Count - 1]), 1)))
    (& $get "AppIcon").Background = $icon

    $frame = & $get "PrevFrame"
    $frame.Background = & $grad $L.Frame
    $bar = & $get "PrevBar"
    $bar.Background = & $grad @($L.Bar)
    $bar.CornerRadius = New-Object Windows.CornerRadius ($L.BarR)
    $bar.BorderBrush = $(if ($opt.Theme -eq "fluent") { & $solid (& $color "#00000000") } else { & $solid $acc })
    foreach ($n in @("PrevBtnA", "PrevBtnB")) { (& $get $n).Fill = & $grad @($L.Bar) }
    (& $get "PrevLights").Visibility = $(if ($L.Lights) { "Visible" } else { "Collapsed" })
    (& $get "PrevBtns").Visibility = $(if ($L.Lights) { "Collapsed" } else { "Visible" })
    $card = & $get "PrevCard"
    $cardColors = @($L.Card)
    if ($opt.Theme -eq "material") { $cardColors = @("#1C2433", ("#{0:X2}{1:X2}{2:X2}" -f $acc.R, $acc.G, $acc.B), "#6B5A8A") }
    $card.Background = & $grad $cardColors
    if ($opt.WallFile -and (Test-Path -LiteralPath $opt.WallFile)) {
      try {
        $bmp = New-Object Windows.Media.Imaging.BitmapImage
        $bmp.BeginInit(); $bmp.CacheOption = "OnLoad"; $bmp.DecodePixelWidth = 600
        $bmp.UriSource = New-Object Uri ($opt.WallFile); $bmp.EndInit()
        $ib = New-Object Windows.Media.ImageBrush ($bmp); $ib.Stretch = "UniformToFill"
        $card.Background = $ib
      } catch {}
    } elseif ($WallPresets.Contains([string]$opt.Wall)) {
      $card.Background = & $grad $WallPresets[[string]$opt.Wall].Colors
    }
    $r = $L.CardR
    $rc = @{ none = 0; square = 4; standard = 12; round = 20 }[$opt.Corners]
    if ($rc -ne $null) { $r = $rc }
    $card.CornerRadius = New-Object Windows.CornerRadius ($r)
    $clock = & $get "PrevClock"
    $clock.FontWeight = [Windows.FontWeights]::($L.Clock)
    $clock.FontFamily = New-Object Windows.Media.FontFamily ($L.Font)
    $clock.Foreground = & $grad @($L.ClockFg)
    $clock.Visibility = $(if ($opt.Clock) { "Visible" } else { "Hidden" })
    $search = & $get "PrevSearch"
    $search.Background = & $grad @($L.Search)
    $search.CornerRadius = New-Object Windows.CornerRadius ($L.SearchR)
    $search.BorderBrush = $(if ($opt.Theme -eq "fluent") { & $solid $acc } else { & $solid (& $color "#2AFFFFFF") })
    $search.BorderThickness = $(if ($opt.Theme -eq "fluent") { New-Object Windows.Thickness (0, 0, 0, 2) } else { New-Object Windows.Thickness (1) })
    (& $get "ThemeHint").Text = $Themes[$opt.Theme].Desc
    & $fadeIn $frame
  }

  # ---------- галерея тем ----------
  $grid = & $get "ThemeGrid"
  foreach ($key in $Themes.Keys) {
    $rb = New-Object Windows.Controls.RadioButton
    $rb.Style = & $res "ThemeCard"; $rb.GroupName = "theme"; $rb.Tag = $key
    $sp = New-Object Windows.Controls.StackPanel
    $sw = New-Object Windows.Controls.Border
    $sw.Height = 46; $sw.CornerRadius = New-Object Windows.CornerRadius (12)
    $sw.Background = & $grad $PreviewLook[$key].Swatch
    $sw.BorderBrush = & $solid (& $color "#22FFFFFF"); $sw.BorderThickness = New-Object Windows.Thickness (1)
    $name = & $text $Themes[$key].Name "RowTitle"
    $name.FontSize = 13; $name.Margin = New-Object Windows.Thickness (4, 7, 4, 2); $name.TextTrimming = [Windows.TextTrimming]::CharacterEllipsis
    [void]$sp.Children.Add($sw); [void]$sp.Children.Add($name)
    $rb.Content = $sp
    if ($key -eq $opt.Theme) { $rb.IsChecked = $true }
    $rb.Add_Checked({ param($s) $opt.Theme = [string]$s.Tag; & $applyLook })
    [void]$grid.Children.Add($rb)
  }

  # ---------- обои новой вкладки ----------
  (& $get "WallCaption").Text = T "ОБОИ НОВОЙ ВКЛАДКИ" "NEW TAB WALLPAPER"
  $wallChips = & $get "WallChips"; $wallHint = & $get "WallHint"
  $wallText = {
    if ($opt.WallFile) { $wallHint.Text = (T "Своя картинка: " "Your picture: ") + [IO.Path]::GetFileName($opt.WallFile) }
    elseif ($opt.Wall -eq "keep") { $wallHint.Text = T "Не менять. Обои можно сменить и потом — кнопкой слева внизу на новой вкладке." "Keep. You can also change it later with the button at the bottom left of the new tab." }
    elseif ($opt.Wall -eq "theme") { $wallHint.Text = T "Обои выбранной темы." "The theme's own wallpaper." }
    else { $wallHint.Text = $WallPresets[[string]$opt.Wall].Name }
  }
  $addWall = {
    param($tag, $brush, $label, $tip)
    $rb = New-Object Windows.Controls.RadioButton
    $rb.Style = & $res "Chip"; $rb.GroupName = "wall"; $rb.Tag = $tag; $rb.Background = $brush; $rb.ToolTip = $tip
    if ($label) { $l = New-Object Windows.Controls.TextBlock; $l.Text = $label; $l.Foreground = & $solid (& $color "#FFFFFFFF"); $l.FontSize = 11; $l.FontWeight = [Windows.FontWeights]::Bold; $rb.Content = $l }
    $rb.Add_Click({
      param($s)
      $t = [string]$s.Tag
      if ($t -eq "custom") {
        $dlg = New-Object Microsoft.Win32.OpenFileDialog
        $dlg.Title = T "Картинка для обоев" "Wallpaper picture"
        $dlg.Filter = (T "Картинки" "Images") + "|*.jpg;*.jpeg;*.png;*.webp;*.bmp;*.gif;*.avif"
        if ($dlg.ShowDialog($window)) { $opt.WallFile = $dlg.FileName; $opt.Wall = "custom" }
        elseif (-not $opt.WallFile) { $s.IsChecked = $false; $keepChip.IsChecked = $true; $opt.Wall = "keep" }
      } else {
        $opt.WallFile = ""; $opt.Wall = $t
      }
      & $wallText
      & $applyLook
    })
    [void]$wallChips.Children.Add($rb)
    return $rb
  }
  $keepChip = & $addWall "keep" (& $solid (& $color "#33FFFFFF")) "—" (T "Не менять" "Keep")
  [void](& $addWall "theme" (& $grad $PreviewLook[$opt.Theme].Swatch) "T" (T "Как в теме" "Theme"))
  foreach ($k in $WallPresets.Keys) { [void](& $addWall $k (& $grad $WallPresets[$k].Colors) "" $WallPresets[$k].Name) }
  [void](& $addWall "custom" $(& $grad @("#3A3B40", "#1E1F23")) "+" (T "Своя картинка…" "Your picture…"))
  $keepChip.IsChecked = $true
  & $wallText

  # ---------- акцент: кружки ----------
  $chips = & $get "AccentChips"
  $hexRow = & $get "HexRow"; $hexBox = & $get "HexBox"
  $addChip = {
    param($tag, $brush, $label, $tip)
    $rb = New-Object Windows.Controls.RadioButton
    $rb.Style = & $res "Chip"; $rb.GroupName = "accent"; $rb.Tag = $tag; $rb.Background = $brush; $rb.ToolTip = $tip
    if ($label) { $l = New-Object Windows.Controls.TextBlock; $l.Text = $label; $l.Foreground = & $solid (& $color "#FFFFFFFF"); $l.FontSize = 11; $l.FontWeight = [Windows.FontWeights]::Bold; $rb.Content = $l }
    $rb.Add_Checked({
      param($s)
      $t = [string]$s.Tag
      if ($t -eq "custom") {
        $hexRow.Visibility = "Visible"
        if ($hexBox.Text -match '^#[0-9a-fA-F]{6}$') { $opt.Accent = $hexBox.Text }
      } else {
        $hexRow.Visibility = "Collapsed"
        $opt.Accent = $t
      }
      & $applyLook
    })
    [void]$chips.Children.Add($rb)
    return $rb
  }
  $winChip = & $addChip "windows" (& $solid $winAccent) "W" (T "Как в Windows" "Windows accent")
  $presetChips = @{}
  foreach ($c in $AccentPresets) { $presetChips[$c] = & $addChip $c (& $solid (& $color $c)) "" $c }
  $rainbow = New-Object Windows.Media.LinearGradientBrush
  $rainbow.StartPoint = "0,0"; $rainbow.EndPoint = "1,1"
  foreach ($s in @(@("#FF453A", 0), @("#FFD60A", 0.35), @("#30D158", 0.6), @("#0A84FF", 1))) { $rainbow.GradientStops.Add((New-Object Windows.Media.GradientStop ((& $color $s[0]), $s[1]))) }
  $customChip = & $addChip "custom" $rainbow "+" (T "Свой цвет" "Custom")
  $hexBox.Add_TextChanged({
    if ($hexBox.Text -match '^#[0-9a-fA-F]{6}$') { $opt.Accent = $hexBox.Text.ToUpper(); & $applyLook }
  })
  if ($opt.Accent -eq "windows") { $winChip.IsChecked = $true }
  elseif ($presetChips.Contains([string]$opt.Accent)) { $presetChips[[string]$opt.Accent].IsChecked = $true }
  else { $hexBox.Text = [string]$opt.Accent; $customChip.IsChecked = $true }

  # ---------- режим и скругление ----------
  foreach ($pair in @(@("ModeKeep", "keep"), @("ModeAuto", "auto"), @("ModeLight", "light"), @("ModeDark", "dark"))) {
    $rb = & $get $pair[0]; $rb.Tag = $pair[1]
    if ($opt.Mode -eq $pair[1]) { $rb.IsChecked = $true }
    $rb.Add_Checked({ param($s) $opt.Mode = [string]$s.Tag })
  }
  foreach ($pair in @(@("CornTheme", "theme"), @("CornNone", "none"), @("CornSquare", "square"), @("CornStandard", "standard"), @("CornRound", "round"))) {
    $rb = & $get $pair[0]; $rb.Tag = $pair[1]
    if ($opt.Corners -eq $pair[1]) { $rb.IsChecked = $true }
    $rb.Add_Checked({ param($s) $opt.Corners = [string]$s.Tag; & $applyLook })
  }

  foreach ($pair in @(@("MotApple", "apple"), @("MotSmooth", "smooth"), @("MotSystem", "system"), @("MotOff", "off"))) {
    $rb = & $get $pair[0]; $rb.Tag = $pair[1]
    if ($opt.Motion -eq $pair[1]) { $rb.IsChecked = $true }
    $rb.Add_Checked({ param($s) $opt.Motion = [string]$s.Tag })
  }

  # ---------- функции ----------
  $flist = & $get "FeatureList"
  $features = @(
    @("NowBar",    (T "Плеер Now Bar" "Now Bar player"),           (T "Музыка из другой вкладки: обложка, пауза, назад/вперёд" "Music from another tab: cover, pause, prev/next")),
    @("Progress",  (T "Полоска загрузки" "Loading bar"),          (T "Тонкая линия под панелью, пока грузится страница" "Thin line under the toolbar while a page loads")),
    @("Center",    (T "Адрес по центру" "Centered address"),      (T "Пока адресная строка не в фокусе" "While the address bar is not focused")),
    @("Clock",     (T "Часы на новой вкладке" "New tab clock"),   (T "Большие часы и дата на стартовой странице" "Big clock and date on the start page")),
    @("Wallpaper", (T "Живые обои" "Animated wallpaper"),         (T "Медленное движение фона новой вкладки" "Slow motion of the new tab background")),
    @("Pdf",       (T "Новый просмотрщик PDF" "New PDF viewer"),  (T "Панель, темы страниц, рисование как в Edge, своя палитра" "Toolbar, page themes, Edge-style ink, own palette"))
  )
  $first = $true
  foreach ($f in $features) {
    if (-not $first) { [void]$flist.Children.Add((& $sep)) }
    $first = $false
    $row = & $switchRow $f[1] $f[2] ([bool]$opt[$f[0]])
    $row.Box.Tag = $f[0]
    $row.Box.Add_Checked({ param($s) $opt[[string]$s.Tag] = $true; & $applyLook })
    $row.Box.Add_Unchecked({ param($s) $opt[[string]$s.Tag] = $false; & $applyLook })
    [void]$flist.Children.Add($row.Row)
  }

  # ---------- браузеры ----------
  $blist = & $get "BrowserList"
  $browserBoxes = @{}
  $first = $true
  foreach ($key in $found.Keys) {
    if (-not $first) { [void]$blist.Children.Add((& $sep)) }
    $first = $false
    $profiles = @(Get-Profiles $key)
    $hint = $found[$key]
    if ($profiles.Count -eq 0) { $hint += "`n" + (T "нет профиля — запустите браузер один раз" "no profile — start the browser once") }
    $row = & $switchRow $Browsers[$key].Name $hint ($profiles.Count -gt 0)
    if ($profiles.Count -eq 0) { $row.Box.IsEnabled = $false }
    $browserBoxes[$key] = $row.Box
    [void]$blist.Children.Add($row.Row)
  }
  if ($found.Count -eq 0) {
    $none = & $text (T "Не нашёл ни одного браузера на движке Firefox." "No Firefox-based browser found.") "RowTitle"
    $none.Margin = New-Object Windows.Thickness (18, 14, 18, 14)
    [void]$blist.Children.Add($none)
  }
  $missing = @($Browsers.Keys | Where-Object { -not $found.Contains($_) } | ForEach-Object { $Browsers[$_].Name })
  (& $get "NotFound").Text = $(if ($missing.Count) { (T "Не найдены: " "Not found: ") + ($missing -join ", ") } else { "" })

  # ---------- страницы ----------
  $pages = @((& $get "Page1"), (& $get "Page2"), (& $get "Page3"))
  $steps = @((& $get "Step1"), (& $get "Step2"), (& $get "Step3"))
  $showPage = {
    param($n)
    $state.Page = $n
    for ($i = 0; $i -lt 3; $i++) {
      $pages[$i].Visibility = $(if ($i -eq $n - 1) { "Visible" } else { "Hidden" })
      $steps[$i].Foreground = $(if ($i -eq $n - 1) { & $res "Ink" } else { & $res "Muted" })
    }
    & $fadeIn $pages[$n - 1]
    (& $get "BackBtn").Visibility = $(if ($n -gt 1) { "Visible" } else { "Hidden" })
    (& $get "UninstallBtn").Visibility = $(if ($n -eq 3) { "Visible" } else { "Hidden" })
    (& $get "NextBtn").Content = $(if ($n -lt 3) { T "Далее" "Next" } else { T "Установить" "Install" })
    if ($n -eq 3) {
      $acc = $(if ($opt.Accent -eq "windows") { T "акцент Windows" "Windows accent" } else { $opt.Accent })
      (& $get "Summary").Text = (T "Тема: " "Theme: ") + $Themes[$opt.Theme].Name + " · " + $acc + $(if ($opt.Pdf) { T " · с просмотрщиком PDF" " · with PDF viewer" } else { "" })
    }
  }
  (& $get "Step1").Add_Click({ & $showPage 1 })
  (& $get "Step2").Add_Click({ & $showPage 2 })
  (& $get "Step3").Add_Click({ & $showPage 3 })
  (& $get "BackBtn").Add_Click({ if ($state.Page -gt 1) { & $showPage ($state.Page - 1) } })

  $rootScale = & $get "RootScale"
  $window.Add_Loaded({
    & $animate $rootScale ([Windows.Media.ScaleTransform]::ScaleXProperty) 1 420 0.3
    & $animate $rootScale ([Windows.Media.ScaleTransform]::ScaleYProperty) 1 420 0.3
  })
  $script:GuiLog = & $get "Log"
  (& $get "DragArea").Add_MouseLeftButtonDown({ try { $window.DragMove() } catch {} })
  (& $get "CloseBtn").Add_Click({ $window.Close() })
  (& $get "DoneBtn").Add_Click({ $window.Close() })

  $showDone = {
    param($action)
    $main = & $get "MainPanel"; $done = & $get "DonePanel"
    (& $get "DoneTitle").Text = $(if ($action -eq "install") { T "Готово!" "All set!" } else { T "Оформление удалено" "Theme removed" })
    (& $get "DoneText").Text = $(if ($action -eq "install") { T "Откройте браузер — он уже в новом виде. Поменять тему или настройки можно, запустив установщик ещё раз." "Open the browser — it already has the new look. Run setup again to change the theme or settings." } else { T "После перезапуска браузер выглядит как раньше." "The browser looks as before after a restart." })
    $done.MinHeight = $main.ActualHeight
    $main.Visibility = "Collapsed"
    $done.Visibility = "Visible"
    & $fadeIn $done
    $ds = & $get "DoneScale"
    & $animate $ds ([Windows.Media.ScaleTransform]::ScaleXProperty) 1 600 0.6
    & $animate $ds ([Windows.Media.ScaleTransform]::ScaleYProperty) 1 600 0.6
  }
  (& $get "DoneLogBtn").Add_Click({
    (& $get "DonePanel").Visibility = "Collapsed"
    (& $get "MainPanel").Visibility = "Visible"
    & $showPage 3
    (& $get "NextBtn").Content = T "Закрыть" "Close"
  })

  $run = {
    param($action)
    if ($script:guiFinished) { $window.Close(); return }
    $keys = @($browserBoxes.Keys | Where-Object { $browserBoxes[$_].IsChecked })
    if ($keys.Count -eq 0) {
      [System.Windows.MessageBox]::Show((T "Включите хотя бы один браузер." "Turn on at least one browser."), "Redesigned Fox") | Out-Null
      return
    }
    # порядок как в списке браузеров
    $keys = @($Browsers.Keys | Where-Object { $keys -contains $_ })
    (& $get "LogBox").Visibility = "Visible"
    $script:GuiLog.Text = ""
    $btn = & $get "NextBtn"
    $btn.IsEnabled = $false; (& $get "UninstallBtn").IsEnabled = $false; (& $get "BackBtn").IsEnabled = $false
    $btn.Content = $(if ($action -eq "install") { T "Устанавливаю…" "Installing…" } else { T "Удаляю…" "Removing…" })
    $ok = Invoke-Modern $action $keys $opt
    if ($ok) {
      $script:guiFinished = $true
      $btn.IsEnabled = $true
      & $showDone $action
    } else {
      Say ""
      Say (T "Что-то пошло не так — подробности выше." "Something went wrong — see above.")
      $btn.Content = T "Попробовать ещё раз" "Try again"
      $btn.IsEnabled = $true; (& $get "UninstallBtn").IsEnabled = $true; (& $get "BackBtn").IsEnabled = $true
    }
  }
  $script:guiFinished = $false
  (& $get "NextBtn").Add_Click({ if ($state.Page -lt 3 -and -not $script:guiFinished) { & $showPage ($state.Page + 1) } else { & $run "install" } })
  (& $get "UninstallBtn").Add_Click({ & $run "uninstall" })

  & $applyLook
  & $showPage 1
  [void]$window.ShowDialog()
}

# ================================================================ запуск
if (-not $SkipAdmin -and -not (Test-Admin)) {
  $argList = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$PSCommandPath`"",
               "-Action", $Action, "-Target", $Target, "-Theme", $Theme, "-Pdf", $Pdf,
               "-Accent", $Accent, "-Mode", $Mode, "-Corners", $Corners, "-Motion", $Motion, "-Wall", "`"$Wall`"", "-Features", "`"$Features`"",
               "-UserAppData", "`"$UserAppData`"")
  if ($Gui) { $argList = @("-STA", "-WindowStyle", "Hidden") + $argList + @("-Gui") }
  else { Write-Host (T "Нужны права администратора (чтобы положить загрузчик в папку браузера). Сейчас Windows спросит разрешение..." "Administrator rights are needed. Windows will ask now...") -ForegroundColor Yellow }
  try {
    $p = Start-Process powershell -Verb RunAs -ArgumentList $argList -Wait -PassThru
    exit $p.ExitCode
  } catch {
    Write-Host (T "Без прав администратора установить не получится." "Cannot continue without administrator rights.") -ForegroundColor Red
    exit 1
  }
}

if ($Gui) {
  try {
    Show-Gui
  } catch {
    try {
      Add-Type -AssemblyName System.Windows.Forms
      [System.Windows.Forms.MessageBox]::Show((T "Окно установщика не открылось. Запустите install.cmd — он сделает то же самое в консоли.`n`n" "The setup window failed to open. Run install.cmd instead.`n`n") + $_.Exception.Message, "Redesigned Fox") | Out-Null
    } catch {}
    exit 1
  }
  exit 0
}

# ---------------- консольный режим ----------------
Say ""
Say "Redesigned Fox $Version" Cyan
if ($found.Count -eq 0) {
  Say (T "Не нашёл ни одного браузера на движке Firefox (Floorp, Firefox, LibreWolf, Waterfox, Zen, Mercury)." "No Firefox-based browser found.") Red
  if (-not $SkipAdmin) { Read-Host (T "Нажмите Enter" "Press Enter") | Out-Null }
  exit 1
}
$keys = @()
if ($Target -eq "ask") {
  Say $(if ($Action -eq "install") { T "Куда установить?" "Install into:" } else { T "Откуда удалить?" "Remove from:" })
  $menu = @($found.Keys)
  for ($i = 0; $i -lt $menu.Count; $i++) { Say ("  {0}. {1}  ({2})" -f ($i + 1), $Browsers[$menu[$i]].Name, $found[$menu[$i]]) }
  if ($menu.Count -gt 1) { Say ("  {0}. {1}" -f ($menu.Count + 1), (T "Все" "All")) }
  $choice = 0
  if ($menu.Count -eq 1) { $choice = 1 } else {
    while ($choice -lt 1 -or $choice -gt $menu.Count + 1) { [int]::TryParse((Read-Host (T "Введите номер" "Enter a number")), [ref]$choice) | Out-Null }
  }
  $keys = $(if ($choice -eq $menu.Count + 1) { $menu } else { @($menu[$choice - 1]) })
} elseif ($Target -in @("all", "both")) {
  $keys = @($found.Keys)
} else {
  $keys = @($Target -split "," | ForEach-Object { $_.Trim() } | Where-Object { $Browsers.Contains($_) })
}

$o = New-Options
if ($Action -eq "install") {
  if ($Theme -eq "ask") {
    Say (T "Какая тема?" "Which theme?")
    $tk = @($Themes.Keys)
    for ($i = 0; $i -lt $tk.Count; $i++) { Say ("  {0}. {1} — {2}" -f ($i + 1), $Themes[$tk[$i]].Name, $Themes[$tk[$i]].Desc) }
    $c = 0
    while ($c -lt 1 -or $c -gt $tk.Count) { [int]::TryParse((Read-Host (T "Введите номер" "Enter a number")), [ref]$c) | Out-Null }
    $Theme = $tk[$c - 1]
  }
  if ($Pdf -eq "ask") {
    $a = Read-Host (T "Поставить новый просмотрщик PDF (панель, темы страниц, рисование как в Edge)? [Д/н]" "Install the new PDF viewer (toolbar, page themes, Edge-style ink)? [Y/n]")
    $Pdf = if ($a -match '^[nNнН]') { "no" } else { "yes" }
  }
  $o.Theme = $Theme
  $o.Pdf = ($Pdf -ne "no")
  $o.Accent = $(if ($Accent -match '^#[0-9a-fA-F]{6}$') { $Accent.ToUpper() } else { "windows" })
  $o.Mode = $Mode
  $o.Corners = $Corners
  $o.Motion = $Motion
  if ($Wall -match '[\\/.]') { $o.WallFile = $Wall; $o.Wall = "custom" } else { $o.Wall = $Wall }
  $on = @($Features -split "," | ForEach-Object { $_.Trim().ToLower() })
  $o.NowBar = $on -contains "nowbar"; $o.Progress = $on -contains "progress"; $o.Center = $on -contains "center"
  $o.Clock = $on -contains "clock"; $o.Wallpaper = $on -contains "wallpaper"
}
$ok = Invoke-Modern $Action $keys $o
Say ""
if ($Action -eq "install") { Say (T "Готово! Откройте браузер." "Done! Start the browser.") Green }
else { Say (T "Готово. После перезапуска браузер выглядит как раньше." "Done. The browser looks as before after a restart.") Green }
if (-not $SkipAdmin) { Say ""; Read-Host (T "Нажмите Enter, чтобы закрыть окно" "Press Enter to close") | Out-Null }
if ($ok) { exit 0 } else { exit 1 }
