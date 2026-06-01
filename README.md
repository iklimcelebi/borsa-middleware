# Borsa Middleware Log System

## Proje Açıklaması
Bu proje, producer-middleware mimarisi ile log işleme sistemi simüle eder.

## Mimari
Producer → Middleware → Dashboard

## Özellikler
- Log filtering (INFO/DEBUG filtreleme)
- Data anonymization (email, kredi kartı gizleme)
- Log enrichment (risk level, transaction id)
- Format system (JSON / CSV / HTML)
- Dashboard UI
- API Key Security
- Docker support

## Çalıştırma

```bash
docker compose up --build

Portlar
Producer: 5001
Middleware: 5000