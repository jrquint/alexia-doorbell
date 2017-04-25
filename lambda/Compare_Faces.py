import boto3
import json

def lambda_handler(event, context):
    person = ''
    #Configure Bucket Name for Images
    bucket='IMAGES BUCKET'
    key_name='uploads/latest.jpeg'
    #Generate list of know faces:
    target_key_names= {'Brendan' : 'known/brendan.jpg', 'Eric' : 'known/eric.jpg', 'Josh' : 'known/josh.jpg', 'Merim' : 'known/merim.jpg', 'Jeff' : 'known/jeff.jpg', 'Jen' : 'known/jen.jpg', 'Mike' : 'known/mike.jpg'}
    # Set Dynamo DB Table and Location
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('faces')

    for name, target_key_name in target_key_names.iteritems():
        client = boto3.client('rekognition')
        response = client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': target_key_name
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key_name
                }
            },
            SimilarityThreshold=50
        )
        print str(response)
        if len(response['FaceMatches']) > 0:
            person = str(name)
            table.put_item(
             Item={
               'name': name,
               'present': 'true'
            }
            )

    return {"type": person}
