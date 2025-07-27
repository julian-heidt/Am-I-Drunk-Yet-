# Are You Drunk Yet? 🍺

A modern web application for calculating Blood Alcohol Content (BAC) with comprehensive observability and monitoring capabilities.

## 🎯 Overview

This application helps users calculate:
- **Number of drinks** needed to reach a target BAC of 0.1%
- **Time to sober** - how long until BAC returns to zero

Built with a unified Flask architecture featuring OpenTelemetry tracing, Prometheus metrics, and Grafana dashboards for complete observability.

⚠️ **Disclaimer**: This tool is for educational and entertainment purposes only. Do not use it to determine fitness to drive or operate machinery.

## 🏗️ Architecture

### Single-Service Design
- **Unified Flask App** - Serves both web UI and API endpoints
- **Same-Origin Requests** - Eliminates CORS issues
- **Simplified Deployment** - Single container with embedded observability

### Observability Stack
- **OpenTelemetry** - Distributed tracing converted to metrics
- **Prometheus** - Metrics collection and storage
- **Grafana** - Real-time dashboards and visualization

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- 4GB+ RAM recommended

### Launch Application
```bash
# Clone and navigate to the project
cd AreYouDrunkYet

# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Access Services
- **Web Application**: http://localhost
- **Prometheus Metrics**: http://localhost:9090
- **Grafana Dashboards**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

## 📊 Features

### Core Functionality
- **BAC Calculation** - Based on Widmark formula
- **Responsive Design** - Works on desktop and mobile
- **Theme Support** - Multiple color themes and dark/light mode
- **Input Validation** - Comprehensive error handling

### Business Intelligence
- **User Demographics** - Weight and gender distribution analysis
- **Usage Patterns** - Peak usage times and calculation frequency
- **Recommendation Insights** - Drink recommendation patterns

### Performance Monitoring
- **Request Tracing** - End-to-end request lifecycle
- **Response Times** - 95th and 50th percentile latencies
- **Error Tracking** - Real-time error rates and types
- **Resource Usage** - Application performance metrics

## 🔧 Technology Stack

### Backend
- **Flask** - Web framework and API server
- **OpenTelemetry** - Distributed tracing instrumentation
- **Prometheus Client** - Metrics collection
- **Gunicorn** - Production WSGI server

### Frontend
- **Bootstrap 5** - UI framework
- **Vanilla JavaScript** - No framework dependencies
- **CSS Custom Properties** - Theme system

### Infrastructure
- **Docker** - Containerization
- **Prometheus** - Metrics storage
- **Grafana** - Visualization platform

## 📈 Metrics & Monitoring

### Custom Business Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `calculations_total` | Counter | Total calculations by gender and result type |
| `calculation_duration_seconds` | Histogram | Time spent on different operations |
| `drinks_recommended` | Histogram | Distribution of drink recommendations |
| `user_weight_kg` | Histogram | User weight distribution patterns |
| `span_duration_seconds` | Histogram | Trace-like timing for operations |

### Default Flask Metrics
- HTTP request rates and response times
- Response status code distribution
- Request size and response size histograms

### Grafana Dashboards

**Are You Drunk Yet - Application Dashboard** includes:
- **Total Calculations** - Usage statistics
- **User Demographics** - Gender and weight distributions  
- **Request Performance** - Response times and rates
- **Business Insights** - Drink recommendation patterns
- **Error Monitoring** - Real-time error tracking
- **Operation Performance** - Individual function timing

## 🧮 BAC Calculation Details

### Widmark Formula
```
BAC = (Alcohol consumed in grams) / (Body weight in grams × r)
```

Where `r` is the Widmark factor:
- **Male**: 0.68
- **Female**: 0.55  
- **Other**: 0.615 (average)

### Assumptions
- **Standard Drink**: 14 grams of alcohol
- **Target BAC**: 0.1% (legal intoxication threshold in many jurisdictions)
- **Metabolism Rate**: 0.015% BAC per hour

## 🐳 Docker Configuration

### Services

| Service | Port | Description |
|---------|------|-------------|
| `app` | 80 | Main Flask application |
| `prometheus` | 9090 | Metrics collection server |
| `grafana` | 3000 | Dashboard and visualization |

### Volumes
- `prometheus-data` - Persistent metrics storage
- `grafana-data` - Dashboard and configuration storage

### Health Checks
- Application health endpoint: `/health`
- Automatic container health monitoring
- Prometheus scraping health validation

## 🔍 API Endpoints

### Web Routes
- `GET /` - Main application interface
- `GET /favicon.ico` - Favicon handler
- `GET /health` - Health check endpoint

### API Routes
- `POST /api/calculate` - BAC calculation endpoint

#### Calculate BAC Request
```json
{
  "weight": 70.0,
  "gender": "male",
  "current_drinks": 2
}
```

#### Calculate BAC Response
```json
{
  "drinks_to_reach_target": 3.2,
  "time_to_sober": 4.5
}
```

## 📁 Project Structure

```
AreYouDrunkYet/
├── app/                                    # Main application
│   ├── main.py                            # Flask app with observability
│   ├── calculator.py                      # BAC calculation logic
│   ├── requirements.txt                   # Python dependencies
│   ├── Dockerfile                         # Container configuration
│   ├── static/                           # Frontend assets
│   │   ├── css/style.css                 # Themes and styling
│   │   └── js/script.js                  # Application logic
│   └── templates/                        # HTML templates
│       └── index.html                    # Main application page
├── grafana/                              # Dashboard configuration
│   └── provisioning/
│       ├── datasources/
│       │   └── datasources.yaml         # Prometheus connection
│       └── dashboards/
│           ├── dashboards.yaml           # Dashboard provider
│           └── are-you-drunk-yet-dashboard.json
├── docker-compose.yml                    # Service orchestration
├── prometheus.yml                        # Metrics collection config
└── README.md                            # This file
```

## 🛠️ Development

### Local Development
```bash
# Install dependencies
cd app
pip install -r requirements.txt

