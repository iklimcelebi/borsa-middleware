# Borsa Middleware Log System

## Project Overview
Bu proje, producer-middleware mimarisi ile log işlemenin filtreleme, anonimleştirme ve kategori bazlı sınıflandırma adımlarını içerir.

## Architecture
Producer → Middleware → Dashboard

## Docker Containers
- Producer container
- Middleware container
- Dashboard arayüzü middleware içinde sunulur

## Middleware Pipeline
1. Filter
2. Anonymization
3. Enrichment
4. Classification
5. Role-based formatting

## Security Layer
- API Key doğrulaması
- Dashboard erişimi anonimleştirilmiş verilerle sağlanır

## Filtering
INFO, DEBUG ve WARNING seviyeleri middleware'de işlenmeden düşer.

## Anonymization
- Email adresleri maskelenir
- Kredi kartı bilgileri sadece son 4 rakam görünür şekilde sunulur

## Enrichment
- Risk seviyesi mantıklı bir haritalama ile atanır
- İşlemle ilgili metadata eklenir

## Classification
- Keyword bazlı kategori sistemi
- PAYMENT, AUTH, DATABASE, NETWORK ve GENERAL kategorileri

## Role Based Formatting
- Developer (JSON): timestamp, level, message, category
- Cyber Security (CSV): timestamp, level, message, category, risk_level, sender_id, transaction_no
- System Admin (HTML): tüm alanlar

## Dashboard
- Toplam Gelen Log
- İşlenen Log
- Filtrelenen Log
- Level Distribution
- Risk Distribution
- Son 20 log tablosu
- Son benchmark sonucu

## Performance Test
`/benchmark` endpoint'i 1000 log üretir, pipeline'dan geçirir ve süreyi ölçer.

## Design Patterns
- Chain of Responsibility: filter → anonymize → enrich pipeline
- Strategy Pattern: role bazlı formatter seçimi
- Factory Pattern: formatter factory ile doğru formatter seçimi

## How To Run
```bash
docker compose up --build
```

## Benchmark
`GET /benchmark` endpoint'i son benchmark sonuçlarını döner.

Portlar
Producer: 5001
Middleware: 5000