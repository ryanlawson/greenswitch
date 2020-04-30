# GreenSwitch

GreenSwitch works by triggering Lambda functions to start and stop instances on a scheduled basis.

Configuration is handled in `serverless.yml`. `InstanceNames` is a comma-separated list of instance names, and `Action` is either `ON` (turn on the instance) or `OFF` (turn off the instance). All instances with the listed names (regardless of ID) will be included. There is a delay of up to one minute before a scheduled trigger actually fires.

An example is below:

```yaml
functions:
  GreenSwitch:
    handler: greenswitch.handler
    events:
      - schedule:
         rate: cron(0 16 ? * 2-6 *)
         enabled: true
         input:
           InstanceNames: MyInstance1,MyInstance2
           Action: ON
      - schedule:
         rate: cron(0 20 ? * 2-6 *)
         enabled: true
         input:
           InstanceNames: MyInstance1,MyInstance2
           Action: OFF
```

The CRON schedule is in UTC format. See the [Serverless documentation](https://www.serverless.com/framework/docs/providers/aws/events/schedule/) for details.
