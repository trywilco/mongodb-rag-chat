#!/bin/bash

echo "Wilco: Hi, Welcome to Wilco MongoDB Atlas Cluster Setup!"
echo "Wilco: We'll guide you through the process of setting up a MongoDB Atlas cluster."
# Step 1: Register or authenticate the user
echo "Wilco: Please register or authenticate using MongoDB Atlas."
echo "Wilco: (If you already have an account, please click login on the MongoDB registeration screen and paste your CLI Key)"
echo "Wilco: Click CMD/CTRL + link to open it (or copy paste it) and click Open on the notification"
atlas auth register --noBrowser
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'auth register', please contact Wilco support."
    exit 1
fi

# Step 2: Create a new organization and capture the Organization ID
echo "Wilco: Creating a new organization named 'WilcoOrg'."
org_output=$(atlas organizations create WilcoOrg)
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'organizations create'. Please contact Wilco support."
    exit 1
fi

# Extract the Organization ID from the output using awk
org_id=$(echo "$org_output" | awk -F"'" '/Organization / {print $2}')

if [ -z "$org_id" ]; then
    echo "Wilco: Failed to create organization or capture the Organization ID. Exiting. Please contact Wilco support."
    exit 1
fi

echo "Wilco: A new Organization created with ID $org_id"

# Step 3: Create a new project and capture the Project ID
echo "Wilco: Creating a new project named 'WilcoMongo'."
project_output=$(atlas projects create WilcoMongo --orgId $org_id)
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'projects create'. Please contact Wilco support."
    exit 1
fi

# Extract the Project ID from the output using awk
project_id=$(echo "$project_output" | awk -F"'" '/Project / {print $2}')

if [ -z "$project_id" ]; then
    echo "Wilco: Failed to create project or capture the Project ID. Exiting. Please contact Wilco support."
    exit 1
fi

echo "Wilco: Project created with ID $project_id"

# Step 4: Add access list entry
echo "Wilco: Adding access list entry for IP address 0.0.0.0 so Wilco can connect to it!"
atlas accessList create 0.0.0.0 --type ipAddress --projectId $project_id
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'accessList create'. Please contact Wilco support."
    exit 1
fi

# Step 5: Create a cluster in the newly created project
echo "Wilco: Creating a MongoDB cluster in the project 'WilcoMongo' for your Wilco application (This might take a few min, dont close anything, once done you'll see your cluster details)"
atlas cluster create WilcoMongo --projectId $project_id --provider AWS --region US_EAST_1 --tier M0 --watch
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'cluster create'. Please contact Wilco support."
    exit 1
fi

# Step 6: Create a database user
echo "Wilco: Creating a database user 'WilcoDbUser' for your Wilco application."
atlas dbusers create atlasAdmin --username WilcoDbUser --password Wilco12345678 --projectId $project_id
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'dbusers create'. Please contact Wilco support."
    exit 1
fi

# Initialize variables to capture specific outputs
matched_string=""
full_connection_string=""
cleaned_connection_string=""

# Output the captured values with labels inside an ASCII square
echo "┌─────────────────── Wilco MongoDB Details ────────────────────────────────────────────────────┐"
echo "| Your Wilco MongoDB Atlas Cluster is being created.                                           |"
echo "| This may take a few minutes. Once done you'll see your details below                         |"
sleep 5
full_connection_string=$(atlas clusters connectionStrings describe WilcoMongo --projectId $project_id | grep -A 1 "mongodb+srv" | tail -n 1)
if [ $? -ne 0 ]; then
    echo "Wilco: Something went wrong with atlas command 'clusters connectionStrings describe'. Please contact Wilco support."
    exit 1
fi

cleaned_connection_string=${full_connection_string#mongodb+srv://}

connection_string="mongodb+srv://WilcoDbUser:Wilco12345678@$cleaned_connection_string"

# Add connection string to the chat server app
cat <<EOF > backend/.env
VECTOR_SEARCH_INDEX_NAME=vector_index
MONGODB_DATABASE_NAME=movies_quest
MONGODB_CONNECTION_URI=$connection_string
EOF

# Restart the services to apply the new connection string
docker compose restart

echo "| Your connection string: >> $connection_string "
echo "| Copy the connection string above from mongodb+srv and paste it in the chat                   |"
echo "└─────────────────── Wilco MongoDB Details ────────────────────────────────────────────────────┘"
