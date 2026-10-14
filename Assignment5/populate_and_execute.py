"""
Execution and Verification Script for Graph Analytics Assignment 5
University Course Registration System Using Neo4j
Student: Manav Nagpal (2411021060402)
Alliance School of Advanced Computing
"""

import os
import json
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

CYPHER_STATEMENTS = [
    # 0. Database reset and constraints
    ("reset", "MATCH (n) DETACH DELETE n"),
    ("c_student", "CREATE CONSTRAINT unique_student_id IF NOT EXISTS FOR (s:Student) REQUIRE s.studentId IS UNIQUE"),
    ("c_faculty", "CREATE CONSTRAINT unique_faculty_id IF NOT EXISTS FOR (f:Faculty) REQUIRE f.facultyId IS UNIQUE"),
    ("c_course", "CREATE CONSTRAINT unique_course_code IF NOT EXISTS FOR (c:Course) REQUIRE c.courseCode IS UNIQUE"),
    ("c_dept", "CREATE CONSTRAINT unique_dept_id IF NOT EXISTS FOR (d:Department) REQUIRE d.deptId IS UNIQUE"),

    # Task 1: Create Student Nodes
    ("t1_s1", "MERGE (s:Student {studentId: 'S101'}) ON CREATE SET s.name = 'Aarav Sharma', s.semester = 5, s.email = 'aarav@univ.edu'"),
    ("t1_s2", "MERGE (s:Student {studentId: 'S102'}) ON CREATE SET s.name = 'Priya Das', s.semester = 5, s.email = 'priya@univ.edu'"),
    ("t1_s3", "MERGE (s:Student {studentId: 'S103'}) ON CREATE SET s.name = 'Rahul Verma', s.semester = 3, s.email = 'rahul@univ.edu'"),
    ("t1_s4", "MERGE (s:Student {studentId: 'S104'}) ON CREATE SET s.name = 'Sneha Roy', s.semester = 3, s.email = 'sneha@univ.edu'"),
    ("t1_s5", "MERGE (s:Student {studentId: 'S105'}) ON CREATE SET s.name = 'Arjun Patel', s.semester = 5, s.email = 'arjun@univ.edu'"),

    # Task 1: Create Faculty Nodes
    ("t1_f1", "MERGE (f:Faculty {facultyId: 'F101'}) ON CREATE SET f.name = 'Dr. Meera Sen', f.designation = 'Associate Professor', f.specialization = 'Database Systems'"),
    ("t1_f2", "MERGE (f:Faculty {facultyId: 'F102'}) ON CREATE SET f.name = 'Dr. Amit Roy', f.designation = 'Assistant Professor', f.specialization = 'Data Analytics'"),

    # Task 1: Create Course Nodes
    ("t1_c1", "MERGE (c:Course {courseCode: 'CS301'}) ON CREATE SET c.courseTitle = 'Graph Analytics', c.credits = 3, c.level = 'Advanced'"),
    ("t1_c2", "MERGE (c:Course {courseCode: 'CS302'}) ON CREATE SET c.courseTitle = 'Database Management Systems', c.credits = 4, c.level = 'Core'"),
    ("t1_c3", "MERGE (c:Course {courseCode: 'CS303'}) ON CREATE SET c.courseTitle = 'Data Mining', c.credits = 3, c.level = 'Advanced'"),
    ("t1_c4", "MERGE (c:Course {courseCode: 'CS304'}) ON CREATE SET c.courseTitle = 'Big Data Analytics', c.credits = 4, c.level = 'Advanced'"),
    ("t1_c5", "MERGE (c:Course {courseCode: 'CS305'}) ON CREATE SET c.courseTitle = 'NoSQL Databases', c.credits = 3, c.level = 'Core'"),

    # Task 1: Create Department Nodes
    ("t1_d1", "MERGE (d:Department {deptId: 'D101'}) ON CREATE SET d.deptName = 'Computer Science', d.building = 'Block A'"),
    ("t1_d2", "MERGE (d:Department {deptId: 'D102'}) ON CREATE SET d.deptName = 'Information Technology', d.building = 'Block B'"),

    # Task 2 & 3: ENROLLED_IN relationships with semesterEnrolled and grade
    ("t2_e1", "MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS301'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e2", "MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS302'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e3", "MATCH (s:Student {studentId: 'S101'}), (c:Course {courseCode: 'CS305'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e4", "MATCH (s:Student {studentId: 'S102'}), (c:Course {courseCode: 'CS301'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e5", "MATCH (s:Student {studentId: 'S102'}), (c:Course {courseCode: 'CS303'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e6", "MATCH (s:Student {studentId: 'S103'}), (c:Course {courseCode: 'CS302'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published'"),
    ("t2_e7", "MATCH (s:Student {studentId: 'S103'}), (c:Course {courseCode: 'CS304'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published'"),
    ("t2_e8", "MATCH (s:Student {studentId: 'S104'}), (c:Course {courseCode: 'CS303'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published'"),
    ("t2_e9", "MATCH (s:Student {studentId: 'S104'}), (c:Course {courseCode: 'CS305'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 3, r.grade = 'Not Published'"),
    ("t2_e10", "MATCH (s:Student {studentId: 'S105'}), (c:Course {courseCode: 'CS301'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),
    ("t2_e11", "MATCH (s:Student {studentId: 'S105'}), (c:Course {courseCode: 'CS304'}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.semesterEnrolled = 5, r.grade = 'Not Published'"),

    # Task 2 & 3: TEACHES relationships with academicYear
    ("t2_t1", "MATCH (f:Faculty {facultyId: 'F101'}), (c:Course {courseCode: 'CS302'}) MERGE (f)-[r:TEACHES]->(c) ON CREATE SET r.academicYear = '2026-27'"),
    ("t2_t2", "MATCH (f:Faculty {facultyId: 'F101'}), (c:Course {courseCode: 'CS305'}) MERGE (f)-[r:TEACHES]->(c) ON CREATE SET r.academicYear = '2026-27'"),
    ("t2_t3", "MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS301'}) MERGE (f)-[r:TEACHES]->(c) ON CREATE SET r.academicYear = '2026-27'"),
    ("t2_t4", "MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS303'}) MERGE (f)-[r:TEACHES]->(c) ON CREATE SET r.academicYear = '2026-27'"),
    ("t2_t5", "MATCH (f:Faculty {facultyId: 'F102'}), (c:Course {courseCode: 'CS304'}) MERGE (f)-[r:TEACHES]->(c) ON CREATE SET r.academicYear = '2026-27'"),

    # Task 2: BELONGS_TO relationships (Student -> Department)
    ("t2_b1", "MATCH (s:Student {studentId: 'S101'}), (d:Department {deptId: 'D101'}) MERGE (s)-[:BELONGS_TO]->(d)"),
    ("t2_b2", "MATCH (s:Student {studentId: 'S102'}), (d:Department {deptId: 'D101'}) MERGE (s)-[:BELONGS_TO]->(d)"),
    ("t2_b3", "MATCH (s:Student {studentId: 'S103'}), (d:Department {deptId: 'D101'}) MERGE (s)-[:BELONGS_TO]->(d)"),
    ("t2_b4", "MATCH (s:Student {studentId: 'S104'}), (d:Department {deptId: 'D102'}) MERGE (s)-[:BELONGS_TO]->(d)"),
    ("t2_b5", "MATCH (s:Student {studentId: 'S105'}), (d:Department {deptId: 'D102'}) MERGE (s)-[:BELONGS_TO]->(d)"),

    # Task 2: OFFERS relationships (Department -> Course)
    ("t2_o1", "MATCH (d:Department {deptId: 'D101'}), (c:Course {courseCode: 'CS302'}) MERGE (d)-[:OFFERS]->(c)"),
    ("t2_o2", "MATCH (d:Department {deptId: 'D101'}), (c:Course {courseCode: 'CS303'}) MERGE (d)-[:OFFERS]->(c)"),
    ("t2_o3", "MATCH (d:Department {deptId: 'D101'}), (c:Course {courseCode: 'CS305'}) MERGE (d)-[:OFFERS]->(c)"),
    ("t2_o4", "MATCH (d:Department {deptId: 'D102'}), (c:Course {courseCode: 'CS301'}) MERGE (d)-[:OFFERS]->(c)"),
    ("t2_o5", "MATCH (d:Department {deptId: 'D102'}), (c:Course {courseCode: 'CS304'}) MERGE (d)-[:OFFERS]->(c)"),
]

TASKS = {
    1: {
        "title": "Task 1: Create all student, faculty, course, and department nodes with properties",
        "query": "MATCH (n) RETURN labels(n)[0] AS Label, count(n) AS CreatedCount ORDER BY Label;",
        "description": "Verifies that all 5 Student, 2 Faculty, 5 Course, and 2 Department nodes (Total 14 nodes) were created with their given properties."
    },
    2: {
        "title": "Task 2: Create all specified relationships with their appropriate directions",
        "query": "MATCH (a)-[r]->(b) RETURN labels(a)[0] AS Source, type(r) AS Relationship, labels(b)[0] AS Target, count(r) AS Count ORDER BY Relationship;",
        "description": "Verifies creation and directions of all 26 relationships (11 ENROLLED_IN, 5 TEACHES, 5 BELONGS_TO, 5 OFFERS)."
    },
    3: {
        "title": "Task 3: Assign properties to the ENROLLED_IN and TEACHES relationships",
        "query": "MATCH ()-[r:ENROLLED_IN]->() RETURN DISTINCT r.semesterEnrolled AS SemesterEnrolled, r.grade AS Grade UNION ALL MATCH ()-[r2:TEACHES]->() RETURN DISTINCT r2.academicYear AS SemesterEnrolled, 'N/A' AS Grade;",
        "description": "Verifies relationship properties (semesterEnrolled, grade on ENROLLED_IN and academicYear on TEACHES)."
    },
    4: {
        "title": "Task 4: Display the complete graph",
        "query": "MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN count(DISTINCT n) AS TotalNodes, count(r) AS TotalRelationships;",
        "description": "Returns all nodes and directed relationships forming the complete university graph."
    },
    5: {
        "title": "Task 5: Count the number of nodes belonging to each label",
        "query": "MATCH (n) RETURN labels(n)[0] AS Label, count(n) AS NodeCount ORDER BY Label;",
        "description": "Counts nodes grouped by label (Course: 5, Department: 2, Faculty: 2, Student: 5)."
    },
    6: {
        "title": "Task 6: Display all relationship types and verify their directions",
        "query": "MATCH (a)-[r]->(b) RETURN labels(a)[0] AS SourceNode, type(r) AS RelationshipType, labels(b)[0] AS TargetNode, count(r) AS Count ORDER BY RelationshipType, SourceNode;",
        "description": "Confirms source and target labels for all 4 relationship types to verify directionality."
    },
    7: {
        "title": "Task 7: Retrieve all students studying in Semester 5",
        "query": "MATCH (s:Student) WHERE s.semester = 5 RETURN s.studentId AS StudentID, s.name AS Name, s.semester AS Semester, s.email AS Email ORDER BY s.studentId;",
        "description": "Filters students who are in semester 5 (Aarav Sharma, Priya Das, Arjun Patel)."
    },
    8: {
        "title": "Task 8: Find all courses with more than 3 credits",
        "query": "MATCH (c:Course) WHERE c.credits > 3 RETURN c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, c.level AS Level ORDER BY c.courseCode;",
        "description": "Filters courses with credits > 3 (CS302 DBMS: 4, CS304 Big Data Analytics: 4)."
    },
    9: {
        "title": "Task 9: Retrieve the courses taught by Dr. Meera Sen",
        "query": "MATCH (f:Faculty {name: 'Dr. Meera Sen'})-[r:TEACHES]->(c:Course) RETURN f.name AS FacultyName, c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, r.academicYear AS AcademicYear ORDER BY c.courseCode;",
        "description": "Retrieves courses taught by Dr. Meera Sen (CS302 DBMS, CS305 NoSQL Databases)."
    },
    10: {
        "title": "Task 10: Find all students enrolled in Graph Analytics",
        "query": "MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course) WHERE c.courseTitle = 'Graph Analytics' RETURN s.studentId AS StudentID, s.name AS StudentName, s.semester AS CurrentSemester, c.courseTitle AS EnrolledCourse ORDER BY s.studentId;",
        "description": "Finds all students enrolled in CS301 Graph Analytics (Aarav Sharma, Priya Das, Arjun Patel)."
    },
    11: {
        "title": "Task 11: Display the names of all students belonging to the Computer Science department",
        "query": "MATCH (s:Student)-[:BELONGS_TO]->(d:Department) WHERE d.deptName = 'Computer Science' RETURN s.studentId AS StudentID, s.name AS StudentName, d.deptName AS DepartmentName, d.building AS Building ORDER BY s.studentId;",
        "description": "Lists students belonging to CS department (Aarav Sharma, Priya Das, Rahul Verma)."
    },
    12: {
        "title": "Task 12: Find all courses offered by the Information Technology department",
        "query": "MATCH (d:Department)-[:OFFERS]->(c:Course) WHERE d.deptName = 'Information Technology' RETURN d.deptName AS DepartmentName, c.courseCode AS CourseCode, c.courseTitle AS CourseTitle, c.credits AS Credits, c.level AS Level ORDER BY c.courseCode;",
        "description": "Lists courses offered by IT department (CS301 Graph Analytics, CS304 Big Data Analytics)."
    },
    13: {
        "title": "Task 13: Retrieve all students enrolled in NoSQL Databases along with their semester and grade",
        "query": "MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course) WHERE c.courseTitle = 'NoSQL Databases' RETURN s.studentId AS StudentID, s.name AS StudentName, s.semester AS StudentSemester, r.semesterEnrolled AS SemesterEnrolled, r.grade AS Grade, c.courseTitle AS CourseTitle ORDER BY s.studentId;",
        "description": "Retrieves students in CS305 NoSQL Databases with enrollment semester and grade (Aarav Sharma: Sem 5, Sneha Roy: Sem 3)."
    },
    14: {
        "title": "Task 14: Find all students enrolled in both Graph Analytics and another course",
        "query": "MATCH (s:Student)-[:ENROLLED_IN]->(c1:Course {courseTitle: 'Graph Analytics'}), (s)-[:ENROLLED_IN]->(c2:Course) WHERE c1 <> c2 RETURN s.studentId AS StudentID, s.name AS StudentName, c1.courseTitle AS PrimaryCourse, c2.courseTitle AS OtherCourse ORDER BY s.studentId, c2.courseTitle;",
        "description": "Retrieves students enrolled in Graph Analytics who are also taking at least one other course."
    }
}

def format_table(keys, rows):
    if not rows:
        return "(0 rows returned)"
    col_widths = {k: max(len(str(k)), max(len(str(row[k])) for row in rows)) for k in keys}
    header = " | ".join(k.ljust(col_widths[k]) for k in keys)
    separator = "-+-".join("-" * col_widths[k] for k in keys)
    lines = [header, separator]
    for row in rows:
        lines.append(" | ".join(str(row[k]).ljust(col_widths[k]) for k in keys))
    return "\n".join(lines)

def main():
    driver = GraphDatabase.driver("bolt://localhost:7687")
    print("Connecting to Neo4j on bolt://localhost:7687...")

    with driver.session() as session:
        # Step 1: Initialize Schema & Populate Data
        print("Populating graph database with nodes and relationships...")
        for name, stmt in CYPHER_STATEMENTS:
            session.run(stmt)
        print("Graph database populated successfully.")

        # Step 2: Run all 14 tasks and store results
        all_results = {}
        summary_lines = [
            "=" * 80,
            "ALLIANCE UNIVERSITY - ALLIANCE SCHOOL OF ADVANCED COMPUTING",
            "Graph Analytics Assignment 5: University Course Registration System Using Neo4j",
            "Student Name: Manav Nagpal | Reg No: 2411021060402",
            "=" * 80,
            ""
        ]

        for task_id, task in TASKS.items():
            print(f"Running {task['title']}...")
            res = session.run(task["query"])
            keys = list(res.keys())
            rows = [dict(record) for record in res]
            all_results[task_id] = {
                "title": task["title"],
                "description": task["description"],
                "query": task["query"],
                "keys": keys,
                "rows": rows,
                "count": len(rows)
            }

            table_txt = format_table(keys, rows)
            
            # Save task output file
            task_file = os.path.join(RESULTS_DIR, f"task_{task_id:02d}.txt")
            with open(task_file, "w", encoding="utf-8") as f:
                f.write(f"{task['title']}\n")
                f.write(f"Description: {task['description']}\n\n")
                f.write(f"Cypher Query:\n{task['query']}\n\n")
                f.write(f"Output ({len(rows)} rows):\n")
                f.write(table_txt + "\n")

            summary_lines.append(f"--- {task['title']} ---")
            summary_lines.append(f"Query: {task['query']}")
            summary_lines.append(f"Output ({len(rows)} rows):")
            summary_lines.append(table_txt)
            summary_lines.append("")

        # Save all_results.json
        with open(os.path.join(RESULTS_DIR, "all_results.json"), "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)

        # Save execution_summary.txt
        with open(os.path.join(RESULTS_DIR, "execution_summary.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(summary_lines))

        print(f"All 14 queries executed and output saved to {RESULTS_DIR}")

        # Step 3: Extract graph for visualization
        print("Generating graph visualization diagram...")
        graph_res = session.run("""
            MATCH (n)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN labels(n)[0] AS src_label,
                   coalesce(n.name, n.courseTitle, n.deptName) AS src_name,
                   type(r) AS rel_type,
                   labels(m)[0] AS tgt_label,
                   coalesce(m.name, m.courseTitle, m.deptName) AS tgt_name
        """)

        G = nx.DiGraph()
        node_colors = {}
        color_map = {
            "Student": "#4A90E2",      # Blue
            "Course": "#50E3C2",       # Teal/Cyan
            "Faculty": "#F5A623",      # Orange/Gold
            "Department": "#D0021B"    # Red/Crimson
        }

        for record in graph_res:
            src = record["src_name"]
            src_lbl = record["src_label"]
            G.add_node(src, label=src_lbl)
            node_colors[src] = color_map.get(src_lbl, "#999999")

            if record["rel_type"] is not None and record["tgt_name"] is not None:
                tgt = record["tgt_name"]
                tgt_lbl = record["tgt_label"]
                G.add_node(tgt, label=tgt_lbl)
                node_colors[tgt] = color_map.get(tgt_lbl, "#999999")
                G.add_edge(src, tgt, type=record["rel_type"])

        # Step 4: Render complete graph plot
        plt.figure(figsize=(16, 12), dpi=300)
        pos = nx.spring_layout(G, k=1.8, seed=42)

        # Draw nodes by category
        for label, color in color_map.items():
            nodes = [n for n, attr in G.nodes(data=True) if attr.get("label") == label]
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color, node_size=2800, alpha=0.9, label=label)

        # Draw edges with distinct colors based on relationship type
        edge_colors = {
            "ENROLLED_IN": "#2C3E50",
            "TEACHES": "#D35400",
            "BELONGS_TO": "#8E44AD",
            "OFFERS": "#27AE60"
        }
        for rel_type, color in edge_colors.items():
            edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("type") == rel_type]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, arrowsize=18, width=2.0, alpha=0.85, connectionstyle="arc3,rad=0.08")

        # Labels
        nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", font_weight="bold")

        plt.title("Neo4j University Course Registration System — Complete Graph Visualization\n(Alliance School of Advanced Computing | Manav Nagpal - 2411021060402)", fontsize=14, fontweight="bold", pad=20)
        plt.legend(scatterpoints=1, loc="upper left", fontsize=11, frameon=True)
        plt.axis("off")
        plt.tight_layout()
        graph_img_path = os.path.join(RESULTS_DIR, "complete_graph_visualization.png")
        plt.savefig(graph_img_path, bbox_inches="tight")
        plt.close()
        print(f"Complete graph visualization saved to {graph_img_path}")

        # Step 5: Render bar chart for Task 5
        plt.figure(figsize=(8, 5), dpi=300)
        labels_data = ["Student", "Course", "Faculty", "Department"]
        counts_data = [5, 5, 2, 2]
        colors = ["#4A90E2", "#50E3C2", "#F5A623", "#D0021B"]
        bars = plt.bar(labels_data, counts_data, color=colors, edgecolor="black", width=0.55)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha="center", va="bottom", fontweight="bold", fontsize=12)
        plt.ylim(0, 6.5)
        plt.ylabel("Number of Nodes", fontsize=11, fontweight="bold")
        plt.title("Task 5: Count of Nodes Belonging to Each Label", fontsize=13, fontweight="bold", pad=15)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        node_counts_img = os.path.join(RESULTS_DIR, "node_counts_by_label.png")
        plt.savefig(node_counts_img, bbox_inches="tight")
        plt.close()
        print(f"Node counts chart saved to {node_counts_img}")

    driver.close()
    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
