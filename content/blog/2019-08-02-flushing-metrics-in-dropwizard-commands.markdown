---
title: Flushing Metrics in Dropwizard Commands
date: 2019-08-02T18:19:32-07:00
tags:
- java
- dropwizard
- datadog
ghcommentid: 147
bbcommentid: 140
---
Users of Dropwizard Metrics will be familiar with `ScheduledReporter`  - it is a nice pattern that allows metrics reporting to be off loaded to a different thread which periodically sends out the collected metrics instead of making a network call every time a metric is collected. In most use cases, this works great - especially if you are running a server.

<!--more-->

However, the implementation of `ScheduledReporter` comes with an interesting quirk - it reports metrics only on the configured schedule, but does not flush the metrics it has collected after the last flush when the reporter is closed.

Datadog Metrics wires up ScheduledReporters that you configure as Dropwizard Lifecycle managed entities, guaranteeing that when your application shuts down, the reporter is closed.

This results in metrics collected immediately before an application is shutdown being discarded. This is especially problematic for Dropwizard commands that have varying run times depending on how much data processing it performs.

Imagine a Dropwizard command that when run downloads a file and processes it. Suppose the usual run time is in minutes, so you have configured your metric reporter's frequency to be `1 minute`, which is reasonable for this command. However, consider the situation where the downloaded file contains no data - the command will finish in seconds, thereby discarding any metric it has collected, as it hasn't ran for long enough for the scheduled reporter's executor to kick in.

## Solution

If you have the ability to override the specific `ScheduledReporter` you are using, you could inherit from it and override the `#close()` method to call `#report` before issuing `#stop`. For example, if you were using the `ConsoleReporter`, you could override the method and then use a [Service Provider Interface](https://docs.oracle.com/javase/tutorial/sound/SPI-intro.html) to provide your new reporter to Datadog Metrics.

The SPI goes in the file `src/main/resources/META-INF/services/io.dropwizard.metrics.ReporterFactory`

```
io.sadique.dropwizard.metrics.flush.CustomReporterFactory
```

```java
public class CustomReporterFactory extends BaseReporterFactory {
  @Override
  public ScheduledReporter build(MetricRegistry registry) {
    return FlushingReporter.forRegistry(registry)
      .build();
  }
}
```

If you are using a reporter like `DataogReporter`, it is hard to override it as the constructor is marked private. In such situations, we can create a wrapper that provides the overridden behavior:

```java
public class FlushOnCloseReporter extends ScheduledReporter  {
  private final ScheduledReporter wrapped;

  public FlushOnCloseReporter(ScheduledReporter wrapped, MetricRegistry registry, String name,
                              MetricFilter filter, TimeUnit rateUnit, TimeUnit durationUnit) {
    super(registry, name, filter, rateUnit, durationUnit);
    this.wrapped = wrapped;
  }

  @Override
  public void report(SortedMap<String, Gauge> gauges, SortedMap<String, Counter> counters,
                     SortedMap<String, Histogram> histograms, SortedMap<String, Meter> meters,
                     SortedMap<String, Timer> timers) {
    wrapped.report(gauges, counters, histograms, meters, timers);
  }

  @Override
  public void start(long period, TimeUnit unit) {
    wrapped.start(period, unit);
  }

  @Override
  public void stop() {
    wrapped.report();
    wrapped.stop();
  }
}
```

And the reporter factory can be modified to wrap the `DatadogReporter`.

```java
public class CustomReporterFactory extends BaseReporterFactory {
  @Override
  public ScheduledReporter build(MetricRegistry registry) {
    DatadogReporter consoleReporter = DatadogReporter.forRegistry(registry)
      .filter(getFilter())
      .convertDurationsTo(getDurationUnit())
      .convertRatesTo(getRateUnit())
      .build();
    return new FlushOnCloseReporter(consoleReporter, registry, "flush-on-close(DatadogReporter)",
      getFilter(), getRateUnit(), getDurationUnit());
  }
}
```

This will ensure that reports are always flushed before the reporter is shutdown by Dropwizard lifecycle.
