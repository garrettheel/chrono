# Chrono

**Note: still in development and likely not yet useful**

Chrono watches time series data and sends notifications when defined thresholds are exceeded.

## Concepts

### Backend

A backend system from which time series data can be retrieved. Currently only `graphite` is supported.

### Watch

Encapsulates a collection of time series data and thresholds on that data.

**Series**

A series of data to be used in a `Trigger`. The format varies based on the backend.

**Trigger**

An expression using one or more `Series`. If the result is `true`, the watch's `state`
will change and notifications may be sent.

```yaml
# Example watch targetting a graphite backend
watches:
  - name: web-response-time
    series:
      responseTime: "sumSeries(stats.gauges.service.web.duration.*.p90)"
    triggers:
      warning: "avg(responseTime) > 3"
```

### Notifier

A destination for notifications when a `Watch` changes state.

**webhook** - HTTP endpoint to receive a webhook notification
