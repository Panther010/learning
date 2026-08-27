# Day 1 Quick Start — Monday, 9 June 2026

**Total time:** 7-8 hours
**Repo:** `/Users/bakulseth/PycharmProjects/learning/`

---

## Morning Session (3 hours) — 9:00 AM - 12:00 PM

### Hour 1: SQL (9:00 - 10:00)
- [ ] Pick 2 hard SQL problems from LeetCode or HackerRank
- [ ] Focus: Window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)
- [ ] Solve them, then:
  ```bash
  cd ~/PycharmProjects/learning
  mkdir -p fundamentals/sql/interview_prep
  # Save your solutions with detailed comments
  git add fundamentals/sql/interview_prep/
  git commit -m "Day 1: Window function practice (2 problems)"
  git push
  ```

### Hour 2: PySpark (10:00 - 11:00)
- [ ] Open PyCharm, create `fundamentals/spark/interview_prep/day01_aggregations.py`
- [ ] Without looking up syntax, write a PySpark job that:
  - Creates a sample DataFrame (products with sales data)
  - Groups by category
  - Aggregates: count, sum, avg, max, min
  - Adds a running total using window function
- [ ] Test it runs locally
- [ ] Commit:
  ```bash
  git add fundamentals/spark/interview_prep/day01_aggregations.py
  git commit -m "Day 1: PySpark aggregations and window practice"
  git push
  ```

### Hour 3: Python DSA + Concept (11:00 - 12:00)
- [ ] Solve 1 medium LeetCode problem in Python
- [ ] Save to `fundamentals/python/interview_prep/day01_leetcode.py` with:
  - Problem description as docstring
  - Time complexity: O(?)
  - Space complexity: O(?)
  - Your solution with comments
- [ ] Learn decorators (30 min):
  - Read about @property, @classmethod, @staticmethod
  - Write example code in `fundamentals/python/concepts/decorators.py`
- [ ] Commit both files

---

## Lunch Break (12:00 PM - 1:00 PM)

---

## Afternoon Session (2.5 hours) — 1:00 PM - 3:30 PM

### Hour 4: AWS Deep Dive (1:00 - 2:00)
- [ ] Study S3 + Glue:
  - S3: buckets, versioning, lifecycle policies, encryption (SSE-S3, SSE-KMS), access patterns
  - Glue: data catalog, crawlers, ETL jobs, job bookmarks
- [ ] Create `docs/notes/aws_services.md` and write summary in your own words
- [ ] Include: when to use what, pricing implications, common patterns
- [ ] Commit the notes

### Hour 5: Concept of the Day (2:00 - 3:00)
- [ ] Topic: **Partitioning Strategies**
  - Hash partitioning (even distribution, no range queries)
  - Range partitioning (time-based, enables pruning)
  - List partitioning (discrete values, regional data)
- [ ] Create `docs/notes/concepts/partitioning_strategies.md`
- [ ] Include:
  - When to use each
  - PySpark examples for each type
  - Trade-offs (write performance vs read performance)
- [ ] Commit

### Half Hour: AI Theory (3:00 - 3:30)
- [ ] Read Anthropic's prompt engineering guide:
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- [ ] Focus: few-shot prompting, chain-of-thought, role prompting
- [ ] Create `docs/notes/ai/01_prompt_engineering_patterns.md`
- [ ] Write examples of each pattern
- [ ] Commit

---

## Evening Session (2.5 hours) — 4:00 PM - 6:30 PM

### Project 1: Docker Setup (4:00 - 5:30)

**Goal:** Get Docker running with a simple PySpark container

- [ ] Install Docker Desktop if not already installed
- [ ] Create project folder:
  ```bash
  cd ~/PycharmProjects/learning
  mkdir -p projects/01_docker_airflow_starter
  cd projects/01_docker_airflow_starter
  ```
- [ ] Create `Dockerfile.spark`:
  ```dockerfile
  FROM python:3.11-slim
  
  # Install Java (required for Spark)
  RUN apt-get update && \
      apt-get install -y openjdk-11-jdk wget && \
      rm -rf /var/lib/apt/lists/*
  
  # Install PySpark
  RUN pip install pyspark==3.5.0
  
  # Set working directory
  WORKDIR /app
  
  CMD ["python"]
  ```
- [ ] Create `spark_jobs/hello_spark.py`:
  ```python
  from pyspark.sql import SparkSession
  
  spark = SparkSession.builder.appName("HelloSpark").getOrCreate()
  
  data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
  df = spark.createDataFrame(data, ["name", "age"])
  
  df.show()
  df.groupBy().avg("age").show()
  
  spark.stop()
  print("✅ Spark job completed successfully")
  ```
- [ ] Test:
  ```bash
  docker build -f Dockerfile.spark -t my-pyspark .
  docker run -v $(pwd)/spark_jobs:/app my-pyspark python hello_spark.py
  ```
- [ ] Create `README.md` documenting what you built
- [ ] Commit everything

### Project 2: Claude API Setup (5:30 - 6:30)

**Goal:** Send your first API call to Claude

- [ ] Go to console.anthropic.com → get API key
- [ ] Store it safely (never commit to git): `export ANTHROPIC_API_KEY=your_key`
- [ ] Install SDK:
  ```bash
  pip install anthropic
  ```
- [ ] Create `projects/02_sql_generator_ai/api_basics.py`:
  ```python
  import anthropic
  import os
  
  client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
  
  message = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": "Explain what a foreign key is in 2 sentences"}
      ]
  )
  
  print(message.content[0].text)
  ```
- [ ] Run it: `python api_basics.py`
- [ ] Experiment: try different prompts, add system prompts
- [ ] Create `projects/02_sql_generator_ai/README.md` explaining what you learned
- [ ] Commit (without API key!)

---

## End of Day Wrap-Up (6:30 - 7:00 PM)

### Daily Non-Negotiables (30 min)

- [ ] Apply to 5-10 jobs on LinkedIn (use Easy Apply filter)
- [ ] Update LinkedIn headline if not done yet: "Senior Data Engineer | Python, PySpark, AWS | Building AI-powered data pipelines"
- [ ] Review your commits for the day:
  ```bash
  git log --oneline --since="1 day ago"
  ```
- [ ] Fill out Day 1 reflection in your study plan

---

## What You'll Have After Day 1

✅ 2 hard SQL problems solved (window functions)
✅ 1 PySpark transformation from scratch
✅ 1 Python LeetCode + decorator knowledge
✅ AWS notes (S3 + Glue)
✅ Partitioning strategies documented
✅ Prompt engineering basics learned
✅ Docker running PySpark jobs
✅ Claude API working
✅ 5-10 job applications sent
✅ 6-8 git commits to your learning repo

**Tomorrow:** Continue Week 1 pattern with new SQL/PySpark/Python problems, study EMR + Redshift, learn generators, continue Docker + Claude projects.

---

## Tips for Success

1. **Strict time-boxing** — Set a timer. When hour is up, commit what you have and move on.
2. **Git commit frequently** — Every task = 1 commit. Builds your GitHub activity graph.
3. **Write comments/docs** — Your future interview self will thank you.
4. **No perfectionism** — Done > perfect. You're building momentum.
5. **Stack Overflow is OK** — But type out solutions yourself, don't copy-paste.

---

Good luck! 🚀
