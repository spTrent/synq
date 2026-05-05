# SYNQ Project

## Запуск в Kubernetes (основной способ)

1. **Подготовка окружения:**
   Убедитесь, что у вас установлен `kubectl` и запущен локальный кластер (Docker Desktop, Minikube или Kind).

2. **Настройка Ingress (один раз):**
   ```bash
   ./setup-ingress.sh
   ```

3. **Запуск всех сервисов:**
   ```bash
   kubectl apply -f k8s/
   ```

4. **Доступ к приложению:**
   - **Frontend:** [http://localhost](http://localhost)
   - **Backend API:** [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
   - **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Остановка
```bash
kubectl delete -f k8s/
```