# Run Flask development server
python main.py

# Access application at http://localhost:5000
```

### Adding New Metrics
```python
from prometheus_client import Counter, Histogram

# Define custom metric
my_metric = Counter('my_metric_total', 'Description', ['label1', 'label2'])

# Record metric
my_metric.labels(label1='value1', label2='value2').inc()
```

### Viewing Metrics
- **Raw metrics**: http://localhost/metrics
- **Prometheus UI**: http://localhost:9090
- **Grafana dashboards**: http://localhost:3000

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `PORT` | `5000` | Application port |

### Prometheus Configuration
- **Scrape interval**: 5 seconds for app metrics
- **Retention**: Default Prometheus retention policy
- **Targets**: Automatic service discovery via Docker

### Grafana Configuration
- **Auto-provisioning**: Datasources and dashboards
- **Default user**: admin/admin
- **Data source**: Prometheus (automatic)

## 🚨 Troubleshooting

### Common Issues

**Application not accessible**
```bash
# Check container status
docker-compose ps

# View application logs
docker-compose logs app

# Restart services
docker-compose restart
```

**Metrics not appearing**
```bash
# Check Prometheus targets
# Go to http://localhost:9090/targets

# Verify metrics endpoint
curl http://localhost/metrics

# Check Prometheus configuration
docker-compose logs prometheus
```

**Grafana dashboard not loading**
```bash
# Check Grafana logs
docker-compose logs grafana

# Verify dashboard provisioning
docker exec grafana ls -la /etc/grafana/provisioning/dashboards/
```

### Performance Tuning

**High memory usage**
```yaml
# In docker-compose.yml, add memory limits
services:
  app:
    mem_limit: 512m
  prometheus:
    mem_limit: 1g
  grafana:
    mem_limit: 256m
```

**Slow response times**
```yaml
# Scale application workers
services:
  app:
    environment:
      - GUNICORN_WORKERS=8
```

## 📝 License

This project is for educational purposes. Please drink responsibly and never drink and drive.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all metrics are properly instrumented
5. Update documentation
6. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review container logs
3. Verify metric collection in Prometheus
4. Check Grafana dashboard configuration

---

**Remember**: This tool is for entertainment only. Always drink responsibly! 🍻 