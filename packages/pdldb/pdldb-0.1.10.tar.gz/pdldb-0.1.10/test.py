from pdldb import S3LakeManager
import os

lake = S3LakeManager(
    base_path=os.getenv("S3_URI"),
    aws_region=os.getenv("AWS_REGION"),
    aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    dynamodb_locking_table=os.getenv("DYNAMODB_LOCKING_TABLE"),
)

print(lake.list_tables())

print(lake.get_data_frame("ohlcv_h"))

""" from pdldb import S3LakeManager
import os
import boto3

# Print environment variables for verification
s3_uri = os.getenv("S3_URI")
aws_region = os.getenv("AWS_REGION")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
dynamo_table = os.getenv("DYNAMODB_LOCKING_TABLE")

print(f"S3_URI: {s3_uri}")
print(f"AWS_REGION: {aws_region}")
print(f"AWS has credentials: {bool(aws_access_key and aws_secret_key)}")
print(f"DynamoDB table: {dynamo_table}")

# Verify we can list the S3 bucket contents directly
try:
    s3_client = boto3.client('s3', 
                            region_name=aws_region,
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key)
    
    # Parse the S3 URI
    bucket = s3_uri.replace('s3://', '').split('/')[0]
    prefix = '/'.join(s3_uri.replace('s3://', '').split('/')[1:])
    if not prefix.endswith('/'):
        prefix += '/'
    
    print(f"\nChecking S3 bucket: {bucket} with prefix: {prefix}")
    
    # List objects to verify access
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    print(f"Direct S3 list response has CommonPrefixes: {'CommonPrefixes' in response}")
    
    if 'CommonPrefixes' in response:
        print("Directories found:")
        for common_prefix in response['CommonPrefixes']:
            prefix_path = common_prefix['Prefix']
            print(f"  - {prefix_path}")
            
            # Check for _delta_log directory
            delta_log_check = s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=f"{prefix_path}_delta_log/",
                MaxKeys=1
            )
            
            is_delta_table = 'Contents' in delta_log_check and len(delta_log_check['Contents']) > 0
            print(f"    Has _delta_log: {is_delta_table}")
            
            if is_delta_table:
                # List some files in the delta log
                log_files = s3_client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=f"{prefix_path}_delta_log/",
                    MaxKeys=5
                )
                if 'Contents' in log_files:
                    print(f"    Delta log files: {[obj['Key'] for obj in log_files['Contents'][:3]]}")
                
except Exception as e:
    print(f"Error accessing S3 directly: {e}")

# Now create the lake manager
lake = S3LakeManager(
    base_path=s3_uri,
    aws_region=aws_region,
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_key,
    dynamodb_locking_table=dynamo_table,
)

tables = lake.list_tables()
print(f"\nLake tables: {tables}")

# Enable debug mode if available
if hasattr(lake, 'enable_debug'):
    lake.enable_debug()

# Try to get more info about the lake manager implementation
print(f"\nLake manager class: {lake.__class__.__name__}")
if hasattr(lake, 'table_manager'):
    print(f"Table manager class: {lake.table_manager.__class__.__name__}")
    if hasattr(lake.table_manager, 'tables'):
        print(f"Tables in table_manager: {lake.table_manager.tables}") """
