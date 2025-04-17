import boto3
import sys

def create_glue_connection(connection_name, connection_type, connection_properties, description='', tags={}):
    glue = boto3.client('glue')

    try:
        # Create the Glue connection
        response = glue.create_connection(
            ConnectionInput={
                'Name': connection_name,
                'Description': description,
                'ConnectionType': connection_type,
                'ConnectionProperties': connection_properties,
                'PhysicalConnectionRequirements': {
                    'AvailabilityZone': 'us-east-1a',  # Modify based on your region
                    'SecurityGroupIdList': ['sg-0123456789abcdef0'],  # Modify with your security group ID
                    'SubnetId': 'subnet-0bb1c79de3EXAMPLE'  # Modify with your subnet ID
                },
                'Tags': tags
            }
        )
        print(f"Connection {connection_name} created successfully.")
        return response
    except glue.exceptions.AlreadyExistsException:
        print(f"Connection {connection_name} already exists.")
        return None
    except Exception as e:
        print(f"Error creating connection {connection_name}: {str(e)}")
        sys.exit(1)


def update_glue_connection(connection_name, connection_properties):
    glue = boto3.client('glue')

    try:
        # Update an existing connection
        response = glue.update_connection(
            Name=connection_name,
            ConnectionProperties=connection_properties
        )
        print(f"Connection {connection_name} updated successfully.")
        return response
    except Exception as e:
        print(f"Error updating connection {connection_name}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    connection_name = sys.argv[1]
    connection_type = sys.argv[2]
    connection_properties = eval(sys.argv[3])  # Convert string to dictionary
    description = sys.argv[4] if len(sys.argv) > 4 else ''
    tags = eval(sys.argv[5]) if len(sys.argv) > 5 else {}

    # Check if the connection exists, and create or update accordingly
    create_connection_response = create_glue_connection(
        connection_name,
        connection_type,
        connection_properties,
        description,
        tags
    )

    if not create_connection_response:
        # If the connection already exists, update it
        print(f"Updating existing connection {connection_name}.")
        update_glue_connection(connection_name, connection_properties)
"""
rds_connection_name = my-rds-mysql-connection

python glue_connection.py my_connection_name JDBC "{'JDBC_CONNECTION_URL': 'jdbc:mysql://<host>:<port>', 'USERNAME': '<username>', 'PASSWORD': '<password>'}" "My JDBC connection" "{'Environment': 'Production'}"

"""