// script.js

const countdownContainer = document.getElementById('countdown-container');

// ------------------------------------
// Geri Sayım Fonksiyonu
// ------------------------------------

// Yılbaşı Tarihini Belirle (1 Ocak bir sonraki yıl)
// Not: Bu kod 2025'te 2026'yı, 2026'da 2027'yi hedefler.
const now = new Date();
const currentYear = now.getFullYear();
const nextYear = currentYear + 1;
const newYearDate = new Date(`January 1, ${nextYear} 00:00:00`).getTime();

function updateCountdown() {
    const currentTime = new Date().getTime();
    const distance = newYearDate - currentTime;

    // Zaman hesaplamaları
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // HTML İçeriğini Oluşturma Fonksiyonu
    const createCountdownBox = (number, label) => {
        // Negatif sayılarda 0 göster
        const displayNum = number < 0 ? 0 : number;
        const formattedNum = displayNum < 10 ? '0' + displayNum : displayNum;

        return `
            <div class="countdown-box">
                <span class="countdown-number">${formattedNum}</span>
                <span class="countdown-label">${label}</span>
            </div>
        `;
    };

    if (distance < 0) {
        // Geri Sayım Bitti
        clearInterval(countdownInterval);
        countdownContainer.innerHTML = '<h2 class="main-title" style="font-size: 4em;">🎉 MUTLU YILLAR! 🎉</h2>';
    } else {
        // Geri Sayımı Güncelle
        countdownContainer.innerHTML =
            createCountdownBox(days, 'Gün') +
            createCountdownBox(hours, 'Saat') +
            createCountdownBox(minutes, 'Dakika') +
            createCountdownBox(seconds, 'Saniye');
    }
}

// Sayacı Her Saniye Güncelle
const countdownInterval = setInterval(updateCountdown, 1000);

// Sayacın İlk Çalıştırması
updateCountdown();