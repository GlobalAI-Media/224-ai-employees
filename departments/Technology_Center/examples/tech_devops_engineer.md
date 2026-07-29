## tech_devops_engineer
**Task:** Describe how to set up a CI/CD pipeline for 224 AI microservices, ensuring zero-downtime deployment and automated rollback.

# CI/CD Pipeline for 224 AI Microservices: Zero-Downtime Deployment & Automated Rollback

## Overview

Managing 224 AI microservices requires a highly automated, resilient pipeline. We'll implement a **canary-based deployment strategy** with **automated health verification** and **instant rollback** using Kubernetes-native patterns.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitLab CI/CD Pipeline                │
├─────────────────────────────────────────────────────────┤
│  1. Build Stage                                         │
│     ├── Multi-arch Docker build (amd64/arm64)           │
│     ├── Vulnerability scanning (Trivy)                  │
│     └── Image signing (Cosign)                          │
│                                                         │
│  2. Test Stage                                          │
│     ├── Unit tests (pytest)                             │
│     ├── Integration tests (Testcontainers)              │
│     └── Contract tests (Pact)                           │
│                                                         │
│  3. Deploy Stage                                        │
│     ├── Staging: Blue/Green with 10% canary             │
│     ├── Production: Progressive rollout (10%→50%→100%)  │
│     └── Health checks every 30s                         │
│                                                         │
│  4. Monitor & Rollback                                  │
│     ├── Prometheus metrics (latency, error rate, CPU)   │
│     ├── Alert if error rate > 1% or latency > 500ms     │
│     └── Automatic rollback to previous revision         │
└─────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Kubernetes Deployment Strategy (Canary + Blue/Green)

```yaml
# canary-deployment.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ai-microservice-{service-name}
  namespace: production
spec:
  replicas: 5
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: ai-microservice-{service-name}
  template:
    metadata:
      labels:
        app: ai-microservice-{service-name}
    spec:
      containers:
      - name: service
        image: registry.global-ai.com/{service}:latest
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: { duration: 60s }
      - setWeight: 50
      - pause: { duration: 120s }
      - setWeight: 100
      analysis:
        templates:
        - templateName: success-rate-analysis
        args:
        - name: service-name
          value: ai-microservice-{service-name}
```

### 2. Automated Analysis Template for Rollback

```yaml
# analysis-template.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-analysis
spec:
  metrics:
  - name: success-rate
    interval: 30s
    count: 10
    failureLimit: 3
    provider:
      prometheus:
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}", status!~"5.."}[1m]))
          /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))
        threshold: 0.99  # 99% success rate required
  - name: latency-p99
    interval: 30s
    count: 10
    failureLimit: 2
    provider:
      prometheus:
        query: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="{{args.service-name}}"}[1m])) by (le)
          )
        threshold: 0.5  # 500ms max p99 latency
```

### 3. CI/CD Pipeline Configuration (GitLab CI)

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy-staging
  - deploy-production
  - monitor

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  K8S_NAMESPACE: production
  ROLLOUT_NAME: ai-microservice-$CI_PROJECT_NAME

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - trivy image --severity HIGH,CRITICAL --exit-code 1 $DOCKER_IMAGE
    - cosign sign --key $COSIGN_KEY $DOCKER_IMAGE
    - docker push $DOCKER_IMAGE
  only:
    - main

test:
  stage: test
  script:
    - pytest tests/unit/
    - pytest tests/integration/ --testcontainers
    - pact-verifier --provider-base-url http://staging-service:8080
  only:
    - main

deploy-staging:
  stage: deploy-staging
  script:
    - kubectl set image rollout/$