# 只讀診斷；不變更 DNS、防火牆、代理或作業系統設定。
$targets = @(
  @{Name='聯合國分類頁'; Url='https://unstats.un.org/unsd/classifications/Econ/isic'},
  @{Name='聯合國 ISIC CSV'; Url='https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_5_english_structure.csv'},
  @{Name='聯合國 ISIC XLSX'; Url='https://unstats.un.org/unsd/classifications/Econ/Download/ISIC5_Exp_Notes_19_Aug_2026.xlsx'},
  @{Name='GLEIF Golden Copy 頁'; Url='https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy'}
)
$report = @()
foreach ($t in $targets) {
  $u = [uri]$t.Url
  $dns = $null; $status = $null; $contentType = $null; $errorText = $null
  try { $dns = ((Resolve-DnsName -Name $u.Host -Type A -ErrorAction Stop | Where-Object IPAddress).IPAddress -join ';') } catch { $errorText = "DNS: $($_.Exception.Message)" }
  try {
    # HEAD 在某些站點不被支援，因此不將 HEAD 失敗視為檔案不可下載
    $r = Invoke-WebRequest -Uri $t.Url -Method Head -MaximumRedirection 5 -TimeoutSec 20 -UseBasicParsing -ErrorAction Stop
    $status=[int]$r.StatusCode; $contentType=$r.Headers['Content-Type']
  } catch {
    if ($_.Exception.Response) {
      $status=[int]$_.Exception.Response.StatusCode
      $contentType=$_.Exception.Response.Headers['Content-Type']
    }
    $errorText = (($errorText, $_.Exception.Message) | Where-Object { $_ }) -join ' | '
  }
  $report += [pscustomobject]@{CheckedAt=(Get-Date).ToString('o');Name=$t.Name;Host=$u.Host;DnsA=$dns;HttpHeadStatus=$status;ContentType=$contentType;Error=$errorText}
}
$report | Format-Table -AutoSize
$path = Join-Path $PWD 'global_dns_download_diagnostic_v2_2_0_results.csv'
$report | Export-Csv -LiteralPath $path -NoTypeInformation -Encoding UTF8
Write-Host "診斷結果已寫入 $path"
