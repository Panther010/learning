# 1. High-Level Architecture

```mermaid
flowchart TD

A[Source Systems]

B[AWS DataSync]

C[S3 Landing Bucket]

D[S3 Object Created Event]

E[SQS Queue]

F[Lambda Validation & Routing]

G[Small File Processing]

H[AWS Glue ETL]

I[PostgreSQL Database]

J[DynamoDB Audit Table]

K[SNS Notification]

L[Dead Letter Queue]

M[Daily Summary Lambda]

N[Email Report]

A --> B
B --> C
C --> D
D --> E
E --> F

F -->|Small Files| G
F -->|Large Files| H

G --> I
H --> I

F --> J
H --> J
G --> J

F -->|Failure| K
H -->|Failure| K

E -->|3 Failed Attempts| L

J --> M
M --> N
```


# 2. Detailed ETL Flow
```mermaid
flowchart TD

Start([File Received])

A[DataSync Scheduled Copy]

B[S3 Landing Bucket]

C[S3 Event Notification]

D[SQS Queue]

E[Lambda Trigger]

F{Validation}

G[File Exists]

H[File Format]

I[Schema Validation]

J[File Size Check]

K{Small or Large?}

L[Lambda Processing]

M[Glue Job]

N[Transform Data]

O[Load to PostgreSQL]

P[Update DynamoDB]

Q[SNS Notification]

R[Dead Letter Queue]

End([Completed])

Start --> A
A --> B
B --> C
C --> D
D --> E

E --> F

F --> G
G --> H
H --> I
I --> J
J --> K

K -->|Small| L
K -->|Large| M

L --> N
M --> N

N --> O
O --> P
P --> End

F -->|Validation Failed| Q
L -->|Processing Failed| Q
M -->|Processing Failed| Q

Q --> R
```


# 3. Lambda Decision Flow
```mermaid
flowchart TD

A[SQS Message]

B[Lambda Invocation]

C[Read File Metadata]

D[Validate File]

E{Validation Passed?}

F[Send SNS Alert]

G[Update DynamoDB]

H{File Size < Threshold?}

I[Process Inside Lambda]

J[Trigger Glue Job]

K[Load into PostgreSQL]

L[Glue Loads into PostgreSQL]

M[Success]

A --> B
B --> C
C --> D

D --> E

E -->|No| F
F --> G

E -->|Yes| H

H -->|Small| I
H -->|Large| J

I --> K
J --> L

K --> G
L --> G

G --> M
```


# 4. Error Handling & Retry Mechanism
```mermaid
flowchart TD

A[SQS Queue]

B[Lambda]

C{Success?}

D[Delete Message]

E[Visibility Timeout<br/>240 Seconds]

F[Retry]

G{Receive Count >= 3?}

H[Dead Letter Queue]

I[SNS Notification]

J[Operations Team]

A --> B

B --> C

C -->|Yes| D

C -->|No| E

E --> F

F --> G

G -->|No| B

G -->|Yes| H

H --> I

I --> J
```


# 5. Daily Reporting Process
```mermaid
flowchart LR

A[EventBridge Cron]

B[Daily Summary Lambda]

C[DynamoDB]

D[Generate Statistics]

E[SNS Email]

F[Business Users]

A --> B

B --> C

C --> D

D --> E

E --> F
```


# 6. Sequence Diagram (Interview Favorite ⭐)
```mermaid
sequenceDiagram

participant Source
participant DataSync
participant S3
participant SQS
participant Lambda
participant Glue
participant PostgreSQL
participant DynamoDB
participant SNS

Source->>DataSync: New Aviation Files
DataSync->>S3: Copy Files

S3->>SQS: Object Created Event

SQS->>Lambda: Trigger Processing

Lambda->>Lambda: Validate File

alt Small File
    Lambda->>PostgreSQL: Load Data
else Large File
    Lambda->>Glue: Start Glue Job
    Glue->>S3: Read File
    Glue->>Glue: Transform Data
    Glue->>PostgreSQL: Bulk Load
end

Lambda->>DynamoDB: Update Status
Glue->>DynamoDB: Update Status

alt Failure
    Lambda->>SNS: Send Notification
    Glue->>SNS: Send Notification
end
```