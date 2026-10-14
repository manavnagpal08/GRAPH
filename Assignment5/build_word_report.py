"""
Word Report Generator for Graph Analytics Assignment 5
University Course Registration System Using Neo4j
Alliance School of Advanced Computing
Student: Manav Nagpal (2411021060402)
"""

import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORT_DIR, exist_ok=True)

with open(os.path.join(RESULTS_DIR, "all_results.json"), "r", encoding="utf-8") as f:
    all_results = json.load(f)

doc = docx.Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Styling Helpers
PRIMARY_COLOR = RGBColor(168, 28, 38)     # Alliance Crimson
NAVY_COLOR = RGBColor(10, 37, 64)         # Deep Navy
SLATE_COLOR = RGBColor(74, 85, 104)       # Slate Gray
DARK_COLOR = RGBColor(26, 32, 44)         # Body Text

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = NAVY_COLOR
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = SLATE_COLOR
    return p

def add_body_p(text, bold=False, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = DARK_COLOR
    return p

def add_code_block(code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="00D4FF"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(headers, rows):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True

    # Header Row
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for row_idx, r_data in enumerate(rows):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = tbl.cell(row_idx + 1, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.color.rgb = DARK_COLOR

    # Table Borders
    tblPr = tbl._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/><w:left w:val="none"/><w:right w:val="none"/></w:tblBorders>')
        tblPr[0].append(borders)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Building Word Document Report...")

# ==============================================================================
# HEADER & LOGO
# ==============================================================================
logo_path = os.path.join(RESULTS_DIR, "logo_0_0.png")
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_after = Pt(2)
    p_logo.add_run().add_picture(logo_path, width=Inches(6.2))

p_dept = doc.add_paragraph()
p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dept.paragraph_format.space_after = Pt(1)
run_dept = p_dept.add_run("Alliance School of Advanced Computing\nFaculty of Engineering and Technology")
run_dept.font.name = "Calibri"
run_dept.font.size = Pt(11)
run_dept.font.bold = True
run_dept.font.color.rgb = NAVY_COLOR

p_loc = doc.add_paragraph()
p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_loc.paragraph_format.space_after = Pt(14)
run_loc = p_loc.add_run("Alliance University - Central Campus, Chikkahadage Cross, Chandapura-Anekal Main Road, Bengaluru 562106\nwww.alliance.edu.in")
run_loc.font.name = "Calibri"
run_loc.font.size = Pt(9)
run_loc.font.color.rgb = SLATE_COLOR

# ==============================================================================
# TITLE & STUDENT DETAILS
# ==============================================================================
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(12)
run_title = p_title.add_run("ASSIGNMENT 5: GRAPH ANALYTICS\nUniversity Course Registration System Using Neo4j")
run_title.font.name = "Calibri"
run_title.font.size = Pt(16)
run_title.font.bold = True
run_title.font.color.rgb = PRIMARY_COLOR

# Student Metadata Table
meta_headers = ["Parameter", "Student & Submission Details"]
meta_rows = [
    ["Student Name", "Manav Nagpal"],
    ["Registration Number", "2411021060402"],
    ["Department / School", "Alliance School of Advanced Computing (ASAC)"],
    ["Course Code & Title", "E1CSA332 / Graph Analytics"],
    ["Program & Specialization", "Bachelor of Technology (B.Tech - CSE / IT / AIDS)"],
    ["Academic Year & Semester", "2026-27 | Semester V"],
    ["Database Technology", "Neo4j Community Server 5.26.0 (Cypher Query Language)"],
    ["Date of Submission", "October 14, 2026"]
]
add_styled_table(meta_headers, meta_rows)

# ==============================================================================
# 1. PROBLEM STATEMENT
# ==============================================================================
add_heading_1("1. Problem Statement")
add_body_p(
    "A university wants to develop a graph database to manage students, faculty members, courses, and academic departments. "
    "The system should represent these entities as nodes and their associations as relationships. You are required to implement "
    "the system using Neo4j and the Cypher query language. The sample data and relationships are provided below. "
    "Your task is to write the Cypher code to create the nodes, assign properties, establish relationships, and answer the "
    "given questions through queries."
)

add_heading_2("1.1 Sample Data")
add_heading_3("A. Student Data")
add_styled_table(
    ["Student ID", "Name", "Semester", "Email"],
    [
        ["S101", "Aarav Sharma", "5", "aarav@univ.edu"],
        ["S102", "Priya Das", "5", "priya@univ.edu"],
        ["S103", "Rahul Verma", "3", "rahul@univ.edu"],
        ["S104", "Sneha Roy", "3", "sneha@univ.edu"],
        ["S105", "Arjun Patel", "5", "arjun@univ.edu"]
    ]
)

add_heading_3("B. Faculty Data")
add_styled_table(
    ["Faculty ID", "Name", "Designation", "Specialization"],
    [
        ["F101", "Dr. Meera Sen", "Associate Professor", "Database Systems"],
        ["F102", "Dr. Amit Roy", "Assistant Professor", "Data Analytics"]
    ]
)

add_heading_3("C. Courses Data")
add_styled_table(
    ["Course Code", "Course Title", "Credits", "Level"],
    [
        ["CS301", "Graph Analytics", "3", "Advanced"],
        ["CS302", "Database Management Systems", "4", "Core"],
        ["CS303", "Data Mining", "3", "Advanced"],
        ["CS304", "Big Data Analytics", "4", "Advanced"],
        ["CS305", "NoSQL Databases", "3", "Core"]
    ]
)

add_heading_3("D. Department Data")
add_styled_table(
    ["Department ID", "Department Name", "Building"],
    [
        ["D101", "Computer Science", "Block A"],
        ["D102", "Information Technology", "Block B"]
    ]
)

add_heading_2("1.2 Relationships to Create")
add_styled_table(
    ["Relationship", "Direction", "Semantic Meaning"],
    [
        ["ENROLLED_IN", "Student → Course", "Student enrolment in a course"],
        ["TEACHES", "Faculty → Course", "Faculty member teaching a course"],
        ["BELONGS_TO", "Student → Department", "Student's parent academic department"],
        ["OFFERS", "Department → Course", "Academic department offering a course"]
    ]
)

add_heading_3("A. Student Enrolments")
add_styled_table(
    ["Student Name", "Enrolled Courses"],
    [
        ["Aarav Sharma", "Graph Analytics, DBMS, NoSQL Databases"],
        ["Priya Das", "Graph Analytics, Data Mining"],
        ["Rahul Verma", "DBMS, Big Data Analytics"],
        ["Sneha Roy", "Data Mining, NoSQL Databases"],
        ["Arjun Patel", "Graph Analytics, Big Data Analytics"]
    ]
)

add_heading_3("B. Faculty Teaching Assignments")
add_styled_table(
    ["Faculty Member", "Courses Taught"],
    [
        ["Dr. Meera Sen", "DBMS, NoSQL Databases"],
        ["Dr. Amit Roy", "Graph Analytics, Data Mining, Big Data Analytics"]
    ]
)

add_heading_3("C. Student–Department Associations")
add_styled_table(
    ["Students", "Department"],
    [
        ["Aarav Sharma, Priya Das, Rahul Verma", "Computer Science"],
        ["Sneha Roy, Arjun Patel", "Information Technology"]
    ]
)

add_heading_3("D. Department–Course Associations")
add_styled_table(
    ["Department", "Courses Offered"],
    [
        ["Computer Science", "DBMS, Data Mining, NoSQL Databases"],
        ["Information Technology", "Graph Analytics, Big Data Analytics"]
    ]
)

add_heading_2("1.3 Relationship Properties")
add_body_p(
    "Assign the following properties to the relevant relationships as specified in the assignment document:\n"
    "• ENROLLED_IN: semesterEnrolled (Integer, e.g., 3 or 5), grade (String, default: 'Not Published')\n"
    "• TEACHES: academicYear (String, default: '2026-27')"
)

# ==============================================================================
# 2. METHODOLOGY & GRAPH ARCHITECTURE
# ==============================================================================
doc.add_page_break()
add_heading_1("2. Methodology & Graph Architecture")
add_body_p(
    "Graph databases store entities as nodes, characteristics as key-value properties, and connections as first-class directed relationships. "
    "Unlike relational databases that rely on compute-intensive multi-table JOINs, graph database engines traverse physical pointers in O(1) time complexity per hop. "
    "This architecture allows for natural, highly efficient modeling of academic relationships."
)

add_heading_2("2.1 Data Integrity & Idempotency Strategy")
add_body_p(
    "To guarantee enterprise-grade data integrity and ensure that rerun scripts never produce duplicate nodes or relationships, "
    "the implementation employs unique schema constraints and idempotent MERGE statements:"
)
add_body_p("1. Unique Constraints: Enforced on Student(studentId), Faculty(facultyId), Course(courseCode), and Department(deptId).")
add_body_p("2. Idempotent Merges: All nodes and relationships use MERGE with ON CREATE SET to prevent duplicate records upon multiple executions.")
add_body_p("3. Directed Edge Cardinality: Strict source-to-target directions are verified against the specification.")

add_heading_2("2.2 Complete University Graph Visualization (Task 4)")
add_body_p("The complete graph network comprises 14 nodes and 26 directed relationships:")

vis_path = os.path.join(RESULTS_DIR, "complete_graph_visualization.png")
if os.path.exists(vis_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_after = Pt(4)
    p_img.add_run().add_picture(vis_path, width=Inches(6.2))

# ==============================================================================
# 3. PROGRAMMING TASKS IMPLEMENTATION & RESULTS
# ==============================================================================
doc.add_page_break()
add_heading_1("3. Detailed Task Implementation, Execution & Verification")
add_body_p(
    "This section presents the Cypher query, verified execution tabular output, and authentic Neo4j Browser screenshot for each of the 14 programming tasks."
)

for task_id in range(1, 15):
    t_data = all_results[str(task_id)]
    
    if task_id == 1:
        add_heading_2("Part A — Graph Creation and Verification")
    elif task_id == 7:
        doc.add_page_break()
        add_heading_2("Part B — Retrieval and Filtering Queries")

    add_heading_3(f"Task {task_id}: {t_data['title'].split(': ')[-1]}")
    add_body_p(t_data['description'], italic=True)

    # Cypher Query Block
    add_body_p("Cypher Query:", bold=True)
    add_code_block(t_data['query'])

    # Tabular Output
    add_body_p(f"Execution Output ({t_data['count']} row{'s' if t_data['count'] != 1 else ''} returned):", bold=True)
    keys = t_data['keys']
    rows = [[str(r.get(k, '')) for k in keys] for r in t_data['rows']]
    add_styled_table(keys, rows)

    # Embedded Screenshot
    screenshot_file = f"task_{task_id:02d}_screenshot.png"
    screenshot_path = os.path.join(RESULTS_DIR, screenshot_file)
    if os.path.exists(screenshot_path):
        add_body_p(f"Neo4j Browser Screenshot (Task {task_id}):", bold=True)
        p_ss = doc.add_paragraph()
        p_ss.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ss.paragraph_format.space_after = Pt(10)
        p_ss.add_run().add_picture(screenshot_path, width=Inches(5.9))

# ==============================================================================
# 4. SUMMARY & VERIFICATION MATRIX
# ==============================================================================
doc.add_page_break()
add_heading_1("4. Verification Matrix & Results Summary")
add_body_p("The table below summarizes the verification of all 14 programming tasks executed on Neo4j Community Server 5.26.0:")

matrix_headers = ["Task #", "Objective", "Expected Count", "Observed Count", "Status"]
matrix_rows = [
    ["1", "Create all entity nodes with properties", "14 nodes", "14 nodes (5 S, 2 F, 5 C, 2 D)", "PASS"],
    ["2", "Create all specified relationships", "26 edges", "26 edges (11 E, 5 T, 5 B, 5 O)", "PASS"],
    ["3", "Assign relationship properties", "3 properties", "semesterEnrolled, grade, academicYear verified", "PASS"],
    ["4", "Display complete graph", "14 nodes, 26 edges", "14 nodes, 26 edges rendered", "PASS"],
    ["5", "Count nodes by label", "4 labels", "Course: 5, Dept: 2, Faculty: 2, Student: 5", "PASS"],
    ["6", "Display relationship types & directions", "4 types", "BELONGS_TO: 5, ENROLLED_IN: 11, OFFERS: 5, TEACHES: 5", "PASS"],
    ["7", "Retrieve Semester 5 students", "3 students", "Aarav Sharma, Priya Das, Arjun Patel", "PASS"],
    ["8", "Find courses with > 3 credits", "2 courses", "CS302 DBMS (4), CS304 Big Data Analytics (4)", "PASS"],
    ["9", "Retrieve courses taught by Dr. Meera Sen", "2 courses", "CS302 DBMS, CS305 NoSQL Databases", "PASS"],
    ["10", "Find students enrolled in Graph Analytics", "3 students", "Aarav Sharma, Priya Das, Arjun Patel", "PASS"],
    ["11", "Display students belonging to CS dept", "3 students", "Aarav Sharma, Priya Das, Rahul Verma", "PASS"],
    ["12", "Find courses offered by IT dept", "2 courses", "CS301 Graph Analytics, CS304 Big Data Analytics", "PASS"],
    ["13", "Retrieve NoSQL students with semester & grade", "2 students", "Aarav Sharma (Sem 5), Sneha Roy (Sem 3)", "PASS"],
    ["14", "Find students in Graph Analytics & another course", "3 students (4 pairs)", "Aarav (2 pairs), Priya (1 pair), Arjun (1 pair)", "PASS"]
]
add_styled_table(matrix_headers, matrix_rows)

# ==============================================================================
# 5. CONCLUSION
# ==============================================================================
add_heading_1("5. Conclusion & Technical Insights")
add_body_p(
    "In this assignment, a complete University Course Registration System was successfully modeled, populated, and queried using Neo4j "
    "and Cypher. The Labeled Property Graph (LPG) model allowed complex multi-entity associations—including student course enrolments, "
    "faculty teaching responsibilities, student departmental affiliations, and departmental course offerings—to be represented naturally "
    "without relational intermediary junction tables."
)
add_body_p(
    "Key observations from the implementation include:\n"
    "1. Expressive Cypher Traversals: Complex associative queries, such as identifying co-enrolments (Task 14) or filtering on nested relationship properties (Task 13), "
    "were expressed cleanly in single pattern-matching statements without complex JOIN logic.\n"
    "2. Relationship-Level Properties: Neo4j's native support for relationship properties (e.g., semesterEnrolled, grade, academicYear) enabled contextual details to be stored directly on graph edges.\n"
    "3. Scalability & Integrity: The utilization of unique constraints paired with MERGE statements ensures complete idempotency and resilience against duplicate data insertion upon script re-execution."
)

output_docx_path = os.path.join(REPORT_DIR, "Graph_Analytics_Assignment_5_Report.docx")
doc.save(output_docx_path)
print(f"Report saved successfully to {output_docx_path}")
