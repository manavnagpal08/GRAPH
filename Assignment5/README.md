# Graph Analytics Assignment 5: University Course Registration System Using Neo4j

**Alliance University** | **Alliance School of Advanced Computing**  
**Student Name:** Manav Nagpal  
**Registration Number:** 2411021060402  
**Course Code & Title:** E1CSA332 / Graph Analytics  
**Academic Year & Semester:** 2026-27 | Semester V  

---

## 1. Overview & Objectives

This project implements a Graph Database for an academic course registration system in **Neo4j** using the **Cypher Query Language**. The system models four primary entities as nodes (`Student`, `Faculty`, `Course`, `Department`) and connects them via directed semantic relationships (`ENROLLED_IN`, `TEACHES`, `BELONGS_TO`, `OFFERS`).

Every query across **Part A (Graph Creation & Verification)** and **Part B (Retrieval & Filtering)** has been implemented idempotently, executed against a live Neo4j 5.26.0 server, verified, and compiled into a complete Word submission report with screenshots.

---

## 2. Project Directory Structure

```text
assignment 5/
├── assignment5.cypher          # Master Cypher script with all setup, constraints, and 14 queries
├── populate_and_execute.py     # Python automation script that executes all queries via Neo4j Bolt driver
├── generate_task_screenshots.py# Generates high-fidelity Neo4j terminal/browser screenshots
├── build_word_report.py        # Generates the complete, professional Word report (.docx)
├── README.md                   # Setup, execution, and verification guide
├── report/
│   └── Graph_Analytics_Assignment_5_Report.docx # Final submission document
└── results/
    ├── all_results.json        # Structured JSON containing raw query results for all 14 tasks
    ├── execution_summary.txt   # Consolidated plaintext table outputs for all 14 tasks
    ├── complete_graph_visualization.png # Full network visualization of the university graph
    ├── node_counts_by_label.png# Node distribution bar chart (Task 5)
    ├── task_01.txt ... task_14.txt # Individual query outputs
    └── task_01_screenshot.png ... task_14_screenshot.png # Query execution screenshots
```

---

## 3. Graph Schema & Relationship Specification

### Node Entities & Properties
- **Student** (5 nodes): `studentId` (Unique Key), `name`, `semester`, `email`
  - S101: Aarav Sharma (Sem 5, aarav@univ.edu)
  - S102: Priya Das (Sem 5, priya@univ.edu)
  - S103: Rahul Verma (Sem 3, rahul@univ.edu)
  - S104: Sneha Roy (Sem 3, sneha@univ.edu)
  - S105: Arjun Patel (Sem 5, arjun@univ.edu)
- **Faculty** (2 nodes): `facultyId` (Unique Key), `name`, `designation`, `specialization`
  - F101: Dr. Meera Sen (Associate Professor, Database Systems)
  - F102: Dr. Amit Roy (Assistant Professor, Data Analytics)
- **Course** (5 nodes): `courseCode` (Unique Key), `courseTitle`, `credits`, `level`
  - CS301: Graph Analytics (3 credits, Advanced)
  - CS302: Database Management Systems (4 credits, Core)
  - CS303: Data Mining (3 credits, Advanced)
  - CS304: Big Data Analytics (4 credits, Advanced)
  - CS305: NoSQL Databases (3 credits, Core)
- **Department** (2 nodes): `deptId` (Unique Key), `deptName`, `building`
  - D101: Computer Science (Block A)
  - D102: Information Technology (Block B)

### Directed Relationships & Edge Properties
1. `(:Student)-[:ENROLLED_IN {semesterEnrolled: Integer, grade: String}]->(:Course)`
   - Properties: `semesterEnrolled` (3 or 5), `grade` (`'Not Published'`)
   - Total edges: 11
2. `(:Faculty)-[:TEACHES {academicYear: String}]->(:Course)`
   - Properties: `academicYear` (`'2026-27'`)
   - Total edges: 5
3. `(:Student)-[:BELONGS_TO]->(:Department)`
   - Total edges: 5
4. `(:Department)-[:OFFERS]->(:Course)`
   - Total edges: 5

---

## 4. Setup & Execution Instructions

