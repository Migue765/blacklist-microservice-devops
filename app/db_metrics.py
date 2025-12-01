"""
Database metrics helper for New Relic
Measures and records database query response times
"""
import time
import functools
from contextlib import contextmanager

def measure_db_time(operation_type="query"):
    """
    Decorator to measure database operation time and record metrics
    
    Args:
        operation_type: Type of operation (query, insert, update, delete)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Record metric in New Relic
                try:
                    import newrelic.agent
                    metric_name = f'Custom/Database/{operation_type.capitalize()}Time'
                    newrelic.agent.record_custom_metric(metric_name, elapsed_time)
                    newrelic.agent.record_custom_metric('Custom/Database/TotalQueries', 1)
                    newrelic.agent.add_custom_attribute('db_operation', operation_type)
                    newrelic.agent.add_custom_attribute('db_response_time_ms', elapsed_time)
                except (ImportError, AttributeError):
                    pass  # New Relic not available
                
                return result
            except Exception as e:
                elapsed_time = (time.time() - start_time) * 1000
                
                # Record error metric
                try:
                    import newrelic.agent
                    newrelic.agent.record_custom_metric(f'Custom/Database/{operation_type.capitalize()}Error', 1)
                    newrelic.agent.record_custom_metric('Custom/Database/TotalErrors', 1)
                    newrelic.agent.add_custom_attribute('db_operation', operation_type)
                    newrelic.agent.add_custom_attribute('db_error_time_ms', elapsed_time)
                except (ImportError, AttributeError):
                    pass
                
                raise
        return wrapper
    return decorator


@contextmanager
def db_operation_timer(operation_type="query"):
    """
    Context manager to measure database operation time
    
    Usage:
        with db_operation_timer("insert"):
            db.session.add(entry)
            db.session.commit()
    """
    start_time = time.time()
    try:
        yield
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Record metric in New Relic
        try:
            import newrelic.agent
            metric_name = f'Custom/Database/{operation_type.capitalize()}Time'
            newrelic.agent.record_custom_metric(metric_name, elapsed_time)
            newrelic.agent.record_custom_metric('Custom/Database/TotalQueries', 1)
            newrelic.agent.add_custom_attribute('db_operation', operation_type)
            newrelic.agent.add_custom_attribute('db_response_time_ms', elapsed_time)
            
            # Record slow query if > 100ms
            if elapsed_time > 100:
                newrelic.agent.record_custom_metric('Custom/Database/SlowQueries', 1)
                newrelic.agent.add_custom_attribute('slow_query_time_ms', elapsed_time)
        except (ImportError, AttributeError):
            pass  # New Relic not available
    except Exception as e:
        elapsed_time = (time.time() - start_time) * 1000
        
        # Record error metric
        try:
            import newrelic.agent
            newrelic.agent.record_custom_metric(f'Custom/Database/{operation_type.capitalize()}Error', 1)
            newrelic.agent.record_custom_metric('Custom/Database/TotalErrors', 1)
            newrelic.agent.add_custom_attribute('db_operation', operation_type)
            newrelic.agent.add_custom_attribute('db_error_time_ms', elapsed_time)
        except (ImportError, AttributeError):
            pass
        
        raise


def record_db_metric(operation_type, elapsed_time_ms, success=True):
    """
    Record a database metric directly
    
    Args:
        operation_type: Type of operation (query, insert, update, delete)
        elapsed_time_ms: Time elapsed in milliseconds
        success: Whether the operation was successful
    """
    try:
        import newrelic.agent
        if success:
            metric_name = f'Custom/Database/{operation_type.capitalize()}Time'
            newrelic.agent.record_custom_metric(metric_name, elapsed_time_ms)
            newrelic.agent.record_custom_metric('Custom/Database/TotalQueries', 1)
            
            # Record slow query if > 100ms
            if elapsed_time_ms > 100:
                newrelic.agent.record_custom_metric('Custom/Database/SlowQueries', 1)
        else:
            newrelic.agent.record_custom_metric(f'Custom/Database/{operation_type.capitalize()}Error', 1)
            newrelic.agent.record_custom_metric('Custom/Database/TotalErrors', 1)
        
        newrelic.agent.add_custom_attribute('db_operation', operation_type)
        newrelic.agent.add_custom_attribute('db_response_time_ms', elapsed_time_ms)
    except (ImportError, AttributeError):
        pass  # New Relic not available

