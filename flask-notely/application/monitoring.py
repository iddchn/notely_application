from prometheus_flask_exporter import PrometheusMetrics

def setup_monitoring(app):
    PrometheusMetrics(app)
    app.logger.info("Monitoring setup complete")
