"""
Comprehensive performance monitoring and optimization system.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import psutil
import gc

from src.core.performance_optimization import EnhancedPerformanceOptimizer
from src.integration.performance_integration import PerformanceIntegrationManager


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_percent: float
    process_memory_mb: float
    process_cpu_percent: float
    cache_hit_rate: float
    ai_cache_hit_rate: float
    db_cache_hit_rate: float
    active_connections: int
    response_time_avg: float
    error_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class PerformanceMonitor:
    """Comprehensive performance monitoring system."""
    
    def __init__(self, integration_manager: PerformanceIntegrationManager):
        self.integration_manager = integration_manager
        self.optimizer = integration_manager.optimizer
        self.logger = logging.getLogger(__name__)
        
        # Monitoring configuration
        self.monitoring_enabled = False
        self.monitoring_interval = 30  # seconds
        self.metrics_history = []
        self.max_history_size = 1000
        
        # Performance thresholds
        self.thresholds = {
            "cpu_critical": 90.0,
            "cpu_warning": 75.0,
            "memory_critical": 90.0,
            "memory_warning": 80.0,
            "response_time_critical": 10.0,
            "response_time_warning": 5.0,
            "cache_hit_rate_warning": 0.3,
            "error_rate_critical": 0.2,
            "error_rate_warning": 0.1
        }
        
        # Alert tracking
        self.alerts_sent = {}
        self.alert_cooldown = 300  # 5 minutes
        
        # Performance trends
        self.trend_analysis_enabled = True
        self.trend_window = 100  # Number of metrics to analyze for trends
        
        # Background tasks
        self.monitoring_task = None
        self.optimization_task = None
    
    async def start_monitoring(self) -> None:
        """Start comprehensive performance monitoring."""
        if self.monitoring_enabled:
            return
        
        self.monitoring_enabled = True
        
        # Start integration manager monitoring
        await self.integration_manager.start_performance_monitoring()
        
        # Start monitoring tasks
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        self.optimization_task = asyncio.create_task(self._optimization_loop())
        
        self.logger.info("Comprehensive performance monitoring started")
    
    async def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.monitoring_enabled = False
        
        # Stop monitoring tasks
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        if self.optimization_task:
            self.optimization_task.cancel()
            try:
                await self.optimization_task
            except asyncio.CancelledError:
                pass
        
        # Stop integration manager monitoring
        await self.integration_manager.stop_performance_monitoring()
        
        self.logger.info("Performance monitoring stopped")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_enabled:
            try:
                # Collect performance metrics
                metrics = await self._collect_metrics()
                
                # Store metrics
                self.metrics_history.append(metrics)
                
                # Maintain history size
                if len(self.metrics_history) > self.max_history_size:
                    self.metrics_history = self.metrics_history[-self.max_history_size:]
                
                # Check thresholds and send alerts
                await self._check_thresholds(metrics)
                
                # Analyze trends if enabled
                if self.trend_analysis_enabled:
                    await self._analyze_trends()
                
                # Wait for next monitoring cycle
                await asyncio.sleep(self.monitoring_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _optimization_loop(self) -> None:
        """Automatic optimization loop."""
        while self.monitoring_enabled:
            try:
                # Apply automatic optimizations every 5 minutes
                await asyncio.sleep(300)
                
                if not self.monitoring_enabled:
                    break
                
                # Get and apply optimizations
                optimizations = await self.integration_manager.apply_automatic_optimizations()
                
                if optimizations.get("applied_optimizations"):
                    self.logger.info(f"Applied automatic optimizations: {optimizations['applied_optimizations']}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in optimization loop: {e}")
                await asyncio.sleep(300)
    
    async def _collect_metrics(self) -> PerformanceMetrics:
        """Collect comprehensive performance metrics."""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024 * 1024)
            process_cpu = process.cpu_percent()
            
            # Cache metrics
            cache_stats = self.optimizer.cache.get_stats()
            ai_cache_stats = self.optimizer.ai_response_cache.get_stats()
            db_cache_stats = self.optimizer.db_query_cache.get_stats()
            
            # Connection metrics
            connection_stats = {}
            for name, pool in self.optimizer.connection_pools.items():
                connection_stats[name] = pool.get_stats()
            
            active_connections = sum(
                stats.get("active_connections", 0) 
                for stats in connection_stats.values()
            )
            
            # Performance metrics from components
            system_summary = await self.integration_manager.get_system_performance_summary()
            
            # Calculate average response time and error rate
            response_time_avg = 0.0
            error_rate = 0.0
            
            if "components" in system_summary:
                response_times = []
                error_counts = []
                total_requests = []
                
                for component_stats in system_summary["components"].values():
                    if isinstance(component_stats, dict):
                        if "avg_response_time" in component_stats:
                            response_times.append(component_stats["avg_response_time"])
                        if "error_count" in component_stats and "total_messages" in component_stats:
                            error_counts.append(component_stats["error_count"])
                            total_requests.append(component_stats["total_messages"])
                
                if response_times:
                    response_time_avg = sum(response_times) / len(response_times)
                
                if error_counts and total_requests:
                    total_errors = sum(error_counts)
                    total_reqs = sum(total_requests)
                    error_rate = total_errors / max(total_reqs, 1)
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available_mb=memory.available / (1024 * 1024),
                disk_percent=disk.percent,
                process_memory_mb=process_memory,
                process_cpu_percent=process_cpu,
                cache_hit_rate=cache_stats.get("hit_rate", 0.0),
                ai_cache_hit_rate=ai_cache_stats.get("hit_rate", 0.0),
                db_cache_hit_rate=db_cache_stats.get("hit_rate", 0.0),
                active_connections=active_connections,
                response_time_avg=response_time_avg,
                error_rate=error_rate
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")
            # Return default metrics on error
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_available_mb=0.0,
                disk_percent=0.0,
                process_memory_mb=0.0,
                process_cpu_percent=0.0,
                cache_hit_rate=0.0,
                ai_cache_hit_rate=0.0,
                db_cache_hit_rate=0.0,
                active_connections=0,
                response_time_avg=0.0,
                error_rate=0.0
            )
    
    async def _check_thresholds(self, metrics: PerformanceMetrics) -> None:
        """Check performance thresholds and send alerts."""
        alerts = []
        
        # CPU alerts
        if metrics.cpu_percent > self.thresholds["cpu_critical"]:
            alerts.append({
                "level": "critical",
                "metric": "cpu",
                "value": metrics.cpu_percent,
                "threshold": self.thresholds["cpu_critical"],
                "message": f"Critical CPU usage: {metrics.cpu_percent:.1f}%"
            })
        elif metrics.cpu_percent > self.thresholds["cpu_warning"]:
            alerts.append({
                "level": "warning",
                "metric": "cpu",
                "value": metrics.cpu_percent,
                "threshold": self.thresholds["cpu_warning"],
                "message": f"High CPU usage: {metrics.cpu_percent:.1f}%"
            })
        
        # Memory alerts
        if metrics.memory_percent > self.thresholds["memory_critical"]:
            alerts.append({
                "level": "critical",
                "metric": "memory",
                "value": metrics.memory_percent,
                "threshold": self.thresholds["memory_critical"],
                "message": f"Critical memory usage: {metrics.memory_percent:.1f}%"
            })
        elif metrics.memory_percent > self.thresholds["memory_warning"]:
            alerts.append({
                "level": "warning",
                "metric": "memory",
                "value": metrics.memory_percent,
                "threshold": self.thresholds["memory_warning"],
                "message": f"High memory usage: {metrics.memory_percent:.1f}%"
            })
        
        # Response time alerts
        if metrics.response_time_avg > self.thresholds["response_time_critical"]:
            alerts.append({
                "level": "critical",
                "metric": "response_time",
                "value": metrics.response_time_avg,
                "threshold": self.thresholds["response_time_critical"],
                "message": f"Critical response time: {metrics.response_time_avg:.2f}s"
            })
        elif metrics.response_time_avg > self.thresholds["response_time_warning"]:
            alerts.append({
                "level": "warning",
                "metric": "response_time",
                "value": metrics.response_time_avg,
                "threshold": self.thresholds["response_time_warning"],
                "message": f"Slow response time: {metrics.response_time_avg:.2f}s"
            })
        
        # Cache hit rate alerts
        if metrics.cache_hit_rate < self.thresholds["cache_hit_rate_warning"]:
            alerts.append({
                "level": "warning",
                "metric": "cache_hit_rate",
                "value": metrics.cache_hit_rate,
                "threshold": self.thresholds["cache_hit_rate_warning"],
                "message": f"Low cache hit rate: {metrics.cache_hit_rate:.2f}"
            })
        
        # Error rate alerts
        if metrics.error_rate > self.thresholds["error_rate_critical"]:
            alerts.append({
                "level": "critical",
                "metric": "error_rate",
                "value": metrics.error_rate,
                "threshold": self.thresholds["error_rate_critical"],
                "message": f"Critical error rate: {metrics.error_rate:.2f}"
            })
        elif metrics.error_rate > self.thresholds["error_rate_warning"]:
            alerts.append({
                "level": "warning",
                "metric": "error_rate",
                "value": metrics.error_rate,
                "threshold": self.thresholds["error_rate_warning"],
                "message": f"High error rate: {metrics.error_rate:.2f}"
            })
        
        # Send alerts with cooldown
        for alert in alerts:
            await self._send_alert(alert)
    
    async def _send_alert(self, alert: Dict[str, Any]) -> None:
        """Send performance alert with cooldown."""
        alert_key = f"{alert['metric']}_{alert['level']}"
        now = time.time()
        
        # Check cooldown
        if alert_key in self.alerts_sent:
            if now - self.alerts_sent[alert_key] < self.alert_cooldown:
                return  # Still in cooldown
        
        # Send alert (log for now, could be extended to send notifications)
        if alert["level"] == "critical":
            self.logger.critical(alert["message"])
        else:
            self.logger.warning(alert["message"])
        
        # Record alert time
        self.alerts_sent[alert_key] = now
        
        # Trigger immediate optimization for critical alerts
        if alert["level"] == "critical":
            await self._handle_critical_alert(alert)
    
    async def _handle_critical_alert(self, alert: Dict[str, Any]) -> None:
        """Handle critical performance alerts with immediate action."""
        try:
            if alert["metric"] == "memory":
                # Trigger garbage collection
                gc.collect()
                self.logger.info("Triggered garbage collection due to critical memory alert")
                
                # Clear some cache entries
                await self.optimizer.cache.cleanup_expired()
                await self.optimizer.ai_response_cache.cleanup_expired()
                await self.optimizer.db_query_cache.cleanup_expired()
                
            elif alert["metric"] == "cpu":
                # Reduce cache sizes temporarily
                original_cache_size = self.optimizer.cache.max_size
                self.optimizer.cache.max_size = max(original_cache_size // 2, 100)
                self.logger.info("Reduced cache size due to critical CPU alert")
                
            elif alert["metric"] == "response_time":
                # Enable more aggressive caching
                self.optimizer.cache.default_ttl = min(self.optimizer.cache.default_ttl * 1.5, 7200)
                self.logger.info("Increased cache TTL due to critical response time alert")
                
        except Exception as e:
            self.logger.error(f"Error handling critical alert: {e}")
    
    async def _analyze_trends(self) -> None:
        """Analyze performance trends."""
        if len(self.metrics_history) < self.trend_window:
            return
        
        try:
            recent_metrics = self.metrics_history[-self.trend_window:]
            
            # Analyze CPU trend
            cpu_values = [m.cpu_percent for m in recent_metrics]
            cpu_trend = self._calculate_trend(cpu_values)
            
            # Analyze memory trend
            memory_values = [m.memory_percent for m in recent_metrics]
            memory_trend = self._calculate_trend(memory_values)
            
            # Analyze response time trend
            response_time_values = [m.response_time_avg for m in recent_metrics]
            response_time_trend = self._calculate_trend(response_time_values)
            
            # Log significant trends
            if abs(cpu_trend) > 0.1:  # More than 0.1% per measurement
                direction = "increasing" if cpu_trend > 0 else "decreasing"
                self.logger.info(f"CPU usage trend: {direction} at {abs(cpu_trend):.2f}% per measurement")
            
            if abs(memory_trend) > 0.1:
                direction = "increasing" if memory_trend > 0 else "decreasing"
                self.logger.info(f"Memory usage trend: {direction} at {abs(memory_trend):.2f}% per measurement")
            
            if abs(response_time_trend) > 0.01:  # More than 0.01s per measurement
                direction = "increasing" if response_time_trend > 0 else "decreasing"
                self.logger.info(f"Response time trend: {direction} at {abs(response_time_trend):.3f}s per measurement")
                
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend slope using simple linear regression."""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x_values = list(range(n))
        
        # Calculate means
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        # Calculate slope
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Get the most recent performance metrics."""
        if not self.metrics_history:
            return None
        return self.metrics_history[-1]
    
    def get_metrics_history(self, hours: int = 1) -> List[PerformanceMetrics]:
        """Get performance metrics history for the specified number of hours."""
        if not self.metrics_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history if m.timestamp >= cutoff_time]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        current = self.metrics_history[-1]
        
        # Calculate averages over last hour
        recent_metrics = self.get_metrics_history(1)
        if recent_metrics:
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
            avg_response_time = sum(m.response_time_avg for m in recent_metrics) / len(recent_metrics)
            avg_cache_hit_rate = sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics)
        else:
            avg_cpu = current.cpu_percent
            avg_memory = current.memory_percent
            avg_response_time = current.response_time_avg
            avg_cache_hit_rate = current.cache_hit_rate
        
        return {
            "current": current.to_dict(),
            "averages_1h": {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_memory,
                "response_time_avg": avg_response_time,
                "cache_hit_rate": avg_cache_hit_rate
            },
            "thresholds": self.thresholds,
            "monitoring_enabled": self.monitoring_enabled,
            "metrics_count": len(self.metrics_history),
            "alerts_sent": len(self.alerts_sent),
            "timestamp": datetime.now().isoformat()
        }
    
    async def export_metrics(self, filepath: str, hours: int = 24) -> bool:
        """Export performance metrics to JSON file."""
        try:
            metrics = self.get_metrics_history(hours)
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "hours": hours,
                "metrics_count": len(metrics),
                "metrics": [m.to_dict() for m in metrics]
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info(f"Exported {len(metrics)} metrics to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
            return False
    
    async def optimize_based_on_metrics(self) -> Dict[str, Any]:
        """Optimize system based on current performance metrics."""
        if not self.metrics_history:
            return {"error": "No metrics available for optimization"}
        
        current = self.metrics_history[-1]
        optimizations = {}
        
        try:
            # Memory optimization
            if current.memory_percent > 80:
                gc.collect()
                await self.optimizer.cache.cleanup_expired()
                optimizations["memory_cleanup"] = True
            
            # Cache optimization
            if current.cache_hit_rate < 0.3:
                # Increase cache TTL
                self.optimizer.cache.default_ttl = min(self.optimizer.cache.default_ttl * 1.2, 7200)
                optimizations["increased_cache_ttl"] = True
            
            # Response time optimization
            if current.response_time_avg > 5.0:
                # Enable more aggressive caching
                self.optimizer.ai_response_cache.default_ttl = min(
                    self.optimizer.ai_response_cache.default_ttl * 1.3, 3600
                )
                optimizations["increased_ai_cache_ttl"] = True
            
            # CPU optimization
            if current.cpu_percent > 85:
                # Reduce batch sizes temporarily
                if isinstance(self.optimizer, EnhancedPerformanceOptimizer):
                    for model in self.optimizer.batch_processor.model_batch_sizes:
                        current_size = self.optimizer.batch_processor.model_batch_sizes[model]
                        self.optimizer.batch_processor.model_batch_sizes[model] = max(1, current_size - 1)
                optimizations["reduced_batch_sizes"] = True
            
            self.logger.info(f"Applied metric-based optimizations: {optimizations}")
            return {"optimizations": optimizations, "timestamp": datetime.now().isoformat()}
            
        except Exception as e:
            self.logger.error(f"Error in metric-based optimization: {e}")
            return {"error": str(e)}


class PerformanceDashboard:
    """Simple performance dashboard for monitoring."""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.logger = logging.getLogger(__name__)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for performance dashboard."""
        try:
            summary = self.monitor.get_performance_summary()
            
            # Add additional dashboard-specific data
            dashboard_data = {
                **summary,
                "status": "healthy" if self._is_system_healthy(summary) else "degraded",
                "recommendations": self._get_quick_recommendations(summary)
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {"error": str(e)}
    
    def _is_system_healthy(self, summary: Dict[str, Any]) -> bool:
        """Determine if system is healthy based on metrics."""
        if "current" not in summary:
            return False
        
        current = summary["current"]
        
        # Check critical thresholds
        if current.get("cpu_percent", 0) > 90:
            return False
        if current.get("memory_percent", 0) > 90:
            return False
        if current.get("response_time_avg", 0) > 10:
            return False
        if current.get("error_rate", 0) > 0.2:
            return False
        
        return True
    
    def _get_quick_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Get quick performance recommendations."""
        recommendations = []
        
        if "current" not in summary:
            return recommendations
        
        current = summary["current"]
        
        # Memory recommendations
        if current.get("memory_percent", 0) > 80:
            recommendations.append("Consider increasing available memory or reducing cache sizes")
        
        # CPU recommendations
        if current.get("cpu_percent", 0) > 75:
            recommendations.append("High CPU usage detected - consider optimizing AI model usage")
        
        # Cache recommendations
        if current.get("cache_hit_rate", 0) < 0.4:
            recommendations.append("Low cache hit rate - consider increasing cache TTL or size")
        
        # Response time recommendations
        if current.get("response_time_avg", 0) > 5:
            recommendations.append("Slow response times - enable more aggressive caching")
        
        return recommendations