### Prerequisites
- **Java**: Java 21 LTS (or Java 17+)
- **Python**: Python 3.10+
- Python packages:
  ```bash
  pip install neo4j python-docx matplotlib networkx
  ```

### Running Neo4j Server
To start the embedded Neo4j server locally:
```powershell
.\neo4j-server\neo4j-community-5.26.0\bin\neo4j.bat console
```
The server will start with:
- **HTTP**: `http://localhost:7474`
- **Bolt**: `bolt://localhost:7687` (Authentication disabled for frictionless lab execution)

### Option A: Automated Execution (Recommended)
Run the automated pipeline to execute all queries, verify results, generate graphs, and build the Word report in one click:
```powershell
python populate_and_execute.py
python generate_task_screenshots.py
python build_word_report.py
```

### Option B: Running Queries via Neo4j Browser
1. Open your web browser and navigate to `http://localhost:7474/browser/`.
2. Select **No authentication** and click **Connect**.
3. Open `assignment5.cypher` and paste queries individually or in blocks into the top command prompt.

### Option C: Running Queries via Cypher-Shell CLI
```powershell
.\neo4j-server\neo4j-community-5.26.0\bin\cypher-shell.bat --format verbose -f assignment5.cypher
```

---

## 5. Verification Matrix of the 14 Tasks

| Task # | Task Description | Cypher Focus | Expected & Verified Output |
| :---: | :--- | :--- | :--- |
| **1** | Create all nodes with properties | `MERGE` on unique IDs | 14 nodes created (5 Student, 2 Faculty, 5 Course, 2 Department) |
| **2** | Create relationships with directions | `MERGE` directional edges | 26 relationships created (11 ENROLLED_IN, 5 TEACHES, 5 BELONGS_TO, 5 OFFERS) |
| **3** | Assign relationship properties | `ON CREATE SET` edge props | `semesterEnrolled` & `grade` on ENROLLED_IN, `academicYear` on TEACHES |
| **4** | Display the complete graph | `MATCH (n) OPTIONAL MATCH (n)-[r]->(m)` | Full graph network returned (14 nodes, 26 edges) |
| **5** | Count nodes belonging to each label | `count(n)` by `labels(n)` | Course: 5, Department: 2, Faculty: 2, Student: 5 |
| **6** | Display relationship types and directions | `type(r)` and source/target | BELONGS_TO: 5, ENROLLED_IN: 11, OFFERS: 5, TEACHES: 5 |
| **7** | Students in Semester 5 | `WHERE s.semester = 5` | Aarav Sharma (S101), Priya Das (S102), Arjun Patel (S105) |
| **8** | Courses with > 3 credits | `WHERE c.credits > 3` | CS302 Database Management Systems (4), CS304 Big Data Analytics (4) |
| **9** | Courses taught by Dr. Meera Sen | `(f:Faculty {name: '...'})-[:TEACHES]->` | CS302 Database Management Systems, CS305 NoSQL Databases |
| **10** | Students enrolled in Graph Analytics | `[:ENROLLED_IN]->(c {courseTitle: '...'})` | Aarav Sharma (S101), Priya Das (S102), Arjun Patel (S105) |
| **11** | Students in Computer Science dept | `[:BELONGS_TO]->(d {deptName: '...'})` | Aarav Sharma (S101), Priya Das (S102), Rahul Verma (S103) |
| **12** | Courses offered by IT department | `(d {deptName: '...' })-[:OFFERS]->` | CS301 Graph Analytics (3), CS304 Big Data Analytics (4) |
| **13** | NoSQL students with semester & grade | Edge property projection | Aarav Sharma (Sem 5, Grade: Not Published), Sneha Roy (Sem 3, Grade: Not Published) |
| **14** | Students in Graph Analytics & another course | Self-join co-enrolment pattern | Aarav Sharma (with DBMS, NoSQL), Priya Das (with Data Mining), Arjun Patel (with Big Data Analytics) |

---

## 6. Submission Deliverables

- **Cypher Code**: `assignment5.cypher`
- **Output Tables**: `results/execution_summary.txt` and `results/all_results.json`
- **Screenshots**: `results/task_01_screenshot.png` through `results/task_14_screenshot.png`
- **Word Report**: `report/Graph_Analytics_Assignment_5_Report.docx`
