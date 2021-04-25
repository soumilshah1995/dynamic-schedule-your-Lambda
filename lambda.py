__AUTHOR__ = "Soumil shah "
__EMAIL__  = ["shahsoumil519@gmail.com"]

try:
    import json
    import boto3
    import os
except Exception as e:
    pass



# ------------------------------------Settings ---------------------------------------
global AWS_ACCESS_KEY
global AWS_SECRET_KEY
global AWS_REGION_NAME
global BUCKET
global URL
global DESTINATION

AWS_ACCESS_KEY = "XXX"
AWS_SECRET_KEY ="XXXXX/XXXX"
AWS_REGION_NAME = "us-east-1"
# ---------------------------------------------------------------------------------------



class EventBridge(object):

    def __init__(self, instance=None):
        self.instance =instance
        self.client = boto3.client("events",
                                   aws_access_key_id=AWS_ACCESS_KEY,
                                   aws_secret_access_key=AWS_SECRET_KEY,
                                   region_name=AWS_REGION_NAME)

    def run(self):
        try:

            response = self.client.put_rule(
                Name=self.instance.RuleName,
                ScheduleExpression=self.instance.ScheduleExpression,
                State=self.instance.State,
                Description=self.instance.Description,
            )

            response = self.client.put_targets(
                Rule = self.instance.RuleName,
                Targets = [
                    {
                        'Id': self.instance.Id,
                        'Arn': self.instance.lambdaArn,
                        'Input': json.dumps(self.instance.inputEvent),
                    },
                ],
            )
            return response

        except Exception as e:
            return 'error'


class InputTriggers(object):

    def __init__(self, RuleName='', ScheduleExpression='',
                 State='DISABLED', Description='', lambdaArn='',
                 inputEvent = {}, Id='test-id'):

        self.RuleName           = RuleName
        self.ScheduleExpression = "cron({})".format(ScheduleExpression)
        self.State              = State
        self.Description        = Description
        self.lambdaArn          = lambdaArn
        self.inputEvent         = inputEvent
        self.Id                 = Id


def lambda_handler(event=None, context=None):
    try:
        instance_ = InputTriggers(RuleName='MyProgramaticRule',
                                  ScheduleExpression='0/15 * * * ? *',
                                  lambdaArn='arn:aws:lambda:us-east-1:586073383152:function:lambda2')

        instanceEvent = EventBridge(instance=instance_)
        isFlag = instanceEvent.run()
        print(isFlag)
        return isFlag

    except Exception as e:
        print('error : {} '.format(e))


lambda_handler()
