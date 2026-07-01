## 1. End-to-End Cloud Migration Architecture (Main Diagram ⭐)

```mermaid
flowchart TD

%%====================
%% Source Systems
%%====================

subgraph Sources
A1[SAP]
A2[RDBMS]
A3[Salesforce]
A4[SFTP]
A5[REST APIs]
end

%%====================
%% Ingestion
%%====================

subgraph Ingestion
B1[AWS AppFlow]
B2[AWS DMS]
B3[AWS DataSync]
B4[AWS Glue]
end

%%====================
%% Raw Layer
%%====================

subgraph Raw Layer
C1[S3 Raw Bucket]
C2[Data Protection Engine]
end

%%====================
%% Bronze Layer
%%====================

subgraph Bronze Layer
D1[SQS]
D2[Lambda Validation]
D3[Step Functions]
D4[AWS Glue Bronze ETL]
D5[S3 Bronze]
end

%%====================
%% Silver Layer
%%====================

subgraph Silver Layer
E1[Step Functions]
E2[AWS Glue Silver ETL]
E3[S3 Silver]
end

%%====================
%% Gold Layer
%%====================

subgraph Gold Layer
F1[Step Functions]
F2[AWS Glue Gold ETL]
F3[S3 Gold]
end

%%====================
%% Analytics
%%====================

subgraph Analytics
G1[Glue Catalog]
G2[Amazon Athena]
G3[Redshift Spectrum]
G4[Power BI]
end

%%====================
%% Secure Layer
%%====================

subgraph Secure Layer
H1[Decrypt PII]
H2[Secure Database]
end

%%====================
%% Monitoring
%%====================

subgraph Monitoring
I1[DynamoDB Metadata]
I2[CloudWatch]
I3[SNS Alerts]
end

%%====================
%% Flow
%%====================

A1 --> B2
A2 --> B2
A3 --> B1
A4 --> B3
A5 --> B4

B1 --> C2
B2 --> C2
B3 --> C2
B4 --> C2

C2 --> C1

C1 --> D1
D1 --> D2
D2 --> D3
D3 --> D4
D4 --> D5

D5 --> E1
E1 --> E2
E2 --> E3

E3 --> F1
F1 --> F2
F2 --> F3

D4 --> G1
E2 --> G1
F2 --> G1

G1 --> G2
G1 --> G3

G2 --> G4
G3 --> G4

F3 --> H1
H1 --> H2

D2 --> I1
D4 --> I1
E2 --> I1
F2 --> I1

I2 --> I3
```
---

## 2. Medallion Architecture

```mermaid
flowchart LR

A[Source Systems]

B[Raw Layer]

C[Bronze Layer]

D[Silver Layer]

E[Gold Layer]

F[Secure Layer]

G[Power BI]

A --> B
B --> C
C --> D
D --> E

E --> G

E --> F
F --> G
```

## 3. Bronze Layer Processing

```mermaid
flowchart TD

A[S3 Raw Bucket]

B[S3 Event]

C[SQS]

D[Lambda]

E[File Validation]

F[Register Metadata]

G[DynamoDB]

H[Step Function]

I[Glue Bronze Job]

J[S3 Bronze]

K[Glue Catalog]

A --> B

B --> C

C --> D

D --> E

E --> F

F --> G

F --> H

H --> I

I --> J

I --> K
```

## 4. Silver & Gold Processing

```mermaid
flowchart TD

A[S3 Bronze]

B[Step Function]

C[Glue Silver]

D[S3 Silver]

E[Glue Catalog]

F[Step Function]

G[Glue Gold]

H[S3 Gold]

I[Glue Catalog]

J[Redshift Spectrum]

K[Athena]

L[Power BI]

A --> B

B --> C

C --> D

C --> E

D --> F

F --> G

G --> H

G --> I

I --> J

I --> K

J --> L

K --> L
```

## 5. Pipeline Orchestration

```mermaid
flowchart TD

Start([Pipeline Trigger])

A[Lambda]

B[Step Functions]

C[Glue Bronze]

D[Glue Silver]

E[Glue Gold]

F[Update Glue Catalog]

G[Update DynamoDB]

H[CloudWatch Logs]

I[SNS Alert]

End([Completed])

Start --> A

A --> B

B --> C

C --> D

D --> E

E --> F

F --> G

G --> End

C -.Failure.-> I

D -.Failure.-> I

E -.Failure.-> I

A --> H

C --> H

D --> H

E --> H
```

## 6. High Water Mark Processing
```mermaid
flowchart TD

A[Pipeline Start]

B[Read High Water Mark]

C{Source Modified?}

D[Skip Processing]

E[Read New Data]

F[Process Incremental Data]

G[Update High Water Mark]

H[DynamoDB]

End([Finish])

A --> B

B --> H

H --> C

C -->|No| D

C -->|Yes| E

E --> F

F --> G

G --> H

G --> End
```

## Sequence Diagram

```mermaid
sequenceDiagram

participant Source
participant Ingestion
participant S3
participant Lambda
participant StepFunction
participant Glue
participant GlueCatalog
participant DynamoDB
participant Athena
participant Redshift
participant PowerBI

Source->>Ingestion: Generate Data

Ingestion->>S3: Load Raw Data

S3->>Lambda: S3 Event

Lambda->>Lambda: Validate File

Lambda->>DynamoDB: Register Metadata

Lambda->>StepFunction: Start Workflow

StepFunction->>Glue: Bronze ETL

Glue->>GlueCatalog: Update Metadata

Glue->>S3: Write Bronze

StepFunction->>Glue: Silver ETL

Glue->>S3: Write Silver

Glue->>GlueCatalog: Update Metadata

StepFunction->>Glue: Gold ETL

Glue->>S3: Write Gold

Glue->>GlueCatalog: Update Metadata

Athena->>GlueCatalog: Read Metadata

Redshift->>GlueCatalog: External Tables

PowerBI->>Athena: Query Data

PowerBI->>Redshift: Query Data
```
