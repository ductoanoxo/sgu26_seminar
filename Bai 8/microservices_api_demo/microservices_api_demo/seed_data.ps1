$products = @(
    @{
        name = "Sony WH-1000XM5"
        description = "Industry Leading Noise Canceling Headphones"
        price = 34999
        rating = 5
        image = "https://m.media-amazon.com/images/I/61+btW9S96L._AC_SL1500_.jpg"
    },
    @{
        name = "AirPods Max Pink"
        description = "High-fidelity audio with Active Noise Cancellation"
        price = 54900
        rating = 5
        image = "https://m.media-amazon.com/images/I/81UAn9kXitL._AC_SL1500_.jpg"
    },
    @{
        name = "Bose QuietComfort Ultra"
        description = "World-class noise cancellation, quieter than ever before"
        price = 42900
        rating = 5
        image = "https://m.media-amazon.com/images/I/51n6N-7XWNL._AC_SL1500_.jpg"
    },
    @{
        name = "JBL Flip 6 Blue"
        description = "Bold sound for every adventure"
        price = 12900
        rating = 4
        image = "https://m.media-amazon.com/images/I/71u9S+HqZpL._AC_SL1500_.jpg"
    },
    @{
        name = "Marshall Emberton II"
        description = "Rich, clear and loud, like the artist intended"
        price = 16900
        rating = 5
        image = "https://m.media-amazon.com/images/I/71Y-V79O2OL._AC_SL1500_.jpg"
    }
)

foreach ($p in $products) {
    $json = $p | ConvertTo-Json
    Write-Host "Seeding product: $($p.name)"
    try {
        Invoke-RestMethod -Uri "http://localhost:8181/v1/api/products" -Method Post -Body $json -ContentType "application/json"
        Write-Host "Success!" -ForegroundColor Green
    } catch {
        Write-Host "Failed to seed $($p.name): $_" -ForegroundColor Red
    }
}
