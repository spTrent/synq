# Лабораторная работа №7: Метрики, Скрейпинг и Трейсинг

## Описание выполненных работ

### 1. Метрики (Backend)
- Реализован эндпоинт `/metrics` с использованием `prometheus-fastapi-instrumentator`.
- Добавлены стандартные метрики HTTP (counter и histogram) с группировкой по шаблонам маршрутов (низкая кардинальность).
- Добавлена бизнес-метрика `synq_registrations_total` (Counter), которая инкрементируется при успешной регистрации нового пользователя.
- Файл реализации: `backend/app/monitoring.py`.
- Подключение в приложении: `backend/app/api/main.py`.

### 2. Скрейпинг
- **Docker Compose:** Настроен job в Prometheus для сбора метрик с сервиса `backend:8000/metrics`.
- **Kubernetes:** Prometheus настроен на автоматическое обнаружение подов с аннотациями `prometheus.io/scrape: "true"`.
- Конфигурация Prometheus (K8s): `k8s/monitoring/prometheus.yaml`.

### 3. Трейсинг
- Интегрирован OpenTelemetry в Backend для сбора трейсов.
- Настроен экспорт трейсов по протоколу OTLP в Tempo.
- В Kubernetes и Docker Compose добавлен сервис Tempo.
- Файл конфигурации Tempo: `monitoring/tempo.yml` (Docker) и `k8s/monitoring/tempo.yaml` (K8s).

### 4. Grafana
- Подключены источники данных:
  - **Prometheus:** `http://prometheus-service.monitoring.svc.cluster.local:9090`
  - **Tempo:** `http://tempo.monitoring.svc.cluster.local:3200` (с привязкой к Prometheus для Service Map).
- Создан дашборд "Synq Backend Dashboard" с панелями:
  - HTTP Request Rate (Rate of `http_request_duration_seconds_count`).
  - Total Registrations (Business metric `synq_registrations_total`).
- Дашборд и датасорсы автоматически провижинятся через ConfigMap в K8s и файлы в Docker Compose.

## Инструкции по проверке

### Проверка метрик
```bash
# Проброс порта к backend
kubectl port-forward svc/dev-backend-service 8000:8000
# Проверка эндпоинта
curl localhost:8000/metrics | grep synq_registrations_total
```

### Проверка Prometheus Targets
1. Пробросьте порт к Prometheus: `kubectl port-forward svc/prometheus-service -n monitoring 9090:9090`.
2. Откройте `http://localhost:9090/targets`.
3. Найдите цель `kubernetes-pods` (или соответствующую вашему поду), статус должен быть **UP**.

### Проверка Grafana
1. Пробросьте порт к Grafana: `kubectl port-forward svc/grafana-service -n monitoring 3000:3000`.
2. Откройте `http://localhost:3000` (вход анонимный с правами Admin).
3. Перейдите в **Dashboards** -> **Synq Backend Dashboard**.
4. Для проверки трейсов перейдите в **Explore**, выберите DataSource **Tempo** и выполните поиск (Search) или выберите Trace ID из логов/Service Map.

## Скриншоты
Скриншоты должны быть размещены в этой директории:
1. `prometheus_targets.png` - страница Targets со статусом UP.
2. `grafana_dashboard.png` - дашборд с метриками backend.
3. `grafana_tempo_trace.png` - развернутый trace в Explore.
